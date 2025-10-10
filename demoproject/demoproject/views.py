import json
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages
from .utils import get_help_text, format_analysis_output
from .forms import CustomUserCreationForm

try:
    from django_ratelimit.decorators import ratelimit

    RATELIMIT_AVAILABLE = True
except ImportError:
    RATELIMIT_AVAILABLE = False

    def ratelimit(key=None, rate=None, method=None, block=True):
        def decorator(func):
            return func

        return decorator


try:
    from cryptic import CrypticAnalyzer

    CRYPTIC_AVAILABLE = True
except ImportError:
    CRYPTIC_AVAILABLE = False

# Logger para auditoría
logger = logging.getLogger("terminal")


def home(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                "home"
            )  # Asegúrate de que 'home' sea el nombre de tu URL de inicio
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def run_demo(request):
    return render(
        request,
        "run_demo.html",
        {
            "cryptic_available": CRYPTIC_AVAILABLE,
            "ratelimit_available": RATELIMIT_AVAILABLE,
        },
    )


@login_required
@require_http_methods(["POST"])
@ratelimit(key="user", rate="30/m", method="POST", block=False)
def execute_command(request):
    # Respuesta clara y segura cuando se excede el rate limit
    if getattr(request, "limited", False):
        logger.warning(f"Rate limit excedido por usuario {request.user.username}")
        response = JsonResponse(
            {
                "success": False,
                "error": True,
                "output": (
                    "⚠️ Límite de solicitudes excedido.\n\n"
                    "Por seguridad, hemos limitado temporalmente las peticiones. "
                    "Espera unos segundos y vuelve a intentarlo.\n\n"
                    "Si el problema persiste o necesitas mayor capacidad, contacta al administrador."
                ),
            }
        )
        # HTTP 429 Too Many Requests con cabecera de reintento sugerido
        response.status_code = 429
        response["Retry-After"] = "60"
        return response
    try:
        data = json.loads(request.body)
        command = data.get("command", "").strip()

        logger.info(f"Usuario {request.user.username} ejecutó: {command[:100]}")

        if not command:
            return JsonResponse(
                {"success": False, "output": "Error: Comando vacío", "error": True}
            )

        max_length = getattr(settings, "MAX_COMMAND_LENGTH", 1000)
        if len(command) > max_length:
            return JsonResponse(
                {
                    "success": False,
                    "output": f"Error: Comando demasiado largo (máximo {max_length} caracteres)",
                    "error": True,
                }
            )
        parts = command.split(maxsplit=2)

        if len(parts) == 1 and parts[0].lower() in ["help", "--help", "-h"]:
            return JsonResponse(
                {"success": True, "output": get_help_text(), "error": False}
            )

        if len(parts) < 2:
            return JsonResponse(
                {
                    "success": False,
                    "output": 'Uso: cryptic <comando> "<texto>"\nEscribe "help" para más información',
                    "error": True,
                }
            )

        if parts[0].lower() != "cryptic" or parts[1].lower() != "analyze":
            return JsonResponse(
                {
                    "success": False,
                    "output": 'Error: Comando no válido\nEscribe "help" para más información',
                    "error": True,
                }
            )

        text_to_analyze = parts[2].strip("\"'")
        if len(parts) < 3 or not text_to_analyze:
            return JsonResponse(
                {
                    "success": False,
                    "output": 'Error: Debe proporcionar un texto a analizar\nUso: cryptic <comando> "<texto>"',
                    "error": True,
                }
            )

        max_text_length = getattr(settings, "MAX_ANALYSIS_TEXT_LENGTH", 5000)
        if len(text_to_analyze) > max_text_length:
            return JsonResponse(
                {
                    "success": False,
                    "output": f"Error: Texto demasiado largo (máximo {max_text_length} caracteres)",
                    "error": True,
                }
            )

        if not CRYPTIC_AVAILABLE:
            return JsonResponse(
                {
                    "success": False,
                    "output": "❌ Error: Librería cryptic no disponible\n\nInstalación:\n  pip install cryptic\n\nO agregue cryptic a requirements.txt",
                    "error": True,
                }
            )

        try:
            analyzer = CrypticAnalyzer()
            analysis = analyzer.analyze_data(text_to_analyze)

            output = format_analysis_output(text_to_analyze, analysis)

            logger.info(f"Análisis completado para usuario {request.user.username}")

            return JsonResponse(
                {
                    "success": True,
                    "output": output,
                    "error": False,
                    "analysis_data": {
                        "sensitivity_level": analysis.sensitivity_level.value,
                        "protection_status": analysis.protection_status.value,
                        "confidence": analysis.confidence,
                        "has_sensitive_data": bool(
                            analysis.sensitive_analysis
                            and analysis.sensitive_analysis.matches
                        ),
                    },
                }
            )

        except Exception as e:
            logger.error(
                f"Error en análisis para usuario {request.user.username}: {str(e)}"
            )
            return JsonResponse(
                {
                    "success": False,
                    "output": f"❌ Error durante el análisis: {str(e)}",
                    "error": True,
                }
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "output": "Error: Formato JSON inválido", "error": True}
        )
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return JsonResponse(
            {"success": False, "output": f"Error inesperado: {str(e)}", "error": True}
        )

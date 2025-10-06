

def format_analysis_output(text_to_analyze, analysis):
    """
    Formatea el resultado del análisis para mostrar en terminal.
    Similar al formato del CLI original.
    """
    output_lines = []

    # Header
    output_lines.append(f"\n🔍 Analizando: {text_to_analyze}")
    output_lines.append("=" * 60)

    # Ícono según estado de protección
    status_icons = {
        "Protegido": "🔒",
        "Sin protección": "⚠️ ",
        "Parcialmente protegido": "🟡",
    }
    status_icon = status_icons.get(analysis.protection_status.value, "❓")

    # Preview del dato
    data_preview = (text_to_analyze[:50] + "...") if len(text_to_analyze) > 50 else text_to_analyze
    output_lines.append(f"{status_icon} {data_preview}")

    # Información principal
    output_lines.append(f"   Estado: {analysis.protection_status.value}")
    output_lines.append(f"   Sensibilidad: {analysis.sensitivity_level.value}")
    output_lines.append(f"   Confianza: {analysis.confidence:.1%}")

    # Datos sensibles encontrados
    if analysis.sensitive_analysis and analysis.sensitive_analysis.matches:
        output_lines.append("   ⚠️  Datos sensibles encontrados:")
        for match in analysis.sensitive_analysis.matches[:5]:  # Máximo 5
            validation_icon = "✓" if match.is_validated else "⚠"
            output_lines.append(f"     {validation_icon} {match.data_type.value}: {match.matched_text}")

        # Si hay más matches
        if len(analysis.sensitive_analysis.matches) > 5:
            remaining = len(analysis.sensitive_analysis.matches) - 5
            output_lines.append(f"     ... y {remaining} más")

    # Hash detectado
    if analysis.hash_analysis and analysis.hash_analysis.possible_types:
        hash_type = analysis.hash_analysis.possible_types[0][0].value
        confidence = analysis.hash_analysis.possible_types[0][1]
        output_lines.append(f"   🔒 Hash detectado: {hash_type} (confianza: {confidence:.1%})")

    # Recomendaciones
    if analysis.recommendations:
        output_lines.append("\n💡 Recomendaciones:")
        for i, rec in enumerate(analysis.recommendations[:3], 1):  # Máximo 3
            output_lines.append(f"   {i}. {rec}")

    return "\n".join(output_lines)


def get_help_text():
    return """
            🔐 Cryptic Terminal - Ayuda

            COMANDO DISPONIBLE:
            cryptic analyze "<texto>"    Analiza un texto en busca de datos sensibles

            EJEMPLOS:
            cryptic analyze "juan.perez@empresa.cl"
                → Detecta y valida direcciones de correo electrónico

            cryptic analyze "12.345.678-5"
                → Detecta y valida RUTs chilenos

            cryptic analyze "4111-1111-1111-1111"
                → Detecta números de tarjetas de crédito

            cryptic analyze "+56912345678"
                → Detecta números de teléfono chilenos

            cryptic analyze "$2b$12$LQv3c1yqBWVHxkd0LHAkCO"
                → Detecta y clasifica hashes criptográficos

            TIPOS DE DATOS DETECTADOS:
            • Correos electrónicos
            • RUTs chilenos
            • Números de tarjetas de crédito
            • Números de teléfono
            • Hashes (bcrypt, argon2, SHA, MD5, etc.)
            • Tokens y claves API
            • Direcciones IP
            • URLs

            COMANDOS ESPECIALES:
            help, --help, -h    Muestra esta ayuda
            clear               Limpia la terminal

            NOTAS:
            • Los comandos están limitados a 30 por minuto por usuario
            • Máximo 1000 caracteres por comando
            • El análisis es completamente local y seguro
            """

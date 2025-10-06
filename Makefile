.PHONY: dev help cleanup start

# Colores para output
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help:
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@echo "$(YELLOW)make dev$(NC)      - Inicia el entorno de desarrollo Tailwind + Django"
	@echo "$(YELLOW)make start$(NC)    - Instala dependencias y configura el proyecto"
	@echo "$(YELLOW)make cleanup$(NC)  - Mata procesos huérfanos de desarrollo"
	@echo "$(YELLOW)make help$(NC)     - Muestra esta ayuda"
start:
	@echo "$(YELLOW)  Verificando instalación de uv...$(NC)"
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "$(YELLOW)  Instalando uv...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		# Asegurar que la sesión actual vea ~/.local/bin donde se instala uv por defecto; \
		export PATH="$$HOME/.local/bin:$$PATH"; \
		if ! command -v uv >/dev/null 2>&1; then \
			echo "No se pudo instalar uv o no está en PATH"; exit 1; \
		fi; \
		echo "$(GREEN)  uv instalado correctamente$(NC)"; \
	else \
		echo "$(GREEN)  uv ya está instalado$(NC)"; \
	fi
	@uv add ../libprueba/dist/cryptic-0.1.0-py3-none-any.whl
	@echo "$(GREEN) Sincronizando dependencias...$(NC)"
	@uv sync --active
	@echo "$(GREEN) Verificando instalación de Tailwind CSS...$(NC)"
	@if [ ! -f "demoproject/static/css/tailwindcss" ]; then \
		echo "$(YELLOW)  Descargando Tailwind CSS...$(NC)"; \
		curl -sLo demoproject/static/css/tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64; \
		chmod +x demoproject/static/css/tailwindcss; \
		echo "$(GREEN)  Tailwind CSS instalado correctamente$(NC)"; \
	else \
		echo "$(GREEN)  Tailwind CSS ya está instalado$(NC)"; \
	fi
	@if [ -d ".venv" ]; then \
		echo "$(YELLOW)  Activando entorno virtual existente...$(NC)"; \
		export PATH=".venv/bin:$$PATH" && echo "$(GREEN)Entorno virtual listo$(NC)"; \
	else \
		echo "$(YELLOW)  Creando entorno virtual...$(NC)"; \
		uv venv && export PATH=".venv/bin:$$PATH" && echo "$(GREEN)Entorno virtual creado y listo$(NC)"; \
	fi
	@echo "$(GREEN) Configuración completada. Usa $(YELLOW)make dev$(GREEN) para iniciar el desarrollo.$(NC)"

dev:
	@echo "$(GREEN) Iniciando entorno de desarrollo...$(NC)"
	@echo "$(GREEN) Proyecto: Cryptic Demo$(NC)"
	@echo "$(GREEN) Django server: http://localhost:8000$(NC)"
	@echo ""
	@echo "$(YELLOW) Iniciando Tailwind CSS watcher...$(NC)"
	@echo "$(YELLOW) Directorio: demoproject/static/css$(NC)"
	@cd demoproject/static/css && ./tailwindcss -i input.css -o output.css --watch &
	@echo "$(YELLOW) Iniciando Django development server...$(NC)"
	@echo "$(YELLOW) Directorio: demoproject$(NC)"
	@cd demoproject && uv run manage.py runserver

cleanup:
	@echo "$(YELLOW) Deteniendo procesos de desarrollo huérfanos...$(NC)"
	@lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "$(YELLOW)  No se encontró proceso en puerto 8000$(NC)"
	@pkill -f "tailwindcss.*--watch" 2>/dev/null || echo "$(YELLOW)  No se encontró proceso de Tailwind$(NC)"
	@pkill -f "manage.py runserver" 2>/dev/null || echo "$(YELLOW)  No se encontró proceso de Django$(NC)"
	@echo "$(GREEN) Limpieza completada$(NC)"

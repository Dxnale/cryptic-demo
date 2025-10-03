.PHONY: dev help cleanup

# Colores para output
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help:
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@echo "$(YELLOW)make dev$(NC)      - Inicia el entorno de desarrollo (Tailwind + Django)"
	@echo "$(YELLOW)make cleanup$(NC)  - Mata procesos huérfanos de desarrollo"
	@echo "$(YELLOW)make help$(NC)     - Muestra esta ayuda"

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

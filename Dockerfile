# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen --no-install-project

# Copy project
COPY . .

# Collect static files
RUN uv run python demoproject/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "sh", "-c", "DJANGO_SETTINGS_MODULE=demoproject.settings_prod gunicorn demoproject.wsgi:application --bind 0.0.0.0:8000"]
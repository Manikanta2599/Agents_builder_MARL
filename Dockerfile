FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY anti_gravity_system/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY anti_gravity_system/ ./anti_gravity_system/
COPY anti_gravity_system/config/ ./config/

# Set env vars
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "anti_gravity_system.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

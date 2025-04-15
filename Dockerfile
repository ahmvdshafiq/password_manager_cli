FROM python:3.10-slim

WORKDIR /app

# Copy code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint for CLI
ENTRYPOINT ["python", "password_manager.py"]

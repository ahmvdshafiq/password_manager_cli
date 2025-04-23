FROM python:3.11

# Install Tkinter only (no need for mysqlclient!)
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY password_manager.py .

# Install Python packages
RUN pip install mysql-connector-python

# Run the app
CMD ["python", "password_manager.py"]

FROM python:3.11

# Install Tkinter and other required system packages
RUN apt-get update && apt-get install -y \
    python3-tk \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code
COPY password_manager.py .

# Install Python dependencies
RUN pip install mysql-connector-python

# Run the app
CMD ["python", "password_manager.py"]

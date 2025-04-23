FROM python:3.11-slim

WORKDIR /app

COPY password_manager.py .

RUN pip install mysql-connector-python

CMD ["python", "password_manager.py"]

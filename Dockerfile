FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN pip install flask cryptography sqlalchemy mysql-connector-python

EXPOSE 8000
CMD ["python", "password_manager.py"]

FROM python:3.10.12
WORKDIR /app
COPY . .
RUN pip install flask flask-pymongo google-cloud-storage pika pillow pytesseract
CMD ["python", "app.py"]
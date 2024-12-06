FROM python:3.10.12
WORKDIR /app
COPY . .
RUN pip install google-cloud-storage pymongo pika pillow pytesseract
CMD ["python", "worker.py"]


import pika
from pytesseract import image_to_string
from google.cloud import storage
from pymongo import MongoClient
from PIL import Image
import json
import os

# MongoDB configuration
MONGO_URI = "mongodb+srv://andavarapuvamsi3:qISi9R1HeApjKYlJ@dcscproject.puj7i.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client.ocr_database
results_collection = db.results

# Google Cloud Storage configuration
GCS_BUCKET = "dcscprojectb1"
storage_client = storage.Client()

# RabbitMQ configuration
RABBITMQ_HOST = "rabbitmq"

def process_task(ch, method, properties, body):
    task = json.loads(body)
    gcs_path = task['gcs_path']

    # Download the image from Google Cloud Storage
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob(gcs_path)
    local_path = f'/tmp/{gcs_path}'
    blob.download_to_filename(local_path)

    # Perform OCR
    image = Image.open(local_path)
    text = image_to_string(image)

    # Save the result in MongoDB
    result = {'gcs_path': gcs_path, 'text': text}
    results_collection.insert_one(result)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='ocr_tasks')
channel.basic_consume(queue='ocr_tasks', on_message_callback=process_task)

print("Worker is waiting for tasks...")
channel.start_consuming()

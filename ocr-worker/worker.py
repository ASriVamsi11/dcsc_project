import pika
import pytesseract
from pytesseract import image_to_string
from google.cloud import storage
from pymongo import MongoClient
from PIL import Image, ImageFilter, ImageEnhance
import json
import os

host = "localhost"  # Hostname or IP address
port = 27017        # Port number
username = "admin"  # Root username
password = "secret" # Root password

# MongoDB configuration
MONGO_URI = f"mongodb://{username}:{password}@{host}:{port}/"
#MONGO_URI = "mongodb+srv://andavarapuvamsi3:qISi9R1HeApjKYlJ@dcscproject.puj7i.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client.ocr_database
results_collection = db.results

# Google Cloud Storage configuration
GCS_BUCKET = "dcscprojectb1"
storage_client = storage.Client()

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"

# Tesseract executable path
pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Adjust this path for your system
# For Windows: pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy:
    - Convert to grayscale
    - Sharpen the image
    - Enhance contrast
    """
    image = Image.open(image_path)
    image = image.convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
    image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast
    return image

def process_task(ch, method, properties, body):
    task = json.loads(body)
    task_id = task['task_id']
    gcs_path = task['gcs_path']
    languages = task.get('languages', 'eng')

    print(f"Processing task {task_id} with languages: {languages}")

    # Download the image from Google Cloud Storage
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob(gcs_path)
    local_path = f'/tmp/{gcs_path}'
    blob.download_to_filename(local_path)

    try:
        print(f"Processing task {task_id} with image: {local_path}")
        print(f"Using languages: {languages}")

        processed_image = preprocess_image(local_path)
        # Perform OCR
        # image = Image.open(local_path)
        text = image_to_string(processed_image, lang=languages)

        if not text.strip():
            print("No text detected with selected languages. Trying English as fallback")
            text = image_to_string(processed_image, lang="eng")

        print(f"Detected text for {task_id}:\n{text}")

        # Save the result in MongoDB
        result = {'task_id': task_id, 'gcs_path': gcs_path, 'text': text, 'languages':languages}
        results_collection.insert_one(result)

        print(f"Result saved for {task_id}")
    except Exception as e:
        print(f"Error processing task {task_id}: {e}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='ocr_tasks')
channel.basic_consume(queue='ocr_tasks', on_message_callback=process_task)

print("Worker is waiting for tasks...")
channel.start_consuming()

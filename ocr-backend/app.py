from flask import Flask, request, jsonify
from google.cloud import storage
from pymongo import MongoClient
import pika
import json
import os

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = "mongodb+srv://andavarapuvamsi3:qISi9R1HeApjKYlJ@dcscproject.puj7i.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client.ocr_database
results_collection = db.results

# Google Cloud Storage configuration
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/asrivamsi11/dcsc_project/dcscproject-34b356ce3665.json"

GCS_BUCKET = "dcscprojectb1"
storage_client = storage.Client()

# RabbitMQ configuration
RABBITMQ_HOST = "rabbitmq"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    local_path = f'/tmp/{filename}'
    file.save(local_path)

    # Upload to Google Cloud Storage
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob(filename)
    blob.upload_from_filename(local_path)

    # Queue task in RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='ocr_tasks')

    message = json.dumps({'gcs_path': filename})
    channel.basic_publish(exchange='', routing_key='ocr_tasks', body=message)
    connection.close()

    return jsonify({'message': 'Task added to queue'})

@app.route('/results', methods=['GET'])
def get_results():
    results = list(results_collection.find({}, {'_id': 0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

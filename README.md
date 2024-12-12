# OCR System: Optical Character Recognition Web Application

This project is a cloud-based Optical Character Recognition (OCR) system designed to process images and extract text in multiple languages. It is built using a microservices architecture and deployed on Kubernetes. The system leverages React for the frontend, Flask for the backend, and Tesseract for OCR processing.

---

## **Table of Contents**

1. [Features](#features)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Install Required Tools](#2-install-required-tools)
    - [3. Build Docker Images](#3-build-docker-images)
    - [4. Configure Google Cloud Storage](#4-configure-google-cloud-storage)
    - [5. Set Up Kubernetes Secrets](#5-set-up-kubernetes-secrets)
    - [6. Deploy the Application to Kubernetes](#6-deploy-the-application-to-kubernetes)
    - [7. Running Locally Using Minikube](#7-running-locally-using-minikube)
5. [Scaling and Monitoring](#scaling-and-monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

---

## **Features**

- Multi-language OCR processing (English, Hindi, Chinese, and Spanish).
- Scalable architecture using Kubernetes.
- Frontend for image upload and text display.
- Google Cloud Storage for image management.
- MongoDB for result storage.
- RabbitMQ for asynchronous task handling.

---

## **Architecture**

1. **Frontend**:
   - Built with React.
   - Users can upload images and retrieve processed text.

2. **Backend**:
   - Flask-based API.
   - Manages image uploads, queues tasks, and fetches results.

3. **Worker**:
   - Python-based processing service.
   - Retrieves images from Google Cloud Storage, performs OCR, and stores results in MongoDB.

4. **Database**:
   - MongoDB stores extracted text and metadata.

5. **Queue**:
   - RabbitMQ handles asynchronous task distribution.

6. **Storage**:
   - Google Cloud Storage stores uploaded images.

---

## **Prerequisites**

1. **Tools and Dependencies**:
   - Docker
   - Kubernetes (Minikube for local setup)
   - Node.js (18+)
   - Python (3.10+)
   - Google Cloud SDK
   - MongoDB Community Edition
   - RabbitMQ

2. **Environment Configuration**:
   - Service account JSON for Google Cloud Storage.
   - Kubernetes cluster setup (local or cloud).

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/ocr-system.git
cd ocr-system
```

### 2. Install Required Tools
Node.js
```bash
sudo apt update
sudo apt install -y nodejs npm
```

### Python
Install Python and dependencies:
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip install flask pymongo pika google-cloud-storage pytesseract
```

### Docker
Install Docker following the official guide.

### Kubernetes and Minikube
Install Minikube:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## 3. Build Docker Images

### Option 1: Using Docker Commands

#### Frontend
```bash
docker build -t ocr-frontend ./frontend
```

#### Backend
```bash
docker build -t ocr-backend ./backend
```

#### Worker
```bash
docker build -t ocr-worker ./worker
```

#### Push Images (if using a container registry)
```bash
docker tag ocr-backend gcr.io/<project-id>/ocr-backend
docker push gcr.io/<project-id>/ocr-backend
```

### Option 2: Using Makefile

If your project includes a Makefile, you can use the following commands to build and push the images:
```bash
make build
make push
```
## 4. Configure Google Cloud Storage

### Create a Service Account
1. Navigate to [Google Cloud Console](https://console.cloud.google.com).
2. Create a service account with "Storage Admin" permissions.
3. Download the service account key as a JSON file.

### Create a Storage Bucket
```bash
gsutil mb -p <your-project-id> gs://<bucket-name>
```

## 5. Set Up Kubernetes Secrets

### Create a secret for Google Cloud credentials
```bash
kubectl create secret generic google-credentials \
  --from-file=key.json=/path/to/your-service-account-key.json
```

### Verify the secret
```bash
kubectl get secrets
```

## 6. Deploy the Application to Kubernetes

### Apply the manifests
```bash
kubectl apply -f k8s/mongodb-deployment.yaml
kubectl apply -f k8s/rabbitmq-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

### Verify deployments
```bash
kubectl get pods
kubectl get services
```

## 7. Running Locally Using Minikube

### Start Minikube
```bash
minikube start
```

### Access the Frontend
```bash
minikube service ocr-frontend
```

### Forward Ports (Optional)
```bash
kubectl port-forward service/ocr-frontend 8080:80
```

## Scaling and Monitoring

### Scale Worker Pods
```bash
kubectl scale deployment ocr-worker --replicas=3
```

### Monitor Logs
```bash
kubectl logs <pod-name>
```

### Enable Autoscaling
```bash
kubectl autoscale deployment ocr-worker --cpu-percent=50 --min=1 --max=5
```

## Troubleshooting

### Pods Not Running
Check pod status:
```bash
kubectl get pods
```

View logs:
```bash
kubectl logs <pod-name>
```

### External IP Pending
Use Minikube service:
```bash
minikube service ocr-frontend
```

### CSS Not Loading
Verify frontend build:
```bash
npm run build
```

### RabbitMQ Connection Errors
Check RabbitMQ logs:
```bash
kubectl logs <rabbitmq-pod-name>
```

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit changes:
    ```bash
    git commit -m "Added feature-name"
    ```
4. Push changes and open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.



# =====================================================================
# API DOCUMENTATION & DEPLOYMENT GUIDE
# =====================================================================

## 🔗 REST API ENDPOINTS

### Base URL
```
http://localhost:5000/api
```

---

## 📡 ENDPOINT 1: Health Check

**Description**: Verify if the API is running and model is loaded

**Endpoint**: `GET /api/health`

**Request**:
```bash
curl http://localhost:5000/api/health
```

**Response (200 OK)**:
```json
{
    "status": "healthy",
    "model_loaded": true,
    "timestamp": "2026-02-25T10:30:45.123456"
}
```

---

## 🎯 ENDPOINT 2: Single Prediction

**Description**: Predict spam/ham for a single message

**Endpoint**: `POST /api/predict`

**Content-Type**: `application/json`

**Request Body**:
```json
{
    "message": "Congratulations! You won 1 million dollars. Claim now!!!"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"message":"Congratulations! You won 1 million dollars."}'
```

**Response (200 OK)**:
```json
{
    "message": "Congratulations! You won 1 million dollars. Claim now!!!",
    "prediction": "SPAM",
    "spam_probability": 0.9547,
    "confidence": 0.9547,
    "timestamp": "2026-02-25T10:35:20.456789"
}
```

**Response (400 Bad Request)**:
```json
{
    "error": "Missing message field"
}
```

**Response (503 Service Unavailable)**:
```json
{
    "error": "Model not loaded"
}
```

---

## 📦 ENDPOINT 3: Batch Prediction

**Description**: Predict spam/ham for multiple messages at once

**Endpoint**: `POST /api/predict_batch`

**Content-Type**: `application/json`

**Request Body**:
```json
{
    "messages": [
        "Hey, how are you?",
        "Free money now!!!",
        "Let's meet tomorrow at 5pm",
        "Your account has been suspended"
    ]
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/predict_batch \
  -H "Content-Type: application/json" \
  -d '{"messages":["Hey there","Free money!"]}'
```

**Response (200 OK)**:
```json
{
    "predictions": [
        {
            "message": "Hey, how are you?",
            "prediction": "HAM",
            "spam_probability": 0.0234,
            "confidence": 0.9766
        },
        {
            "message": "Free money now!!!",
            "prediction": "SPAM",
            "spam_probability": 0.9812,
            "confidence": 0.9812
        },
        {
            "message": "Let's meet tomorrow at 5pm",
            "prediction": "HAM",
            "spam_probability": 0.0145,
            "confidence": 0.9855
        },
        {
            "message": "Your account has been suspended",
            "prediction": "SPAM",
            "spam_probability": 0.8934,
            "confidence": 0.8934
        }
    ]
}
```

**Constraints**:
- Maximum 1000 messages per request
- Each message must be non-empty string
- Empty messages are skipped

---

## ℹ️ ENDPOINT 4: Model Info

**Description**: Get information about the trained model

**Endpoint**: `GET /api/model_info`

**Request**:
```bash
curl http://localhost:5000/api/model_info
```

**Response (200 OK)**:
```json
{
    "model_name": "Gradient Boosting",
    "version": "2.0",
    "status": "ready",
    "timestamp": "2026-02-25T10:40:15.789012"
}
```

---

## 📝 PYTHON CLIENT EXAMPLE

```python
import requests
import json

class SpamDetectionClient:
    def __init__(self, api_url='http://localhost:5000/api'):
        self.api_url = api_url
    
    def health_check(self):
        """Check if API is running"""
        response = requests.get(f'{self.api_url}/health')
        return response.json()
    
    def predict(self, message):
        """Predict single message"""
        response = requests.post(
            f'{self.api_url}/predict',
            json={'message': message}
        )
        return response.json()
    
    def predict_batch(self, messages):
        """Predict multiple messages"""
        response = requests.post(
            f'{self.api_url}/predict_batch',
            json={'messages': messages}
        )
        return response.json()
    
    def model_info(self):
        """Get model information"""
        response = requests.get(f'{self.api_url}/model_info')
        return response.json()

# Usage
client = SpamDetectionClient()

# Check health
print(client.health_check())

# Single prediction
result = client.predict("Free money now!!!")
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")

# Batch prediction
messages = [
    "Hey there!",
    "You won a prize!",
    "See you tomorrow?"
]
results = client.predict_batch(messages)
for r in results['predictions']:
    print(f"{r['message']}: {r['prediction']}")
```

---

## 📊 JAVASCRIPT/FETCH EXAMPLE

```javascript
class SpamDetectionClient {
    constructor(apiUrl = 'http://localhost:5000/api') {
        this.apiUrl = apiUrl;
    }

    async healthCheck() {
        return fetch(`${this.apiUrl}/health`)
            .then(r => r.json());
    }

    async predict(message) {
        return fetch(`${this.apiUrl}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        }).then(r => r.json());
    }

    async predictBatch(messages) {
        return fetch(`${this.apiUrl}/predict_batch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages })
        }).then(r => r.json());
    }

    async getModelInfo() {
        return fetch(`${this.apiUrl}/model_info`)
            .then(r => r.json());
    }
}

// Usage
const client = new SpamDetectionClient();

// Single prediction
client.predict('Free money now!!!').then(result => {
    console.log(`${result.prediction}: ${result.confidence * 100}%`);
});

// Batch prediction
client.predictBatch(['Hello!', 'Free money!']).then(result => {
    result.predictions.forEach(p => {
        console.log(`${p.message} -> ${p.prediction}`);
    });
});
```

---

## 🚀 DEPLOYMENT OPTIONS

### 1. HEROKU DEPLOYMENT (RECOMMENDED - FREE)

**Step 1**: Create Heroku Account
- Go to https://www.heroku.com
- Sign up (free tier available)

**Step 2**: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

**Step 3**: Prepare Files

Create `requirements.txt`:
```
flask
flask-cors
scikit-learn
pandas
numpy
nltk
gunicorn
```

Create `Procfile` (no extension):
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.9.13
```

**Step 4**: Deploy

```bash
# Login
heroku login

# Create app
heroku create your-spam-detector-app

# Add model file
git add spam_detection_model.pkl
git commit -m "Add trained model"

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Check status
heroku ps:scale web=1
```

**Access Your Live API**:
```
https://your-spam-detector-app.herokuapp.com/api/health
```

---

### 2. AWS LAMBDA + API GATEWAY (SERVERLESS)

**Step 1**: Prepare Model
```bash
# Create deployment package
zip -r deployment.zip app.py spam_detection_model.pkl
```

**Step 2**: Create Lambda Function
- Go to AWS Lambda Console
- Create new function
- Upload deployment.zip
- Set handler to `app.handler`
- Timeout: 30 seconds
- Memory: 512 MB (minimum for ML models)

**Step 3**: Create API Gateway
- Create new REST API
- Create POST method
- Link to Lambda function
- Enable CORS

**Step 4**: Deploy
- Deploy API
- Get invoke URL (example: `https://abc123.execute-api.us-east-1.amazonaws.com/prod`)

---

### 3. GOOGLE CLOUD RUN (CONTAINERIZED)

**Step 1**: Create Docker Image

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

**Step 2**: Deploy
```bash
# Authenticate
gcloud auth login

# Build
gcloud builds submit --tag gcr.io/PROJECT-ID/spam-detector

# Deploy
gcloud run deploy spam-detector \
    --image gcr.io/PROJECT-ID/spam-detector \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

---

### 4. MICROSOFT AZURE APP SERVICE

**Step 1**: Create Web App
- Go to Azure Portal
- Create new Web App
- Runtime: Python 3.9
- OS: Linux

**Step 2**: Deploy via Git
```bash
# Clone repository
git clone <azure-repo-url>

# Deploy
git push azure main
```

---

### 5. DOCKER LOCAL DEPLOYMENT

**Step 1**: Build Image
```bash
docker build -t spam-detector .
```

**Step 2**: Run Container
```bash
docker run -p 5000:5000 spam-detector
```

**Step 3**: Test
```bash
curl http://localhost:5000/api/health
```

**Step 4**: Push to Docker Hub
```bash
docker tag spam-detector:latest username/spam-detector:latest
docker login
docker push username/spam-detector:latest
```

---

## 🔒 SECURITY CONSIDERATIONS

### 1. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # ...
```

### 2. Authentication
```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/predict', methods=['POST'])
@require_api_key
def predict():
    # ...
```

### 3. Input Validation
```python
def validate_message(message):
    if not isinstance(message, str):
        return False, "Message must be string"
    if len(message) < 1:
        return False, "Message cannot be empty"
    if len(message) > 5000:
        return False, "Message too long (max 5000 chars)"
    return True, None
```

### 4. HTTPS Only
```bash
# In Heroku
heroku config:set SECURE_SSL_REDIRECT=True
```

---

## 📊 MONITORING & LOGGING

### 1. Request Logging
```python
import logging
from datetime import datetime

logging.basicConfig(
    filename='api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.after_request
def log_response(response):
    logger.info(f"Response: {response.status_code}")
    return response
```

### 2. Performance Monitoring
```python
import time

@app.route('/api/predict', methods=['POST'])
def predict():
    start = time.time()
    # ... prediction logic ...
    elapsed = time.time() - start
    logger.info(f"Prediction took {elapsed:.3f}s")
    return jsonify(result)
```

### 3. Error Tracking
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/123456",
    integrations=[FlaskIntegration()]
)
```

---

## 🧪 TESTING API ENDPOINTS

### Using Postman
1. Download Postman from https://www.postman.com
2. Create new request
3. Select POST method
4. Enter endpoint URL
5. Set body as JSON
6. Test different scenarios

### Using pytest
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_predict_spam(client):
    response = client.post(
        '/api/predict',
        json={'message': 'Free money now!!!'}
    )
    assert response.status_code == 200
    assert response.json['prediction'] == 'SPAM'

def test_predict_ham(client):
    response = client.post(
        '/api/predict',
        json={'message': 'Hello, how are you?'}
    )
    assert response.status_code == 200
    assert response.json['prediction'] == 'HAM'
```

---

## 📈 LOAD TESTING

### Using Apache Bench
```bash
# Test 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:5000/api/health

# With POST data
ab -n 1000 -c 10 -p data.json \
   -T application/json \
   http://localhost:5000/api/predict
```

### Using Locust
```python
from locust import HttpUser, task, between

class SpamDetectorUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict(self):
        self.client.post(
            "/api/predict",
            json={"message": "Test message"}
        )
```

---

## 💡 BEST PRACTICES

✅ **Do:**
- Use proper HTTP status codes
- Validate all inputs
- Log important events
- Monitor performance
- Use HTTPS in production
- Set appropriate timeouts
- Document API thoroughly
- Test edge cases
- Monitor error rates
- Keep models updated

❌ **Don't:**
- Store credentials in code
- Return stack traces to clients
- Allow unbounded requests
- Ignore timeout risks
- Deploy without testing
- Log sensitive information
- Use hardcoded API keys
- Ignore security warnings
- Deploy directly from dev

---

## 🎓 SUMMARY

This API is production-ready and can handle:
- ✓ Real-time predictions
- ✓ Batch processing
- ✓ Error handling
- ✓ HTTP standards compliance
- ✓ Easy deployment to cloud
- ✓ Scalability
- ✓ Monitoring and logging

Deploy with confidence! 🚀

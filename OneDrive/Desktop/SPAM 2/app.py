from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import os
import sys
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__, template_folder='templates')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variable
spam_model = None

# ===========================
# LOAD MODEL ON STARTUP
# ===========================

def load_model(model_path='spam_model.pkl'):
    """
    Load the trained spam detection model
    Make sure the model file is in the same directory or provide the full path
    """
    global spam_model
    try:
        # Try different possible paths
        possible_paths = [
            model_path,
            f'./{model_path}',
            os.path.join(os.getcwd(), model_path),
            os.path.join(os.path.dirname(__file__), model_path)
        ]
        
        model_file = None
        for path in possible_paths:
            if os.path.exists(path):
                model_file = path
                break
        
        if not model_file:
            logger.error(f"✗ Model file not found at any location: {model_path}")
            return False
        
        with open(model_file, 'rb') as f:
            model_dict = pickle.load(f)
            spam_model = {
                'model': model_dict['model'],
                'preprocessor': model_dict.get('preprocessor'),
                'feature_engineer': model_dict.get('feature_engineer'),
                'model_name': model_dict.get('model_name', 'Unknown Model')
            }
        logger.info(f"✓ Model loaded: {spam_model['model_name']} from {model_file}")
        return True
    except Exception as e:
        logger.error(f"✗ Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# Load model immediately when app starts
try:
    if not load_model('spam_model.pkl'):
        logger.warning("⚠️ Model loading failed at startup")
except Exception as e:
    logger.error(f"⚠️ Error during initial model load: {str(e)}")

# ===========================
# API ROUTES
# ===========================

@app.route("/")
def index():
    """Serve the main HTML interface"""
    return render_template('index.html')

@app.route("/api")
def api_home():
    return jsonify({"message": "Spam Detection API is running ✅", "version": "2.0"})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': spam_model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict spam/ham for a single message
    
    Request JSON:
    {
        "message": "Your message here"
    }
    
    Response:
    {
        "prediction": "SPAM" or "HAM",
        "spam_probability": 0.95,
        "confidence": 0.95,
        "timestamp": "2026-02-25T..."
    }
    """
    try:
        if not spam_model:
            return jsonify({'error': 'Model not loaded'}), 503
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Clean and preprocess
        cleaned = message.lower().strip() if spam_model['preprocessor'] else message.lower().strip()
        
        # Predict
        prediction = spam_model['model'].predict([cleaned])[0]
        probability = spam_model['model'].predict_proba([cleaned])[0][1]
        
        result = {
            'message': message,
            'prediction': 'SPAM' if prediction == 1 else 'HAM',
            'spam_probability': float(probability),
            'confidence': float(max(probability, 1 - probability)),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Prediction: {result['prediction']} (confidence: {result['confidence']:.2%})")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/predict_batch', methods=['POST'])
def predict_batch():
    """
    Predict on multiple messages
    
    Request JSON:
    {
        "messages": ["message1", "message2", ...]
    }
    
    Response:
    {
        "predictions": [
            {
                "message": "...",
                "prediction": "SPAM" or "HAM",
                "spam_probability": 0.95,
                "confidence": 0.95
            },
            ...
        ]
    }
    """
    try:
        if not spam_model:
            return jsonify({'error': 'Model not loaded'}), 503
        
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing messages field'}), 400
        
        messages = data['messages']
        if not isinstance(messages, list):
            return jsonify({'error': 'Messages must be a list'}), 400
        
        if len(messages) == 0 or len(messages) > 1000:
            return jsonify({'error': 'Messages list must have 1-1000 items'}), 400
        
        # Process all messages
        results = []
        for msg in messages:
            if not isinstance(msg, str) or not msg.strip():
                continue
            
            # Clean and preprocess
            cleaned = msg.lower().strip() if spam_model['preprocessor'] else msg.lower().strip()
            
            # Predict
            prediction = spam_model['model'].predict([cleaned])[0]
            probability = spam_model['model'].predict_proba([cleaned])[0][1]
            
            results.append({
                'message': msg,
                'prediction': 'SPAM' if prediction == 1 else 'HAM',
                'spam_probability': float(probability),
                'confidence': float(max(probability, 1 - probability))
            })
        
        return jsonify({'predictions': results})
    
    except Exception as e:
        logger.error(f"Error in batch prediction: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/model_info', methods=['GET'])
def model_info():
    """Get model information and performance metrics"""
    try:
        if not spam_model:
            return jsonify({'error': 'Model not loaded'}), 503
        
        return jsonify({
            'model_name': spam_model['model_name'],
            'version': '2.0',
            'status': 'ready',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# ===========================
# MAIN
# ===========================

if __name__ == "__main__":
    # Load model
    if not load_model('spam_model.pkl'):
        logger.warning("Model not found. API will work but predictions will fail.")
    
    # Run Flask server
    print("\n" + "="*60)
    print("🚀 Spam Detection System Started")
    print("="*60)
    print("📱 Web Interface: http://127.0.0.1:5000")
    print("🔗 API Base URL: http://127.0.0.1:5000/api")
    print("="*60)
    print("Press CTRL+C to stop the server\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
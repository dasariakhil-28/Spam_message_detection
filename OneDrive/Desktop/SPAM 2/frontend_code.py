# =====================================================================
# PROFESSIONAL SPAM DETECTION - FRONTEND CODE (REACT + FLASK)
# =====================================================================
# This is a complete, production-ready frontend for your spam detection system
# To be used with VS Code
# =====================================================================

# ===========================
# 1. FLASK BACKEND (app.py) - Put this in VS Code with Python environment
# ===========================

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import sys
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variable
spam_model = None

# ===========================
# LOAD MODEL ON STARTUP
# ===========================

def load_model(model_path='spam_detection_model.pkl'):
    """
    Load the trained spam detection model
    Make sure the model file is in the same directory or provide the full path
    """
    global spam_model
    try:
        with open(model_path, 'rb') as f:
            model_dict = pickle.load(f)
            spam_model = {
                'model': model_dict['model'],
                'preprocessor': model_dict['preprocessor'],
                'feature_engineer': model_dict['feature_engineer'],
                'model_name': model_dict['model_name']
            }
        logger.info(f"✓ Model loaded: {spam_model['model_name']}")
        return True
    except FileNotFoundError:
        logger.error(f"✗ Model file not found: {model_path}")
        return False
    except Exception as e:
        logger.error(f"✗ Error loading model: {str(e)}")
        return False

# ===========================
# API ROUTES
# ===========================

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
        cleaned = spam_model['preprocessor'].clean_text(message)
        
        # Extract features
        X_features = spam_model['feature_engineer'].transform([cleaned])
        
        # Predict
        prediction = spam_model['model'].predict(X_features)[0]
        probability = spam_model['model'].predict_proba(X_features)[0][1]
        
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
            cleaned = spam_model['preprocessor'].clean_text(msg)
            
            # Extract features
            X_features = spam_model['feature_engineer'].transform([cleaned])
            
            # Predict
            prediction = spam_model['model'].predict(X_features)[0]
            probability = spam_model['model'].predict_proba(X_features)[0][1]
            
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

if __name__ == '__main__':
    # Load model
    if not load_model('spam_detection_model.pkl'):
        logger.warning("Model not found. API will work but predictions will fail.")
    
    # Run Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)


# ===========================
# 2. FRONTEND CODE (React Component)
# Save as SpamDetector.jsx in your React project
# ===========================

"""
// SpamDetector.jsx - React Component for Spam Detection

import React, { useState, useEffect } from 'react';
import './SpamDetector.css';

const SpamDetector = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [batchMode, setBatchMode] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const API_URL = 'http://localhost:5000/api';

  // Fetch model info on component mount
  useEffect(() => {
    fetchModelInfo();
    loadHistory();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await fetch(`${API_URL}/model_info`);
      const data = await response.json();
      setModelInfo(data);
    } catch (err) {
      setError('Failed to fetch model info');
      console.error(err);
    }
  };

  const predictMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) {
      setError('Please enter a message');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data);
        setHistory([data, ...history.slice(0, 9)]); // Keep last 10
        localStorage.setItem('spamHistory', JSON.stringify([data, ...history.slice(0, 9)]));
        setMessage('');
      } else {
        setError(data.error || 'Prediction failed');
      }
    } catch (err) {
      setError('Connection error. Make sure Flask server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const predictBatch = async () => {
    if (messages.length === 0) {
      setError('Please enter at least one message');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/predict_batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messages.filter(m => m.trim()) })
      });

      const data = await response.json();

      if (response.ok) {
        setHistory([...data.predictions, ...history].slice(0, 50));
        localStorage.setItem('spamHistory', JSON.stringify([...data.predictions, ...history].slice(0, 50)));
        setMessages([]);
        setPrediction(null);
      } else {
        setError(data.error || 'Batch prediction failed');
      }
    } catch (err) {
      setError('Connection error');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = () => {
    const saved = localStorage.getItem('spamHistory');
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  };

  const getPredictionColor = (pred) => {
    return pred === 'SPAM' ? '#ff6b6b' : '#51cf66';
  };

  const getPredictionIcon = (pred) => {
    return pred === 'SPAM' ? '⚠️' : '✅';
  };

  return (
    <div className="spam-detector-container">
      <div className="header">
        <h1>🛡️ AI Spam Detection System</h1>
        <p>Professional spam detection using Machine Learning</p>
        {modelInfo && (
          <div className="model-info">
            <span>Model: {modelInfo.model_name}</span>
            <span>Version: {modelInfo.version}</span>
          </div>
        )}
      </div>

      <div className="mode-toggle">
        <button
          className={!batchMode ? 'active' : ''}
          onClick={() => setBatchMode(false)}
        >
          Single Message
        </button>
        <button
          className={batchMode ? 'active' : ''}
          onClick={() => setBatchMode(true)}
        >
          Batch Prediction
        </button>
      </div>

      {error && <div className="error-message">⚠️ {error}</div>}

      {!batchMode ? (
        // Single message mode
        <form onSubmit={predictMessage} className="input-form">
          <div className="input-group">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Enter message to check..."
              className="message-input"
              disabled={loading}
            />
            <button
              type="submit"
              className="predict-button"
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Analyze Message'}
            </button>
          </div>
        </form>
      ) : (
        // Batch mode
        <div className="batch-input">
          <textarea
            value={messages.join('\\n')}
            onChange={(e) => setMessages(e.target.value.split('\\n'))}
            placeholder="Enter messages (one per line)..."
            className="batch-textarea"
            disabled={loading}
          />
          <button
            onClick={predictBatch}
            className="predict-button"
            disabled={loading}
          >
            {loading ? 'Analyzing...' : `Analyze ${messages.filter(m => m.trim()).length} Messages`}
          </button>
        </div>
      )}

      {prediction && (
        <div className="prediction-result">
          <div
            className="result-box"
            style={{ borderLeft: `4px solid ${getPredictionColor(prediction.prediction)}` }}
          >
            <div className="result-header">
              <span className="result-icon">{getPredictionIcon(prediction.prediction)}</span>
              <span className="result-label">{prediction.prediction}</span>
              <span className="confidence">{(prediction.confidence * 100).toFixed(1)}%</span>
            </div>
            <div className="result-message">"{prediction.message}"</div>
            <div className="result-details">
              <div className="detail-item">
                <label>Spam Score:</label>
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: (prediction.spam_probability * 100) + '%',
                      backgroundColor: getPredictionColor(prediction.prediction)
                    }}
                  />
                </div>
                <span>{(prediction.spam_probability * 100).toFixed(2)}%</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-section">
          <h2>📋 Recent Predictions</h2>
          <div className="history-list">
            {history.map((item, idx) => (
              <div key={idx} className="history-item">
                <span className="history-icon">{getPredictionIcon(item.prediction)}</span>
                <span className="history-text">{item.message.substring(0, 50)}...</span>
                <span className="history-badge" style={{ color: getPredictionColor(item.prediction) }}>
                  {item.prediction}
                </span>
                <span className="history-confidence">{(item.confidence * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SpamDetector;
"""

# ===========================
# 3. CSS STYLING
# Save as SpamDetector.css
# ===========================

"""
.spam-detector-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  margin: 0 0 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header p {
  font-size: 1.1em;
  opacity: 0.9;
  margin: 0;
}

.model-info {
  margin-top: 15px;
  font-size: 0.9em;
  opacity: 0.8;
  display: flex;
  gap: 20px;
  justify-content: center;
}

.mode-toggle {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  justify-content: center;
}

.mode-toggle button {
  padding: 10px 20px;
  border: 2px solid white;
  background: transparent;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s;
}

.mode-toggle button.active {
  background: white;
  color: #667eea;
  font-weight: bold;
}

.mode-toggle button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.input-form,
.batch-input {
  background: white;
  border-radius: 10px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.input-group {
  display: flex;
  gap: 10px;
  flex-direction: column;
}

.message-input,
.batch-textarea {
  padding: 15px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1em;
  resize: vertical;
  min-height: 120px;
  font-family: 'Segoe UI', sans-serif;
  transition: border-color 0.3s;
}

.message-input:focus,
.batch-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.predict-button {
  padding: 12px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.predict-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.predict-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #ff6b6b;
  color: white;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
  text-align: center;
}

.prediction-result {
  margin-bottom: 30px;
}

.result-box {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 1.3em;
  font-weight: bold;
}

.result-icon {
  font-size: 1.5em;
}

.result-label {
  flex: 1;
}

.confidence {
  background: #f0f0f0;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9em;
  color: #666;
}

.result-message {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  color: #666;
  font-style: italic;
  word-break: break-word;
}

.result-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-item label {
  font-weight: bold;
  min-width: 100px;
  color: #666;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s;
}

.history-section {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.history-section h2 {
  margin: 0 0 20px;
  color: #333;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 5px;
  border-left: 3px solid #e0e0e0;
  transition: all 0.3s;
}

.history-item:hover {
  background: #f0f0f0;
  border-left-color: #667eea;
}

.history-icon {
  font-size: 1.2em;
}

.history-text {
  flex: 1;
  color: #666;
  font-size: 0.9em;
}

.history-badge {
  font-weight: bold;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.85em;
}

.history-confidence {
  color: #999;
  font-size: 0.85em;
  min-width: 50px;
  text-align: right;
}

@media (max-width: 600px) {
  .header h1 {
    font-size: 2em;
  }

  .mode-toggle {
    flex-direction: column;
  }

  .mode-toggle button {
    width: 100%;
  }

  .result-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .detail-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .progress-bar {
    width: 100%;
  }
}
"""

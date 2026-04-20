#!/usr/bin/env python
"""
Simple script to run the Spam Detection Flask App
"""

if __name__ == "__main__":
    from app import app, load_model
    
    print("=" * 60)
    print("🚀 SPAM DETECTION WEB APPLICATION")
    print("=" * 60)
    
    # Load the model
    print("\n📦 Loading spam detection model...")
    if load_model('spam_model.pkl'):
        print("✅ Model loaded successfully!")
    else:
        print("⚠️  Model not found. Please ensure 'spam_model.pkl' is in the same directory.")
    
    print("\n" + "=" * 60)
    print("🌐 STARTING WEB SERVER")
    print("=" * 60)
    print("\n📍 Open your browser and go to:")
    print("   👉 http://127.0.0.1:5000")
    print("\n💡 You can now manually type messages to detect spam!")
    print("=" * 60 + "\n")
    
    # Run the Flask app
    app.run(host="127.0.0.1", port=5000, debug=True)

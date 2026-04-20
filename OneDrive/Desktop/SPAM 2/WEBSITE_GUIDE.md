# ✨ SPAM DETECTION WEBSITE - QUICK START

Your spam detection website is now ready! Follow these steps to get it running:

## 📋 Prerequisites
Make sure you have completed the setup with these dependencies installed:

```
pip install flask flask-cors scikit-learn pandas numpy nltk
```

## 🚀 How to Run

### Option 1: Using the run script (Recommended)
```bash
python run.py
```

### Option 2: Direct Python command
```bash
python app.py
```

## 🌐 Access the Website

1. Run the server using one of the commands above
2. Open your web browser
3. Go to: **http://127.0.0.1:5000**

You should see a beautiful interface where you can type messages to detect spam!

## 💻 Features

✅ **Manual Spam Detection** - Type any message and get instant spam detection
✅ **Probability Score** - See the percentage likelihood it's spam  
✅ **Confidence Score** - Check how confident the model is
✅ **Beautiful UI** - Modern, responsive interface
✅ **Real-time Processing** - Instant results as you submit

## 📝 Example Messages to Try

**Legitimate Messages (HAM):**
- "Hey, can we meet tomorrow at 2 PM?"
- "Thanks for your help!"
- "The meeting is rescheduled to Friday"

**Spam Messages:**
- "Congratulations! You've won a free iPhone! Click here to claim"
- "BUY NOW!!! 50% OFF LIMITED TIME OFFER!!!"
- "You've been selected for a special prize. Send us your credit card info"

## 🔧 API Endpoints (for advanced use)

If you want to use the API directly:

### Single Message Prediction
```
POST /api/predict
{
    "message": "Your message here"
}
```

Response:
```
{
    "message": "...",
    "prediction": "SPAM or HAM",
    "spam_probability": 0.95,
    "confidence": 0.95,
    "timestamp": "..."
}
```

### Health Check
```
GET /api/health
```

### Model Info
```
GET /api/model_info
```

## ⚠️ Troubleshooting

**"Cannot connect to server"**
- Make sure the Flask app is running
- Check that port 5000 is not in use
- Try: `python run.py`

**"Model not found"**
- Ensure `spam_model.pkl` is in the same directory as `app.py`
- Check that you have trained the model first

**"Module not found"**
- Install requirements: `pip install -r requirements.txt`

## 📚 Project Structure

```
.
├── app.py                      # Main Flask application
├── run.py                      # Easy startup script
├── spam_model.pkl              # Trained ML model
├── templates/
│   └── index.html              # Web interface
├── requirements.txt            # Dependencies
└── spam.csv                    # Training data
```

## 🎯 Next Steps

- Customize the UI by editing `templates/index.html`
- Train your own model if needed
- Deploy to production using Heroku, AWS, or similar services

Enjoy your spam detector! 🎉

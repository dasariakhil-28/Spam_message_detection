"""
Quick Model Generator Script
This script creates a spam detection model from scratch
"""

import pickle
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
import sys

warnings.filterwarnings('ignore')

def train_model():
    print("=" * 70)
    print("🚀 SPAM DETECTION MODEL TRAINING")
    print("=" * 70)
    
    try:
        # Create sample training data
        print("\n📂 Preparing training data...")
        
        spam_messages = [
            "Congratulations! You've won a free iPhone! Click here to claim",
            "BUY NOW!!! 50% OFF LIMITED TIME OFFER!!!",
            "You've been selected for a special prize. Send us your credit card info",
            "URGENT: Your account will be closed. Verify here immediately",
            "Free money waiting for you! Click now to receive",
            "Earn $5000 per week working from home! No experience needed",
            "You are a WINNER!!! Claim your prize NOW",
            "LAST CHANCE to get cheap medications! Order now",
            "You have inherited $1,000,000! Contact us immediately",
            "Get the hottest deals! Click here for free samples",
            "Cheap mortgages available! No credit checks needed",
            "Hot singles in your area! Click to view",
            "Weight loss pills that REALLY work! Order now",
            "Refinance your home loan TODAY! Save thousands",
            "Lonely? Meet thousands of singles here",
            "Limited time offer! 90% discount on everything",
            "Your package could not be delivered. Click to reschedule",
            "You have unclaimed tax returns waiting",
            "Casino bonus! Play now and win big",
            "Stock tips that will make you rich! Subscribe now"
        ]
        
        ham_messages = [
            "Hey, can we meet tomorrow at 2 PM?",
            "Thanks for your help with the project!",
            "The meeting is rescheduled to Friday",
            "I'll send you the files by email",
            "Let's grab coffee sometime soon",
            "Good morning! How are you today?",
            "The report has been submitted successfully",
            "Can you review my code when you have time?",
            "Looking forward to seeing you at the conference",
            "I received your package. Thank you!",
            "Let me know if you need any clarification",
            "Happy birthday! Hope you have a great day",
            "See you at the meeting tomorrow",
            "Thanks for the update on the project",
            "I'm available for a call anytime this week",
            "Your reservation has been confirmed",
            "The presentation went really well",
            "Please send me the final version",
            "I'll follow up with you next week",
            "Great work on completing the task!"
        ]
        
        X = spam_messages + ham_messages
        y = np.array([1] * len(spam_messages) + [0] * len(ham_messages))
        
        print(f"✅ Prepared {len(X)} training messages")
        print(f"   - Spam: {len(spam_messages)}")
        print(f"   - Ham: {len(ham_messages)}")
        
        # Create and train model
        print("\n🔧 Training model...")
        
        model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
        
        model.fit(X, y)
        
        # Evaluate
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred)
        recall = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)
        
        print("\n📊 Model Performance:")
        print(f"   - Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   - Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"   - Recall:    {recall:.4f} ({recall*100:.2f}%)")
        print(f"   - F1 Score:  {f1:.4f}")
        
        # Save model
        print("\n💾 Saving model...")
        model_dict = {
            'model': model,
            'preprocessor': None,
            'feature_engineer': None,
            'model_name': 'Naive Bayes with TF-IDF'
        }
        
        with open('spam_model.pkl', 'wb') as f:
            pickle.dump(model_dict, f)
        
        print("✅ Model saved as spam_model.pkl")
        
        print("\n" + "=" * 70)
        print("🎉 Training complete! Your website is ready to use.")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = train_model()
    sys.exit(0 if success else 1)

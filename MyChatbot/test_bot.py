import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

# Initialize tools
lemmatizer = WordNetLemmatizer()

# Load the trained model
try:
    with open('chatbot_model.pkl', 'rb') as f:
        clf, vectorizer, responses = pickle.load(f)
except FileNotFoundError:
    print("Error: Model not found. Run 'train.py' first!")
    exit()

# --- DEFINE YOUR TEST CASES HERE ---
# Format: "Sentence to test": "expected_tag"
test_cases = {
    "Hello there": "greeting",
    "See you later alligator": "goodbye",
    "Tell me a joke please": "funny",
    "Who created this bot?": "creator",
    "My computer is slow": "tech_help",  # Note: This might fail if you didn't add tech_help tag
    "What are your specs?": "pc_specs",
    "I am feeling very sad": "mood_sad",
    "Play some rock music": "music",
    "You are an idiot": "insult"
}

print(f"{'TEST SENTENCE':<30} | {'PREDICTED':<15} | {'CONFIDENCE':<10} | {'RESULT'}")
print("-" * 75)

score = 0
total = len(test_cases)

for sentence, expected_tag in test_cases.items():
    # 1. Preprocess (same as training)
    words = nltk.word_tokenize(sentence)
    clean_words = [lemmatizer.lemmatize(w.lower()) for w in words]
    input_text = " ".join(clean_words)
    
    # 2. Predict
    input_vector = vectorizer.transform([input_text])
    predicted_tag = clf.predict(input_vector)[0]
    
    # 3. Get Confidence Score
    probs = clf.predict_proba(input_vector)
    max_prob = np.max(probs)
    
    # 4. Check Result
    status = "✅ PASS" if predicted_tag == expected_tag else f"❌ FAIL (Expected: {expected_tag})"
    if predicted_tag == expected_tag:
        score += 1
        
    print(f"{sentence:<30} | {predicted_tag:<15} | {max_prob:.2f}       | {status}")

print("-" * 75)
print(f"Final Score: {score}/{total} ({score/total*100:.0f}%)")
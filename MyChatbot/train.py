import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier

# Initialize tools
lemmatizer = WordNetLemmatizer()

# Ensure NLTK data is downloaded
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt_tab", quiet=True)

print("Loading data...")

# --- THE FIX IS HERE (added encoding='utf-8') ---
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

patterns = []
tags = []
responses = {}

for intent in data["intents"]:
    # Store responses for later
    responses[intent["tag"]] = intent["responses"]
    
    for pattern in intent["patterns"]:
        # Tokenize: Split sentence into words
        words = nltk.word_tokenize(pattern)
        # Lemmatize: 'running' -> 'run', 'cats' -> 'cat'
        clean_words = [lemmatizer.lemmatize(w.lower()) for w in words]

        # Rejoin words to form a processed sentence
        patterns.append(" ".join(clean_words))
        tags.append(intent["tag"])

# 2. Convert Text to Numbers (Bag of Words)
# Uses regex to keep words only
vectorizer = CountVectorizer(token_pattern=r"\b\w+\b")
X = vectorizer.fit_transform(patterns)
y = tags

print("Training Neural Network...")

# 3. Train the Model (Neural Network)
# (128, 64) = Two layers of neurons.
clf = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=3000, random_state=42)
clf.fit(X, y)

# 4. Save the "Brain"
print("Training complete! Saving model to 'chatbot_model.pkl'...")
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump((clf, vectorizer, responses), f)

print("Done. You can now run 'chat.py'.")
import pickle
import nltk
import random
import numpy as np
import datetime
import psutil
import platform
import re
import subprocess
import webbrowser
import wikipedia
import os
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# --- CONFIGURATION: YOUR EXACT PATHS ---
PATHS = {
    # ✅ UPDATED WITH THE PATHS YOU PROVIDED
    "vscode": r"C:\Users\Ayush\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "opera": r"C:\Users\Ayush\AppData\Local\Programs\Opera GX\opera.exe",
    
    # Folders (You can change these if needed)
    "project_folder": r"C:\Users\Ayush\py ai",
    "downloads": r"C:\Users\Ayush\Downloads",
    "documents": r"C:\Users\Ayush\Documents"
}

# --- LOAD BRAIN ---
try:
    with open("chatbot_model.pkl", "rb") as f:
        clf, vectorizer, responses = pickle.load(f)
except FileNotFoundError:
    print("Error: Model not found. Please run 'train.py' first!")
    exit()

# --- SPECIAL FUNCTIONS ---

def get_system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    system = platform.system()
    return f"I am running on {system}. CPU Usage: {cpu}%. RAM Usage: {ram}%."

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."

def get_date():
    today = datetime.date.today()
    return f"Today's date is {today.strftime('%B %d, %Y')}."

def calculate(user_input):
    expression = re.findall(r"[0-9+\-*/(). ]+", user_input)
    if not expression:
        return "I couldn't find a math problem in that sentence."
    try:
        math_string = "".join(expression)
        result = eval(math_string)
        return f"The answer is {result}."
    except Exception:
        return "Sorry, I couldn't solve that math problem."

def search_wikipedia(query):
    clean_query = query.replace("who is", "").replace("what is", "").replace("tell me about", "").replace("search for", "").strip()
    if not clean_query:
        return "What do you want me to search for?"

    print(f"DEBUG: Searching Wikipedia for '{clean_query}'...")
    try:
        results = wikipedia.search(clean_query)
        if not results:
            return "I couldn't find anything related to that."
        first_result = results[0]
        page = wikipedia.page(first_result, auto_suggest=False)
        return f"According to Wikipedia: {page.summary[:500]}..."
    except wikipedia.DisambiguationError as e:
        return f"That is too vague. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.PageError:
        return "I couldn't find a page for that exact topic."
    except Exception as e:
        return f"Error connecting to Wikipedia: {e}"

def open_application(intent, user_input):
    print(f"DEBUG: Processing command '{intent}'...")
    
    try:
        # --- 1. OPEN VS CODE (Smart Path Detection) ---
        if intent == "open_vscode":
            target_folder = PATHS["project_folder"] # Default backup
            
            # Detect if user typed a path (Look for pattern like "C:\...")
            path_match = re.search(r'[a-zA-Z]:\\[\w\\ ]+', user_input)
            
            if path_match:
                extracted_path = path_match.group(0).strip()
                if os.path.exists(extracted_path):
                    target_folder = extracted_path
                else:
                    return f"Error: The path '{extracted_path}' does not exist on your PC."

            if os.path.exists(PATHS["vscode"]):
                # We pass the extracted folder to VS Code
                subprocess.Popen([PATHS["vscode"], target_folder])
                return f"VS Code opened in: {target_folder}"
            else:
                return f"Error: VS Code not found at {PATHS['vscode']}"

        # --- 2. OPEN OPERA GX ---
        elif intent == "open_opera":
            if os.path.exists(PATHS["opera"]):
                subprocess.Popen([PATHS["opera"]])
                return "Opera GX launched."
            else:
                return f"Error: Opera not found at {PATHS['opera']}"

        # --- 3. OPEN FOLDERS ---
        elif intent == "open_folder":
            target_path = PATHS["project_folder"] # Default
            
            # Check for path in input first
            path_match = re.search(r'[a-zA-Z]:\\[\w\\ ]+', user_input)
            if path_match and os.path.exists(path_match.group(0)):
                target_path = path_match.group(0)
            # Keywords fallback
            elif "download" in user_input.lower():
                target_path = PATHS["downloads"]
            elif "document" in user_input.lower():
                target_path = PATHS["documents"]
            
            if os.path.exists(target_path):
                os.startfile(target_path)
                return f"Opened folder: {target_path}"
            else:
                return f"Error: Folder not found at {target_path}"

        # --- 4. STANDARD APPS ---
        elif intent == "open_chrome":
            try:
                subprocess.Popen(["start", "chrome"], shell=True)
            except Exception:  # <--- FIXED: Added 'Exception' to silence the warning
                webbrowser.open("https://www.google.com")
            return "Chrome launched."
            
        elif intent == "open_notepad":
            subprocess.Popen(["notepad.exe"])
            return "Notepad opened."
            
        elif intent == "open_youtube":
            webbrowser.open("https://www.youtube.com")
            return "YouTube opened."

    except Exception as e:
        return f"Error opening app: {e}"

    return "I don't know how to open that app yet."
# --- MAIN CHAT BOT ---

def get_response(user_input):
    # 1. Preprocess
    words = nltk.word_tokenize(user_input)
    clean_words = [lemmatizer.lemmatize(w.lower()) for w in words]
    input_text = " ".join(clean_words)

    # 2. Predict Intent
    input_vector = vectorizer.transform([input_text])
    predicted_tag = clf.predict(input_vector)[0]

    # 3. Check Confidence
    probs = clf.predict_proba(input_vector)
    max_prob = np.max(probs)

    if max_prob < 0.5:
        # Randomize the "I don't know" response to feel more human
        fallback_responses = [
            "I missed that. Could you say it differently?",
            "My circuits are confused. What do you mean?",
            "I'm still learning, Ayush. Can you teach me that?",
            "404 Error: Understanding not found.",
            "That went over my head. Try again?"
        ]
        return random.choice(fallback_responses)

    # 4. HANDLE SPECIAL TAGS
    if predicted_tag in ["open_vscode", "open_opera", "open_folder", "open_chrome", "open_notepad", "open_youtube"]:
        return open_application(predicted_tag, user_input)
        
    elif predicted_tag == "time":
        return get_time()

    elif predicted_tag == "date":
        return get_date()

    elif predicted_tag == "system_info":
        return get_system_info()

    elif predicted_tag == "calc":
        return calculate(user_input)

    elif predicted_tag == "wikipedia":
        return search_wikipedia(user_input)

    # 5. Standard AI Response
    return random.choice(responses[predicted_tag])

# --- RUN LOOP ---
# --- RUN LOOP ---
# This "if" statement is CRITICAL. It prevents the chat loop 
# from running when we import the file into the GUI.
if __name__ == "__main__":
    print("\n--- SUPER CHATBOT (AI + Tools) ---")
    while True:
        # ... your loop code ...
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        bot_reply = get_response(user_input)
        print(f"Bot: {bot_reply}")
# AI Assistant 🤖⚡
A high-performance assistant built with Python. This bot combines Natural Language Processing (NLP) with system-level automation for a sleek, interactive experience.

## ✨ Key Features
* 🧠 Neural Network Brain: Uses MLPClassifier to categorize intents with high accuracy.

* 🖥️ System Automation: Open VS Code (at specific paths), Opera GX, Notepad, and Chrome.

* 📂 Folder Navigation: Quick access to Downloads, Documents, and project directories.

* 🌐 Wikipedia Integration: Real-time info retrieval with smart search fallback.

* 📊 System Monitoring: Live tracking of CPU usage, RAM stats, and platform info.

* 🎨 Cyberpunk UI: A modern, Dark Mode interface built with CustomTkinter.


## 🛠️ Tech Stack
* Language: Python 3.11+

* NLP: NLTK (Tokenization & Lemmatization)

* ML: Scikit-Learn (CountVectorizer & MLP Neural Network)

* GUI: CustomTkinter

* Utilities: Psutil, Wikipedia-API, Subprocess

## 🚀 Getting Started
### 1. Installation
* Clone the repository and install the required dependencies:

```sh
pip install nltk scikit-learn customtkinter psutil wikipedia
```
### 2. Training the Model
* Whenever you update intents.json, you must retrain the model to learn the new patterns:

Bash
python train.py
3. Running the App
Launch the graphical interface directly:

```Bash
python gui.py
```
## 📂 Project Structure
* gui.pyw: The main entry point for the graphical application.

* chat.py: The logic engine handling responses and system commands.

* train.py: Script to train the Neural Network.

* intents.json: The knowledge base containing patterns and responses.

* chatbot_model.pkl: The serialized "brain" of your trained model.

## ⚙️ Configuration
* Update your application paths in the PATHS dictionary within chat.py:

### Windows
```
PATHS = {
    "vscode": r"C:\Users\User_name\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "opera": r"C:\Users\User_name\AppData\Local\Programs\Opera GX\opera.exe"
}
```
## 🤝 Credits
Developed by Ayush. Built for speed, utility, and chatty vibes. 🚀
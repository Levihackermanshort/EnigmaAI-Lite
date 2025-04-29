from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

app = Flask(__name__)

# --- Intent Classification (Simplified) ---
def classify_intent(query):
    if re.search(r"(who is|who was)", query, re.IGNORECASE):
        return "WHO_IS"
    elif re.search(r"(what is|what was)", query, re.IGNORECASE):
        return "WHAT_IS"
    elif re.search(r"(tell me about)", query, re.IGNORECASE):
        return "TELL_ME_ABOUT"
    else:
        return "UNKNOWN"

# --- Knowledge Base ---
knowledge_base = {
    "Enigma AI": "I am Enigma AI Lite, a simple chatbot designed to help answer your questions using information from the internet.",
    "Python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
    "Flask": "Flask is a lightweight web application framework for Python, designed to be simple and easy to use.",
}

# --- Search Function (Using DuckDuckGo Instant Answer API) ---
def search_ddg(query):
    url = f"https://api.duckduckgo.com/"
    params = {
        'q': query,
        'format': 'json',
        'pretty': 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Try to get the most relevant information
        answer = data.get('AbstractText', '') or \
                 data.get('Answer', '') or \
                 next((topic.get('Text', '') for topic in data.get('RelatedTopics', []) if topic.get('Text')), '')
        
        return answer if answer else "I couldn't find specific information about that."
    
    except Exception as e:
        print(f"Error during search: {e}")
        return "Sorry, I encountered an error while searching for information."

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query", "").strip()
    
    if not query:
        return jsonify({
            "answer": "Please ask me a question!",
            "source": None
        })

    # Check knowledge base first
    for key, value in knowledge_base.items():
        if key.lower() in query.lower():
            return jsonify({
                "answer": value,
                "source": "Local Knowledge Base"
            })

    # If not in knowledge base, search online
    answer = search_ddg(query)
    
    return jsonify({
        "answer": answer,
        "source": "DuckDuckGo" if answer else None
    })

if __name__ == "__main__":
    app.run(debug=True) 
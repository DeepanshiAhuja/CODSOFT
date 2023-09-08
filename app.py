from flask import Flask, render_template, request
import random
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chatbot_response():
    return render_template("chat.html")
if __name__ == '__main__':
    app.run(debug=True)
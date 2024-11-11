from flask import Flask, request, jsonify, render_template
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot("intents.json")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if user_input:
        response = chatbot.handle_user_input(user_input)
    else:
        response = "I'm here to help, but I didn't catch that."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

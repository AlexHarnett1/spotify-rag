from flask import Blueprint, request, jsonify
from server.rag.rag import ask_user_question

routes = Blueprint("routes", __name__)

@routes.route("/api/ping", methods=["GET"])
def ping():
    print('PINGING')
    return jsonify({"message": "pong"})

@routes.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["userMessage"]
    print('User message: ', user_message)
    
    reply = ask_user_question(user_message)
    return jsonify({"message": reply})

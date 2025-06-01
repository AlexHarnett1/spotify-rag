from flask import Blueprint, request, jsonify

routes = Blueprint("routes", __name__)

@routes.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

@routes.route("/chat", methods=["POST"])
def chat():
    return 'HELLO'

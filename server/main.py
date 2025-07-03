from server.rag.rag import ask_user_question
from flask import Flask, request, jsonify
from flask_cors import CORS
from server.router.routes import routes


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
app.register_blueprint(routes)  # Register router

if __name__ ==  "__main__":
    app.run(port=3001)



# Terminal logic
# def main():
#     ask_user_question()


# if __name__ == "__main__":
#     main()
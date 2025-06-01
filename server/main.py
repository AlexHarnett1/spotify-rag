from server.rag.rag import ask_user_question
from flask import Flask, request, jsonify
from server.router.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)  # Register router

if __name__ ==  "__main__":
    app.run(port=5000)



# Terminal logic
# def main():
#     ask_user_question()


# if __name__ == "__main__":
#     main()
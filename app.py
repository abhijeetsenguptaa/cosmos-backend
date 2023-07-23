# app.py
from flask import Flask,jsonify
from flask_cors import CORS
from routes.user_route import userRoute
from routes.message_route import chatbot_bp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify(
        {'msg':'Welcome to Cosmos'}
        )

# Registering the userRoute blueprint
app.register_blueprint(userRoute, url_prefix='/user')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

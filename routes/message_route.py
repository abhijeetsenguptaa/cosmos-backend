
from flask import Flask, Blueprint, request,jsonify
import os
import openai
from middleware.authentication import authentication
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Create the chatbot blueprint
chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chat', methods=['POST'])
@authentication
def chat(decoded_code):
    data = request.get_json()
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({'message': 'Invalid request data.'}), 400

    # Send user input as a prompt to the GPT-3.5 Turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "assistant",
                "content": "You have to act as a advisor to parents for there small kids."
                # "content":"You are a male parenting influencer with expertise in solving various parenting challenges. Your goal is to answer user questions in the same language they use and respond with a human-like tone, replicating the user's style. Ask clarifying questions to parents if needed."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7,  # Controls the randomness of the response
        max_tokens=150  # Control the length of the generated response
    )

    # Get the chatbot's response from the API response
    chatbot_response = response['choices'][0]['message']['content']

    return jsonify({'chatbot_response': chatbot_response})

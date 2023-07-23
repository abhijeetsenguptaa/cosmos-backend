# routes/user_routes.py
from flask import Blueprint, jsonify, request
import bcrypt
from configs.connection import get_db_connection
import jwt

userRoute = Blueprint('user', __name__)

@userRoute.route('/')
def users():
    return jsonify(
        {
            'msg': 'users'
        }
    )

@userRoute.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Connect to the MongoDB database
    db = get_db_connection()

    # Get the "users" collection
    users_collection = db.users

    # Find the user with the given email in the "users" collection
    user = users_collection.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Generate a JWT token upon successful login
        token = jwt.encode({'email':user['email']}, 'abhijeet', algorithm='HS256')

        return jsonify({'message': 'Login successful!', 'token': token})
    
    else:
        return jsonify({'message': 'Invalid credentials. Please try again.'})


@userRoute.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Connect to the MongoDB database
    db = get_db_connection()

    # Get the "users" collection
    users_collection = db.users

    # Check if the email already exists in the "users" collection
    if users_collection.find_one({'email': email}):
        return jsonify({'message': 'Email already exists. Please choose a different email.'}), 409

    # Insert the new user details into the "users" collection
    user_data = {
        'email': email,
        'password': hashed_password
    }
    users_collection.insert_one(user_data)

    return jsonify({'message': f'Registration successful for email: {email}'})


@userRoute.route('/delete', methods=['POST'])
def delete():
    # Handle user account deletion here
    data = request.get_json()
    email = data.get('email')

    # Connect to the MongoDB database
    db = get_db_connection()

    # Get the "users" collection
    users_collection = db.users

    # Check if the email exists in the "users" collection
    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({'message': 'Email does not exist.'}), 404

    # Delete the user account from the "users" collection
    users_collection.delete_one({'email': email})

    return jsonify({'message': f'User account "{email}" deleted successfully.'})

from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

class Authentication:
    @staticmethod
    def register_user(users_collection):
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')

            if not username or not email or not password or not confirm_password:
                return jsonify({'error': 'Missing required fields'}), 400

            if password != confirm_password:
                return jsonify({'error': 'Passwords do not match'}), 400

            # Check if the user already exists
            if users_collection.find_one({'email': email}):
                return jsonify({'error': 'User already exists'}), 400

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create the user document
            user = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'images': []
            }

            # Insert the user into the database
            users_collection.insert_one(user)

            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def login_user(users_collection):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({'error': 'Missing required fields'}), 400

            user = users_collection.find_one({'email': email})
            if not user:
                return jsonify({'error': 'User not found'}), 404

            if not check_password_hash(user['password'], password):
                return jsonify({'error': 'Invalid credentials'}), 401

            session['user_id'] = str(user['_id'])
            return jsonify({'message': 'Login successful'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
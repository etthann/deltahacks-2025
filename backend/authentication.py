from flask import request, jsonify
import bcrypt
import re

class Authentication:

    @staticmethod
    def register_user(users_collection):
        try:
            data = request.json
            username = data['username']
            password = data['password'].encode('utf-8')
            email = data['email']
            confirm_password = data['confirmPassword'].encode('utf-8')

            # Validate the request data
            validation_message = Authentication.validate_request_data(users_collection, username, password, email,
                                                                      confirm_password)
            if validation_message is not None:
                return validation_message

            # Hash the password
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # Store the user with the hashed password
            users_collection.insert_one({
                'username': username,
                'password': hashed_password,
                'email': email
            })

            return jsonify({'message': 'User created successfully'}), 200
        except Exception as e:
            return jsonify({'message': 'An error occurred'}), 500

    @staticmethod
    def validate_request_data(users_collection, username, password, email=None, confirm_password=None):
        username_regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).*$'
        validations = {
            'Email is required': not email,
            'Username is required': not username,
            'Password is required': not password,
            'Confirm password is required': not confirm_password,
            'Invalid email address': email and not re.match(r"[^@]+@[^@]+\.[^@]+", email),
            'Passwords do not match': password != confirm_password,
            'Password must be at least 8 characters': password and len(password) < 8,
            'Username must be at least 4 characters': username and len(username) < 4,
            'Username must be alphanumeric, contain an uppercase letter and at least one special character': username and not re.match(
                username_regex, username),
            'Username already exists': username and users_collection.find_one({'username': username}) is not None,
            'Email already exists': email and users_collection.find_one({'email': email}) is not None
        }

        for message, condition in validations.items():
            if condition:
                return jsonify({'message': message}), 400

        return None

    @staticmethod
    def login_user(users_collection):
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Missing username or password'}), 400

        username = data['username']
        password = data['password'].encode('utf-8')

        if username is None or password is None or username == '' or password == '':
            return jsonify({'message': 'Missing username or password'}), 400

        user = users_collection.find_one({'username': username})
        if user is None:
            return jsonify({'message': 'User does not exist'}), 401

        if not bcrypt.checkpw(password, user['password']):
            return jsonify({'message': 'Invalid password'}), 401

        return jsonify({'message': 'Logged in successfully'}), 200
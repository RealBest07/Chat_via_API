from datetime import datetime, timedelta
from typing import Annotated
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests
from main import chatbotdb 

app = Flask(__name__)
app.config['SECRET_KEY'] = "48c0acb322f89dce580bb7d6b889bc94c86bdabb952f9440373a68c0f3dad8cc"
app.config['JWT_SECRET_KEY'] = "48c0acb322f89dce580bb7d6b889bc94c86bdabb952f9440373a68c0f3dad8cc"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

fake_users_db = {
    "best": {
        "username": "best",
        "full_name": "best pheerapon",
        "email": "best@pp.com",
        "hashed_password": "$2b$12$9WlCpHu254avxcQe34txuOo/ZC5JWfPrgcvtebxPPDZTRdp0XZ29S",#Hard_password
        "disabled": False,
    }
}


@app.route('/token', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = fake_users_db.get(username)
    if not user or not bcrypt.check_password_hash(user['hashed_password'], password):
        return jsonify({"message": "Incorrect username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


@app.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    user = fake_users_db.get(current_user)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user), 200

@app.route('/response', methods=['GET','POST'])
@jwt_required()
def chat():
    url = "http://127.0.0.1:5001/question"  # replace with your actual URL
    response = requests.get(url)
    data = response.json()
    chat_response = chatbotdb(data, "mongodb://localhost:27017/",'question_db','questions' )
    current_user = get_jwt_identity()
    user = fake_users_db.get(current_user)
    if not user:
        return jsonify({"response": "User not found"}), 404
    
    return jsonify({'response': chat_response})

if __name__ == "__main__":
    app.run(port=5002)

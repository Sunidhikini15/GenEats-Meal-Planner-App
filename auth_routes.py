from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if User.find_user(data["email"]):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    User.create_user(data["username"], data["email"], hashed_password)
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.find_user(data["email"])
    
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])
    return jsonify({"token": token}), 200

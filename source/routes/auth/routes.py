from flask import Blueprint, request, jsonify
from source.models.model import MongoDB
from werkzeug.security import generate_password_hash, check_password_hash
from source.utils import utils

mongo = MongoDB()

auth_bp = Blueprint('auth', __name__,url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    user = mongo.users.find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "Email not registered."}), 400

    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Incorrect password."}), 400

    return jsonify({"success": True, "message": "Login successful."}), 200


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    if not utils.is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400

    if not utils.is_valid_password(password):
        return jsonify({"success": False, "message": "Password must be at least 8 characters long, include an uppercase letter, lowercase letter, and a number."}), 400

    if mongo.users.find_one({"email": email}):
        return jsonify({"success": False, "message": "Email already registered."}), 400

    hashed_password = generate_password_hash(password)
    mongo.users.insert_one({
        "email": email,
        "password": hashed_password
    })

    return jsonify({"success": True, "message": "Signup successful."}), 201
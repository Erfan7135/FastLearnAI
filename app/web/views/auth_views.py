from flask import request, jsonify, Blueprint, session, g
from app.web.db.models.base import User
from app.web.app import db
from app.web.hooks import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/user", methods=["GET"])
def get_user():
    return g.user.as_dict() 

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # print(data)
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not password or not username:
        return jsonify({"error": "Email and password are required"}), 400
    
    if User.find_by(email=email):
        return jsonify({"error": "Email already exists"}), 400
    
    if User.find_by(username=username):
        return jsonify({"error": "Username already exists"}), 400
    
    new_user = User(email=email, username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id  # Login Immediately after signup

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.find_by(email=email)
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    session.permanent = True  # Make the session permanent
    session['user_id'] = user.id
    
    return jsonify({"message": "Successfully logged in.", "user": user.as_dict()})

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({"message": "Successfully logged out."}), 200

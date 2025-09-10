from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__, url_prefix='/auth/')

@user_bp.route('/register', methods=['POST'])
def register():
    return "", 501 

@user_bp.route('/login', methods=['POST'])
def login():
    return "", 501 

@user_bp.route('/logout', methods=['POST'])
def logout():
    return "", 501 

@user_bp.route('/refresh', methods=['POST'])
def refresh():
    return "", 501 

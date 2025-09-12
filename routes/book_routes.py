from flask import Blueprint, request, jsonify

book_bp = Blueprint('book', __name__)

@book_bp.route('/', methods=['GET'])
def all_books():
    return "", 501 

@book_bp.route('/<int:book_id>', methods=['GET'])
def single_book(book_id):
    return "", 501 

@book_bp.route('/search', methods=['GET'])
def search(book_id):
    title = request.args.get('title')
    category = request.args.get('category')
    return "", 501 
from flask import Blueprint, request, jsonify
from models.book import Book
from utils.serializers import serialize_rows

book_bp = Blueprint('book', __name__)


@book_bp.route('/', methods=['GET'])
def all_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    query = Book.query.order_by(Book.id).paginate(page=page, per_page=per_page)

    return serialize_rows(query), 200

@book_bp.route('/<int:book_id>', methods=['GET'])
def single_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())

@book_bp.route('/search', methods=['GET'])
def search():
    title = request.args.get('title')
    category = request.args.get('category')
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    query = Book.query

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))

    result = query.order_by(Book.id).paginate(page=page, per_page=per_page)

    return serialize_rows(result), 200
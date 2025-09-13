from flask import Blueprint, request, jsonify
from sqlalchemy import select
from models.book import Book
from utils.serializers import serialize_rows
from extensions import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def all_categories():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    subquery = db.session.query(Book.category).distinct().order_by(Book.category)
    pagination = subquery.paginate(page=page, per_page=per_page)

    data = [{"name": category[0]} for category in pagination.items]

    return jsonify({
        "data": data,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    })
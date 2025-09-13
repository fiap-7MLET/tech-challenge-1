from flask import jsonify

def serialize_rows(rows):
    items = rows.items
    books_data = [book.to_dict() for book in items]
    return jsonify({
            "data": books_data,
            "page": rows.page,
            "per_page": rows.per_page,
            "total": rows.total,
            "pages": rows.pages
        })
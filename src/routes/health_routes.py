from flask import Blueprint, jsonify
from extensions import db
from sqlalchemy import select, literal_column

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health():
    status = "ok"
    db_status = "up"
    error = False
    try:
        db.session.execute(select(literal_column("1")))
    except Exception as e:
        status = "error"
        db_status = f"[DB Health Error] {e}"
        error = True

    return jsonify({
        "status": status,
        "database": db_status
    }), 500 if error else 200
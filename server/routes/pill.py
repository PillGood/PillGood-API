from flask import Blueprint, request, jsonify
pill_bp = Blueprint('pill', __name__, url_prefix='/pill')

@pill_bp.route('/', methods=['GET'])
def index():
    return 'Pill Page'
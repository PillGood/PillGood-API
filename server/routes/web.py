from flask import Blueprint, render_template, request, jsonify, url_for
from server.services import qr_service
import io, json, string, random

web_bp = Blueprint("web", __name__)

@web_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@web_bp.route('/qrcode', methods=['GET'])
def qrcode():
    return render_template('qrcode.html')

@web_bp.route('/qrcode', methods=['POST'])
def generator_qrcode():
    data = list(request.form.to_dict(flat=False).keys())[0]

    hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))

    image = qr_service.create_qr_code(data)
    image.save('./server/static/image/code.png?' + hash)

    return jsonify({
        'code': 'success',
        'url': url_for('static', filename='image/code.png?' + hash)
    })
    
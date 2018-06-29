from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@web_bp.route('/qrcode', methods=['GET'])
def generator_qrcode():
    return render_template('qrcode.html')
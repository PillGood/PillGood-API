from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from server.routes.pill import pill_bp
app.register_blueprint(pill_bp)
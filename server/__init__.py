from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from server.config import config_by_name

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config])

    db.init_app(app)
    
    from server.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from server.routes.pill import pill_bp
    app.register_blueprint(pill_bp)

    return app

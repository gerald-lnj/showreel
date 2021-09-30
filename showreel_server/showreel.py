from flask import Flask
from flask_cors import CORS
from app.api.clip import clip_bp
from app.api.reel import reel_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(clip_bp)
    app.register_blueprint(reel_bp)
    CORS(app)
    return app


app = create_app()

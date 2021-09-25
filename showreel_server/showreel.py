from flask import Flask


def create_app():
    from app.api.views import bp
    app = Flask(__name__)

    app.register_blueprint(bp)
    return app

app = create_app()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
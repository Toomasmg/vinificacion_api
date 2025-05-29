from flask import Flask
from config import Config
from database import db, init_app
from routes.variety import variety_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.register_blueprint(variety_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

from flask import Flask
from config import Config
from database import db, init_app
from routes.grape_reception import grape_reception_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # ✅ Esto ya carga SECRET_KEY desde config.py

    init_app(app)

    # SOLO EN DESARROLLO: resetear tablas
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Registrar rutas
    app.register_blueprint(grape_reception_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

from flask import Flask
from config import Config
from database import db, init_app

def create_app():
    app = Flask(__name__)

    # Cargar configuración desde config.py
    app.config.from_object(Config)

    # Inicializar base de datos
    init_app(app)
    from models import grape_reception
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

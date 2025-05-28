from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.database import db
from routes.fermentations import fermentations_bp
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración desde el entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "vinificacion-secreta"

    # Inicializar base de datos y migraciones
    db.init_app(app)
    Migrate(app, db)

    # Registrar los blueprints
    app.register_blueprint(fermentations_bp)

    return app

# Ejecutar la aplicación
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

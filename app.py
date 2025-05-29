from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.database import db
from routes.grapes_receptions import grape_reception_bp
from routes.varieties import variety_bp
from routes.fermentations import fermentations_bp
from models.variety import Variety
from models.grape_reception import GrapeReception
from models.fermentation import Fermentation
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "vinificacion-secreta"

    db.init_app(app)
    Migrate(app, db)

    # Blueprints
    app.register_blueprint(grape_reception_bp)
    app.register_blueprint(variety_bp)
    app.register_blueprint(fermentations_bp)

    # Página de inicio
    @app.route('/')
    def index():
        return render_template('index.html')

    # Vista general con todos los datos
    @app.route('/dashboard')
    def dashboard():
        varieties = Variety.query.all()
        receptions = GrapeReception.query.all()
        fermentations = Fermentation.query.all()
        return render_template("dashboard.html", varieties=varieties, receptions=receptions, fermentations=fermentations)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)

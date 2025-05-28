from flask import Flask
from flask_cors import CORS
from config.config import DATABASE_CONNECTION_URI
from models.database import db
from routes.fermentations import fermentations_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "vinosecreto"

db.init_app(app)
CORS(app)

# Registrar blueprint de fermentation
app.register_blueprint(fermentations_bp)

@app.route("/")
def home():
    return "Bienvenido a la API de Vinificación 🍇"

# Crear las tablas automáticamente si no existen
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    print("🚀 Servidor Flask iniciado en http://localhost:5000")
    app.run(debug=True)

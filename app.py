from flask import Flask, redirect
from config.config import DATABASE_CONNECTION_URI
from routes.aging import aging_bp
from routes.Storage import storage_bp
from models.db import db

app = Flask(__name__)
app.secret_key = 'clave_secreta'

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.register_blueprint(aging_bp)
app.register_blueprint(storage_bp)

# Ruta raíz redirige a /storage
@app.route('/')
def index():
    return redirect('/storage')

with app.app_context():
    from models.Aging import Aging
    from models.storage import Storage
    from models.grape_variety import GrapeVariety
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

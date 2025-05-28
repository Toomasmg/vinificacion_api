from config import DATABASE_CONECTION_URI
from routes.bottlings import bottling_bp
from flask import Flask
from models.db import db
from sqlalchemy import text
app = Flask(__name__)

app.secret_key = "secret_key"
app.register_blueprint(bottling_bp)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.bottling import Bottling
    from models.aging import Aging
    db.session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    db.drop_all()
    db.session.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    db.create_all()

if __name__ == "__main__" :
    app.run(debug=True)
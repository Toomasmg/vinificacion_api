from flask import Flask,redirect,url_for,render_template
from config.config import DATABASE_CONECTION_URI
from models.db import db
from routes.variety import variety_bp
from routes.grape_reception import grape_reception_bp
from routes.fermentations import fermentations_bp
from routes.bottlings import bottling_bp
from sqlalchemy import text
app = Flask(__name__)
app.register_blueprint(variety_bp)
app.register_blueprint(grape_reception_bp)
app.register_blueprint(fermentations_bp)
app.register_blueprint(bottling_bp)

app.secret_key = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
@app.route("/")
def index():
    return render_template("index.html")
# for rule in app.url_map.iter_rules():
    # print(rule.endpoint, rule)
with app.app_context():
    from models.variety import Variety
    from models.grape_reception import GrapeReception
    from models.fermentation import Fermentation
    from models.bottling import Bottling
    from models.aging import Aging
    db.session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    db.drop_all()
    db.session.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
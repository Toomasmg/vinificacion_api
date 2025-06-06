import os
from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
from werkzeug.utils import secure_filename
from models.db import db
from models.grape_reception import GrapeReception
from models.variety import Variety
from datetime import datetime

grape_reception_bp = Blueprint("grape_reception", __name__, url_prefix="/receptions")

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@grape_reception_bp.route("/", methods=["GET"])
def list_receptions():
    receptions = GrapeReception.query.all()
    return render_template("grape_reception/receptions.html", receptions=receptions)

@grape_reception_bp.route("/add", methods=["GET"])
def show_add_form():
    varieties = Variety.query.all()
    return render_template("grape_reception/add_reception.html", varieties=varieties)

@grape_reception_bp.route("/add", methods=["POST"])
def add_reception():
    try:
        name = request.form["name"]
        grape_type = request.form["grape_type"]
        quantity = int(request.form["quantity"])
        weight = float(request.form["weight"])
        reception_date = datetime.strptime(request.form["reception_date"], "%Y-%m-%d").date()
        variety_id = request.form["variety_id"]

        image_file = request.files.get("image")
        image_path = None

        if image_file and image_file.filename != "" and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)

        new_reception = GrapeReception(
            name=name,
            grape_type=grape_type,
            quantity=quantity,
            weight=weight,
            reception_date=reception_date,
            variety_id=variety_id,
            image_path=image_path
        )

        db.session.add(new_reception)
        db.session.commit()
        flash("Recepción agregada con éxito", "success")
        return redirect(url_for("grape_reception.list_receptions"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar recepción: {str(e)}", "danger")
        return redirect(url_for("grape_reception.show_add_form"))

@grape_reception_bp.route("/edit/<string:reception_id>", methods=["GET"])
def edit_reception_form(reception_id):
    reception = GrapeReception.query.get(reception_id)
    if reception is None:
        abort(404)
    return render_template("grape_reception/edit_reception.html", reception=reception)

@grape_reception_bp.route("/edit/<string:reception_id>", methods=["POST"])
def edit_reception(reception_id):
    reception = GrapeReception.query.get(reception_id)
    if reception is None:
        abort(404)

    try:
        reception.name = request.form["name"]
        reception.grape_type = request.form["grape_type"]
        reception.quantity = int(request.form["quantity"])
        reception.weight = float(request.form["weight"])
        reception.reception_date = datetime.strptime(request.form["reception_date"], "%Y-%m-%d").date()
        db.session.commit()
        flash("Recepción actualizada con éxito", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {str(e)}", "danger")

    return redirect(url_for("grape_reception.list_receptions"))

@grape_reception_bp.route("/delete/<string:reception_id>", methods=["POST"])
def delete_reception(reception_id):
    reception = GrapeReception.query.get(reception_id)
    if reception is None:
        abort(404)

    try:
        db.session.delete(reception)
        db.session.commit()
        flash("Recepción eliminada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")

    return redirect(url_for("grape_reception.list_receptions"))

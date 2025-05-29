from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db
from models.variety import Variety

variety_bp = Blueprint("variety", __name__, url_prefix="/varieties")

# Mostrar todas las variedades
@variety_bp.route("/", methods=["GET"])
def list_varieties():
    varieties = Variety.query.all()
    return render_template("variety/varieties.html", varieties=varieties)

# Mostrar formulario para agregar
@variety_bp.route("/add", methods=["GET"])
def show_add_variety():
    return render_template("variety/add_variety.html")

# Guardar nueva variedad
@variety_bp.route("/add", methods=["POST"])
def add_variety():
    name = request.form["name"]
    description = request.form["description"]

    try:
        new_variety = Variety(name=name, description=description)
        db.session.add(new_variety)
        db.session.commit()
        flash("Variedad agregada con éxito", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for("variety.list_varieties"))

# Mostrar formulario para editar
@variety_bp.route("/delete/<string:variety_id>", methods=["POST"])
def delete_variety(variety_id):
    variety = Variety.query.get(variety_id)
    if not variety:
        flash("Variedad no encontrada", "danger")
        return redirect(url_for("variety.list_varieties"))

    try:
        db.session.delete(variety)
        db.session.commit()
        flash("Variedad eliminada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")

    return redirect(url_for("variety.list_varieties"))

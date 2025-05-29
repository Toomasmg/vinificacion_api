from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db
from models.variety import Variety

variety_bp = Blueprint("variety", __name__, url_prefix="/varieties")

# ----------------------
# MOSTRAR TODAS LAS VARIEDADES
# ----------------------
@variety_bp.route("/", methods=["GET"])
def list_varieties():
    varieties = Variety.query.all()
    return render_template("variety/varieties.html", varieties=varieties)

# ----------------------
# FORMULARIO PARA AGREGAR VARIEDAD
# ----------------------
@variety_bp.route("/add", methods=["GET"])
def show_add_variety():
    return render_template("variety/add_variety.html")

# ----------------------
# GUARDAR NUEVA VARIEDAD
# ----------------------
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

# ----------------------
# FORMULARIO PARA EDITAR VARIEDAD
# ----------------------
@variety_bp.route("/edit/<string:variety_id>", methods=["GET"])
def edit_variety_form(variety_id):
    variety = Variety.query.get(variety_id)
    if not variety:
        flash("Variedad no encontrada", "danger")
        return redirect(url_for("variety.list_varieties"))
    return render_template("variety/edit_variety.html", variety=variety)

# ----------------------
# ACTUALIZAR VARIEDAD
# ----------------------
@variety_bp.route("/edit/<string:variety_id>", methods=["POST"])
def edit_variety(variety_id):
    variety = Variety.query.get(variety_id)
    if not variety:
        flash("Variedad no encontrada", "danger")
        return redirect(url_for("variety.list_varieties"))

    try:
        variety.name = request.form["name"]
        variety.description = request.form["description"]
        db.session.commit()
        flash("Variedad actualizada con éxito", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {str(e)}", "danger")

    return redirect(url_for("variety.list_varieties"))

# ----------------------
# ELIMINAR VARIEDAD
# ----------------------
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
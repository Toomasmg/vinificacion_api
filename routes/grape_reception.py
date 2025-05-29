from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
from database import db
from models.grape_reception import GrapeReception
from datetime import datetime

# Crear el Blueprint para la recepción de uvas
grape_reception_bp = Blueprint("grape_reception", __name__, url_prefix="/receptions")

# ----------------------
# MOSTRAR TODAS
# ----------------------
@grape_reception_bp.route("/", methods=["GET"])
def list_receptions():
    receptions = GrapeReception.query.all()
    return render_template("grape_reception/receptions.html", receptions=receptions)

# ----------------------
# FORMULARIO DE CARGA
# ----------------------
@grape_reception_bp.route("/add", methods=["GET"])
def show_add_form():
    varieties = Variety.query.all()
    return render_template("grape_reception/add_reception.html",varieties=varieties)

# ----------------------
# GUARDAR NUEVA RECEPCIÓN
# ----------------------
@grape_reception_bp.route("/add", methods=["POST"])
def add_reception():
    try:
        # Tomar los datos del formulario
        name = request.form["name"]
        grape_type = request.form["grape_type"]
        quantity = int(request.form["quantity"])
        weight = float(request.form["weight"])
        reception_date = datetime.strptime(request.form["reception_date"], "%Y-%m-%d").date()
        variety_id = request.form["variety_id"]


        # Crear objeto
        new_reception = GrapeReception(
            name=name,
            grape_type=grape_type,
            quantity=quantity,
            weight=weight,
            reception_date=reception_date
            variety_id=variety_id
        )

        db.session.add(new_reception)
        db.session.commit()

        flash("Recepción agregada con éxito", "success")
        return redirect(url_for("grape_reception.list_receptions"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar recepción: {str(e)}", "danger")
        return redirect(url_for("grape_reception.show_add_form"))

# ----------------------
# FORMULARIO DE EDICIÓN
# ----------------------
@grape_reception_bp.route("/edit/<string:reception_id>", methods=["GET"])
def edit_reception_form(reception_id):
    reception = GrapeReception.query.get(reception_id)
    if reception is None:
        abort(404)
    return render_template("grape_reception/edit_reception.html", reception=reception)

# ----------------------
# ACTUALIZAR RECEPCIÓN
# ----------------------
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

# ----------------------
# ELIMINAR RECEPCIÓN
# ----------------------
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

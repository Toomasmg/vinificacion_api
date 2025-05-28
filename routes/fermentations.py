from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.fermentation import Fermentation
from models.database import db
from datetime import datetime

fermentations_bp = Blueprint("fermentations", __name__)

# Listar todas las fermentaciones
@fermentations_bp.route("/fermentations")
def list_fermentations():
    fermentations = Fermentation.query.all()
    return render_template("fermentations/list.html", fermentations=fermentations)

# Mostrar formulario para crear nueva fermentación
@fermentations_bp.route("/fermentations/new")
def new_fermentation():
    return render_template("fermentations/new.html")

# Crear nueva fermentación con datos del formulario
@fermentations_bp.route("/fermentations/create", methods=["POST"])
def create_fermentation():
    try:
        fermentation = Fermentation(
            start_date=datetime.strptime(request.form["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(request.form["end_date"], "%Y-%m-%d").date() if request.form["end_date"] else None,
            temperature=float(request.form["temperature"]),
            acidity=float(request.form["acidity"]),
            ph=float(request.form["ph"]),
            notes=request.form["notes"]
        )
        db.session.add(fermentation)
        db.session.commit()
        flash("Fermentación registrada con éxito", "success")
        return redirect(url_for("fermentations.list_fermentations"))
    except Exception as e:
        flash(f"Error al registrar fermentación: {e}", "danger")
        return redirect(url_for("fermentations.new_fermentation"))

# Mostrar formulario para editar fermentación existente
@fermentations_bp.route("/fermentations/edit/<string:id>")
def edit_fermentation(id):
    fermentation = Fermentation.query.get(id)
    if not fermentation:
        flash("Fermentación no encontrada", "warning")
        return redirect(url_for("fermentations.list_fermentations"))
    return render_template("fermentations/edit.html", fermentation=fermentation)

# Actualizar fermentación con datos del formulario de edición
@fermentations_bp.route("/fermentations/update/<string:id>", methods=["POST"])
def update_fermentation(id):
    fermentation = Fermentation.query.get(id)
    if not fermentation:
        flash("Fermentación no encontrada", "warning")
        return redirect(url_for("fermentations.list_fermentations"))
    try:
        fermentation.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        fermentation.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date() if request.form["end_date"] else None
        fermentation.temperature = float(request.form["temperature"])
        fermentation.acidity = float(request.form["acidity"])
        fermentation.ph = float(request.form["ph"])
        fermentation.notes = request.form["notes"]

        db.session.commit()
        flash("Fermentación actualizada", "success")
    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")
    return redirect(url_for("fermentations.list_fermentations"))

# Eliminar fermentación por id
@fermentations_bp.route("/fermentations/delete/<string:id>")
def delete_fermentation(id):
    fermentation = Fermentation.query.get(id)
    if fermentation:
        db.session.delete(fermentation)
        db.session.commit()
        flash("Fermentación eliminada", "success")
    else:
        flash("Fermentación no encontrada", "warning")
    return redirect(url_for("fermentations.list_fermentations"))

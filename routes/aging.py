from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Aging import Aging
from models.variety import Variety
from models.db import db

aging_bp = Blueprint('aging_bp', __name__)

@aging_bp.route('/aging', methods=['GET'])
def view_agings():
    agings = Aging.query.all()
    grape_varieties = Variety.query.all()
    return render_template('aging/aging.html', agings=agings, grape_varieties=grape_varieties)

@aging_bp.route('/aging', methods=['POST'])
def create_aging():
    aging = Aging(
        grape_variety_id=request.form['grape_variety_id'],
        barrel_type=request.form['barrel_type'],
        start_date=request.form['start_date'],
        end_date=request.form.get('end_date')
    )
    db.session.add(aging)
    db.session.commit()
    flash('Crianza agregada correctamente', 'success')
    return redirect(url_for('aging_bp.view_agings'))

@aging_bp.route('/aging/editar/<string:id>', methods=['GET'])
def edit_aging(id):
    aging = Aging.query.get_or_404(id)
    grape_varieties = Variety.query.all()
    return render_template('aging/edit_aging.html', aging=aging, grape_varieties=grape_varieties)

@aging_bp.route('/aging/editar/<string:id>', methods=['POST'])
def update_aging(id):
    aging = Aging.query.get_or_404(id)
    aging.grape_variety_id = request.form['grape_variety_id']
    aging.barrel_type = request.form['barrel_type']
    aging.start_date = request.form['start_date']
    aging.end_date = request.form['end_date']
    db.session.commit()
    flash('Crianza actualizada correctamente', 'success')
    return redirect(url_for('aging_bp.view_agings'))

@aging_bp.route('/aging/eliminar/<string:id>', methods=['POST'])
def delete_aging(id):
    aging = Aging.query.get_or_404(id)
    db.session.delete(aging)
    db.session.commit()
    flash('Crianza eliminada', 'warning')
    return redirect(url_for('aging_bp.view_agings'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.storage import Storage
from models.db import db

storage_bp = Blueprint('storage_bp', __name__)

@storage_bp.route('/storage', methods=['GET'])
def view_storages():
    storages = Storage.query.all()
    return render_template('storage/storage.html', storages=storages)

@storage_bp.route('/storage', methods=['POST'])
def create_storage():
    storage = Storage(
        wine_name=request.form['wine_name'],
        grape_variety_id=request.form['grape_variety_id'],
        container_type=request.form['container_type'],
        quantity_liters=request.form['quantity_liters'],
        location=request.form.get('location')
    )
    db.session.add(storage)
    db.session.commit()
    flash('Almacenamiento creado correctamente', 'success')
    return redirect(url_for('storage_bp.view_storages'))

@storage_bp.route('/storage/editar/<string:id>', methods=['GET'])
def edit_storage(id):
    storage = Storage.query.get_or_404(id)
    return render_template('storage/edit_storage.html', storage=storage)

@storage_bp.route('/storage/editar/<string:id>', methods=['POST'])
def update_storage(id):
    storage = Storage.query.get_or_404(id)
    storage.wine_name = request.form['wine_name']
    storage.grape_variety_id = request.form['grape_variety_id']
    storage.container_type = request.form['container_type']
    storage.quantity_liters = request.form['quantity_liters']
    storage.location = request.form['location']
    db.session.commit()
    flash('Almacenamiento actualizado correctamente', 'success')
    return redirect(url_for('storage_bp.view_storages'))

@storage_bp.route('/storage/eliminar/<string:id>', methods=['POST'])
def delete_storage(id):
    storage = Storage.query.get_or_404(id)
    db.session.delete(storage)
    db.session.commit()
    flash('Almacenamiento eliminado', 'warning')
    return redirect(url_for('storage_bp.view_storages'))

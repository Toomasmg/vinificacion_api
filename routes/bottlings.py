from models.db import db
from models.bottling import Bottling
from flask import Blueprint,request,flash,url_for,render_template,redirect
from datetime import datetime
import uuid

bottling_bp = Blueprint("bottling_bp",__name__)

@bottling_bp.route("/")

def get_bottling():
    bottling_list = Bottling.query.all()#obtenemos todos los embotellamientos
    return render_template("bottling/bottlings.html",bottling=bottling_list)

@bottling_bp.route("/bottling", methods=["POST"])
def add_bottling():
    date_bottling = request.form["date_bottling"] #recibimos lo que ingresa en formato form(formulario del html)
    total_volume= request.form["total_volume"]
    bottle_quantity = request.form["bottle_quantity"]
    lot_number = request.form["lot_number"]
    observation = request.form.get("observation","")

    bottle_type = request.form.get("bottle_type")
    capacity_ml = request.form["capacity_ml"]

    aging_id = request.form["aging_id"]
    if aging_id.strip() == "":
        aging_id = None
    
    if Bottling.query.filter_by(lot_number=lot_number).first():
        flash("El numero del lote ya se encuentra registrado","warning")
        return redirect(request.referrer)
    #------calcular podsibles errores de datos
    user_volume = float(total_volume)
    # Capacidad de botella en litros
    bottle_capacity_liter = float(capacity_ml) / 1000  

    estimated_volume = int(bottle_quantity) * bottle_capacity_liter  #Estimamos el volumen total a partir de cantidad de botellas

    # Comparamos
    difference = abs(user_volume - estimated_volume)
    #botellas requeridas
    required_bottles = round(user_volume / bottle_capacity_liter)
    if difference > 5:#botellas o litros perdidos
        flash(f"El volumen total difiere mucho del calculado. Revisá los datos. "
        f"Con {user_volume} L y botellas de {capacity_ml} ml, deberías tener unas {required_bottles} botellas aprox.",
        "warning")
        return redirect(request.referrer)
    if difference > 1:#perdida leve
        flash("Tienes una perdida leve","info")
    try:
        if date_bottling:
            date_bottling = datetime.strptime(date_bottling,"%Y-%m-%d").date()
        else: 
            date_bottling = datetime.today().date()#si no ingreso la fecha que se añada la de hoy
        
        new_bottling=Bottling(
            id = str(uuid.uuid4()),
            date_bottling = date_bottling,
            total_volume = total_volume,
            bottle_type= bottle_type,
            capacity_ml = capacity_ml,
            bottle_quantity = bottle_quantity,
            lot_number = lot_number,
            observation = observation,
            aging_id = aging_id,

        )
        db.session.add(new_bottling)
        db.session.commit()
        flash("Embotellado creado correctamente","success")
        return redirect(url_for("bottling_bp.get_bottling"))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear embotellado:{e}","error")
    return redirect(url_for("bottling_bp.get_bottling"))


@bottling_bp.route("/bottling/edit/<string:id>",methods =["GET","POST"])
def edit_bottling(id):
    bottling = Bottling.query.get_or_404(id)
    if request.method == "POST":#verificamos si existe los atributos
        date_bottling = request.form.get("date_bottling" )
        total_volume= request.form.get("total_volume")
        bottle_quantity = request.form.get("bottle_quantity")
        lot_number = request.form.get("lot_number")
        observation= request.form.get("observation","")
        bottle_type = request.form.get("bottle_type")
        capacity_ml = request.form.get("capacity_ml")
        aging_id = request.form.get("aging_id")

        user_volume = float(total_volume)
        # Capacidad de botella en litros
        bottle_capacity_liter = float(capacity_ml) / 1000  

        estimated_volume = int(bottle_quantity) * bottle_capacity_liter  #Estimamos el volumen total a partir de cantidad de botellas

        # Comparamos
        difference = abs(user_volume - estimated_volume)
        #botellas requeridas
        required_bottles = round(user_volume / bottle_capacity_liter)
        if difference > 5:#botellas o litros perdidos
            flash(f" El volumen total difiere mucho del calculado. Revisá los datos. "
            f"Con {user_volume} L y botellas de {capacity_ml} ml, deberías tener unas {required_bottles} botellas aprox.",
            "warning")
            return redirect(request.referrer)
        if difference > 1:#perdida leve
            flash("Tienes una perdida leve","info")
        try:
            if date_bottling:
                date_bottling = datetime.strptime(date_bottling,"%Y-%m-%d").date()#transformamos la fecha en fromato date
            else: 
                date_bottling = datetime.today().date()#si no ingreso la fecha que se añada la de hoy
            bottling.aging_id = aging_id
            bottling.date_bottling = date_bottling
            bottling.total_volume = total_volume
            bottling.bottle_quantity = bottle_quantity
            bottling.lot_number = lot_number
            bottling.observation = observation
            bottling.bottle_type= bottle_type
            bottling.capacity_ml =  capacity_ml
            bottling.aging_id = aging_id
            db.session.commit()
            flash("Botellado actualizado correctamente","success")
            return redirect(url_for("bottling_bp.get_bottling"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear embotellado:{e}","error")
            return redirect(url_for("bottling_bp.edit_bottling",id=id))
    return render_template("bottling/edit_bottling.html",bottling=bottling)

@bottling_bp.route("/bottling/delete/<string:id>", methods=["POST"])
def delete_bottling(id):
    bottling=Bottling.query.get_or_404(id)

    try:
        db.session.delete(bottling)
        db.session.commit()
        flash("embotellado eliminado","success")
    
    except Exception as e:
        db.session.rollback()
        flash(f"error al elminar embotellado:{e}","error")
    return redirect(url_for("bottling_bp.get_bottling"))

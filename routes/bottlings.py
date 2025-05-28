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
    bottling_code = request.form["bottling_code"]
    date_bottling = request.form["date_bottling"]
    aging_id = request.form["aging_id"]

    if aging_id.strip() == "":
        aging_id = None

    if not aging_id or not bottling_code:
        flash("EL ID de crianza y el codigo son obligatorios","error")
    try:
        if date_bottling:
            date_bottling = datetime.strptime(date_bottling,"%Y-%m-%d").date()
        else: 
            date_bottling = datetime.today().date()#si no ingreso la fecha que se añada la de hoy
        
        new_bottling=Bottling(
            id = str(uuid.uuid4()),
            aging_id = aging_id,
            date_bottling = date_bottling,
            bottling_code = bottling_code
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
    if request.method == "POST":
        aging_id = request.form.get("aging_id")#verificamos si existe los atributos
        date_bottling = request.form.get("date_bottling" )
        bottling_code = request.form.get("bottling_code")

        if not aging_id or not bottling_code:
            flash("EL ID de crianza y el codigo son obligatorios","error")
            return redirect(request.referrer)#volvemos para atras 
        
        try:
            if date_bottling:
                date_bottling = datetime.strptime(date_bottling,"%Y-%m-%d").date()#transformamos la fecha en fromato date
            else: 
                date_bottling = datetime.today().date()#si no ingreso la fecha que se añada la de hoy
            bottling.aging_id = aging_id
            bottling.date_bottling = date_bottling
            bottling.bottling_code = bottling_code
            db.session.commit()
            flash("Botellado actualizado correctamente","success")
            return redirect(url_for("bottling_bp.bottlings"))
        
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

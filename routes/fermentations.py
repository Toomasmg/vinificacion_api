from flask import Blueprint, render_template, request, redirect, url_for,flash
from models.database import db
from models.fermentation import Fermentation
from datetime import datetime

fermentation_bp = Blueprint("fermentation", __name__, url_prefix="/fermentation")

@fermentation_bp.route
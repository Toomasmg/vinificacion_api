from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy
db = SQLAlchemy()

# Función para inicializar SQLAlchemy con la app Flask
def init_app(app):
    db.init_app(app)

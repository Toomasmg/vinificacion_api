import os
from dotenv import load_dotenv


# Cargar las variables del archivo .env
load_dotenv()

class Config:
    # URI de conexión a MySQL usando variables del entorno
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    
    # Desactiva seguimiento de modificaciones (mejora rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #clave secreta    
    SECRET_KEY = os.getenv("SECRET_KEY")

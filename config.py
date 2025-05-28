import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DB")
port = os.getenv("MYSQL_PORT")
DATABASE_CONECTION_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
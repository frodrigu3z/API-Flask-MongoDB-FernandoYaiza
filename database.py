from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from gorra import Gorra, Base

load_dotenv()
usuario = os.environ.get("MYSQLDB_USUARIO")
password = os.environ.get("MYSQLDB_PASSWORD")
host = os.environ.get("MYSQLDB_HOST")
bd = os.environ.get("MYSQLDB_BD")

DATABASE_URL = f'mysql+pymysql://{usuario}:{password}@{host}/{bd}'

# Creamos el motor de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Obtener una sesión de la base de datos
def obtener_bd():
    bd = SessionLocal()
    try:
        yield bd
    finally:
        bd.close()

# Leer todas las gorras de la base de datos
def leer_gorras(bd: Session = Depends(obtener_bd)):
    gorras = bd.query(Gorra).all()
    return gorras
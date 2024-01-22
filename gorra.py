from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy.orm import declarative_base

# Creamos la base para el modelo
Base = declarative_base()

# Definimos el modelo Gorra
class Gorra(Base):
    __tablename__ = "gorras"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    stock = Column(Integer)
    fecha_lanzamiento = Column(Date)
    nombre_imagen = Column(String)
    imagen = Column(LargeBinary)
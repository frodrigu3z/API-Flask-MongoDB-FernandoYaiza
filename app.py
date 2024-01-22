from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from database import obtener_bd
from gorra import Gorra
from database import Gorra
from pydantic import BaseModel
import base64

app = FastAPI()

# Modelo para validar los datos de entrada de la API
class GorraModelo(BaseModel):
    descripcion: str
    stock: int
    fecha_lanzamiento: str
    nombre_imagen: str

# Convertir una instancia de Gorra en un diccionario
def gorra_a_diccionario(gorra):
    if gorra.imagen is not None:
        gorra.imagen = base64.b64encode(gorra.imagen).decode('ascii')
    return {c.name: getattr(gorra, c.name) for c in gorra.__table__.columns}

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola, Bienvenido!"}

# Ruta para obtener todas las gorras
@app.get("/gorras")
def leer_gorras(db: Session = Depends(obtener_bd)):
    gorras = db.query(Gorra).all()
    return {"gorras": [gorra_a_diccionario(gorra) for gorra in gorras]}

# Ruta para crear una nueva gorra
@app.post("/gorra")
def crear_gorra(gorra: GorraModelo, db: Session = Depends(obtener_bd)):
    nueva_gorra = Gorra(**gorra.dict())
    db.add(nueva_gorra)
    db.commit()
    return {"gorra": gorra_a_diccionario(nueva_gorra)}

# Ruta para obtener una gorra por su id
@app.get("/gorra/{id}")
def leer_gorra(id: int, db: Session = Depends(obtener_bd)):
    gorra = db.query(Gorra).filter(Gorra.id == id).first()
    if gorra is None:
        raise HTTPException(status_code=404, detail="Gorra no encontrada")
    return {"gorra": gorra_a_diccionario(gorra)}

# Ruta para eliminar una gorra por su id
@app.delete("/gorra/{id}")
def eliminar_gorra(id: int, db: Session = Depends(obtener_bd)):
    gorra = db.query(Gorra).filter(Gorra.id == id).first()
    if gorra is None:
        raise HTTPException(status_code=404, detail="Gorra no encontrada")
    db.delete(gorra)
    db.commit()
    return {"mensaje": "Gorra eliminada"}

# Ruta para actualizar una gorra por su id
@app.put("/gorra/{id}")
def actualizar_gorra(id: int, gorra: GorraModelo, imagen: UploadFile = File(None), db: Session = Depends(obtener_bd)):
    gorra_existente = db.query(Gorra).filter(Gorra.id == id).first()
    if gorra_existente is None:
        raise HTTPException(status_code=404, detail="Gorra no encontrada")
    for clave, valor in gorra.dict().items():
        if valor is not None:
            setattr(gorra_existente, clave, valor)
    if imagen:
        gorra_existente.imagen = imagen.file.read()
    db.commit()
    return {"gorra": gorra_a_diccionario(gorra_existente)}83414e9e43fc48cd318289eef3

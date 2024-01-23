from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuramos la URI de MongoDB
app.config["MONGO_URI"] = 'mongodb+srv://fernandoyaiza:pr4cticafl4sk@cluster0.nwmz277.mongodb.net/fernandoyaizabd'

mongo = PyMongo(app)

# Ruta para el inicio '/'
@app.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "Hola, Bienvenido! -  API REST MONGODB"})

# Definimos la ruta para obtener todas las gorras
@app.route('/gorras', methods=['GET'])
def get_gorras():
    gorras = mongo.db.gorras.find()
    response = json_util.dumps(gorras)
    return Response(response, mimetype='application/json')

# Definimos la ruta para obtener una gorra por su ID
@app.route('/gorras/<id>', methods=['GET'])
def get_gorra(id):
    gorra = mongo.db.gorras.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(gorra)
    return Response(response, mimetype='application/json')

# Definimos la ruta para crear una nueva gorra
@app.route('/gorras', methods=['POST'])
def create_gorra():
    request_data = request.get_json()
    descripcion = request_data.get('descripcion')
    stock = request_data.get('stock')
    fecha_lanzamiento = request_data.get('fecha_lanzamiento')
    nombre_imagen = request_data.get('nombre_imagen')
    imagen = request_data.get('imagen')
    # Insertamos la nueva gorra en la base de datos
    id = mongo.db.gorras.insert_one({'descripcion': descripcion, 'stock': stock, 'fecha_lanzamiento': fecha_lanzamiento, 'nombre_imagen': nombre_imagen, 'imagen': imagen})
    response = {
        'id': str(id.inserted_id),
        'descripcion': descripcion,
        'stock': stock,
        'fecha_lanzamiento': fecha_lanzamiento,
        'nombre_imagen': nombre_imagen,
        'imagen': imagen
    }
    return response

# Definimos la ruta para eliminar una gorra por su ID
@app.route('/gorras/<id>', methods=['DELETE'])
def delete_gorra(id):
    gorra = mongo.db.gorras.find_one({'_id': ObjectId(id)})
    if gorra:
        mongo.db.gorras.delete_one({'_id': ObjectId(id)})
        response = jsonify({'mensaje': 'Gorra ' + id + ' fue eliminada satisfactoriamente'})
        return response
    else:
        return not_found()

# Definimos la ruta para actualizar una gorra por su ID
@app.route('/gorras/<id>', methods=['PUT'])
def update_gorra(id):
    request_data = request.get_json()
    descripcion = request_data.get('descripcion')
    stock = request_data.get('stock')
    fecha_lanzamiento = request_data.get('fecha_lanzamiento')
    nombre_imagen = request_data.get('nombre_imagen')
    imagen = request_data.get('imagen')
    gorra = mongo.db.gorras.find_one({'_id': ObjectId(id)})
    if gorra:
        # Actualizamos la gorra en la base de datos
        mongo.db.gorras.update_one({'_id': ObjectId(id)}, {'$set':
        {
            'descripcion': descripcion,
            'stock': stock,
            'fecha_lanzamiento': fecha_lanzamiento,
            'nombre_imagen': nombre_imagen,
            'imagen': imagen
        }})
        response = jsonify({'mensaje': 'Gorra ' + id + ' fue actualizada satisfactoriamente'})
        return response
    else:
        return not_found()

# Definimos el manejador de errores para el error 404
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'mensaje': 'Recurso no encontrado: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)

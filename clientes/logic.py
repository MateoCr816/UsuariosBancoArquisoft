from clientes.models import Cliente
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime

def getClientes():
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    usuarios_collection = db['clientes']
    usuarios_collection = usuarios_collection.find({})
    usuarios = [ Cliente.from_mongo(usuario) for usuario in usuarios_collection ]
    client.close()

    return usuarios

def getUsuario(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    usuarios_collection = db['usuarios']
    usuario = usuarios_collection.find_one({'_id': ObjectId(id)})
    client.close()

    if usuario is None:
        raise ValueError('Usuario not found')

    return Usuario.from_mongo(usuario)

def verifyUsuarioData(data):
    if 'name' not in data:
        raise ValueError('name is required')
    
    usuario = Usuario()
    usuario.name = data['name']
    usuario.min_threshold = data['min_threshold'] if 'min_threshold' in data else None
    usuario.max_threshold = data['max_threshold'] if 'max_threshold' in data else None

    return usuario

def createUsuario(data):

    # Verify usuario data
    usuario = verifyUsuarioData(data)

    # Create usuario in MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    usuarios_collection = db['usuarios']
    usuario.id = usuarios_collection.insert(
        {
            'name': usuario.name,
            'min_threshold': usuario.min_threshold,
            'max_threshold': usuario.max_threshold
        }
    )
    client.close()
    return usuario

def deletePlace(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    result = places_collection.remove({'_id': ObjectId(id)})
    client.close()
    return result

def updateUsuario(id, data):

    # Verify usuario data
    usuario = verifyUsuarioData(data)

    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    usuarios_collection = db['usuarios']
    result = usuarios_collection.update(
        {'_id': ObjectId(id)},
        {'$set': {
            'name': usuario.name,
            'min_threshold': usuario.min_threshold,
            'max_threshold': usuario.max_threshold
            }
        }
    )
    client.close()
    return result
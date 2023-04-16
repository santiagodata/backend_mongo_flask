import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json

T = TypeVar('T')


class InterfaceRepositorio(Generic[T]):
    def __init__(self):
        # Inicializar la conexión a la base de datos utilizando la librería pymongo y el archivo de certificados certifi
        ca = certifi.where()
        # Cargar la configuración de la base de datos desde un archivo JSON
        dataConfig = self.loadFileConfig()
        # Crear un cliente de MongoDB con la cadena de conexión y los certificados cargados
        client = pymongo.MongoClient(dataConfig["data-db-connection"], tlsCAFile=ca)
        # Obtener el nombre de la base de datos a partir de la configuración
        self.baseDatos = client[dataConfig["name-db"]]
        # Obtener el nombre de la colección a partir del nombre de la clase genérica utilizada
        theClass = get_args(self.__orig_bases__[0])
        self.coleccion = theClass[0].__name__.lower()

    def loadFileConfig(self):
        # Cargar la configuración de la base de datos desde un archivo JSON
        with open('config.json') as f:
            data = json.load(f)
        return data

    def save(self, item: T):
        # Obtener la colección en la que se almacenarán los datos
        laColeccion = self.baseDatos[self.coleccion]
        elId = ""
        # Transformar las referencias a objetos DBRef antes de almacenar el ítem
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            # Si el ítem ya tiene un _id, se actualiza en la base de datos
            elId = item._id
            _id = ObjectId(elId)
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = laColeccion.update_one({"_id": _id}, updateItem)
        else:
            # Si el ítem no tiene un _id, se inserta en la base de datos
            _id = laColeccion.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()

        x = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(elId)

    def delete(self, id):
        # Eliminar un ítem de la base de datos por su _id
        laColeccion = self.baseDatos[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

    def update(self, id, item: T):
        # Actualizar un ítem en la base de datos por su _id
        _id = ObjectId(id)
        laColeccion = self.baseDatos[self.coleccion]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    def findById(self, id):
        laColeccion = self.baseDatos[self.coleccion]  # Acceso a la colección en la base de datos
        x = laColeccion.find_one({"_id": ObjectId(id)})  # Búsqueda de un documento por su id
        x = self.getValuesDBRef(x)  # Obtención de los valores de las referencias a otras colecciones
        if x == None:  # Si no se encuentra el documento, se retorna un diccionario vacío
            x = {}
        else:
            x["_id"] = x["_id"].__str__()  # Conversión del id del documento a string
        return x

    def findAll(self):
        laColeccion = self.baseDatos[self.coleccion]  # Acceso a la colección en la base de datos
        data = []
        for x in laColeccion.find():  # Iteración a través de todos los documentos en la colección
            x["_id"] = x["_id"].__str__()  # Conversión del id del documento a string
            x = self.transformObjectIds(x)  # Transformación de los ObjectIds en los documentos
            x = self.getValuesDBRef(x)  # Obtención de los valores de las referencias a otras colecciones
            data.append(x)  # Agregación del documento a la lista de datos
        return data

    def query(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]  # Acceso a la colección en la base de datos
        data = []
        for x in laColeccion.find(theQuery):  # Iteración a través de los documentos que coinciden con la consulta
            x["_id"] = x["_id"].__str__()  # Conversión del id del documento a string
            x = self.transformObjectIds(x)  # Transformación de los ObjectIds en los documentos
            x = self.getValuesDBRef(x)  # Obtención de los valores de las referencias a otras colecciones
            data.append(x)  # Agregación del documento a la lista de datos
        return data

    def queryAggregation(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]  # Acceso a la colección en la base de datos
        data = []
        for x in laColeccion.aggregate(
                theQuery):  # Iteración a través de los documentos que coinciden con la consulta de agregación
            x["_id"] = x["_id"].__str__()  # Conversión del id del documento a string
            x = self.transformObjectIds(x)  # Transformación de los ObjectIds en los documentos
            x = self.getValuesDBRef(x)  # Obtención de los valores de las referencias a otras colecciones
            data.append(x)  # Agregación del documento a la lista de datos
        return data

    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):  # Verifica si el valor es una referencia a otra colección en la base de datos
                laColeccion = self.baseDatos[x[k].collection]  # Obtiene la colección referenciada
                valor = laColeccion.find_one(
                    {"_id": ObjectId(x[k].id)})  # Obtiene el documento referenciado usando el ID
                valor["_id"] = valor[
                    "_id"].__str__()  # Convierte el ID del documento referenciado a una cadena de texto
                x[k] = valor  # Reemplaza el valor de la referencia con el documento referenciado
                x[k] = self.getValuesDBRef(x[k])  # Llama recursivamente a la función para manejar referencias anidadas
            elif isinstance(x[k], list) and len(x[k]) > 0:  # Verifica si el valor es una lista no vacía
                x[k] = self.getValuesDBRefFromList(x[k])  # Llama a otra función para manejar referencias en una lista
            elif isinstance(x[k], dict):  # Verifica si el valor es un diccionario
                x[k] = self.getValuesDBRef(
                    x[k])  # Llama recursivamente a la función para manejar referencias anidadas en el diccionario
        return x

    def getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.baseDatos[
            theList[0]._id.collection]  # Obtiene la colección referenciada usando la primera referencia en la lista
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(
                item.id)})  # Obtiene el documento referenciado usando el ID de cada referencia en la lista
            value["_id"] = value["_id"].__str__()  # Convierte el ID del documento referenciado a una cadena de texto
            newList.append(value)  # Agrega el documento referenciado a la nueva lista
        return newList

    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):  # Verifica si el valor es un ObjectId
                x[attribute] = x[attribute].__str__()  # Convierte el ObjectId a una cadena de texto
            elif isinstance(x[attribute], list):  # Verifica si el valor es una lista
                x[attribute] = self.formatList(x[attribute])  # Llama a otra función para formatear la lista
            elif isinstance(x[attribute], dict):  # Verifica si el valor es un diccionario
                x[attribute] = self.transformObjectIds(
                    x[attribute])  # Llama recursivamente a la función para manejar anidamientos en el diccionario
        return x

    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId): # Verifica si el elemento en la lista es un ObjectId
                newList.append(item.__str__()) # Convierte el ObjectId a una cadena de texto y lo agrega a la nueva lista
        if len(newList) == 0: # Verifica si no se encontraron ObjectId en la lista original
            newList = x # Si no se encontraron ObjectId, se mantiene la lista original sin cambios
        return newList

    def transformRefs(self, item):
        theDict = item.__dict__ # Obtiene el diccionario de atributos del objeto
        keys = list(theDict.keys()) # Obtiene la lista de claves (nombres de atributos) del diccionario
        for k in keys:
            if theDict[k].__str__().count("object") == 1: # Verifica si el valor del atributo es una referencia a otro objeto
                newObject = self.ObjectToDBRef(getattr(item, k)) # Llama a otra función para convertir el objeto referenciado a un DBRef
                setattr(item, k, newObject) # Actualiza el valor del atributo con el DBRef creado
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower() # Obtiene el nombre de la colección a partir del nombre de la clase del objeto
        return DBRef(nameCollection, ObjectId(item._id)) # Crea y devuelve un DBRef usando el nombre de la colección y el ObjectId del objeto


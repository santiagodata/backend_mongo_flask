from repositories.interfaceRepositorio import InterfaceRepositorio
from models.inscripcion import Inscripcion

from bson import ObjectId

class RepositorioInscripcion(InterfaceRepositorio[Inscripcion]):
    def getListadoInscritosEnMateria(self, id_materia):
        # Método para obtener la lista de inscripciones en una materia específica

        # Se define la condición de búsqueda en forma de un diccionario con una estructura de consulta de BSON
        theQuery = {"materia.$id": ObjectId(id_materia)}

        # Se ejecuta la consulta utilizando el método query
        return self.query(theQuery)

    def getMayorNotaPorCurso(self):
        # Método para obtener la inscripción con la mayor nota final en cada materia

        # Se define la consulta de agregación en forma de un diccionario con la función de agregación $group
        query1 = {
            "$group": {
                "_id": "$materia",
                "max": {
                    "$max": "$nota_final"
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }

        # Se crea una lista de consultas de agregación en el orden deseado
        pipeline = [query1]

        # Se ejecuta la consulta de agregación utilizando el método queryAggregation
        return self.queryAggregation(pipeline)

    def promedioNotasEnMateria(self, id_materia):
        # Método para calcular el promedio de las notas finales de las inscripciones en una materia específica

        # Se define la consulta de agregación en forma de una lista de consultas con las funciones de agregación $match y $group
        query1 = {
            "$match": {"materia.$id": ObjectId(id_materia)}
        }
        query2 = {
            "$group": {
                "_id": "$materia",
                "promedio": {
                    "$avg": "$nota_final"
                }
            }
        }

        # Se crea una lista de consultas de agregación en el orden deseado
        pipeline = [query1, query2]

        # Se ejecuta la consulta de agregación utilizando el método queryAggregation
        return self.queryAggregation(pipeline)

    def test(self, id_materia):
        # Método para realizar pruebas o ejemplos de uso del repositorio

        # Se define la consulta de agregación en forma de una lista de consultas con la función de agregación $match
        query1 = {
            "$match": {"materia.$id": ObjectId(id_materia)}
        }

        # Se crea una lista de consultas de agregación en el orden deseado
        pipeline = [query1]

        # Se ejecuta la consulta de agregación utilizando el método queryAggregation
        return self.queryAggregation(pipeline)

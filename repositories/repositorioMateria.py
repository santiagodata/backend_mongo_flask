from bson import ObjectId # Importa la clase ObjectId del módulo bson
from repositories.interfaceRepositorio import InterfaceRepositorio # Importa la interfaz del repositorio
from models.Materia import Materia # Importa el modelo Materia

class RepositorioMateria(InterfaceRepositorio[Materia]): # Define una clase RepositorioMateria que implementa la interfaz InterfaceRepositorio para el modelo Materia
    def getListadoMateriasEnDepartamento(self, id_materia):
        # Define una función getListadoMateriasEnDepartamento que recibe el parámetro id_materia
        theQuery = {"departamento.$id": ObjectId(id_materia)} # Crea una consulta para buscar materias en un departamento específico utilizando el id_materia recibido como parámetro y la clase ObjectId del módulo bson
        return self.query(theQuery) # Realiza la consulta llamando al método query de la clase padre InterfaceRepositorio con la consulta theQuery y retorna los resultados


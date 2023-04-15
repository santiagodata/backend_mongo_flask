from bson import ObjectId
from repositories.interfaceRepositorio import InterfaceRepositorio
from models.Materia import Materia


class RepositorioMateria(InterfaceRepositorio[Materia]):
    def getListadoMateriasEnDepartamento(self, id_materia):
        theQuery = {"departamento.$id": ObjectId(id_materia)}
        return self.query(theQuery)

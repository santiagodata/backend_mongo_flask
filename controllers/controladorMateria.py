from repositories.repositorioMateria import RepositorioMateria
from repositories.repositorioDepartamento import RepositorioDepartamento
from models.Materia import Materia
from models.Departamento import Departamento

class ControladorMateria():
    def __init__(self):
        self.repositorioMateria = RepositorioMateria()
        self.repositorioDepartamento = RepositorioDepartamento()

    def index(self):
        """
        Obtiene todas las materias.
        """
        return self.repositorioMateria.findAll()

    def create(self, infoMateria):
        """
        Crea una nueva materia con la información proporcionada.
        """
        nuevoMateria = Materia(infoMateria)
        return self.repositorioMateria.save(nuevoMateria)

    def show(self, id):
        """
        Obtiene los detalles de una materia por su ID.
        """
        elMateria = Materia(self.repositorioMateria.findById(id))
        return elMateria.__dict__

    def update(self, id, infoMateria):
        """
        Actualiza los detalles de una materia con la información proporcionada.
        """
        materiaActual = Materia(self.repositorioMateria.findById(id))
        materiaActual.nombre = infoMateria["nombre"]
        materiaActual.creditos = infoMateria["creditos"]
        return self.repositorioMateria.save(materiaActual)

    def delete(self, id):
        """
        Elimina una materia por su ID.
        """
        return self.repositorioMateria.delete(id)

    def asignarDepartamento(self, id, id_departamento):
        """
        Asigna un departamento a una materia por su ID.
        """
        materiaActual = Materia(self.repositorioMateria.findById(id))
        departamentoActual = Departamento(self.repositorioDepartamento.findById(id_departamento))
        materiaActual.departamento = departamentoActual
        return self.repositorioMateria.save(materiaActual)

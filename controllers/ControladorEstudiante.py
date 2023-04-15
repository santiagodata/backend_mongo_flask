from repositories.repositorioEstudiante import RepositorioEstudiante
from models.Estudiante import Estudiante


class ControladorEstudiante():
    def __init__(self):
        self.repositorioEstudiante = RepositorioEstudiante()

    def index(self):
        return self.repositorioEstudiante.findAll()

    def create(self, infoEstudiante):
        nuevoEstudiante = Estudiante(infoEstudiante)
        return self.repositorioEstudiante.save(nuevoEstudiante)

    def show(self, id):
        elEstudiante = Estudiante(self.repositorioEstudiante.findById(id))
        return elEstudiante.__dict__

    def update(self, id, infoEstudiante):
        estudianteActual = Estudiante(self.repositorioEstudiante.findById(id))
        estudianteActual.cedula = infoEstudiante["cedula"]
        estudianteActual.nombre = infoEstudiante["nombre"]
        estudianteActual.apellido = infoEstudiante["apellido"]
        return self.repositorioEstudiante.save(estudianteActual)

    def delete(self, id):
        return self.repositorioEstudiante.delete(id)

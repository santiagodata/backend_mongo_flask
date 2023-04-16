from repositories.repositorioEstudiante import RepositorioEstudiante
from models.Estudiante import Estudiante

class ControladorEstudiante():
    def __init__(self):
        self.repositorioEstudiante = RepositorioEstudiante()

    def index(self):
        # Obtener todos los estudiantes del repositorio
        return self.repositorioEstudiante.findAll()

    def create(self, infoEstudiante):
        # Crear una nueva instancia de Estudiante con la información proporcionada
        nuevoEstudiante = Estudiante(infoEstudiante)
        # Guardar el nuevo estudiante en el repositorio
        return self.repositorioEstudiante.save(nuevoEstudiante)

    def show(self, id):
        # Obtener la información del estudiante por ID
        elEstudiante = Estudiante(self.repositorioEstudiante.findById(id))
        # Retornar la información del estudiante en un diccionario
        return elEstudiante.__dict__

    def update(self, id, infoEstudiante):
        # Obtener el estudiante actual por ID
        estudianteActual = Estudiante(self.repositorioEstudiante.findById(id))
        # Actualizar los atributos del estudiante con la información proporcionada
        estudianteActual.cedula = infoEstudiante["cedula"]
        estudianteActual.nombre = infoEstudiante["nombre"]
        estudianteActual.apellido = infoEstudiante["apellido"]
        # Guardar los cambios en el repositorio
        return self.repositorioEstudiante.save(estudianteActual)

    def delete(self, id):
        # Eliminar un estudiante del repositorio por ID
        return self.repositorioEstudiante.delete(id)

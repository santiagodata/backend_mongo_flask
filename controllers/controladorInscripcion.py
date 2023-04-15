from models.Inscripcion import Inscripcion
from models.Estudiante import Estudiante
from models.Materia import Materia
from repositories.repositorioInscripcion import RepositorioInscripcion
from repositories.repositorioEstudiante import RepositorioEstudiante
from repositories.repositorioMateria import RepositorioMateria


class ControladorInscripcion():
    def __init__(self):
        self.repositorioInscripcion = RepositorioInscripcion()
        self.repositorioEstudiantes = RepositorioEstudiante()
        self.repositorioMaterias = RepositorioMateria()

    def index(self):
        return self.repositorioInscripcion.findAll()

    """
    Asignacion estudiante y materia a inscripción
    """

    def create(self, infoInscripcion, id_estudiante, id_materia):
        nuevaInscripcion = Inscripcion(infoInscripcion)
        elEstudiante = Estudiante(self.repositorioEstudiantes.findById(id_estudiante))
        laMateria = Materia(self.repositorioMaterias.findById(id_materia))
        nuevaInscripcion.estudiante = elEstudiante
        nuevaInscripcion.materia = laMateria
        return self.repositorioInscripcion.save(nuevaInscripcion)

    def show(self, id):
        elInscripcion = Inscripcion(self.repositorioInscripcion.findById(id))
        return elInscripcion.__dict__

    """
    Modificación de inscripción (estudiante y materia)
    """

    def update(self, id, infoInscripcion, id_estudiante, id_materia):
        laInscripcion = Inscripcion(self.repositorioInscripcion.findById(id))
        laInscripcion.año = infoInscripcion["año"]
        laInscripcion.semestre = infoInscripcion["semestre"]
        laInscripcion.notaFinal = infoInscripcion["nota_final"]
        elEstudiante = Estudiante(self.repositorioEstudiantes.findById(id_estudiante))
        laMateria = Materia(self.repositorioMaterias.findById(id_materia))
        laInscripcion.estudiante = elEstudiante
        laInscripcion.materia = laMateria
        return self.repositorioInscripcion.save(laInscripcion)

    def delete(self, id):
        return self.repositorioInscripcion.delete(id)

    "Obtener todos los inscritos en una materia"

    def listarInscritosEnMateria(self, id_materia):
        return self.repositorioInscripcion.getListadoInscritosEnMateria(id_materia)

    "Obtener notas mas altas por curso"

    def notasMasAltasPorCurso(self):
        return self.repositorioInscripcion.getMayorNotaPorCurso()

    "Obtener promedio de notas en materia"

    def promedioNotasEnMateria(self, id_materia):
        return self.repositorioInscripcion.promedioNotasEnMateria(id_materia)

    def test(self, id_materia):
        return self.repositorioInscripcion.test(id_materia)

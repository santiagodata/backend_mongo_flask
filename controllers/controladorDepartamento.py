from repositories.repositorioDepartamento import RepositorioDepartamento
from models.Departamento import Departamento
from repositories.repositorioMateria import RepositorioMateria
from repositories.repositorioInscripcion import RepositorioInscripcion


class ControladorDepartamento():
    def __init__(self):
        self.repositorioDepartamento = RepositorioDepartamento()
        self.repositorioMateria = RepositorioMateria()
        self.repositorioInscripcion = RepositorioInscripcion()

    def index(self):
        return self.repositorioDepartamento.findAll()

    def create(self, infoDepartamento):
        nuevoDepartamento = Departamento(infoDepartamento)
        return self.repositorioDepartamento.save(nuevoDepartamento)

    def show(self, id):
        elDepartamento = Departamento(self.repositorioDepartamento.findById(id))
        return elDepartamento.__dict__

    def update(self, id, infoDepartamento):
        DepartamentoActual = Departamento(self.repositorioDepartamento.findById(id))
        DepartamentoActual.nombre = infoDepartamento["nombre"]
        DepartamentoActual.descripcion = infoDepartamento["descripcion"]
        return self.repositorioDepartamento.save(DepartamentoActual)

    def delete(self, id):
        return self.repositorioDepartamento.delete(id)

    def getMaterias(self, idMateria):
        return self.repositorioMateria.getListadoMateriasEnDepartamento(idMateria)

    def getPromedioGeneral(self, idDepartamento):
        elDepartamento = self.repositorioDepartamento.findById(idDepartamento)
        elDepartamento["materias"] = self.repositorioMateria.getListadoMateriasEnDepartamento(idDepartamento)
        suma = 0
        contador = 0
        i = 0
        for materiaActual in elDepartamento["materias"]:
            listadoInscritos = self.repositorioInscripcion.getListadoInscritosEnMateria(materiaActual["_id"])
            elDepartamento["materias"][i]["inscritos"] = listadoInscritos
            i += 1
            for inscripcionActual in listadoInscritos:
                suma += inscripcionActual["nota_final"]
                contador += 1

        promedio = suma / contador
        elDepartamento["promedio_notas"] = promedio
        return elDepartamento

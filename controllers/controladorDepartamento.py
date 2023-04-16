from repositories.repositorioDepartamento import RepositorioDepartamento # Importa la clase RepositorioDepartamento del módulo repositories.repositorioDepartamento
from models.departamento import Departamento # Importa la clase Departamento del módulo models.Departamento
from repositories.repositorioMateria import RepositorioMateria # Importa la clase RepositorioMateria del módulo repositories.repositorioMateria
from repositories.repositorioInscripcion import RepositorioInscripcion # Importa la clase RepositorioInscripcion del módulo repositories.repositorioInscripcion

class ControladorDepartamento(): # Define una clase ControladorDepartamento
    def __init__(self):
        self.repositorioDepartamento = RepositorioDepartamento() # Inicializa una instancia de RepositorioDepartamento
        self.repositorioMateria = RepositorioMateria() # Inicializa una instancia de RepositorioMateria
        self.repositorioInscripcion = RepositorioInscripcion() # Inicializa una instancia de RepositorioInscripcion

    def index(self):
        return self.repositorioDepartamento.findAll() # Obtiene una lista de todos los departamentos

    def create(self, infoDepartamento):
        nuevoDepartamento = Departamento(infoDepartamento) # Crea una nueva instancia de la clase Departamento con la información proporcionada
        return self.repositorioDepartamento.save(nuevoDepartamento) # Guarda el nuevo departamento en el repositorio

    def show(self, id):
        elDepartamento = Departamento(self.repositorioDepartamento.findById(id)) # Obtiene un departamento por su ID y crea una instancia de la clase Departamento con la información obtenida
        return elDepartamento.__dict__ # Retorna un diccionario con los atributos del departamento

    def update(self, id, infoDepartamento):
        DepartamentoActual = Departamento(self.repositorioDepartamento.findById(id)) # Obtiene un departamento por su ID y crea una instancia de la clase Departamento con la información obtenida
        DepartamentoActual.nombre = infoDepartamento["nombre"] # Actualiza el nombre del departamento con la información proporcionada
        DepartamentoActual.descripcion = infoDepartamento["descripcion"] # Actualiza la descripción del departamento con la información proporcionada
        return self.repositorioDepartamento.save(DepartamentoActual) # Guarda los cambios en el repositorio

    def delete(self, id):
        return self.repositorioDepartamento.delete(id) # Elimina un departamento por su ID

    def getMaterias(self, idMateria):
        return self.repositorioMateria.getListadoMateriasEnDepartamento(idMateria) # Obtiene una lista de materias en un departamento por su ID de materia


    def getPromedioGeneral(self, idDepartamento):
        # Obtener información del departamento por ID
        elDepartamento = self.repositorioDepartamento.findById(idDepartamento)

        # Obtener la lista de materias en el departamento
        elDepartamento["materias"] = self.repositorioMateria.getListadoMateriasEnDepartamento(idDepartamento)

        # Inicializar variables para calcular el promedio
        suma = 0
        contador = 0
        i = 0

        # Iterar por cada materia en el departamento
        for materiaActual in elDepartamento["materias"]:
            # Obtener la lista de inscritos en la materia
            listadoInscritos = self.repositorioInscripcion.getListadoInscritosEnMateria(materiaActual["_id"])

            # Agregar la lista de inscritos a la materia en el departamento
            elDepartamento["materias"][i]["inscritos"] = listadoInscritos
            i += 1

            # Iterar por cada inscripción en la materia
            for inscripcionActual in listadoInscritos:
                # Sumar la nota final del inscrito a la suma total
                suma += inscripcionActual["nota_final"]
                contador += 1

        # Calcular el promedio dividiendo la suma total por la cantidad de inscritos
        promedio = suma / contador

        # Agregar el promedio de notas al departamento
        elDepartamento["promedio_notas"] = promedio

        # Retornar el departamento con la información actualizada
        return elDepartamento

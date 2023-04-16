from repositories.interfaceRepositorio import InterfaceRepositorio # Importa la interfaz del repositorio
from models.estudiante import Estudiante # Importa el modelo Estudiante

class RepositorioEstudiante(InterfaceRepositorio[Estudiante]): # Define una clase RepositorioEstudiante que implementa la interfaz InterfaceRepositorio para el modelo Estudiante
    pass # No implementa ninguna funcionalidad adicional, simplemente hereda de la interfaz y no realiza ninguna modificación o adición de métodos

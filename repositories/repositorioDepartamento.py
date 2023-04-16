from repositories.interfaceRepositorio import InterfaceRepositorio # Importa la interfaz del repositorio
from models.departamento import Departamento # Importa el modelo Departamento

class RepositorioDepartamento(InterfaceRepositorio[Departamento]): # Define una clase RepositorioDepartamento que implementa la interfaz InterfaceRepositorio para el modelo Departamento
    pass # No implementa ninguna funcionalidad adicional, simplemente hereda de la interfaz y no realiza ninguna modificación o adición de métodos

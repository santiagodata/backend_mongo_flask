from abc import ABCMeta # Importa la clase ABCMeta del módulo abc

class AbstractModelo(metaclass=ABCMeta): # Define una clase AbstractModelo que utiliza la metaclase ABCMeta
    def __init__(self, data):
        # Define un constructor que recibe el parámetro data
        for llave, valor in data.items(): # Itera sobre las llaves y valores del diccionario data
            setattr(self, llave, valor) # Asigna el valor al atributo con el nombre de la llave utilizando la función setattr de Python

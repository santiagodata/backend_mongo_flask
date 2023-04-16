Aplicación de Control de Inscripciones
Esta es una aplicación de control de inscripciones en un sistema educativo. Permite gestionar las inscripciones de
estudiantes en materias específicas, así como realizar consultas y obtener estadísticas relacionadas con las inscripciones.

Requisitos
La aplicación requiere los siguientes componentes para funcionar correctamente:

Python 3.x
Librerías
Base de datos compatible (En este caso se usa el servicio de MongoDB Atlas)

Instalación
Siga los pasos a continuación para instalar y configurar la aplicación:

Clonar el repositorio de GitHub en su entorno local:
git clone https://github.com/santiagodata/backend_mongo_flask.git

Instalar las librerías requeridas:

Configurar la base de datos: la aplicación utiliza una base de datos específica que debe configurarse antes de su uso. Ver diagram_bd.png para observar una representación gráfica de la Base de Datos


Ejecutar la aplicación:
main.py


Funcionalidades
La aplicación de control de inscripciones ofrece las siguientes funcionalidades:

Crear una nueva inscripción: los usuarios pueden crear nuevas inscripciones proporcionando la información necesaria, como el nombre del estudiante, la materia y otros detalles relevantes. La inscripción se guarda en la base de datos.

Modificar una inscripción existente: los usuarios pueden actualizar los detalles de una inscripción existente, como el año, semestre, nota final, estudiante y materia asociada.

Eliminar una inscripción: los usuarios pueden eliminar una inscripción existente proporcionando su identificador único.

Consultar inscripciones: los usuarios pueden consultar las inscripciones existentes en la base de datos, obtener información detallada de una inscripción específica y obtener listados de inscritos en una materia y promedios de notas en una materia específica.

Obtener estadísticas: los usuarios pueden obtener estadísticas relevantes, como las notas más altas por curso.

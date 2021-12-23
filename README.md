# api-gateway
Api gateway to use a single url for every call
Repositorio encargado de hacer de gateway para todos los repositorios internos de la aplicacion y hacer un manejo simple del jwt. Pero no es el encargado de generar el mismo.
## Instalacion:
La instalacion se hace con pip3 install -r requirements.txt
Tener en cuenta que esto no garantiza que los submodulos esten correctamente instalado si se quiere instalar unitariamente.
## Instalacion en conjunto:
Se genero un docker-compose el cual tiene toda la data necesaria para ejecutar el file de manera local, ademas que ya vincula todas las variables de entorno necesaria
para usarlo de una forma dockerizada. Lo que significa que es altamente recomendable, si se quiere usar esta aplicacion de manera local, hacerlo usando docker compose provisto
## Tests
Al ser una aplicacion que solo tiene el proposito de ser de redireccion, el mismo no tiene tests ya que se vio innecesario.
## Correr de manera local.
Para ejecutar de manera local se debe correr una base de datos local, ya sea con docker, o con alguna base de datos online de su preferencia. 
Al igual que con el sector de instalacion en conjunto, se recomienda que se use con docker-compose esta base de datos.
## Correr con makefile.
Se puede ejecutar el comando de make buildDC para compilar el codigo y luego correr runDC para ejecutar la base de datos y el codigo en conjunto en un ambiente local, asi levantando todos los repositorios accesibles.
##Imposibilidades:
No se puede utilizar este repositorio para generar pagos, dado que el repositorio de payments esta bloqueado a acceso publico debido a datos sensibles que son expuestos alli.
## Variables de entorno necesarias para un uso completo en caso que no se utilice DC:
### COURSES_HOST: URL de donde se va a interactuar con la api de cursos
### EXAMS_HOST: URL de donde se va a interactuar con la api de examenes
### USERS_HOST: URL de donde se va a interactuar con la api de usuarios
### HASH_ALGORITHM: algoritmo de hasheo para la aplicacion
### HASH_SECRET: secreto de la aplicacion

## Acceso a la documentacion:
Se tiene dos posibilidades para acceder a la aplicacion. La primera es mediante el swagger provisto por heroku [en este link](https://ubademy-14-prod.herokuapp.com/doc).
La segunda es accediendo al swagger de cada aplicacion (es mas simple que el configurar el archivo de configuracion localizado en templates/index.html). Para acceder al swagger localmente
es mediante el host creado para tu aplicacion (por lo general localhost:8080) mas el path de /doc.

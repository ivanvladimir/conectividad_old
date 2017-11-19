# Importante!

No olvidar ejecutar el comando ```execute.sh z``` de la carpeta 
```path/to/project/src/python```  para ejecutar todos los 
procesos previos necesarios.

# ONE SCRIPT TO RULE THEM ALL!!!

Scripts para ejecutar el sistema de manera automatizada.

Banderas:

- -f : Primer uso. Instala las dependencias necesarias, importa las variables necesarias y crea el entorno virtual.
- -h : Muestra la ayuda.
- Sin banderas : Ejecuta el script sin la bandera -f .
```
./execute_all.sh [-f][-h]
```

# Flask Skeleton

Flask starter project...

[![Build Status](https://travis-ci.org/realpython/flask-skeleton.svg?branch=master)](https://travis-ci.org/realpython/flask-skeleton)

## Quick Start

### Basics

1. Create and activate a virtualenv
2. Install the requirements

### Set Environment Variables

Update *project/server/config.py*, and then run:

```sh
$ export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
```

### Run the Application

```sh
$ python manage.py runserver
```

So access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

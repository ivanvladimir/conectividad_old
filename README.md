# ConectividadNormativa

## Uso

#### Obtener y pre-procesar archivos.

Ejecutar el script ```execute.sh``` de ```/path/to/project/src/python/```.

Para ejecutar con un menu desplegado ```execute.sh```.

Para ejecutar con alguna bandera especifica ```execute.sh [hidtmaslrze]``` , utilizar la bandera ```h``` para mostrar ayuda.

Para ejecutar todo el proceso utilizar la bandera ```z```, ```execute.sh z```

#### Desplegar sitio web.

Ejecutar el script ```execute.sh``` de ```/path/to/project/webapp/```.

Si es la primera vez que se ejecuta, utilizar la bandera ```-f```.

```execute.sh -f```

#### Etiquetar documentos.

* Nota: Actualmente se puede ejecutar el script ```execute.sh``` de ```/path/to/project/src/python/``` con la bandera ```m```, ```execute.sh m```.

Ir al directorio ```/path/to/project/gate/Java/```.

Para compilar utilizar el script ```compile_embedded.sh```.

Para ejecutar utilizar el script ```run_embedded.sh```.

Para compilar y ejecutar utilizar el script ```compile_run_embedded.sh```.

Es necesario tener la variable ```$GATE_HOME``` en el sistema .

Esta variable se puede se puede crear modificando ```/etc/environment``` en sistemas GNU/Linux y añadiendo el valor de la variable, o exportandola con ```export```.

e.g.

Comando ```nano /etc/environment```

Contenido del archivo:

```
GATE_HOME=/path/to/gate
```

Usando ```export```

```
export GATE_HOME=/path/to/gate
```

Para recargar las variables de entorno puede usar ```source /etc/environment```

## Directorios

### Python

Scripts to crawl and generate database

### Gate

Scrpits para generar etiquetado y procesamiento de archivos

### Webapp

Scripts para servicios Webapp

## Agradecimientos

Apoyo de Proyecto CONACYT Fronteras de la Ciencia Constructivismo jurídico complejo: cognición, complejidad y derecho

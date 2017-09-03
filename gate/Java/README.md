# GATE Embedded

## GATE_HOME

Es necesario tener la variable ```$GATE_HOME``` en el sistema .

Esta variable se puede se puede crear modificando ```/etc/environment``` en sistemas GNU/Linux y añadiendo el valor de la variable, o exportandola con ```export```.

e.g.

Comando ```nano /etc/environment```

Contenido del archivo:

```
# Penserbjorne
GATE_HOME=/path/to/gate
```

Usando ```export```

```
export GATE_HOME=/path/to/gate
```

Para recargar las variables de entorno puede usar ```source /etc/environment```

## Compilar y ejecutar

Para compilar utilizar el script ```compile_embedded.sh```.

Para ejecutar utilizar el script ```run_embedded.sh```.

Para compilar y ejecutar utilizar el script ```compile_run_embedded.sh```.

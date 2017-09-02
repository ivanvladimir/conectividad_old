# GATE Embedded

Es necesario tener la variable ```$GATE_HOME``` en el sistema .

Esta variable se puede se puede crear modificando ```/etc/environment``` en sistemas GNU/Linux y añadiendo el valor de la variable.

e.g.

Comando ```nano /etc/environment```

Contenido del archivo:
```
# Penserbjorne
GATE_HOME=/home/penserbjorne/GATE_Developer_8.4.1
```

Para recargar las variables de entorno puede usar ```source /etc/environment```

Para compilar utilizar el script ```compile_embedded.sh```.

Para ejecutar utilizar el script ```run_embedded.sh```.

Para compilar y ejecutar utilizar el script ```compile_run_embedded.sh```.

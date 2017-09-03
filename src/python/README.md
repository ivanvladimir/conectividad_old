# Orden de ejecucion

Scripts necesarios para obtener los documentos necesarios así como los datos y metadatos básicos necesarios.

## ONE SCRIPT TO RULE THEM ALL!!!

Para ejecutar todo de una sola vez.

Banderas:

- -f : Primer uso. Instala las dependencias necesarias y crea el entorno virtual.
- -r : Eliminar. Forza a eliminar todos los registros creados previamente (documentos, enlaces, entornos virtuales).
- -h : Muestra la ayuda.
- Sin banderas : Ejecuta el script sin las banderas -f -r .
```
./execute_all.sh [-f][-r][-h]
```

## Uno por uno

Es necesario ejecutar estos scripts en este orden, pueden omitirse las banderas -v -i .
```
python download_casos_contenciosos.py
mkdir ./data/extract_text
python extract_text.py --dbname ./data/DB.json --odir ./data/extract_text -v
python basic_statistics.py -v
python module_canonical_name.py --dbname ./data/DB.json -v -i
python extract_articles.py --dbname ./data/DB.json --graph ./data/graph.json -v
```

Hay que realizar un enlace de *./data/DB.json* a *./../../webapp/DB.json* y de *./data/graph.json* a *./../../webapp/project/client/static/graph.json*

```
ln -sf ./data/DB.json ./../../webapp/DB.json
ln -sf ./data/graph.json ./../../webapp/project/client/static/graph.json
```

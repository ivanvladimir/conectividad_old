# Orden de ejecucion
```
python download_casos_contenciosos.py
mkdir ./data/extract_text
python extract_text.py --dbname ./data/DB.json --odir ./data/extract_text -v
python basic_statistics.py -v
python module_canonical_name.py --dbname ./data/DB.json -v -i
python python extract_articles.py --dbname ./data/DB.json --graph ./data/graph.json -v
```
Hay que realizar un enlace de *./data/DB.json* a *./../../webapp/DB.json* y de *./data/graph.json* a *./../../webapp/project/client/static/graph.json*

# Dependencias

## download_casos_contenciosos.py

En Ubuntu:

```
sudo apt-get install python3-requests
sudo apt-get install python3-bs4
sudo pip3 install tinydb
```

## download_casos_contenciosos.py

En Ubuntu:

```
sudo pip3 install tinydb
sudo pip3 -U install nltk
sudo pip3 -U install pdfminer3k
sudo apt-get install python3-numpy
sudo apt-get install python3-scipy
sudo pip3 -U install sklearn
```

Es necesario instalar los siguientes recursos de nltk:

-   corpora/stopwords
-   tokenizers/punkt

```
$ python
>>> import nltk
>>> nltk.download();
NLTK Downloader
---------------------------------------------------------------------------
    d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
---------------------------------------------------------------------------
Downloader> d

Download which package (l=list; x=cancel)?
  Identifier> stopwords
    Downloading package stopwords to /home/penserbjorne/nltk_data...
      Unzipping corpora/stopwords.zip.

---------------------------------------------------------------------------
    d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
---------------------------------------------------------------------------
Downloader> d

Download which package (l=list; x=cancel)?
  Identifier> punkt
    Downloading package punkt to /home/penserbjorne/nltk_data...
      Unzipping tokenizers/punkt.zip.

---------------------------------------------------------------------------
    d) Download   l) List    u) Update   c) Config   h) Help   q) Quit
---------------------------------------------------------------------------
Downloader> q
>>> exit();
```

## basic_statistics.py

En Ubuntu:

```
sudo pip3 install tinydb
sudo apt-get install python3-matplotlib
```

# Resultados y carpeta Data

## Generados por "download_casos_contenciosos.py"

Al 16 de Junio del 2017:

-   Archivos descargados: 674
    -   337 en Word.
    -   337 en PDF
    -   Cada Word tiene un PDF
-   Tiempo aproximado de descarga: 15 a 30 min

Ubicacion:

```
->  data
    ->  contenciosos
        ->  files
```

## Generados por "extract_text.py"

Al 16 de Junio del 2017:

-   Archivos descargados: 337
    -   Uno por cada pareja de Word y PDF
-   Tiempo aproximado de ejecucion:  1.5 min

Ubicacion:

```
->  data
    ->  contenciosos
```

## Generados por "basic_statistics.py"

-   Grafico de barras de vocabulario.
-   Grafo
-   Tiempo aproximado de ejecucion:  3 min

Ubicacion:

-   Carpeta raiz ''python''

# Orden de ejecucion
```
$ ./download_casos_contenciosos.py
$ mkdir ./data/extract_text
$ ./extract_text.py --dbname ./data/DB.json --odir ./data/extract_text -v
$ ./basic_statistics.py -v
$ ./module_canonical_name.py --dbname ./data/DB.json -v -i

```
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

Al 24 de Abril del 2017:

-   Archivos descargados: 662
    -   331 en Word.
    -   331 en PDF
    -   Cada Word tiene un PDF
-   Tiempo aproximado de descarga: 5 a 15 min

Ubicacion:

```
->  data
    ->  contenciosos
        ->  files
```

## Generados por "extract_text.py"

Al 09 de Abril del 2017:

-   Archivos descargados: 330
    -   Uno por cada pareja de Word y PDF
-   Tiempo aproximado de ejecucion:  1.5 min

Ubicacion:

```
->  data
    ->  contenciosos
```

## Generados por "basic_statistics.py"

Resultados de la ejecucion al 09 de Abril del 2017:

-   Grafico de barras de vocabulario.
-   Grafo
-   Tiempo aproximado de ejecucion:  3 min

Ubicacion:

-   Carpeta raiz ''python''

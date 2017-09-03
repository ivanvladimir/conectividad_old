# Orden de ejecucion

## ONE SCRIPT TO RULE THEM ALL!!!

Para ejecutar todo de una sola vez.
```
./execute_all.sh
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

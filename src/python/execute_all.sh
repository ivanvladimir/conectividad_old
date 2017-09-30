#! /bin/bash
# autor: @Penserbjorne - Sebastian Aguilar
# FI-IIMAS-IIJ-UNAM

# Define a timestamp function
timestamp() {
  date +"%T"
}

TIME_INI=$(date -u -d "$(timestamp)" +"%s")

echo $(timestamp) " > ulimit -m 4194304"
#ulimit -m 6291456
ulimit -m 4194304

# Get Parammeter
while getopts fdrh opts; do
   case ${opts} in
      f) FIRST_TIME=true;;
      d) DOWNLOAD=true;;
      r) REMOVE=true ;;
      #r) REMOVE=${OPTARG} ;;
      h) HELP=true ;;
   esac
done

if [ $HELP ]; then
  echo "
  Descripción:
  Scripts necesarios para obtener los documentos necesarios así como los datos y metadatos básicos necesarios.

  -f : Primer uso. Instala las dependencias necesarias y crea el entorno virtual.
  -d : Vuelve a descargar los archivos fuente del repositorio.
  -r : Eliminar. Forza a eliminar todos los registros creados previamente (documentos, enlaces y salidas de datos).
  -h : Muestra la ayuda.
  Sin banderas : Ejecuta el script sin las banderas -f -d -r .

  Uso: ./execute_all.sh [-f][-d][-r][-h]"
  exit
fi

echo "ONE SCRIPT TO RULE THEM ALL!!!"

echo "Es necesrio instalar tkinter para python3 por separado."
echo "Presione una tecla para cotinuar..."
read

echo $(timestamp) " > Begining"

if [ $REMOVE ]; then
  echo $(timestamp) " > rm -rf ./data"
  rm -rf ./data

  echo $(timestamp) " > rm -rf ./../../webapp/DB.json"
  rm -rf ./../../webapp/DB.json

  echo $(timestamp) " > rm -rf ./../../webapp/annotatedDocuments"
  rm -rf ./../../webapp/annotatedDocuments

  echo $(timestamp) " > rm -rf ./../../webapp/project/client/static/graph.json"
  rm -rf ./../../webapp/project/client/static/graph.json
fi

if [ $FIRST_TIME ]; then
  echo $(timestamp) " > virtualenv -p /usr/bin/python3 env"
  virtualenv -p /usr/bin/python3 env
fi

echo $(timestamp) " > source ./env/bin/activate"
source ./env/bin/activate

if [ $FIRST_TIME ]; then
  echo $(timestamp) " > pip install -r requirements.txt"
  pip3 install -r requirements.txt

  python3 -m nltk.downloader all
fi

if [ $FIRST_TIME ] || [ $DOWNLOAD ]; then
  echo $(timestamp) " > download_casos_contenciosos.py"
  python3 ./download_casos_contenciosos.py
fi

echo $(timestamp) " > mkdir ./data/extract_text"
mkdir ./data/extract_text

echo $(timestamp) " > mkdir ./data/AnnotatedDocuments"
mkdir ./data/annotatedDocuments

echo $(timestamp) " > extract_text.py"
python3 extract_text.py

# Se necesita?
#echo $(timestamp) " > basic_statistics.py"
#python3 basic_statistics.py

echo $(timestamp) " > module_canonical_name.py"
python3 module_canonical_name.py

echo $(timestamp) " > cd ./../../gate/Java/"
cd ./../../gate/Java/

echo $(timestamp) " > ./compile_run_embedded.sh"
./compile_run_embedded.sh

echo $(timestamp) " > cd ./../../gate/Java/"
cd ./../src/python

echo $(timestamp) " > extract_articles.py"
python3 extract_articles.py

echo $(timestamp) " > deactivate"
deactivate

echo $(timestamp) " > cd ./../../webapp/"
cd ./../../webapp/

echo $(timestamp) " > ln -sf ./../src/python/data/DB.json ./DB.json"
ln -sf ./../src/python/data/DB.json ./DB.json

echo $(timestamp) " > ln -sf ./../src/python/data/annotatedDocuments ./annotatedDocuments"
ln -sf ./../src/python/data/annotatedDocuments ./annotatedDocuments

echo $(timestamp) " > cd ./project/client/static/"
cd ./project/client/static/

echo $(timestamp) " > ln -sf ./../../../../src/python/data/graph.json ./graph.json"
ln -sf ./../../../../src/python/data/graph.json ./graph.json

echo $(timestamp) " > cd ./../../../../src/python/ "
cd ./../../../../src/python/

echo $(timestamp) " > DONE!"

TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")

echo ""

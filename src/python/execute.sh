#! /bin/bash
# autor: @Penserbjorne - Sebastian Aguilar
# FI-IIMAS-IIJ-UNAM

opt=-1

# Define a timestamp function
timestamp() {
  date +"%T"
}

help(){
  echo "
  ONE SCRIPT TO RULE THEM ALL!!!

  Descripción: Script útilizado para automátizar la ejecución y despliegue del sistema.

  h) Help
  i) Initialize (install dependencies and create environment)
  d) Download data
  t) Extract text
  m) Annotated documents
  a) Extract articles
  s) Basic statistics
  l) Create links
  r) Remove data
  z) Execute all process
  e) Exit

  Uso: ./execute.sh [hidtmaslrze]"
  exit
}

menu(){
  echo -n "
  ONE SCRIPT TO RULE THEM ALL!!!

  Select an option.
    i) Initialize (install dependencies and create environment)
    d) Download data
    t) Extract text
    m) Annotated documents
    a) Extract articles
    s) Basic statistics
    l) Create links
    r) Remove data
    z) Execute all process
    e) Exit
  Option: "
  read opt
}

menuOption(){
  if [ "$opt" = "i" ] || [ "$opt" = "I" ]; then
    initialize
  elif [ "$opt" = "d" ] || [ "$opt" = "D" ]; then
    downloadData
  elif [ "$opt" = "t" ] || [ "$opt" = "T" ]; then
    extractText
  elif [ "$opt" = "m" ] || [ "$opt" = "M" ]; then
    annotatedDocuments
  elif [ "$opt" = "a" ] || [ "$opt" = "A" ]; then
    extractArticles
  elif [ "$opt" = "s" ] || [ "$opt" = "S" ]; then
    basicStatistics
  elif [ "$opt" = "l" ] || [ "$opt" = "L" ]; then
    createLinks
  elif [ "$opt" = "r" ] || [ "$opt" = "R" ]; then
    removeData
  elif [ "$opt" = "h" ] || [ "$opt" = "H" ]; then
    help
  elif [ "$opt" = "z" ] || [ "$opt" = "Z" ]; then
    removeData
    initialize
    downloadData
    extractText
    annotatedDocuments
    extractArticles
    basicStatistics
    createLinks
    exit
  elif [ "$opt" = "e" ] || [ "$opt" = "E" ]; then
    echo "  See you!"
    exit
  else
    echo "  Error: Nope, I don't know what do you want :/ Sorry!"
  fi
}

initialize(){
  TIME_INI=$(date -u -d "$(timestamp)" +"%s")
  echo
  echo $(timestamp) " > Begining"

  echo $(timestamp) " > virtualenv -p /usr/bin/python3 env"
  virtualenv -p /usr/bin/python3 env

  echo $(timestamp) " > source ./env/bin/activate"
  source ./env/bin/activate

  echo $(timestamp) " > pip install -r requirements.txt"
  pip3 install -r requirements.txt

  echo $(timestamp) " > python3 -m nltk.downloader all"
  python3 -m nltk.downloader all

  echo $(timestamp) " > deactivate"
  deactivate

  TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
  echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
  echo
}

downloadData(){
  if [ -d "./env" ]; then
    TIME_INI=$(date -u -d "$(timestamp)" +"%s")
    echo
    echo $(timestamp) " > Begining"

    echo $(timestamp) " > source ./env/bin/activate"
    source ./env/bin/activate

    echo $(timestamp) " > download_casos_contenciosos.py"
    python3 ./download_casos_contenciosos.py -v

    echo $(timestamp) " > deactivate"
    deactivate

    TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
    echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
    echo
  else
    echo "  Theres no enviroment! Please \"Initialize\""
  fi
}

extractText(){
  if [ -d "./env" ]; then
    TIME_INI=$(date -u -d "$(timestamp)" +"%s")
    echo
    echo $(timestamp) " > Begining"

    echo $(timestamp) " > source ./env/bin/activate"
    source ./env/bin/activate

    echo $(timestamp) " > extract_text.py"
    python3 extract_text.py -v

    echo $(timestamp) " > module_canonical_name.py"
    python3 module_canonical_name.py -v

    echo $(timestamp) " > deactivate"
    deactivate

    TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
    echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
    echo
  else
    echo "  Theres no enviroment! Please \"Initialize\""
  fi
}

annotatedDocuments(){
  if [ -d "./env" ]; then
    TIME_INI=$(date -u -d "$(timestamp)" +"%s")
    echo
    echo $(timestamp) " > Begining"

    if [ ! -d "./data/AnnotatedDocuments" ]; then
      echo $(timestamp) " > mkdir ./data/AnnotatedDocuments"
      mkdir ./data/annotatedDocuments
    fi

    echo $(timestamp) " > cd ./../../gate/Java/"
    cd ./../../gate/Java/

    echo $(timestamp) " > ./compile_run_embedded.sh"
    ./compile_run_embedded.sh

    echo $(timestamp) " > cd ./../../src/python/"
    cd ./../../src/python/

    TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
    echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
    echo
  else
    echo "  Theres no enviroment! Please \"Initialize\""
  fi
}

extractArticles(){
  if [ -d "./env" ]; then
    TIME_INI=$(date -u -d "$(timestamp)" +"%s")
    echo
    echo $(timestamp) " > Begining"

    echo $(timestamp) " > source ./env/bin/activate"
    source ./env/bin/activate

    echo $(timestamp) " > extract_articles.py"
    python3 extract_articles.py -v

    echo $(timestamp) " > deactivate"
    deactivate

    TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
    echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
    echo
  else
    echo "  Theres no enviroment! Please \"Initialize\""
  fi
}

basicStatistics(){
  if [ -d "./env" ]; then
    TIME_INI=$(date -u -d "$(timestamp)" +"%s")
    echo
    echo $(timestamp) " > Begining"

    echo $(timestamp) " > source ./env/bin/activate"
    source ./env/bin/activate

    echo $(timestamp) " > basic_statistics.py"
    python3 basic_statistics.py -v

    echo $(timestamp) " > deactivate"
    deactivate

    TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
    echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
    echo
  else
    echo "  Theres no enviroment! Please \"Initialize\""
  fi
}

createLinks(){
  TIME_INI=$(date -u -d "$(timestamp)" +"%s")
  echo
  echo $(timestamp) " > Begining"

  echo $(timestamp) " > cd ./../../webapp/"
  cd ./../../webapp/

  echo $(timestamp) " > ln -sf ./../src/python/data/DB.json ./DB.json"
  ln -sf ./../src/python/data/DB.json ./DB.json

  echo $(timestamp) " > ln -sf ./../src/python/data/annotatedDocuments ./annotatedDocuments"
  ln -sf ./../src/python/data/annotatedDocuments ./annotatedDocuments

  echo $(timestamp) " > ln -sf ./../src/python/data/contenciosos ./contenciosos"
  ln -sf ./../src/python/data/contenciosos ./contenciosos

  echo $(timestamp) " > ln -sf ./../src/python/data/graph.json ./graph.json"
  ln -sf ./../src/python/data/graph.json ./graph.json

  echo $(timestamp) " > cd ./../src/python/ "
  cd ./../src/python/

  TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
  echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
  echo
}

removeData(){
  echo  -n "
  This going to remove all data ( data folder, DB.json, annotatedDocuments and graph.json)
  Continue? y/n: "
  read opt

  if [ "$opt" = "y" ] || [ "$opt" = "Y" ]; then
    TIME_INI=$(date -u -d "$(timestamp)" +"%s")
    echo
    echo $(timestamp) " > Begining"
    echo $(timestamp) " > rm -rf ./data"
    rm -rf ./data

    echo $(timestamp) " > rm -rf ./../../webapp/DB.json"
    rm -rf ./../../webapp/DB.json

    echo $(timestamp) " > rm -rf ./../../webapp/annotatedDocuments"
    rm -rf ./../../webapp/annotatedDocuments

    echo $(timestamp) " > rm -rf ./../../webapp/project/client/static/graph.json"
    rm -rf ./../../webapp/project/client/static/graph.json

    TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
    echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")
    echo
  else
    echo "  Ok, dont worry, sometimes is ... is ... is just fine to don't erase the old moments :)"
  fi
}

echo $(timestamp) " > ulimit -m 2097152 => Max. 2 GB"
ulimit -m 2097152

count=0
for var in "$@"
do
    (( count++ ))
    (( accum += ${#var} ))
    opt=$var
    menuOption
done

# Hubo comandos, salimos ;@
if [ "$opt" != "-1" ]; then
  exit
fi

echo "ONE SCRIPT TO RULE THEM ALL!!!"
echo "Es necesario instalar tkinter para python3 por separado."

while [ "$opt" != "e" ] || [ "$opt" != "E" ] ; do
  menu
  menuOption
done

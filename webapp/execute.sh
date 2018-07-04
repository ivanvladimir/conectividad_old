#! /bin/bash
# autor: @Penserbjorne - Sebastian Aguilar
# FI-IIMAS-IIJ-UNAM

# Define a timestamp function
timestamp() {
  date +"%T"
}

TIME_INI=$(date -u -d "$(timestamp)" +"%s")

# Get Parammeter
while getopts frh opts; do
   case ${opts} in
      f) FIRST_TIME=false;;
      #r) REMOVE=true ;;
      #r) REMOVE=${OPTARG} ;;
      h) HELP=true ;;
   esac
done

if [[ $HELP ]]; then
  echo "
  ONE SCRIPT TO RULE THEM ALL!!!

  Descripción: Scripts necesarios para obtener los documentos necesarios así como los datos y metadatos básicos necesarios.

  -f : Primer uso. Instala las dependencias necesarias, importa las variables necesarias y crea el entorno virtual.
  -h : Muestra la ayuda.

  Uso: ./execute_all.sh [-f][-h]"
  exit
fi

echo "ONE SCRIPT TO RULE THEM ALL!!!"

echo $(timestamp) " > Begining"

if [[ $FIRST_TIME ]] || [[ ! -d "./env" ]]; then
  if [[ ! -d "./env" ]]; then
    REQUIREMENTS=true
  fi
  echo $(timestamp) " > virtualenv -p /usr/bin/python3 env"
  virtualenv -p /usr/bin/python3 env
fi

echo $(timestamp) " > source ./env/bin/activate"
source ./env/bin/activate

if [[ $FIRST_TIME ]] || [[ $REQUIREMENTS ]]; then
  echo $(timestamp) " > pip install -r requirements.txt"
  pip3 install -r requirements.txt

  echo $(timestamp) " > python3 -m nltk.downloader all"
  python3 -m nltk.downloader all
fi

if [[ $FIRST_TIME ]]; then
  echo $(timestamp) " > export APP_SETTINGS=\"project.server.config.ProductionConfig\""
  export APP_SETTINGS="project.server.config.ProductionConfig"

  echo $(timestamp) " > python manage.py create_db"
  python3 manage.py create_db

  echo $(timestamp) " > python manage.py db init"
  python3 manage.py db init

  echo $(timestamp) " > python manage.py db migrate"
  python3 manage.py db migrate

  echo $(timestamp) " > python manage.py create_admin"
  python3 manage.py create_admin

  echo $(timestamp) " > python manage.py create_data"
  python3 manage.py create_data
fi

echo $(timestamp) " > SEMI DONE! RUNING SERVER!!!"

TIME_MID=$(date -u -d "$(timestamp)" +"%s")
echo "Time until this command: " $(date -u -d "0 $TIME_MID sec - $TIME_INI sec" +"%H:%M:%S")

echo $(timestamp) " > python manage.py runserver"
python3 manage.py runserver

echo $(timestamp) " > deactivate"
deactivate

echo $(timestamp) " > DONE!"

TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")

echo ""

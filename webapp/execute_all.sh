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
      f) FIRST_TIME=true;;
      #r) REMOVE=true ;;
      #r) REMOVE=${OPTARG} ;;
      h) HELP=true ;;
   esac
done

if [[ $HELP ]]; then
  echo "
  Descripción:
  Scripts necesarios para obtener los documentos necesarios así como los datos y metadatos básicos necesarios.

  -f : Primer uso. Instala las dependencias necesarias, importa las variables necesarias y crea el entorno virtual.
  -h : Muestra la ayuda.
  Sin banderas : Ejecuta el script sin la bandera -f .

  Uso: ./execute_all.sh [-f][-h]"
  exit
fi

echo "ONE SCRIPT TO RULE THEM ALL!!!"

echo $(timestamp) " > Begining"

if [[ $FIRST_TIME ]]; then
  echo $(timestamp) " > virtualenv virtenv"
  virtualenv virtenv
fi

echo $(timestamp) " > source ./virtenv/bin/activate"
source ./virtenv/bin/activate

if [[ $FIRST_TIME ]]; then
  echo $(timestamp) " > pip install -r requirements.txt"
  pip install -r requirements.txt

  echo $(timestamp) " > export APP_SETTINGS=\"project.server.config.ProductionConfig\""
  export APP_SETTINGS="project.server.config.ProductionConfig"

  echo $(timestamp) " > python manage.py create_db"
  python manage.py create_db

  echo $(timestamp) " > python manage.py db init"
  python manage.py db init

  echo $(timestamp) " > python manage.py db migrate"
  python manage.py db migrate

  echo $(timestamp) " > python manage.py create_admin"
  python manage.py create_admin

  echo $(timestamp) " > python manage.py create_data"
  python manage.py create_data
fi

echo $(timestamp) " > SEMI DONE! RUNING SERVER!!!"

TIME_MID=$(date -u -d "$(timestamp)" +"%s")
echo "Time until this command: " $(date -u -d "0 $TIME_MID sec - $TIME_INI sec" +"%H:%M:%S")

echo $(timestamp) " > python manage.py runserver"
python manage.py runserver

echo $(timestamp) " > deactivate"
deactivate

echo $(timestamp) " > DONE!"

TIME_FIN=$(date -u -d "$(timestamp)" +"%s")
echo "Total time: " $(date -u -d "0 $TIME_FIN sec - $TIME_INI sec" +"%H:%M:%S")

echo ""

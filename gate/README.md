# GATE

## Gate Developer

La aplicación actual ya contiene todos los elementos necesarios para realizar tareas de IE en Gate Developer.

## Notas
- Procurar añadir todos los recursos con codificacion **UTF-8**.
- El **Gazetteer Juridicas** es **case-insensitive**.
- Anotaciones que se muestran en el ejemplo de la aplicación web
    - Actions
    - Articles
    - Case
    - Date2
    - DateSentence
    - PersonCourtMembers
    - ResolutivePoints
    - ConcurrentVote
- Reglas por revisar y/o con dudas
    - CourtMembers
    - Date2
- Reglas por mejorar
    - Articles
    - PersonCourtMembers
    - LastSection
    - ResolutivePointsTemp

### Cargar aplicación

- Abrir **Gate Developer**.
- Ir a **File**.
- Seleccionar **Restore Application from File...**.

<p align="center">
  <img width="300" alt="./images/readme-01.png" src="./images/readme-01.png"/>
</p>

- Seleccionar el archivo **appgate.gapp**
    - El archivo se encuentra en la ruta **/ruta-al-repo/ConectividadNormativa-/gate**
- Dar click en **abrir**.

<p align="center">
  <img height="300" alt="./images/readme-02.png" src="./images/readme-02.png"/>
</p>

- Automaticamente se cargaran todos los recursos necesarios de la aplicacón.

<p align="center">
  <img width="300" alt="./images/readme-03.png" src="./images/readme-03.png"/>
</p>

### Modificar Gazetteer

- Hacer doble click en **Gazetteer Juridicas**.
- Realizar las modificaciones deseadas (añadir listas o añadir elementos a las listas).
- Dar click secundario sobre **Gazetteer Juridicas**
- Seleccionar **Save and Reinitialise**
    - Alternativamente teniendo seleccionado **Gazetteer Juridicas** se puede utilizar el comando **Ctrl-S**

<p align="center">
  <img width="600" alt="./images/readme-04.png" src="./images/readme-04.png"/>
</p>

### Modificar JAPE Transducer

- Realizar los cambios necesarios en el archivo **main.jape**.
    - El archivo se encuentra en la ruta **/ruta-al-repo/ConectividadNormativa-/gate/JAPE**
- Hacer doble click en **JAPE Transducer**.
- Dar click secundario sobre **JAPE Transducer**
- Seleccionar **Reinitialise**

<p align="center">
  <img width="500" alt="./images/readme-05.png" src="./images/readme-05.png"/>
</p>

### Guardar cambios en documentos

#### Documentos nuevos

- Dar click secundario sobre el documento.
- Seleccionar **Save to Datastore...**.

<p align="center">
  <img width="300" alt="./images/readme-06.png" src="./images/readme-06.png"/>
</p>

- Seleccionar el **Datastore** deseado.
- Para este caso solo existe **appgate** pero pueden crear más.

<p align="center">
  <img width="300" alt="./images/readme-07.png" src="./images/readme-07.png"/>
</p>

#### Documentos existentes

- Dar click secundario sobre el documento.
- Seleccionar **Save to its Datastore...**.

<p align="center">
  <img width="300" alt="./images/readme-08.png" src="./images/readme-08.png"/>
</p>

### Guardar cambios en corpus

- El proceso es el mismo que con los documentos, pero haciendo click en los corpus con los que se quiera trabajar.

### Guardar la aplicación actual

- Dar click secundario sobre la aplicacion.
- Seleccionar **Save Application State...**.

<p align="center">
  <img width="300" alt="./images/readme-09.png" src="./images/readme-09.png"/>
</p>

- Seleccionar el archivo **appgate.gapp**
- Dar click en **Guardar**.

<p align="center">
  <img width="400" alt="./images/readme-10.png" src="./images/readme-10.png"/>
</p>

/*
 Penserbjorne - Sebastian Aguilar
 2017
 FI-IIMAS-IIJ-UNAM
*/

for(var i = 0; i < 7; i++){
  document.getElementById("tab" + i).style.display = "none";
}

document.getElementById("tab0").style.display = "block";

var documentFrame = document.getElementById('documentFrame').contentWindow;

function applyCSS() {
    if(document.getElementById('chkbxCaso').checked){
      documentFrame.applyCSS("case","");
    }else {
      documentFrame.applyCSS("case","nCase");
    }

    if(document.getElementById('chkbxEsctructura').checked){
      documentFrame.applyCSS("actions","");
    }else {
      documentFrame.applyCSS("actions","nActions");
    }

    if(document.getElementById('chkbxFechaSentencia').checked){
      documentFrame.applyCSS("datesentence","");
    }else {
      documentFrame.applyCSS("datesentence","nDateSentence");
    }

    if(document.getElementById('chkbxMiembros').checked){
      documentFrame.applyCSS("personcourtmembers","");
    }else {
      documentFrame.applyCSS("personcourtmembers","nPersonCourtMembers");
    }

    if(document.getElementById('chkbxFechas').checked){
      documentFrame.applyCSS("date2","");
    }else {
      documentFrame.applyCSS("date2","nDate2");
    }

    if(document.getElementById('chkbxArticulos').checked){
      documentFrame.applyCSS("articles","");
    }else {
      documentFrame.applyCSS("articles","nArticles");
    }

    if(document.getElementById('chkbxPuntosResolutivos').checked){
      documentFrame.applyCSS("resolutivepoints","");
    }else {
      documentFrame.applyCSS("resolutivepoints","nResolutivePoints");
    }

    if(document.getElementById('chkbxConectores').checked){
      documentFrame.applyCSS("conectores","");
    }else {
      documentFrame.applyCSS("conectores","nConectores");
    }
}

function isActiveTab(me, tab){
  var tabs = document.getElementById("meTab").getElementsByTagName("LI");
  for(var i = 0; i < tabs.length; i++){
    tabs[i].className = "";
    document.getElementById("tab" + i).style.display = "none";
  }

  me.className = 'is-active';
  tab.style.display = "block";

  /*<li onclick="isActiveTab(this, tab3)"><a>Participantes</a></li>
  <li onclick="isActiveTab(this, tab4)"><a>Leyes y artículos</a></li>
  <li onclick="isActiveTab(this, tab5)"><a>Países</a></li>
  <li onclick="isActiveTab(this, tab6)"><a>Fechas</a></li>*/
  if (tab.id == "tab3") {
    fillTab("personcourtmembers", "titleParticipantes", "divParticipantes");
  } else if (tab.id == "tab4") {
    fillTab("articles", "titleArticulos", "divArticulos");
  } else if (tab.id == "tab5") {
    fillTab("country", "titlePaises", "divPaises");
  } else if (tab.id == "tab6") {
    fillTab("date2", "titleFechas", "divFechas");
  }
}

function fillTab(content, title, div){
  var contenido = documentFrame.getSomething(content)
  document.getElementById(title).innerHTML = contenido.length;
  var divContenido = document.getElementById(div);
  divContenido.innerHTML = ""
  for(var i = 0; i < contenido.length; i++){
    var tempDiv = document.createElement("DIV");
    tempDiv.className = "column";
    tempDiv.innerHTML = contenido[i].innerHTML;
    divContenido.appendChild(tempDiv);
  }
}

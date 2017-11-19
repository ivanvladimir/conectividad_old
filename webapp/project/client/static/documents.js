/*
 Penserbjorne - Sebastian Aguilar
 2017
 FI-IIMAS-IIJ-UNAM
*/

for(var i = 2; i < 5; i++){
  document.getElementById("tab" + i).style.display = "none";
}

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
    document.getElementById("tab" + (i+1)).style.display = "none";
  }
  me.className = 'is-active';
  tab.style.display = "block";
}

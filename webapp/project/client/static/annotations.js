/*
 Penserbjorne - Sebastian Aguilar
 2017
 FI-IIMAS-IIJ-UNAM
*/

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

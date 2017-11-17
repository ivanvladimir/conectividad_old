/*
 Penserbjorne - Sebastian Aguilar
 2017
 FI-IIMAS-IIJ-UNAM
*/

function applyCSS(tagName, estilo) {
    var list = document.getElementsByTagName(tagName);
    for (var i = 0; i < list.length; i++) {
      list[i].className = estilo;
    }
}

/*
 Penserbjorne - Sebastian Aguilar
 2017
 FI-IIMAS-IIJ-UNAM
*/

for(var i = 0; i < 7; i++){
  document.getElementById("tab" + i).style.display = "none";
}

document.getElementById("tab0").style.display = "block";

function changeCSS(element_id,doc,nDoc) {
    if(document.getElementById(element_id).checked){
      applyCSS(doc,"");
    }else {
      applyCSS(doc,nDoc);
    }
}


function something_click(event){
	el=event.srcElement;
	info=document.getElementById("info-tag");
	console.log(event);
	if(["articlemention","documentmention","definition","institutionmention"].indexOf(el.tagName.toLowerCase())>=0){
		for (var i = 0; i < el.attributes.length; i++) {
			var attrib = el.attributes[i];
			if (attrib.specified) {
				console.log(attrib.name + " = " + attrib.value);
				info.textContent+=attrib.name+":"+attrib.value;
			}
		}

	}else{
		info.textContent="";
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
  var contenido = documentFrame.getSomething(content);
  document.getElementById(title).innerHTML = contenido.length;
  var divContenido = document.getElementById(div);
  divContenido.innerHTML = ""
  for(var i = 0; i < contenido.length; i++){
    var tempDiv = document.createElement("li");
    tempDiv.className = "";
    tempDiv.innerHTML = contenido[i].innerHTML;
    divContenido.appendChild(tempDiv);
  }
}

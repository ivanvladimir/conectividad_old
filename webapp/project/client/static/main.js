// custom javascript

$( document ).ready(function() {
  console.log('Sanity Check!');
});

function myFilterLaw() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("myFilterLaw");
  filter = input.value.toUpperCase();
  table = document.getElementById("lawsTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[0];
    td2 = tr[i].getElementsByTagName("td")[1];
    td3 = tr[i].getElementsByTagName("td")[2];
    if (td1 || td2 || td3) {
      if (td1.innerHTML.toUpperCase().indexOf(filter) > -1
		  || td2.innerHTML.toUpperCase().indexOf(filter) > -1
		  || td3.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function showInfoPageGrafo(){
	document.getElementById("myModalGrafo").classList.add('is-active');
}

function closeInfoPageGrafo(){
	document.getElementById("myModalGrafo").classList.remove('is-active');
}

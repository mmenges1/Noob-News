// Code retrieved from: https://codepen.io/anon/pen/aMBjYb?page=3
filterSelection("all") //show all columns at start
function filterSelection(nameToFilterBy) {
  var columnLength;
  var i;
  columnLength = document.getElementsByClassName("column2");
  if (nameToFilterBy == "all") nameToFilterBy = "";
  for (i = 0; i < columnLength.length; i++) {
    //remove "show" class from the elements that are not selected
    RemoveClass(columnLength[i], "show2");
    //Add "show" class to the filtered elements
    if (columnLength[i].className.indexOf(nameToFilterBy) > -1) AddClass(columnLength[i], "show2");
  }
}

// Show filtered elements
function AddClass(element, name) {
  var i;
  var array1;
  var array2;
  array1 = element.className.split(" ");
  array2 = name.split(" ");
  for (i = 0; i < array2.length; i++) {
    if (array1.indexOf(array2[i]) == -1) {
      element.className += " " + array2[i];
    }
  }
}

// Hide elements that are not selected
function RemoveClass(element, name) {
  var i;
  var array1;
  var array2;
  array1 = element.className.split(" ");
  array2 = name.split(" ");
  for (i = 0; i < array2.length; i++) {
    while (array1.indexOf(array2[i]) > -1) {
      array1.splice(array1.indexOf(array2[i]), 1);
    }
  }
  element.className = array1.join(" ");
}
// Code retrieved from: https://codepen.io/anon/pen/aMBjYb?page=3

//var elem = document.querySelector('.sidenav');
//var instance = M.Sidenav.init(elem, options);

// Initialize collapsible (uncomment the lines below if you use the dropdown variation)
// var collapsibleElem = document.querySelector('.collapsible');
// var collapsibleInstance = M.Collapsible.init(collapsibleElem, options);

// Or with jQuery

$(document).ready(function(){
  $('.sidenav').sidenav();
  M.updateTextFields();
  $('textarea#desc').characterCounter();
  $('select').formSelect();
});
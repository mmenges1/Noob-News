$(document).ready(function() {
  // JQuery code to be added in here.
  $("#about-btn").click( function(event) {
    alert("You clicked the button using JQuery!");
  });
});

$('button').click(function(){
  $('button').toggleClass('active');
  $('.title').toggleClass('active');
  $('nav').toggleClass('active');
});

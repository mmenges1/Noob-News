$(document).ready(function() {
  // JQuery code to be added in here.
  $("#about-btn").click( function(event) {
    alert("You clicked the button using JQuery!");
  });
});

$(document.getElementById("button1")).click(function(){
  $((document.getElementById("button1")).toggleClass('active'));
  $('.title').toggleClass('active');
  $('nav').toggleClass('active');
});

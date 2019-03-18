$('#suggestion').keyup(function(){
  var query;

query = $(this).val();

$.get('/noobnews/suggest/', {suggestion: query}, function(data){

    $('#cats').html(data);
  });

});

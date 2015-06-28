window.loadCharacterBar = (url) ->

  $.get url, (data) ->
   # console.log data
    $('#dumping-ground').html(data).animate({'width': '400px', 'padding': '14px', 'opacity': 1})
   

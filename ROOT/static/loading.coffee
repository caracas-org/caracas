window.loadCharacterBar = (url) ->

  $.get url, (data) ->
   # console.log data
    $('#dumping-ground').replaceWith(data).animate({'width': '400px', 'padding': '14px'})
   

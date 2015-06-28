window.loadCharacterBar = (url) ->

  $.get url, (data) ->
   # console.log data
    $('#dumping-ground').replaceWith(data)
   

markers = {}

addMarker = (achievement) ->
  lat = achievement.achievement_lat
  lon = achievement.achievement_lon
  latLng = [lat, lon]
  idx = "i#{lat}|#{lon}"
  if markers.hasOwnProperty idx
    return
  markers[idx] = true
  L.marker(latLng).addTo(map)

setAllMarker = () ->
  bounds = map.getBounds()
  swla = bounds._southWest.lat
  swlo = bounds._southWest.lng
  nela = bounds._northEast.lat
  nelo = bounds._northEast.lng

  lad = nela - swla
  lod = nelo - swlo

  lat = (swla + nela) / 2
  lon = (swlo + nelo) / 2

  delta = Math.max lad, lod
  delta *= 1.5

  url = "/a/api/get/?format=json&lat=#{lat}&lon=#{lon}&box_radius=#{delta}"
  console.log 'moveend', map.getBounds()
  console.log url


  $.getJSON url, (data) ->
   # console.log data
   addMarker achievement for achievement in data.achievements

  return

map.on 'moveend', setAllMarker

setAllMarker()

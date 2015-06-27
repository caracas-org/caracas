map.on 'moveend', (e) ->
  bounds = map.getBounds()
  swla = bounds._southWest.lat
  swlo = bounds._southWest.lng
  nela = bounds._northEast.lat
  nelo = bounds._northEast.lng

  lad = nela - swla
  lod = nelo - swlo


  console.log swla, swlo, nela, nelo
  console.log swla - lad, swlo - lod, nela + lad, nelo + lod
  console.log 'moveend', map.getBounds()
  return

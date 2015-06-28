markers = {}
icons = {}

ourIcon = L.Icon.extend(options:
  # shadowUrl: 'leaf-shadow.png'
  iconSize: [64, 64 ]
  shadowSize: [0, 0 ]
  iconAnchor: [32, 64 ]
  shadowAnchor: [0, 0 ]
  popupAnchor: [-3, -76 ])

# var greenIcon = new LeafIcon({iconUrl: 'leaf-green.png'}),
    # redIcon = new LeafIcon({iconUrl: 'leaf-red.png'}),
    # orangeIcon = new LeafIcon({iconUrl: 'leaf-orange.png'});

addMarker = (achievement) ->
  lat = achievement.achievement_lat
  lon = achievement.achievement_lon
  latLng = [lat, lon]
  idx = "i#{lat}|#{lon}"
  if markers.hasOwnProperty idx
    return
  console.log achievement
  icon_url = achievement.achievement_image
  if icon_url != ""

    if icons.hasOwnProperty icon_url
      icon = icons[icon_url]
    else
      icon = new ourIcon({iconUrl: icon_url})
      icons[icon_url] = icon
    markers[idx] = true
    # { achievement_lon: 6.7681
    #  achievement_name: "Hans Wurst"
    #  achievement_lat: 51.2457
    #  achievement_description: "Hoho"
    #  achievement_max_progress: 1
    #  achievement_id: 1
    #  achievement_image: "/media/snowboard.png" } 
    popup_text = "<h4>#{achievement.achievement_name}</h4><p>#{achievement.achievement_description}</p><p><a href=\"\#\" onclick='$.achievement_unlocked(#{achievement.achievement_id}, #{user_id}, \"team_caracas\");'>I did this allready</a></p>"
    L.marker(latLng, {icon: icon}).bindPopup(popup_text).addTo(map)
  else
    L.marker(latLng).bindPopup(popup_text).addTo(map)

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

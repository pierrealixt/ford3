const setupMap = (location_x, location_y) => {
  let map_container = document.getElementById('address_map')
  map_container.innerHTML = ''
  let current_location = [location_x, location_y]
  // This code is adapted from the fiddle demo for: https://github.com/jonataswalker/ol-geocoder
  let olsource = new ol.source.OSM()
  let olview = new ol.View({
    center: [0, 0],
    zoom: 5
  })

  console.log(current_location)
  if (location_x.length === 0 && location_y.length === 0) {
    olview.setCenter([2753529.9913838077, -3460334.186405535])
  } else {
    olview.setCenter(current_location)
  }

  let baseLayer = new ol.layer.Tile({ source: olsource })

  let map = new ol.Map({

    target: map_container,
    view: olview,
    layers: [baseLayer]
  })
  // popup
  let popup = new ol.Overlay.Popup()
  map.addOverlay(popup)
  addMarker(map, current_location)
  // Instantiate with some options and add the Control
  let geocoder = new Geocoder('nominatim', {
    provider: 'osm',
    lang: 'en',
    placeholder: 'Search for ...',
    limit: 5,
    debug: true,
    autoComplete: true,
    keepOpen: false
  })
  map.addControl(geocoder)
  // Listen when an address is chosen
  geocoder.on('addresschosen', function (evt) {
    setupMap(evt.coordinate[0], evt.coordinate[1])
    setAddress(evt)
  })
  // olview.animate({
  //   center: current_location,
  //   duration: 2000
  // })

  map.on('singleclick', function (evt) {
    setLocation(evt)
    addMarker(map, evt.coordinate)
  })
}

const marker = null
const markerVectorLayer = null
const vectorSource = null

const addMarker = (map, current_location) => {
  if (this.markerVectorLayer) {
    this.vectorSource.clear()
  }
  // Location 0, 0 indicates no location has been saved
  if (!((current_location[0] == 0) && (current_location[1] == 0))) {
    this.marker = new ol.Feature({
      geometry: new ol.geom.Point(current_location)
    })
    this.vectorSource = new ol.source.Vector({
      features: [this.marker]
    })
    this.markerVectorLayer = new ol.layer.Vector({
      source: this.vectorSource,
      style: new ol.style.Style({
        image: new ol.style.Circle({
          radius: 7,
          fill: new ol.style.Fill({
            color: '#F99824'
          })
        })
      })
    })
    map.addLayer(this.markerVectorLayer)
  }
}

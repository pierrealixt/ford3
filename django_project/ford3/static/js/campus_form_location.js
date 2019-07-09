
$(document).ready(function () {
  let locationX = document.querySelector('#id_campus-location-location_value_x').value || 0
  let locationY = document.querySelector('#id_campus-location-location_value_y').value || 0
  setupMap(locationX, locationY)
})

const setAddress = (evt) => {
  let input_line_1 = document.querySelector('#id_campus-location-physical_address_line_1')
  let input_line_2 = document.querySelector('#id_campus-location-physical_address_line_2')
  let input_city = document.querySelector('#id_campus-location-physical_address_city')
  let input_code = document.querySelector('#id_campus-location-physical_address_postal_code')
  let hidden_location_x = document.querySelector('#id_campus-location-location_value_x')
  let hidden_location_y = document.querySelector('#id_campus-location-location_value_y')
  let address_details = evt['address']['details']
  let original_details = evt['address']['original']['details']

  let city = address_details['city']
  let line1 = address_details['houseNumber'] + ' ' + address_details['road']
  let line2 = original_details['suburb']
  let post_code = address_details['postcode']
  let coord_x = evt['coordinate'][0]
  let coord_y = evt['coordinate'][1]

  input_line_1.value = line1
  input_line_2.value = line2
  input_city.value = city
  input_code.value = post_code
  hidden_location_x.value = coord_x
  hidden_location_y.value = coord_y
}

const setLocation = (evt) => {
  let coord_x = evt['coordinate'][0]
  let coord_y = evt['coordinate'][1]

  let hidden_location_x = document.querySelector('#id_campus-location-location_value_x')
  let hidden_location_y = document.querySelector('#id_campus-location-location_value_y')

  hidden_location_x.value = coord_x
  hidden_location_y.value = coord_y
}

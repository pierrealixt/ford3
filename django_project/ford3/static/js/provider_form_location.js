
$(document).ready(function () {
  let locationX = document.querySelector('#id_location_value_x').value || 0
  let locationY = document.querySelector('#id_location_value_y').value || 0
  setupMap(locationX, locationY)
})

const setAddress = (evt) => {
  let inputLine1 = document.querySelector('#id_physical_address_line_1')
  let inputLine2 = document.querySelector('#id_physical_address_line_2')
  let inputCity = document.querySelector('#id_physical_address_city')
  let inputCode = document.querySelector('#id_physical_address_postal_code')
  let hiddenLocationX = document.querySelector('#id_location_value_x')
  let hiddenLocationY = document.querySelector('#id_location_value_y')
  let addressDetails = evt.address.details
  let originalDetails = evt.address.original.details

  let city = addressDetails.city
  let line1 = addressDetails.houseNumber + ' ' + addressDetails.road
  let line2 = originalDetails.suburb
  let postCode = addressDetails.postcode
  let coordX = evt['coordinate'][0]
  let coordY = evt['coordinate'][1]

  inputLine1.value = line1
  inputLine2.value = line2
  inputCity.value = city
  inputCode.value = postCode
  hiddenLocationX.value = coordX
  hiddenLocationY.value = coordY
}

const setLocation = (evt) => {
  document.querySelector('#id_location_value_x').value = evt.coordinate[0]
  document.querySelector('#id_location_value_y').value = evt.coordinate[1]
}

$(document).ready(function () {
  disablePostalAddress()
})

$('#id_postal_address_differs').click(function (e) {
  setPostalAddressEnabled()
})

function setPostalAddressEnabled () {
  let postal_address_does_differ = document.getElementById('id_postal_address_differs').checked
  let postal_address_container = document.getElementById('postal_address_container')

  if (postal_address_does_differ) {
    postal_address_container.style.pointerEvents = 'unset'
    postal_address_container.style.opacity = '1'
    $(':input', '#postal_address_container').each(function () {
      this.required = true
    })
  } else {
    disablePostalAddress()
  }
}

function disablePostalAddress () {
  let postal_address_does_differ = document.getElementById('id_postal_address_differs').checked
  let postal_address_container = document.getElementById('postal_address_container')

  if (postal_address_does_differ) {
    setPostalAddressEnabled()
  } else {
    postal_address_container.style.pointerEvents = 'none'
    postal_address_container.style.opacity = '0.4'
    $(':input', '#postal_address_container').each(function () {
      this.required = false
    })
  }
}

$(document).ready(function () {
  innitiateRemoveCampusButtons()
  disablePostalAddress()
})

function innitiateRemoveCampusButtons () {
  $('.remove-campus-button').click(function () {
    if ($('.campus_name').length < 1) {
      alert('At least one campus should be filled')
      return false
    }
    this_button_parrent_parent = $(this).parent().parent()
    this_button_parrent_parent.remove()
  })
}

$(document).on('submit', 'form', function (e) {
  campus_name_elements = $('.campus_name').elements
  return true
})

$('#add-campus-name').click(
  function () {
    addCampusNameInput()
    innitiateRemoveCampusButtons()
  }
)

function addCampusNameInput () {
  var campus_container = $('#campus-names-input-wrapper')
  var result_html = ('<div>' +
            '<div class="row my-3 campus-name-fade-in">' +
                '<div class="col-md-4"><label>' +
                    'Campus Name ' +
                '</label></div>' +
                '<div class="col-md-7">' +
                    '<input name="campus_name" required class="campus_name" ' +
                    'type="text" placeholder="•••••••••••••••••"/>' +
                '</div>' +
                '<div class="col-md-1">' +
                    '<div class="remove-campus-button">' +
                    '<div class="remove-campus-button-inner ">X</div></div>' +
                '</div>' +
            '</div></div>')
  let new_input = $.parseHTML(result_html)
  campus_container.append(new_input)
}

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
  let postal_address_container = document.getElementById('postal_address_container')
  postal_address_container.style.pointerEvents = 'none'
  postal_address_container.style.opacity = '0.4'
  $(':input', '#postal_address_container').each(function () {
    this.required = false
  })
}

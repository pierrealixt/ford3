
const getNewEvent = () => {
  return document.getElementById('new-event')
}

const getNewEventExample = () => {
  return document.getElementById('new-event-example')
}

const getAddEventButton = () => {
  return document.querySelector('button[data-action="add-event"]')
}

const getCreateEventButton = () => {
  return getNewEvent().querySelector('button[data-action="create-event"]')
}

const getCancelCreateEventButton = () => {
  return getNewEvent().querySelector('button[data-action="cancel-create-event"]')
}

const getEditEventButton = () => {
  return document.querySelector('button[data-action="edit-event"]')
}

const getUpdateEventButton = () => {
  return document.querySelector('button[data-action="update-event"]')
}

const getCancelUpdateEventButton = () => {
  return document.querySelector('button[data-action="cancel-update-event"]')
}

const getCreateEventUrl = () => {
  return document.getElementById('create-campus-event-url').value
}

const getEventFieldElem = (event, field) => {
  return event.querySelector(`input[name="${field}"]`)
}

const getEventFieldValue = (event, field) => {
  const fieldElem = getEventFieldElem(event, field)
  if (fieldElem.required) {
    if (fieldElem.value.length > 0) { return fieldElem.value } else { return false }
  } else {
    return fieldElem.value
  }
}

const getEventInputElements = (eventElement) => {
  return eventElement.querySelectorAll('input')
}

const displayNewEvent = () => {
  const newEventExample = getNewEventExample()
  const newEvent = newEventExample.cloneNode(true)
  newEvent.id = 'new-event'
  newEvent.classList.remove('d-none')
  newEventExample.parentNode.appendChild(newEvent)
  return newEvent
}

const fetchEventData = (eventElement) => {
  return {
    name: getEventFieldValue(eventElement, 'name'),
    date_start: getEventFieldValue(eventElement, 'date_start'),
    date_end: getEventFieldValue(eventElement, 'date_end'),
    http_link: getEventFieldValue(eventElement, 'http_link')
  }
}

const showError = (key, eventElement) => {
  const elem = getEventFieldElem(eventElement, key)
  elem.classList.add('input-invalid')
}

const hideError = (key, eventElement) => {
  const elem = getEventFieldElem(eventElement, key)
  elem.classList.remove('input-invalid')
}

const hideButton = (button) => {
  button.classList.add('d-none')
}

const showButton = (button) => {
  button.classList.remove('d-none')
}

const toggleInputsDisability = (inputs) => {
  inputs.forEach((input) => {
    input.disabled = !input.disabled
  })
}

const validateEvent = (eventData, eventElement) => {
  let formValid = true

  Object.keys(eventData).forEach((key) => {
    const value = eventData[key]
    if (value === false) {
      formValid = false
      showError(key, eventElement)
    } else {
      hideError(key, eventElement)
    }
  })
  return formValid
}

const ajaxCreateNewEvent = (event) => {
  console.log('ajaxCreateNewEvent')
  return
  const url = `${getCreateEventUrl()}`
  const request = new XMLHttpRequest()
  request.open('POST', url, true)

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
    }
  }

  request.send()
}

const ajaxUpdateEvent = (event) => {
  console.log('ajaxUpdateEvent')
  console.log(event)
}

const setFocusToInput = (inputElement) => {
  inputElement.focus()
}

const setClickEventToAddButton = () => {
  getAddEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()
    const eventElement = displayNewEvent()

    const inputs = getEventInputElements(eventElement)
    setFocusToInput(inputs[0])
    setDatepicker()

    hideButton(getAddEventButton())

    console.log('am i here')

    showButton(getCreateEventButton())
    showButton(getCancelCreateEventButton())

    setClickEventToCreateButton()
    setClickEventToCancelCreateButton()
  })
}

const setClickEventToCreateButton = () => {
  getCreateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()

    const eventElement = getNewEvent()
    const eventData = fetchEventData(eventElement)
    if (validateEvent(eventData, eventElement)) {
      ajaxCreateNewEvent(eventData)
    }
  })
}

const setClickEventToCancelCreateButton = () => {
  getCancelCreateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()

    hideButton(getCreateEventButton())
    hideButton(getCancelCreateEventButton())
    showButton(getAddEventButton())
    const eventElement = evt.target.parentNode
    eventElement.parentNode.removeChild(eventElement)
  })
}

const setClickEventToEditButton = () => {
  getEditEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()
    const eventElement = evt.target.parentNode
    const inputs = getEventInputElements(eventElement)

    toggleInputsDisability(inputs)

    setDatepicker()
    hideButton(getEditEventButton())
    showButton(getUpdateEventButton())
    showButton(getCancelUpdateEventButton())

    setFocusToInput(inputs[0])
    setClickEventToUpdateButton()
    setClickEventToCancelUpdateButton()
  })
}

const setClickEventToCancelUpdateButton = () => {
  getCancelUpdateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()
    const eventElement = evt.target.parentNode
    const inputs = getEventInputElements(eventElement)

    toggleInputsDisability(inputs)

    showButton(getEditEventButton())

    hideButton(getUpdateEventButton())
    hideButton(getCancelUpdateEventButton())
  })
}
const setClickEventToUpdateButton = () => {
  getUpdateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()
    const eventElement = evt.target.parentNode
    const event = fetchEventData(eventElement)

    if (validateEvent(event, eventElement)) {
      event['id'] = eventElement.dataset['eventId']
      ajaxUpdateEvent(event)
    }
  })
}

const setDatepicker = () => {
  $('.mydatepicker').datepicker()
}

const setupEvents = () => {
  setClickEventToAddButton()
  setClickEventToEditButton()
}

(function () {
  setupEvents()
})()

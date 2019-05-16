
const getNewEvent = () => {
  return document.getElementById('new-event')
}

const getNewEventExample = () => {
  return document.getElementById('new-event-example')
}

const getEvents = () => {
  return document.querySelectorAll('.event')
}

const getEventsList = () => {
  return document.getElementById('events-list')
}

const getEventExample = () => {
  return document.getElementById('event-example')
}

const getCreateEventButton = () => {
  return getNewEvent().querySelector('button[data-action="create-event"]')
}

const getEditEventButtons = () => {
  return document.querySelectorAll('button[data-action="edit-event"]')
}

const getEditEventButton = (elem) => {
  return elem.querySelector('button[data-action="edit-event"]')
}

const getUpdateEventButton = (elem) => {
  console.log(elem)
  return elem.querySelector('button[data-action="update-event"]')
}

const getCreateOrUpdateEventUrl = () => {
  return document.getElementById('create-or-update-campus-event-url').value
}

const getEventFieldElem = (event, field) => {
  return event.querySelector(`input[name="${field}"]`)
}

const getFormErrorAlertElem = (elem) => {
  return elem.querySelector('div[data-role="new-event-form-error"]')
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

const getCSRFTokenFromCookies = () => {
  let csrfToken

  document.cookie.split(';').forEach((cookie) => {
    const csrfRegex = RegExp('csrftoken')
    if (csrfRegex.test(cookie.trim())) {
      csrfToken = cookie.trim().split('=')[1]
    }
  })

  return csrfToken
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

const hideElement = (element) => {
  element.classList.add('d-none')
}

const showElement = (element) => {
  element.classList.remove('d-none')
}

const toggleInputsDisability = (inputs) => {
  inputs.forEach((input) => {
    input.disabled = !input.disabled
  })
}

const resetInputs = (inputs) => {
  inputs.forEach((input) => {
    input.value = ''
  })
}

const populateInputs = (inputs, data) => {
  inputs.forEach((input) => {
    const key = input.name
    const value = data[key]
    input.value = value
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

const insertEvent = (eventData) => {
  const eventExample = getEventExample()
  const eventElement = eventExample.cloneNode(true)

  const firstNode = getEventsList().querySelectorAll('div')[0]
  getEventsList().insertBefore(eventElement, firstNode)

  return eventElement
}

const resetForm = () => {
  const formEventElement = getNewEvent()
  const formInputs = getEventInputElements(formEventElement)
  resetInputs(formInputs)
}

const eventToPostData = (event) => {
  let data = []
  Object.keys(event).forEach((key) => {
    data.push(`${key}=${event[key]}`)
  })
  return data.join('&')
}

const ajaxCreateEvent = (event) => {
  const data = eventToPostData(event)

  const url = `${getCreateOrUpdateEventUrl()}`
  const request = new XMLHttpRequest()
  request.open('POST', url, true)
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
  request.setRequestHeader('X-CSRFToken', getCSRFTokenFromCookies())

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      const data = JSON.parse(request.responseText)
      if (data.success) {
        hideElement(getFormErrorAlertElem())
        // showElement(getFormSuccessAlertElem())

        const eventData = data.campus_event
        const eventElement = insertEvent(eventData)

        const inputs = getEventInputElements(eventElement)
        populateInputs(inputs, eventData)
        eventElement.dataset['eventId'] = eventData.id

        showElement(eventElement)

        resetForm()
      } else {
        const alert = getFormErrorAlertElem()
        alert.innerHTML = data.error_msg
        showElement(alert)
      }
    }
  }

  request.send(data)
}

const ajaxUpdateEvent = (event, eventElement) => {
  const data = eventToPostData(event)

  const url = `${getCreateOrUpdateEventUrl()}`
  const request = new XMLHttpRequest()
  request.open('POST', url, true)
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
  request.setRequestHeader('X-CSRFToken', getCSRFTokenFromCookies())

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      const data = JSON.parse(request.responseText)
      if (data.success) {
        hideElement(getFormErrorAlertElem(eventElement))
        // showElement(getFormSuccessAlertElem())

        const eventData = data.campus_event
        // const eventElement = insertEvent(eventData)

        const inputs = getEventInputElements(eventElement)
        populateInputs(inputs, eventData)
        toggleInputsDisability(inputs)
        // eventElement.dataset['eventId'] = eventData.id

        // showElement(eventElement)

        // resetForm()

        showElement(getEditEventButton(eventElement))
        hideElement(getUpdateEventButton(eventElement))
      } else {
        const alert = getFormErrorAlertElem(eventElement)
        alert.innerHTML = data.error_msg
        showElement(alert)
      }
    }
  }

  request.send(data)
}

const setFocusToInput = (inputElement) => {
  inputElement.focus()
}

const setClickEventToCreateButton = () => {
  getCreateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()

    const eventElement = getNewEvent()
    const eventData = fetchEventData(eventElement)
    if (validateEvent(eventData, eventElement)) {
      ajaxCreateEvent(eventData)
    }
  })
}

const setClickEventToEditButton = () => {
  console.log(getEditEventButtons().length)

  getEditEventButtons().forEach((button) => {
    button.addEventListener('click', function (evt) {
      evt.preventDefault()
      const eventElement = evt.target.parentNode
      const inputs = getEventInputElements(eventElement)

      toggleInputsDisability(inputs)

      setDatepicker()
      hideElement(button)
      showElement(getUpdateEventButton(eventElement))

      setFocusToInput(inputs[0])
      setClickEventToUpdateButton(eventElement)
    })
  })
}

const setClickEventToUpdateButton = (eventElement) => {
  getUpdateEventButton(eventElement).addEventListener('click', function (evt) {
    evt.preventDefault()
    const event = fetchEventData(eventElement)

    if (validateEvent(event, eventElement)) {
      event['id'] = eventElement.dataset['eventId']
      ajaxUpdateEvent(event, eventElement)
    }
  })
}

const setDatepicker = () => {
  $('.mydatepicker').datepicker({ dateFormat: 'yy-mm-dd' })
}

const setupEvents = () => {
  setClickEventToCreateButton()
  setDatepicker()
  if (getEvents().length > 0) { setClickEventToEditButton() }
}

(function () {
  setupEvents()
})()

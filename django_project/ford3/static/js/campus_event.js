
const getFormEvent = () => {
  return document.getElementById('form-event')
}

const getEvents = () => {
  return document.querySelectorAll('.event')
}

const getEventsList = () => {
  return document.querySelector('#events-list ul')
}

const getEventExample = () => {
  return document.querySelector('#events-list li.event-example')
}

const getCreateEventButton = () => {
  return getFormEvent().querySelector('button[data-action="create-event"]')
}

const getEditEventButtons = () => {
  return document.querySelectorAll('button[data-action="edit-event"]')
}

const getUpdateEventButton = () => {
  return getFormEvent().querySelector('button[data-action="update-event"]')
}

const getCreateOrUpdateEventUrl = () => {
  return document.getElementById('create-or-update-campus-event-url').value
}

const getEventFieldElem = (event, field) => {
  return event.querySelector(`input[name="${field}"]`)
}

const getFormErrorAlertElem = () => {
  return document.querySelector('div[data-role="new-event-form-error"]')
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

const findEvent = (eventId) => {
  return document.querySelector(`li[data-event-id="${eventId}"]`)
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

const reloadEvent = (eventData) => {
  const oldEvent = findEvent(eventData.id)

  const eventExample = getEventExample()
  const event = eventExample.cloneNode(true)

  populateEvent(event, eventData)
  showElement(event)

  getEventsList().insertBefore(event, oldEvent)

  oldEvent.parentNode.removeChild(oldEvent)
}

const insertEvent = (eventData) => {
  const eventExample = getEventExample()
  const eventElement = eventExample.cloneNode(true)

  const firstNode = getEventsList().querySelectorAll('li')[0]
  getEventsList().insertBefore(eventElement, firstNode)

  return eventElement
}

const populateEvent = (eventElement, eventData) => {
  eventElement.dataset['eventId'] = eventData.id

  eventElement.querySelectorAll('span').forEach((span) => {
    const role = span.dataset['role']
    let value = eventData[role]

    if (role === 'http_link') {
      let a = span.querySelector('a')
      a.href = value
      a.innerHTML = value
    } else {
      span.innerHTML = value
    }
  })
}

const resetForm = () => {
  const formElement = getFormEvent()
  const formInputs = getEventInputElements(formElement)
  resetInputs(formInputs)
}

const eventToPostData = (event) => {
  let data = []
  Object.keys(event).forEach((key) => {
    data.push(`${key}=${event[key]}`)
  })
  return data.join('&')
}

const setFocusToInput = (inputElement) => {
  inputElement.focus()
}

const getEventData = (eventElement) => {
  let eventData = {}
  eventElement.querySelectorAll('span').forEach((span) => {
    const role = span.dataset['role']
    let value = span.innerHTML
    if (role === 'http_link') {
      value = span.querySelector('a').innerHTML
    }

    eventData[role] = value
  })

  return eventData
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

        populateEvent(eventElement, eventData)
        showElement(eventElement)

        resetForm()

        setClickToEditButtons()
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
        const eventData = data.campus_event
        resetForm()

        reloadEvent(eventData)

        hideElement(getFormErrorAlertElem())
        hideElement(getUpdateEventButton())
        showElement(getCreateEventButton())

        setClickToEditButtons()
      } else {
        const alert = getFormErrorAlertElem()
        alert.innerHTML = data.error_msg
        showElement(alert)
      }
    }
  }

  request.send(data)
}

const setClickToCreateButton = () => {
  getCreateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()

    const eventElement = getFormEvent()
    const eventData = fetchEventData(eventElement)
    if (validateEvent(eventData, eventElement)) {
      ajaxCreateEvent(eventData)
    }
  })
}

const setClickToEditButtons = () => {
  getEditEventButtons().forEach((button) => {
    button.addEventListener('click', function (evt) {
      evt.preventDefault()

      const eventElement = evt.target.parentNode
      const eventData = getEventData(eventElement)

      getFormEvent().dataset['eventId'] = eventElement.dataset['eventId']

      const inputs = getEventInputElements(getFormEvent())
      populateInputs(inputs, eventData)
      setFocusToInput(inputs[0])

      hideElement(getCreateEventButton())
      showElement(getUpdateEventButton())
    })
  })
}

const setClickToUpdateButton = () => {
  getUpdateEventButton().addEventListener('click', function (evt) {
    evt.preventDefault()

    const eventElement = getFormEvent()
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
  setClickToCreateButton()
  setClickToUpdateButton()
  setDatepicker()
  if (getEvents().length > 0) { setClickToEditButtons() }
}

(function () {
  setupEvents()
})()

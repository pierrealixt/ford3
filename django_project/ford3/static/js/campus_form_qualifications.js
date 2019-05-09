
const getSaqaQualificationsListElement = () => {
  return document.getElementById('saqa-qualifications-list')
}

const getAddQualificationButtonElement = () => {
  return document.querySelector('button[data-action="add-qualif"]')
}

const getRemoveQualificationButtonElement = () => {
  return document.querySelector('button[data-action="remove-qualif"]')
}

const getClearQualificationsButtonElement = () => {
  return document.querySelector('button[data-action="clear-qualifs"]')
}

const getCreateQualificationButtonElement = () => {
  return document.querySelector('button[data-action="create-qualif"]')
}

const getCreateQualificationInputElement = () => {
  return document.querySelector('input[data-action="create-qualif"]')
}

const getProviderIdInputElement = () => {
  return document.getElementById('provider-id')
}

const getCampusQualificationsListElement = () => {
  return document.getElementById('campus-qualifications-list')
}

const getSelectedQualificationsFromList = (list) => {
  return list.querySelectorAll('li.selected')
}

const getSaqaQualificationsInputElem = () => {
  return document.getElementById('id_campus-qualifications-saqa_ids')
}

const getCreateQualificationFormErrorAlertElement = () => {
  return document.getElementById('create-qualif-form-error-alert')
}

const getSearchFormErrorAlertElement = () => {
  return document.getElementById('search-error-alert')
}

const getCreateQualificationUrl = () => {
  return document.getElementById('create-qualif-url').value
}

const getSearchQualificationsUrl = () => {
  return document.getElementById('search-qualif-url').value
}

const populateForm = (saqaId) => {
  let saqaIds = getSaqaQualificationsInputElem().value.split(' ')
  saqaIds.push(saqaId)
  getSaqaQualificationsInputElem().value = saqaIds.join(' ')
}

const removeSaqaQualification = (saqaId) => {
  let saqaIds = getSaqaQualificationsInputElem().value.split(' ')

  saqaIds = saqaIds.filter(function (value, index, arr) {
    return value !== saqaId
  })

  getSaqaQualificationsInputElem().value = saqaIds.join(' ')
}

const getCampusQualificationText = () => {
  return document.getElementsByClassName('qualif-texts')
}

const findLiElem = (elem) => {
  if (elem.tagName === 'LI') {
    return elem
  } else {
    return findLiElem(elem.parentElement)
  }
}

const setToggleEvent = (elem) => {
  elem.addEventListener('click', function (evt) {
    if (evt.target.tagName !== 'A') {
      const liElem = findLiElem(evt.target)
      liElem.classList.toggle('selected')
    }
  })
}

const setClickEventToLi = () => {
  const qualifElems = document.querySelectorAll('li[data-saqa-id]')
  qualifElems.forEach(function (qualifElem) {
    setToggleEvent(qualifElem)
  })
}

// isEnabled true = disabled add button
const toggleAddButton = (isEnabled) => {
  const addButton = getAddQualificationButtonElement()
  // qualificationText[0]= add button and qualificationText[1]= remove button
  const qualificationText = getCampusQualificationText()
  addButton.disabled = isEnabled
  if (isEnabled) {
    addButton.classList.remove('left-arrow-button')
    addButton.classList.add('left-arrow-grey-button')
    qualificationText[0].classList.add('disabled')
  } else {
    addButton.classList.remove('left-arrow-grey-button')
    addButton.classList.add('left-arrow-button')
    qualificationText[0].classList.remove('disabled')
  }
}

const toggleRemoveButton = (isEnabled) => {
  const removeButton = getRemoveQualificationButtonElement()
  // qualificationText[0]= add button and qualificationText[1]= remove button
  removeButton.disabled = isEnabled
  const qualificationText = getCampusQualificationText()
  if (isEnabled) {
    removeButton.classList.remove('right-arrow-button')
    removeButton.classList.add('right-arrow-grey-button')
    qualificationText[1].classList.add('disabled')
  } else {
    removeButton.classList.add('right-arrow-button')
    removeButton.classList.remove('right-arrow-grey-button')
    qualificationText[1].classList.remove('disabled')
  }
}

const checkSaqaList = () => {
  const saqaList = getSaqaQualificationsListElement()
  if (saqaList.length === 0 || saqaList.getElementsByTagName('li').length < 1) {
    toggleAddButton(true)
  }
}

const checkCampusList = () => {
  const campusList = getCampusQualificationsListElement()
  if (campusList.length === 0 || campusList.getElementsByTagName('li').length < 1) {
    toggleRemoveButton(true)
  }
}

const checkLists = () => {
  checkSaqaList()
  checkCampusList()
}

const appendNodeToCampusQualificationsList = (node) => {
  const firstNode = getCampusQualificationsListElement().querySelectorAll('li')[0]
  getCampusQualificationsListElement().insertBefore(node, firstNode)
}

const setClickEventToAddButton = () => {
  const addQualifButton = getAddQualificationButtonElement()
  addQualifButton.addEventListener('click', function (evt) {
    evt.stopPropagation()

    const saqaQualifListElem = getSaqaQualificationsListElement()
    const selectedQualifElems = getSelectedQualificationsFromList(saqaQualifListElem)

    selectedQualifElems.forEach(function (selectedQualifElem) {
    // remove the selected class attached to the node
      selectedQualifElem.classList.remove('selected')

      // clone the node
      var clonedNode = selectedQualifElem.cloneNode(true)

      // hide the node
      selectedQualifElem.style.display = 'none'

      // append the cloned node to the campus qualifications list

      appendNodeToCampusQualificationsList(clonedNode)

      setToggleEvent(clonedNode)

      let saqaId = selectedQualifElem.dataset['saqaId']
      populateForm(saqaId)
      checkSaqaList()
      toggleRemoveButton(false)
    })
  })
}

const setClickEventToRemoveButton = () => {
  let removeQualifButton = getRemoveQualificationButtonElement()
  removeQualifButton.addEventListener('click', function (evt) {
    evt.stopPropagation()
    const saqaQualifListElem = getSaqaQualificationsListElement()
    const campusQualifListElem = getCampusQualificationsListElement()
    let selectedQualifElems = getSelectedQualificationsFromList(campusQualifListElem)

    selectedQualifElems.forEach(function (selectedQualifElem) {
      let qualifElem = saqaQualifListElem.querySelector('li[data-saqa-id="' + selectedQualifElem.dataset['saqa-id'] + '"]')
      if (qualifElem) { qualifElem.style.display = 'list-item' }

      campusQualifListElem.removeChild(selectedQualifElem)

      let saqaId = selectedQualifElem.dataset['saqaId']
      removeSaqaQualification(saqaId)
      checkCampusList()
    })
  })
}

const setClickEventToClearButton = () => {
  const button = getClearQualificationsButtonElement()
  const input = getSearchQualifInputElem()

  button.addEventListener('click', function (evt) {
    evt.stopPropagation()

    input.value = ''

    const saqaQualifListElem = getSaqaQualificationsListElement()
    saqaQualifListElem.querySelectorAll('li').forEach(function (li) {
      saqaQualifListElem.removeChild(li)
      checkSaqaList()
    })
  })
}
const getSearchQualifInputElem = () => {
  return document.querySelector('input[data-action="search-qualif"]')
}

const buildSaqaQualificationLiContent = (saqa) => {
  let linkText = document.createTextNode(saqa.saqa_id)
  let link = document.createElement('a')
  link.href = 'http://regqs.saqa.org.za/viewQualification.php?id=' + saqa.saqa_id
  link.target = '_blank'
  link.appendChild(linkText)
  return link
}

const buildLiElement = (saqa) => {
  const saqaNodeExample = document.querySelector('.qualif-li-example')
  let saqaNode = saqaNodeExample.cloneNode(true)

  saqaNode.classList.remove('qualif-li-example')
  saqaNode.classList.add('qualif-li')

  saqaNode.setAttribute('data-saqa-id', saqa.id)
  saqaNode.querySelector('.qualif-name').innerHTML = saqa.name
  if (saqa.accredited) {
    saqaNode.querySelector('.qualif-saqa-id').appendChild(buildSaqaQualificationLiContent(saqa))
  }

  saqaNode.classList.remove('d-none')

  return saqaNode
}

const displaySaqaQualificationsResults = (results) => {
  const list = getSaqaQualificationsListElement()
  list.querySelectorAll('li').forEach(function (li) {
    list.removeChild(li)
  })

  if (results.length > 0) {
    const providerId = getProviderIdInputElement().value

    results.forEach(function (saqa) {
      if (saqa.accredited || (!saqa.accredited && saqa.creator_provider_id === parseInt(providerId))) {
        let saqaNode = buildLiElement(saqa)

        list.appendChild(saqaNode)

        setToggleEvent(saqaNode)
      }
    })
  } else {
    getSearchFormErrorAlertElement().classList.remove('d-none')
  }
}

const ajaxSearchQualifications = (query) => {
  const url = `${getSearchQualificationsUrl()}?q=${query}`
  const request = new XMLHttpRequest()
  request.open('GET', url, true)

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      var data = JSON.parse(request.responseText)
      displaySaqaQualificationsResults(data['results'])
      toggleAddButton(false)
    }
  }

  request.onerror = function () {
  // There was a connection error of some sort
  }

  request.send()
}

const setSearchEvent = () => {
  let timeout = null
  const elem = getSearchQualifInputElem()
  elem.onkeyup = function (e) {
    if (e.keyCode === 13) {
      // Cancel the default action, if needed
      e.preventDefault()
      alert('enter pressed')
    }
    getSearchFormErrorAlertElement().classList.add('d-none')
    clearTimeout(timeout)

    timeout = setTimeout(function () {
      if (elem.value.length > 3) { ajaxSearchQualifications(elem.value) }
    }, 842)
  }
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

const ajaxCreateQualification = (data) => {
  const url = getCreateQualificationUrl()
  const request = new XMLHttpRequest()
  request.open('POST', url, true)
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
  request.setRequestHeader('X-CSRFToken', getCSRFTokenFromCookies())

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      const data = JSON.parse(request.responseText)
      if (data.success) {
        const saqaNode = buildLiElement(data.saqa_qualification)

        // add click event to node
        setToggleEvent(saqaNode)

        // append node to the campus qualification list
        appendNodeToCampusQualificationsList(saqaNode)

        // add the saqa id to the input
        populateForm(data.saqa_qualification.id)

        // reset the form
        getCreateQualificationInputElement().value = ''
      } else {
        const alert = getCreateQualificationFormErrorAlertElement()
        alert.innerHTML = data.error
        alert.classList.remove('d-none')
      }
    }
  }

  request.send(data)
}

const createQualification = () => {
  const qualificationName = getCreateQualificationInputElement().value
  const providerId = getProviderIdInputElement().value
  const data = `saqa_qualification_name=${qualificationName}&provider_id=${providerId}`
  ajaxCreateQualification(data)
}

const clearCreateQualificationFormErrors = () => {
  const alert = getCreateQualificationFormErrorAlertElement()
  alert.innerHTML = ''
  alert.classList.add('d-none')
}

const setCreateQualifEvent = () => {
  const button = getCreateQualificationButtonElement()
  button.addEventListener('click', (evt) => {
    clearCreateQualificationFormErrors()
    createQualification()
  })
}

const setupEvents = () => {
  setClickEventToLi()
  setClickEventToAddButton()
  setClickEventToRemoveButton()
  setClickEventToClearButton()
  setSearchEvent()
  setCreateQualifEvent()
}

(function () {
  checkLists()
  setupEvents()
})()

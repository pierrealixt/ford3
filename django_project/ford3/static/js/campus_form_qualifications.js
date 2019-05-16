
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

const getCreateQualificationNameElement = () => {
  return document.querySelector('input[data-role="qualif-name"]')
}

const getCreateQualificationFosElement = () => {
  return document.querySelector('select[data-role="qualif-fos"]')
}

const getCreateQualificationSubFosElement = () => {
  return document.querySelector('select[data-role="qualif-sfos"]')
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

const getListSfosUrl = () => {
  return document.getElementById('list-sfos').value
}

const getListById = (listId) => {
  return document.getElementById(listId)
}

const getArrowWidgetForList = (listId) => {
  if (listId === 'campus-qualifications-list') {
    return document.querySelector('.remove-qualif-widget')
  } else if (listId === 'saqa-qualifications-list') {
    return document.querySelector('.add-qualif-widget')
  }
}

const findLiElem = (elem) => {
  if (elem.tagName === 'LI') {
    return elem
  } else {
    return findLiElem(elem.parentElement)
  }
}

const getSearchQualifInputElem = () => {
  return document.querySelector('input[data-action="search-qualif"]')
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

const toggleArrowWidget = (listId) => {
  const list = getListById(listId)
  const widget = getArrowWidgetForList(listId)
  if (getSelectedQualificationsFromList(list).length > 0) {
    widget.classList.remove('disabled')
  } else {
    widget.classList.add('disabled')
  }
}

const appendNodeToCampusQualificationsList = (node) => {
  const firstNode = getCampusQualificationsListElement().querySelectorAll('li')[0]
  getCampusQualificationsListElement().insertBefore(node, firstNode)
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

const createQualification = () => {
  const qualificationName = getCreateQualificationNameElement().value
  const fosId = getCreateQualificationFosElement().value
  const providerId = getProviderIdInputElement().value
  let data = {
    'saqa_qualification': {
      'name': qualificationName,
      'provider_id': providerId,
      'fos_id': fosId
    }
  }
  const sfosId = getCreateQualificationSubFosElement().value
  if (sfosId) {
    data['saqa_qualification']['sfos_id'] = sfosId
  }
  ajaxCreateQualification(data)
}

const clearCreateQualificationFormErrors = () => {
  const alert = getCreateQualificationFormErrorAlertElement()
  alert.innerHTML = ''
  alert.classList.add('d-none')
}

const ajaxSearchQualifications = (query) => {
  const url = `${getSearchQualificationsUrl()}?q=${query}`
  const request = new XMLHttpRequest()
  request.open('GET', url, true)

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      const data = JSON.parse(request.responseText)
      displaySaqaQualificationsResults(data['results'])
    }
  }

  request.send()
}

const ajaxCreateQualification = (data) => {
  const url = getCreateQualificationUrl()
  const request = new XMLHttpRequest()
  request.open('POST', url, true)
  request.setRequestHeader('Content-Type', 'application/json')
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
        getCreateQualificationNameElement().value = ''
      } else {
        const alert = getCreateQualificationFormErrorAlertElement()
        alert.innerHTML = data.error
        alert.classList.remove('d-none')
      }
    }
  }

  console.log(JSON.stringify(data))
  request.send(JSON.stringify(data))
}

const ajaxGetSfos = (fosId) => {
  const url = getListSfosUrl().replace('0', fosId)
  const request = new XMLHttpRequest()
  request.open('GET', url, true)

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      const data = JSON.parse(request.responseText)
      console.log(data)
      const selectElem = getCreateQualificationSubFosElement()
      const option = document.createElement('option')
      option.value = '0'
      option.innerHTML = '--Choose a sub-field of study or not--'
      selectElem.appendChild(option)
      data['results'].forEach((result) => {
        const option = document.createElement('option')
        option.value = result['id']
        option.innerHTML = result['name']
        selectElem.appendChild(option)
      })
      selectElem.classList.remove('d-none')
    }
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

const setOnChangeFosEvent = () => {
  getCreateQualificationFosElement().addEventListener('change', function (evt) {
    const fosId = getCreateQualificationFosElement().value
    const selectElem = getCreateQualificationSubFosElement()
    selectElem.querySelectorAll('option').forEach((option) => {
      selectElem.removeChild(option)
    })
    ajaxGetSfos(fosId)
  })
}

const setCreateQualifEvent = () => {
  const button = getCreateQualificationButtonElement()
  button.addEventListener('click', (evt) => {
    clearCreateQualificationFormErrors()
    createQualification()
  })
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
    })
    toggleArrowWidget(saqaQualifListElem.id)
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
      let qualifElem = saqaQualifListElem.querySelector(`li[data-saqa-id="${selectedQualifElem.dataset['saqa-id']}"]`)
      if (qualifElem) { qualifElem.style.display = 'list-item' }

      campusQualifListElem.removeChild(selectedQualifElem)

      let saqaId = selectedQualifElem.dataset['saqaId']
      removeSaqaQualification(saqaId)
    })

    toggleArrowWidget(campusQualifListElem.id)
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
    })
  })
}

const setToggleEvent = (elem) => {
  elem.addEventListener('click', function (evt) {
    if (evt.target.tagName !== 'A') {
      const liElem = findLiElem(evt.target)
      liElem.classList.toggle('selected')

      const listId = liElem.parentElement.id
      toggleArrowWidget(listId)
    }
  })
}

const setClickEventToLi = () => {
  const qualifElems = document.querySelectorAll('li[data-saqa-id]')
  qualifElems.forEach(function (qualifElem) {
    setToggleEvent(qualifElem)
  })
}
const setupEvents = () => {
  setClickEventToLi()
  setClickEventToAddButton()
  setClickEventToRemoveButton()
  setClickEventToClearButton()
  setSearchEvent()
  setCreateQualifEvent()
  setOnChangeFosEvent()
}

(function () {
  setupEvents()
})()

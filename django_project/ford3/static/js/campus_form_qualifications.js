
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

const getCampusQualificationsListElement = () => {
  return document.getElementById('campus-qualifications-list')
}

const getSelectedQualificationsFromList = (list) => {
  return list.querySelectorAll('li.selected')
}

const getSaqaQualificationsInputElem = () => {
  return document.getElementById('id_campus-qualifications-saqa_ids')
}

const addSaqaQualification = (saqaId) => {
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

const setToggleEvent = (elem) => {
  elem.addEventListener('click', function (evt) {
    if (evt.target.tagName !== 'A') { evt.target.classList.toggle('selected') }
  })
}

const setClickEventToLi = () => {
  const qualifElems = document.querySelectorAll('li[data-saqa-id]')
  qualifElems.forEach(function (qualifElem) {
    setToggleEvent(qualifElem)
  })
}

//isEnabled true = disabled add button
const toggleAddButton = (isEnabled) => {
  const addButton = getAddQualificationButtonElement()
  //qualificationText[0]= add button and qualificationText[1]= remove button
  const qualificationText = getCampusQualificationText()
  addButton.disabled = isEnabled
  if(isEnabled) {
    addButton.classList.remove("left-arrow-button")
    addButton.classList.add("left-arrow-grey-button")
    qualificationText[0].classList.add("disabled")
  }
  else {
    addButton.classList.remove("left-arrow-grey-button")
    addButton.classList.add("left-arrow-button")
    qualificationText[0].classList.remove("disabled")
  }
}

const toggleRemoveButton = (isEnabled) => {
  const removeButton = getRemoveQualificationButtonElement()
  //qualificationText[0]= add button and qualificationText[1]= remove button
  removeButton.disabled = isEnabled
  const qualificationText = getCampusQualificationText()
  if(isEnabled) {
    removeButton.classList.remove("right-arrow-button")
    removeButton.classList.add("right-arrow-grey-button")
    qualificationText[1].classList.add("disabled")
  }
  else {
    removeButton.classList.add("right-arrow-button")
    removeButton.classList.remove("right-arrow-grey-button")
    qualificationText[1].classList.remove("disabled")
  }

}

const checkSaqaList = () => {
    const saqaList = getSaqaQualificationsListElement()
    if (saqaList.length == 0 || saqaList.getElementsByTagName("li").length < 1) {
        toggleAddButton(true);
    }
}

const checkCampusList = () => {
  const campusList = getCampusQualificationsListElement()
  if(campusList.length == 0 || campusList.getElementsByTagName("li").length < 1) {
    toggleRemoveButton(true)
  }
}

const checkLists = () => {
  checkSaqaList()
  checkCampusList()
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
      const campusQualifListElem = getCampusQualificationsListElement()
      campusQualifListElem.appendChild(clonedNode)

      setToggleEvent(clonedNode)

      let saqaId = selectedQualifElem.dataset['saqaId']
      addSaqaQualification(saqaId)
      checkSaqaList()
      toggleRemoveButton(false)
    })
  })
}

const setClickEventToRemoveButton = () => {
  var removeQualifButton = getRemoveQualificationButtonElement()
  removeQualifButton.addEventListener('click', function (evt) {
    evt.stopPropagation()
    const saqaQualifListElem = getSaqaQualificationsListElement()
    const campusQualifListElem = getCampusQualificationsListElement()
    var selectedQualifElems = getSelectedQualificationsFromList(campusQualifListElem)

    selectedQualifElems.forEach(function (selectedQualifElem) {
      var qualifElem = saqaQualifListElem.querySelector('li[data-saqa-id="' + selectedQualifElem.dataset['saqa-id'] + '"]')
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
  let linkText = document.createTextNode('(' + saqa.saqa_id + ')')
  let link = document.createElement('a')
  link.href = 'http://regqs.saqa.org.za/viewQualification.php?id=' + saqa.saqa_id
  link.target = '_blank'
  link.appendChild(linkText)
  return link
}

const displaySaqaQualificationsResults = (results) => {
  const list = getSaqaQualificationsListElement()
  list.querySelectorAll('li').forEach(function (li) {
    list.removeChild(li)
  })

  results.forEach(function (saqa) {
    let saqaNode = document.createElement('li')
    saqaNode.setAttribute('data-saqa-id', saqa.saqa_id)
    const saqaNodeContent = document.createTextNode(saqa.name)
    const saqaLink = buildSaqaQualificationLiContent(saqa)
    saqaNode.appendChild(saqaLink)
    saqaNode.appendChild(document.createTextNode('\u00A0'))
    saqaNode.appendChild(saqaNodeContent)

    list.appendChild(saqaNode)

    setToggleEvent(saqaNode)
  })
}

const ajaxSearchQualifications = (query) => {
  const url = '/ford3/saqa_qualifications?q=' + query
  const request = new XMLHttpRequest()
  request.open('GET', url, true)

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
    // Success!
      var data = JSON.parse(request.responseText)
      displaySaqaQualificationsResults(data['results'])
      toggleAddButton(false)
    } else {
    // We reached our target server, but it returned an error

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
    clearTimeout(timeout)

    timeout = setTimeout(function () {
      if (elem.value.length > 3) { ajaxSearchQualifications(elem.value) }
    }, 842)
  }
}

const setupEvents = () => {
  setClickEventToLi()
  setClickEventToAddButton()
  setClickEventToRemoveButton()
  setClickEventToClearButton()
  setSearchEvent()
}

(function () {
  checkLists()
  setupEvents()
})()


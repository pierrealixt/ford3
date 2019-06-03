
const getTheAlphabet = () => {
  return document.getElementById('the-alphabet')
}

const getLetters = () => {
  return getTheAlphabet().querySelectorAll('li')
}

const getSelectedLetter = () => {
  return getTheAlphabet().querySelector('li.selected')
}

const getListOccupationsUrl = () => {
  return document.getElementById('list-occupations-url').value
}

const getOccupationsList = () => {
  return document.getElementById('occupations-list')
}

const getFormOccupationsInput = () => {
  return document.getElementById('id_qualification-interets-jobs-occupations_ids')
}

const getSelectedOccupationsList = () => {
  return document.getElementById('selected-occupations')
}

const isOccupationSelected = (occupationId) => {
  return getFormOccupationsInput().value.split(' ').includes(occupationId.toString())
}

const getSearchOccupationsInput = () => {
  return document.getElementById('search-occupations')
}

const getNoResultAlert = () => {
  return document.getElementById('search-no-result')
}

const buildAlphabet = () => {
  const alphabet = 'abcdefghijklmnopqrstuvwxyz'
  const alphabetList = getTheAlphabet()
  alphabet.split('').forEach((letter, index) => {
    const liNode = document.createElement('li')
    liNode.classList.add(`letter-${letter}`)
    if (index === 0) {
      liNode.classList.add(`selected`)
    }
    liNode.innerHTML = letter.toUpperCase()
    alphabetList.appendChild(liNode)
  })
}

const toggleLetter = (newLetter, oldLetter) => {
  if (newLetter) { newLetter.classList.add('selected') }
  if (oldLetter) { oldLetter.classList.remove('selected') }
}

const hideElement = (elem) => {
  elem.classList.add('d-none')
}

const showElement = (elem) => {
  elem.classList.remove('d-none')
}

const toggleOccupationId = (occupationId) => {
  let ids = getFormOccupationsInput().value.split(' ')
  if (ids.includes(occupationId)) {
    ids = ids.filter(function (value, index, arr) {
      return value !== occupationId
    })
  } else {
    ids.push(occupationId)
  }
  getFormOccupationsInput().value = ids.join(' ')
}

const getOccupation = (occupationId) => {
  return getOccupationsList().querySelector(`li[data-occupation-id="${occupationId}"]`)
}

const setClickToLetters = () => {
  getLetters().forEach((liLetter) => {
    liLetter.addEventListener('click', function (evt) {
      resetSearch()

      const clickedLetter = evt.target
      toggleLetter(clickedLetter, getSelectedLetter())

      ajaxFetchOccupations(clickedLetter.innerHTML)
    })
  })
}

const resetSearch = () => {
  getSearchOccupationsInput().value = ''
}

const setSearch = () => {
  let timeout = null
  const elem = getSearchOccupationsInput()
  elem.onkeyup = function (e) {
    hideElement(getNoResultAlert())
    clearTimeout(timeout)

    toggleLetter(null, getSelectedLetter())
    timeout = setTimeout(function () {
      if (elem.value.length > 2) {
        ajaxFetchOccupations(elem.value)
      }
    }, 842)
  }
}

const setupEvents = () => {
  setClickToLetters()
  setSearch()
  document.querySelectorAll('#selected-occupations span').forEach(span => {
    setClickRemoveOccupationSelectionList(span)
  })
  $('[data-toggle="tooltip"]').tooltip()
}

const removeOccupationFromSelectionList = (occupationId) => {
  const li = getSelectedOccupationsList().querySelector(`li[data-occupation-id="${occupationId}"]`)
  getSelectedOccupationsList().removeChild(li)
}

const removeSelectedClassFromOccupation = (occupation) => {
  occupation.classList.remove('selected-occupation')
}

const addSelectedClassToOccupation = (occupation) => {
  occupation.classList.add('selected-occupation')
}

const setClickRemoveOccupationSelectionList = (span) => {
  span.addEventListener('click', function (evt) {
    const occupation = evt.target.parentNode
    const occupationId = occupation.dataset['occupationId']

    if (isOccupationSelected(occupationId)) {
      // yes it is already selected
      // remove from selection list
      removeOccupationFromSelectionList(occupationId)
      // remove selected class
      const tempOcc = getOccupation(occupationId)
      if (tempOcc) {
        // only if the occupation is visible
        removeSelectedClassFromOccupation(tempOcc)
      }
    }

    toggleOccupationId(occupationId)
  })
}
const addOccupationStateInSelectionList = (occupationId) => {
  const occupation = getOccupation(occupationId)
  const newLi = document.createElement('li')
  newLi.dataset['occupationId'] = occupation.dataset['occupationId']
  newLi.innerHTML = occupation.innerHTML
  newLi.classList.add('h-100')
  const spanDel = document.createElement('span')
  spanDel.innerHTML = 'X'
  newLi.appendChild(spanDel)

  getSelectedOccupationsList().appendChild(newLi)
  setClickRemoveOccupationSelectionList(spanDel)
}

const setClickToOccupationLi = () => {
  getOccupationsList().querySelectorAll('li').forEach(occupationLi => {
    occupationLi.addEventListener('click', function (evt) {
      const occupation = evt.target
      const occupationId = occupation.dataset['occupationId']
      if (isOccupationSelected(occupationId)) {
        // yes it is already selected
        // remove from selection list
        removeOccupationFromSelectionList(occupationId)
        // remove selected class
        removeSelectedClassFromOccupation(occupation)
      } else {
        // no it is not
        // add to the selection list
        addOccupationStateInSelectionList(occupationId)
        // add the selected class
        addSelectedClassToOccupation(occupation)
      }

      // add or remove id from input
      toggleOccupationId(occupationId)
    })
  })
}

const buildLiElem = (item) => {
  const li = document.createElement('li')
  li.dataset['occupationId'] = item.id
  li.dataset['toggle'] = 'tooltip'
  li.dataset['placement'] = 'top'
  li.title = item.name
  li.innerHTML = item.name
  if (isOccupationSelected(item.id)) {
    li.classList.add('selected-occupation')
  }
  return li
}

const displayResults = (data) => {
  getOccupationsList().querySelectorAll('.occupation-column').forEach(column => {
    getOccupationsList().removeChild(column)
  })

  const itemsPerColumn = 7
  let columnsCount
  if (data.results.length < itemsPerColumn) {
    columnsCount = data.results.length
  } else {
    columnsCount = Math.ceil(data.results.length / itemsPerColumn)
  }

  for (let i = 0; i < columnsCount; i++) {
    const column = document.createElement('ul')
    column.classList.add('occupation-column')
    getOccupationsList().appendChild(column)

    const items = data.results.splice(0, itemsPerColumn)
    items.forEach(item => {
      const li = buildLiElem(item)
      column.appendChild(li)
    })
  }

  setClickToOccupationLi()
}

const ajaxFetchOccupations = (query) => {
  const url = `${getListOccupationsUrl()}?q=${query}`
  const request = new XMLHttpRequest()
  request.open('GET', url, true)
  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      const data = JSON.parse(request.responseText)
      if (data.results.length > 0) {
        showElement(getOccupationsList())
        hideElement(getNoResultAlert())

        displayResults(data)
      } else {
        showElement(getNoResultAlert())
        hideElement(getOccupationsList())
      }
    }
  }

  request.send()
}

(function () {
  buildAlphabet()
  setupEvents()
  ajaxFetchOccupations(getSelectedLetter().innerHTML)
})()


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
  return document.getElementById('id_3-occupations_ids')
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
  newLetter.classList.add('selected')
  oldLetter.classList.remove('selected')
}

const setClickToLetters = () => {
  getLetters().forEach((liLetter) => {
    liLetter.addEventListener('click', function (evt) {
      const clickedLetter = evt.target
      toggleLetter(clickedLetter, getSelectedLetter())

      ajaxFetchOccupations(clickedLetter.innerHTML)
    })
  })
}

const setSearch = () => {
  let timeout = null
  const elem = getSearchOccupationsInput()
  elem.onkeyup = function (e) {
    // getSearchFormErrorAlertElement().classList.add('d-none')
    clearTimeout(timeout)

    timeout = setTimeout(function () {
      if (elem.value.length > 4) { ajaxFetchOccupations(elem.value) }
    }, 842)
  }
}

const setupEvents = () => {
  setClickToLetters()
  setSearch()
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

const toggleOccupationSelection = (occupation) => {
  occupation.classList.toggle('selected-occupation')
}

const prout = (occupation) => {
  const li = document.createElement('li')
  li.dataset['occupationId'] = occupation.dataset['occupationId']
  li.innerHTML = occupation.innerHTML

  getSelectedOccupationsList().appendChild(li)
}

const setClickToOccupationLi = () => {
  getOccupationsList().querySelectorAll('li').forEach(occupationLi => {
    occupationLi.addEventListener('click', function (evt) {
      const occupation = evt.target

      prout(occupation)

      toggleOccupationSelection(occupation)

      const occupationId = occupation.dataset['occupationId']
      toggleOccupationId(occupationId)
    })
  })
}

const displayResults = (data) => {
  getOccupationsList().querySelectorAll('.occupation-column').forEach(column => {
    getOccupationsList().removeChild(column)
  })

  const itemsPerColumn = 7
  const columnsCount = Math.round(data.results.length / itemsPerColumn)

  for (let i = 0; i < columnsCount; i++) {
    const column = document.createElement('ul')
    column.classList.add('occupation-column', 'border')
    getOccupationsList().appendChild(column)

    const items = data.results.splice(0, itemsPerColumn)
    items.forEach(item => {
      const li = document.createElement('li')
      li.dataset['occupationId'] = item.id
      li.innerHTML = item.name
      if (isOccupationSelected(item.id)) {
        li.classList.add('selected-occupation')
      }
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
      displayResults(data)
    }
  }

  request.send()
}

(function () {
  buildAlphabet()
  setupEvents()
  ajaxFetchOccupations(getSelectedLetter().innerHTML)
})()

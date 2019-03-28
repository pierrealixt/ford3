
const getSaqaQualificationsListElement = () => {
  return document.getElementById('saqa-qualifications-list')
}

const getAddQualificationButtonElement = () => {
  return document.querySelector('button[data-action="add-qualif"]')
}

const getRemoveQualificationButtonElement = () => {
  return document.querySelector('button[data-action="remove-qualif"]')
}

const getCampusQualificationsListElement = () => {
  return document.getElementById('campus-qualifications-list')
}

const getSelectedQualificationsFromList = (list) => {
  return list.querySelectorAll('li.selected')
}

const getSaqaQualificationsInputElem = () => {
  return document.getElementById('id_3-saqa_ids')
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

const setToggleEvent = (elem) => {
  elem.addEventListener('click', function (evt) {
    evt.target.classList.toggle('selected')
  })
}

const setClickEventToLi = () => {
  const qualifElems = document.querySelectorAll('li[data-saqa-id]')
  qualifElems.forEach(function (qualifElem) {
    setToggleEvent(qualifElem)
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
      const campusQualifListElem = getCampusQualificationsListElement()
      campusQualifListElem.appendChild(clonedNode)

      setToggleEvent(clonedNode)

      let saqaId = selectedQualifElem.dataset['saqa-id']
      addSaqaQualification(saqaId)
    })
  })
}

const setClickEventToRemoveButton = () => {
  var removeQualifButton = getRemoveQualificationButtonElement()
  removeQualifButton.addEventListener('click', function (evt) {
    evt.stopPropagation()
    var saqaQualifListElem = getSaqaQualificationsListElement()
    var campusQualifListElem = getCampusQualificationsListElement()
    var selectedQualifElems = getSelectedQualificationsFromList(campusQualifListElem)

    selectedQualifElems.forEach(function (selectedQualifElem) {
      var qualifElem = saqaQualifListElem.querySelector('li[data-saqa-id="' + selectedQualifElem.dataset['saqa-id'] + '"]')

      qualifElem.style.display = 'list-item'

      campusQualifListElem.removeChild(selectedQualifElem)

      let saqaId = selectedQualifElem.dataset['saqa-id']
      removeSaqaQualification(saqaId)
    })
  })
}

const setupEvents = () => {
  setClickEventToLi()
  setClickEventToAddButton()
  setClickEventToRemoveButton()
}

// var searchQualifElem = document.getElementById('search_qualif')
// var timeout = null
// searchQualifElem.onkeyup = (function (e) {
//   clearTimeout(timeout)

//   timeout = setTimeout(function () {
//     console.log('Input Value:', searchQualifElem.value)
//   }, 500)
// }

(function () {
  setupEvents()
})()

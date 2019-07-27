
const nodeToInsertBefore = () => {
  return document.querySelector('#div_id_qualification-requirements-aps_calculator_link')
}

const getApsWidget = () => {
  return document.querySelector('#aps-widget')
}

const getStoreElem = () => {
  return document.querySelector('#id_qualification-requirements-admission_point_scores')
}

(function () {
  APS.forEach((aps) => {
    let divAps = document.createElement('div')
    divAps.classList.add('form-group', 'row')
    divAps.innerHTML = `
          <div class="col-sm-3">
              <label>${aps.group.name}</label>
          </div>
          <div class="col-sm-6">
              <input data-group="${aps.group.id}" data-field="aps-score" type="integer" value="${parseInt(aps.value) === 0 ? '' : aps.value}" class="form-control w-100" />
          </div>
    `
    nodeToInsertBefore().parentElement.insertBefore(divAps, nodeToInsertBefore())
    divAps.querySelector('input[type="integer"]').addEventListener('focusout', (event) => {
      const value = event.target.value
      const groupId = event.target.dataset['group']

      if (value.length > 0) {
        if (parseInt(value) <= 0) {
          alert('Admission point score should be a number greater than 0.')
          event.target.parentElement.parentElement.querySelector('input[type="integer"]').value = ''
          return
        }
        let newStore = []
        getStoreElem().value.split(',').forEach((aps) => {
          const parseAps = /\(([0-9]*) ([0-9]*)\)/.exec(aps)
          if (parseAps[1] === groupId) {
            const editedAps = `(${groupId} ${value})`
            newStore.push(editedAps)
          } else {
            newStore.push(aps)
          }
        })
        getStoreElem().value = newStore.join(',')
      }
    })
  })
})()

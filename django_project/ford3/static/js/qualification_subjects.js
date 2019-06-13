
const getSubjects = () => {
  // we get the subjects from the jinja template in qualification_form.html
  return SUBJECTS
}

const getSubjectsScoresInputElement = () => {
  // we use this input to save subject ids and their mininum score
  // (subject_id, mininum_score) (.., ..) ...
  return document.querySelector('#id_qualification-requirements-subjects_scores')
}

const subjectsWidget = () => {
  return document.querySelector('#subjects-widget')
}

const getAddNewSubjectFormButtonElem = () => {
  return document.querySelector('#add-new-subject-form')
}

const showAddNewSubjectFormButton = () => {
  getAddNewSubjectFormButtonElem().style.display = 'block'
}

const hideAddNewSubjectFormButton = () => {
  getAddNewSubjectFormButtonElem().style.display = 'none'
}

const hideAddButton = (subjectForm) => {
  subjectForm.querySelector('input[data-action="add-subject"]').parentNode.style.display = 'none'
}

const showEditButton = (subjectForm) => {
  subjectForm.querySelector('input[data-action="edit-subject"]').style.display = 'block'
}

const showRemoveButton = (subjectForm) => {
  subjectForm.querySelector('input[data-action="remove-subject"]').style.display = 'block'
}

const disableSelect = (subjectForm) => {
  subjectForm.querySelector('select').disabled = true
}

const createSelectSubjectsElem = (data) => {
  const div = document.createElement('div')
  div.classList.add('col-sm-3')
  const select = document.createElement('select')

  select.dataset['field'] = 'subject-id'
  select.classList.add('w-100', 'select', 'form-control')
  const selectedSubjectIds = getSelectedSubjects()

  if (Object.keys(data).includes('subjectId')) {
    const subject = getSubjects().filter(subject => subject.id === parseInt(data.subjectId))[0]

    const option = document.createElement('option')
    option.value = subject.id
    option.innerHTML = subject.name
    select.appendChild(option)
    select.disabled = true
  } else {
    getSubjects().forEach(subject => {
      if (!selectedSubjectIds.includes(subject.id)) {
        const option = document.createElement('option')
        option.value = subject.id
        option.innerHTML = subject.name
        select.appendChild(option)
      }
    })
  }

  div.appendChild(select)
  return div
}

const createInputMinScoreElem = (data) => {
  const div = document.createElement('div')
  div.classList.add('col-sm-2')

  const input = document.createElement('input')
  input.classList.add('form-control', 'w-100')
  input.dataset['field'] = 'min-score'
  input.placeholder = 'Mininum score'
  if (Object.keys(data).includes('minScore')) {
    input.value = data.minScore
  }

  div.appendChild(input)
  return div
}

const createButtonAddElem = (isNewData) => {
  const div = document.createElement('div')
  div.classList.add('col-sm-2')
  div.style.display = isNewData ? 'block' : 'none'

  let input = document.createElement('input')
  input.type = 'button'
  input.value = 'Add'
  input.dataset['action'] = 'add-subject'

  input.classList.add('edu-button', 'edu-button-blue', 'border-0', 'h-100', 'm-0')
  input.addEventListener('click', function (event) {
    addSubject(event.target)
  })
  div.appendChild(input)
  return div
}

const createButtonEditElem = (isNewData) => {
  const div = document.createElement('div')
  div.classList.add('col-sm-2')

  let input = document.createElement('input')
  input.type = 'button'
  input.value = 'Edit'
  input.style.display = isNewData ? 'none' : 'block'
  input.dataset['action'] = 'edit-subject'
  input.classList.add('edu-button', 'edu-button-blue', 'border-0', 'h-100', 'm-0')
  input.addEventListener('click', function (event) {
    editSubject(event.target)
  })
  div.appendChild(input)
  return div
}

const createButtonRemoveElem = (isNewData) => {
  const div = document.createElement('div')
  div.classList.add('col-sm-2')

  let input = document.createElement('input')
  input.type = 'button'
  input.value = 'Remove'
  input.style.display = isNewData ? 'none' : 'block'
  input.classList.add('edu-button', 'edu-button-blue', 'border-0', 'h-100', 'm-0')
  input.dataset['action'] = 'remove-subject'
  input.addEventListener('click', function (event) {
    removeSubject(event.target)
  })
  div.appendChild(input)
  return div
}

const createLabel = (formIndex) => {
  let div = document.createElement('div')
  div.classList.add('col-sm-3')
  let label = document.createElement('label')
  const text = document.createTextNode(`Required subject ${formIndex + 1}`)
  label.appendChild(text)
  div.appendChild(label)
  return div
}

const getNextSubjectFormIndex = () => {
  return subjectsWidget().querySelectorAll('.subject-form').length
}

const isDataEmpty = (data) => {
  return Object.keys(data).length === 0
}

const createSubjectForm = (data = {}) => {
  const isNewData = isDataEmpty(data)
  const formIndex = getNextSubjectFormIndex()
  const subjectForm = document.createElement('div')
  subjectForm.classList.add('col-sm-12', 'subject-form', 'mb-3')
  subjectForm.dataset['formIndex'] = formIndex
  const row = document.createElement('div')
  row.classList = 'row'

  const label = createLabel(formIndex)
  const select = createSelectSubjectsElem(data)
  const input = createInputMinScoreElem(data)
  const addButton = createButtonAddElem(isNewData)
  const editButton = createButtonEditElem(isNewData)
  const removeButton = createButtonRemoveElem(isNewData)

  row.appendChild(label)
  row.appendChild(select)
  row.appendChild(input)
  row.appendChild(addButton)
  row.appendChild(editButton)
  row.appendChild(removeButton)

  subjectForm.appendChild(row)
  return subjectForm
}

const parseSubjectForm = (subjectForm) => {
  const selectedSubjectIndex = subjectForm.querySelector('select').selectedIndex
  return {
    'subjectId': parseInt(subjectForm.querySelectorAll('option')[selectedSubjectIndex].value),
    'minScore': parseInt(subjectForm.querySelector('input').value)
  }
}

const displayError = (subjectForm) => {
  alert('Minimum score should be a number between 1 and 99.')
}

const clearMinScoreInput = (subjectForm, minScore = '') => {
  subjectForm.querySelector('input[data-field="min-score"]').value = minScore
}

const subjectDataValid = (subjectData) => {
  return subjectData.minScore > 0 && subjectData.minScore < 100 && !isNaN(subjectData.minScore)
}

const subjectAsTuple = (subjectData) => {
  return `(${subjectData.subjectId} ${subjectData.minScore})`
}

const parseSubjectTuple = (tuple) => {
  return /\(([0-9]*) ([0-9]*)\)/.exec(tuple)
}

const getSelectedSubjects = () => {
  return getSubjectsScores().map(tuple => {
    let result = parseSubjectTuple(tuple)
    return parseInt(result[1]) // subject id
  })
}

const getSubjectsScores = () => {
  return getSubjectsScoresInputElement().value.split(',').filter(t => t)
}

const saveSubject = (subjectData) => {
  const store = getSubjectsScores()
  store.push(subjectAsTuple(subjectData))
  getSubjectsScoresInputElement().value = store.join(',')
}

const addSubject = (target) => {
  const subjectForm = target.parentNode.parentNode
  const data = parseSubjectForm(subjectForm)
  if (subjectDataValid(data)) {
    saveSubject(data)
    hideAddButton(subjectForm)
    showEditButton(subjectForm)
    showRemoveButton(subjectForm)
    disableSelect(subjectForm)
    showAddNewSubjectFormButton()
  } else {
    displayError(subjectForm)
    clearMinScoreInput(subjectForm)
  }
}

const editSubject = (target) => {
  const subjectForm = target.parentNode.parentNode
  const data = parseSubjectForm(subjectForm)

  const subjectFormIndex = subjectForm.parentNode.dataset['formIndex']
  let store = getSubjectsScores()

  if (subjectDataValid(data)) {
    store[subjectFormIndex] = subjectAsTuple(data)
    getSubjectsScoresInputElement().value = store.join(',')
  } else {
    displayError(subjectForm)
    const minScore = parseSubjectTuple(store[subjectFormIndex])[2]
    clearMinScoreInput(subjectForm, minScore)
  }
}

const removeSubject = (target) => {
  const subjectForm = target.parentNode.parentNode
  const subjectFormIndex = subjectForm.parentNode.dataset['formIndex']
  let store = getSubjectsScores()
  store.splice(subjectFormIndex, 1)
  getSubjectsScoresInputElement().value = store.join(',')

  subjectsWidget().innerHTML = ''
  buildSubjectForms()
}

const buildSubjectForms = () => {
  getSubjectsScores().forEach(tuple => {
    const data = parseSubjectTuple(tuple)

    const subjectForm = createSubjectForm({
      'subjectId': data[1],
      'minScore': data[2]
    })

    subjectsWidget().appendChild(subjectForm)
  })
}

const addNewSubjectForm = (event) => {
  subjectsWidget().appendChild(createSubjectForm())
  hideAddNewSubjectFormButton()
}

const showSubjectsWidget = () => {
  buildSubjectForms()
  addNewSubjectForm()
  getAddNewSubjectFormButtonElem().addEventListener('click', addNewSubjectForm)
}

const resetSubjectsWidget = () => {
  getSubjectsScoresInputElement().value = ''
  subjectsWidget().innerHTML = ''
  hideAddNewSubjectFormButton()
  getAddNewSubjectFormButtonElem().removeEventListener('click', addNewSubjectForm, false)
}

(function () {
  document.querySelectorAll('input[name="qualification-requirements-require_certain_subjects"]').forEach(input => {
    if (input.checked && input.value === 'True') {
      showSubjectsWidget()
    }
    input.addEventListener('change', function (event) {
      const changedInput = event.target
      if (changedInput.checked && changedInput.value === 'True') {
        showSubjectsWidget()
      } else if (changedInput.checked && changedInput.value === 'False') {
        if (getSubjectsScores().length > 0) {
          if (confirm('Are you sure to remove the subjects already saved?')) {
            resetSubjectsWidget()
          }
        } else {
          resetSubjectsWidget()
        }
      }
    })
  })
})()

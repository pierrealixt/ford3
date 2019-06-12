
const getSubjects = () => {
  // we get the subjects from the jinja template in qualification_form.html
  return SUBJECTS
}

const getSubjectsScoresInputElement = () => {
  // we use this input to save subject ids and their mininum score
  // (subject_id mininum_score) (.. ..) ...
  return document.querySelector('#id_qualification-requirements-subjects_scores')
}

const subjectsWidget = () => {
  return document.querySelector('#subjects-widget')
}

const hideAddButton = (subjectForm) => {
  subjectForm.querySelector('input[data-action="add-subject"]').style.display = 'none'
}

const showEditButton = (subjectForm) => {
  subjectForm.querySelector('input[data-action="edit-subject"]').style.display = 'block'
}

const showRemoveButton = (subjectForm) => {
  subjectForm.querySelector('input[data-action="remove-subject"]').style.display = 'block'
}

const createSelectSubjectsElem = () => {
  const select = document.createElement('select')
  select.classList = 'col-sm-4'
  // select.dataset['field'] = 'subjects'
  const selectedSubjectIds = getSelectedSubjects()

  getSubjects().forEach(subject => {
    if (!selectedSubjectIds.includes(subject.id)) {
      const option = document.createElement('option')
      option.value = subject.id
      option.innerHTML = subject.name
      select.appendChild(option)
    }
  })
  return select
}

const createInputMinScoreElem = () => {
  const input = document.createElement('input')
  input.classList = 'col-sm-4'
  return input
}

const createButtonAddElem = () => {
  let input = document.createElement('input')
  input.classList = 'col-sm-4'
  input.type = 'button'
  input.value = 'Add'
  input.dataset['action'] = 'add-subject'
  input.addEventListener('click', function (event) {
    addSubject(event.target)
  })
  return input
}

const createButtonEditElem = () => {
  let input = document.createElement('input')
  input.classList = 'col-sm-2'
  input.type = 'button'
  input.value = 'Edit'
  input.style.display = 'none'
  input.dataset['action'] = 'edit-subject'
  input.addEventListener('click', function (event) {
    // editSubject(event.target)
  })
  return input
}

const createButtonRemoveElem = () => {
  let input = document.createElement('input')
  input.classList = 'col-sm-2'
  input.type = 'button'
  input.value = 'Remove'
  input.style.display = 'none'
  input.dataset['action'] = 'remove-subject'
  input.addEventListener('click', function (event) {
    // removeSubject(event.target)
  })
  return input
}

const createSubjectForm = () => {
  const subjectForm = document.createElement('div')
  subjectForm.classList = 'col-sm-12'
  const row = document.createElement('div')
  row.classList = 'row'
  subjectForm.appendChild(row)

  const select = createSelectSubjectsElem()
  const input = createInputMinScoreElem()
  const addButton = createButtonAddElem()
  const editButton = createButtonEditElem()
  const removeButton = createButtonRemoveElem()

  row.appendChild(select)
  row.appendChild(input)
  row.appendChild(addButton)
  row.appendChild(editButton)
  row.appendChild(removeButton)
  return subjectForm
}

const addNewSubjectForm = () => {
  subjectsWidget().appendChild(createSubjectForm())
}

const parseSubjectForm = (subjectForm) => {
  const selectedSubjectIndex = subjectForm.querySelector('select').selectedIndex
  return {
    'subjectId': parseInt(subjectForm.querySelectorAll('option')[selectedSubjectIndex].value),
    'minScore': parseInt(subjectForm.querySelector('input').value)
  }
}

const displayError = (subjectForm) => {
  alert('error')
}

const subjectDataValid = (subjectData) => {
  return subjectData.minScore > 0 && !isNaN(subjectData.minScore)
}

const subjectAsTuple = (subjectData) => {
  return `(${subjectData.subjectId} ${subjectData.minScore})`
}

const getSelectedSubjects = () => {
  return getSubjectsScores().map(tuple => {
    let result = /\(([0-9]*) ([0-9]*)\)/.exec(tuple)
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
  const subjectForm = target.parentNode
  const data = parseSubjectForm(subjectForm)
  if (subjectDataValid(data)) {
    saveSubject(data)
    hideAddButton(subjectForm)
    showEditButton(subjectForm)
    showRemoveButton(subjectForm)
  } else {
    displayError(subjectForm)
  }
}

(function () {
  addNewSubjectForm()

  // events
  document.querySelector('#add-new-subject-form').addEventListener('click', function (event) {
    addNewSubjectForm()
  })
  // document.querySelectorAll('input[data-action="add-subject"]').forEach(button => {
  //   button.addEventListener('click', function (event) {
  //     addSubject(event.target)
  //   })
  // })
  // addSubjectButtonElement().addEventListener('click', function (event) {

  // })
})()

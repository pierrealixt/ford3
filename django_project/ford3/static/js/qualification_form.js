let multipleSelectedLists = {}
let multipleSelectHandler = (e) => {
  // Handler for multiple select changed event
  let $div = $(e)
  let $listSelectedDiv = $div.parent().find('.list-selected')
  let inputName = $listSelectedDiv.data('name')
  let value = $div.data('value')
  let updateHiddenInputs = false
  let maxSelected = parseInt($listSelectedDiv.data('max-selected'))
  if (!multipleSelectedLists.hasOwnProperty(inputName)) {
    multipleSelectedLists[inputName] = []
  }

  if ($div.hasClass('selected')) {
    $div.removeClass('selected')
    let index = $.inArray(value, multipleSelectedLists[inputName])
    if (index !== -1) {
      multipleSelectedLists[inputName].splice(index, 1)
    }
    updateHiddenInputs = true
  } else {
    if (multipleSelectedLists[inputName].length < maxSelected) {
      multipleSelectedLists[inputName].push(value)
      $div.addClass('selected')
      updateHiddenInputs = true
    }
  }
  if (updateHiddenInputs) {
    updateListSelected($listSelectedDiv, inputName)
  }
}

let updateListSelected = (listSelectedHiddenInput, inputName) => {
  // Function to update multiple list selected
  listSelectedHiddenInput.html('')
  if (!multipleSelectedLists.hasOwnProperty(inputName)) {
    return false
  }
  for (let i = 0; i < multipleSelectedLists[inputName].length; i++) {
    let selectedValue = multipleSelectedLists[inputName][i]
    listSelectedHiddenInput.append('<input type="hidden" name="' + inputName + '" value="' + selectedValue + '">')
  }
}

let subjectList = 1
// let addSubject = (e, selectedValue = '', minimumScoreValue = '') => {
//   // Function to add new subject
//   let $row = $(e).parent().parent().parent()
//   let $clone = $row.clone()
//   $row.parent().append($clone)
//   let $subjectInput = $clone.find('.subject-list')
//   $subjectInput.change(subjectChangedHandler)
//   $subjectInput.val(selectedValue)
//   let $minimumScoreInput = $clone.find('.subject-minimum-score')
//   $minimumScoreInput.change(minimumScoreChangedHandler)
//   $clone.find('.col-form-label').html('New Subject')
//   $clone.find('.subject-list').attr('name', '2-subject')
//   $clone.find('.subject-minimum-score').val(minimumScoreValue)
//   $clone.find('.subject-minimum-score').attr('name', '2-subject-minimum-score')
//   let $row_button = $row.find('.add-subject-btn')
//   $row_button.addClass('remove-subject-btn').removeClass('add-subject-btn')
//   $row_button.attr('onclick', 'removeSubject(this)')
//   $row_button.html('Remove Subject')
// }

$(document).ready(function () {
  let add_subject_button = $('.add-subject-btn')
  add_subject_button.click().click()
})

let removeSubject = (e) => {
  let $row = $(e).parent().parent().parent()
  $row.remove()
}

let subjectChangedHandler = (e) => {
  // Handler for Subject select changed event
  let $target = $(e.target)
  let selectedValue = $target.find(':selected').val()
  let $subjectListInput = $('#subject-list')
  customSelectChangedHandler($target, $subjectListInput, selectedValue)
}

let minimumScoreChangedHandler = (e) => {
  // Handler for minimum score input changed event
  let $target = $(e.target)
  let selectedValue = $target.val()
  let $subjectListInput = $('#minimum-score-list')
  customSelectChangedHandler($target, $subjectListInput, selectedValue)
}

let customSelectChangedHandler = ($target, $hiddenListInput, selectedValue) => {
  // This is for subject and minimum score div
  let subjectListInputValue = $hiddenListInput.val().split(',')

  // Get index
  let subjectIndex = 0
  let name = $target.attr('name')
  let splittedName = name.split('_')
  if (splittedName.length > 1) {
    subjectIndex = splittedName[1] - 1
  }
  if (subjectIndex > subjectListInputValue.length - 1) {
    for (let i = subjectListInputValue.length - 1; i < subjectIndex; i++) {
      subjectListInputValue.push('-1')
    }
  }
  if (!selectedValue) {
    selectedValue = -1
  }
  subjectListInputValue[subjectIndex] = selectedValue
  $hiddenListInput.val(subjectListInputValue.join(','))
};

(function () {
  // Datepicker
  $('.dateinput').datepicker()

  // Change form check to inline
  let formCheck = $('.form-check')
  formCheck.addClass('form-check-inline')

  // Multiple select
  let $selectMultiple = $('.selectmultiple')
  if ($selectMultiple.length) {
    $selectMultiple.parent().prev().removeClass('col-md-3').addClass('col-md-12')
    $.each($selectMultiple, function (index, selectDiv) {
      let inputName = $(selectDiv).attr('name')
      if (!multipleSelectedLists.hasOwnProperty(inputName)) {
        multipleSelectedLists[inputName] = []
      }
      let backgroundColorClass = $(selectDiv).data('background-color')
      let maxSelected = $(selectDiv).data('max-selected')
      $(selectDiv).attr('name', '')
      $(selectDiv).hide()
      $(selectDiv).parent().append('<div class="list-selected" data-name="' + inputName + '" data-max-selected="' + maxSelected + '"></div>')
      // Get list of select
      let childrenIndex = 1
      $(selectDiv).children().each(function () {
        let oddClass = ''
        let selectedClass = ''
        if ($(this).is(':selected')) {
          multipleSelectedLists[inputName].push(parseInt($(this).val()))
          selectedClass = 'selected'
        }
        if (childrenIndex % 2) {
          oddClass = 'odd'
        }
        $(selectDiv).parent().append(
          '<span onclick="multipleSelectHandler(this)" class="multiple-select-square ' +
                    backgroundColorClass + ' ' + oddClass + ' ' + selectedClass + '" data-value="' + $(this).val() + '">' + $(this).text() + '</span>'
        )
        childrenIndex++
      })
      updateListSelected($(selectDiv).parent().find('.list-selected'), inputName)
    })
  }

  // Subject form
//   let subjectInput = $('.subject-list')
//   let minimumScoreList = $('#minimum-score-list').val().split(',')
//   if (subjectInput.length) {
//     let subjectInputParent = subjectInput.parent()
//     subjectInput.change(subjectChangedHandler)
//     subjectInputParent.parent().parent().before().append('<input type="hidden" name="subject-length" id="subject-length" value=1>')
//     subjectInputParent.addClass('row')
//     let minimumScoreValue = ''
//     if (typeof minimumScoreList[0] !== 'undefined') {
//       minimumScoreValue = minimumScoreList[0]
//     }
//     subjectInputParent.append('<div class="col-md-4"><input type="number" name="subject-minimum-score" placeholder="Minimum Score" class="textInput form-control subject-minimum-score" value="' + minimumScoreValue + '"></div>')
//     subjectInputParent.append('<div class="col-md-4"><button type="button" class="add-subject-btn btn btn-default" onclick="addSubject(this)">Add Subject</button></div>')
//     $('.subject-minimum-score').change(minimumScoreChangedHandler)
//   }
//   let subjectListHiddenInput = $('#subject-list')
//   let selectedSubjects = subjectListHiddenInput.val().split(',')
//   $.each(selectedSubjects, function (subjectIndex, selectedValue) {
//     if (subjectIndex === 0) {
//       return true
//     }
//     let subjectInputName = '2-subject'
//     if (subjectIndex > 1) {
//       subjectInputName += '_' + subjectIndex
//     }
//     // Get the subject select div
//     let $input = $('select[name="' + subjectInputName + '"]').children()
//     let minimumScoreValue = ''
//     if (typeof minimumScoreList[subjectIndex] !== 'undefined') {
//       minimumScoreValue = minimumScoreList[subjectIndex]
//       if (minimumScoreValue === '-1') {
//         minimumScoreValue = ''
//       }
//     }
//     addSubject($input, selectedValue, minimumScoreValue)
//   })
})()

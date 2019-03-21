let multipleSelectedLists = {};
let interestSelectedHandler = (e) => {
    let $div = $(e);
    let $listSelectedDiv = $div.parent().find('.list-selected');
    let inputName = $listSelectedDiv.data('name');
    let value = $div.data('value');
    let updateHiddenInputs = false;
    let maxSelected = parseInt($listSelectedDiv.data('max-selected'));
    if (!multipleSelectedLists.hasOwnProperty(inputName)) {
        multipleSelectedLists[inputName] = [];
    }

    if ($div.hasClass('selected')) {
        $div.removeClass('selected');
        let index = $.inArray(value, multipleSelectedLists[inputName]);
        if (index !== -1) {
            multipleSelectedLists[inputName].splice(index, 1);
        }
        updateHiddenInputs = true;
    } else {
        if (multipleSelectedLists[inputName].length < maxSelected) {
            multipleSelectedLists[inputName].push(value);
            $div.addClass('selected');
            updateHiddenInputs = true;
        }
    }
    if (updateHiddenInputs) {
        $listSelectedDiv.html('');
        for (let i = 0; i < multipleSelectedLists[inputName].length; i++) {
            let selectedValue = multipleSelectedLists[inputName][i];
            $listSelectedDiv.append('<input type="hidden" name="' + inputName + '" value="' + selectedValue + '">')
        }
    }
};

let subjectList = 1;
let addSubject = (e) => {
     subjectList++;
     let $row = $(e).parent().parent().parent();
     let $clone = $row.clone();
     $row.parent().append($clone);
     $clone.find('.col-form-label').html('Subject ' + subjectList + ':');
     $clone.find('.subject-list').attr('name',  '2-subject_' + subjectList);
     $clone.find('.subject-minimum-score').val('');
     $clone.find('.subject-minimum-score').attr('name',  'subject-minimum-score_' + subjectList);
     $(e).remove();
     $('#subject-length').val(subjectList);
};

(function () {
    // Show sidebar
    let sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');

    // Change form check to inline
    let formCheck = $('.form-check');
    formCheck.addClass('form-check-inline');

    // Multiple select
    let $selectMultiple = $('.selectmultiple');
    if ($selectMultiple.length) {
        $selectMultiple.parent().prev().removeClass('col-md-3').addClass('col-md-12');
        $.each($selectMultiple, function (index, selectDiv) {
            let inputName = $(selectDiv).attr('name');
            let backgroundColorClass = $(selectDiv).data('background-color');
            let maxSelected = $(selectDiv).data('max-selected');
            $(selectDiv).attr('name', '');
            $(selectDiv).hide();
            $(selectDiv).parent().append('<div class="list-selected" data-name="' + inputName + '" data-max-selected="' + maxSelected + '"></div>');
            // Get list of select
            let childrenIndex = 1;
            $(selectDiv).children().each(function () {
                let oddClass = '';
                if (childrenIndex % 2) {
                    oddClass = 'odd';
                }
                $(selectDiv).parent().append('<span onclick="interestSelectedHandler(this)" class="multiple-select-square ' + backgroundColorClass + ' ' + oddClass + '" data-value="' + $(this).val() + '">' + $(this).text() + '</span>');
                childrenIndex++;
            });
        });
    }

    // Subject form
    let subjectInput = $('.subject-list');
    if (subjectInput.length) {
        let subjectInputParent = subjectInput.parent();
        subjectInputParent.parent().parent().before().append('<input type="hidden" name="subject-length" id="subject-length" value=1>');
        subjectInputParent.addClass('row');
        subjectInputParent.append('<div class="col-md-4"><input type="number" name="subject-minimum-score" placeholder="Minimum Score" class="textInput form-control subject-minimum-score"></div>');
        subjectInputParent.append('<div class="col-md-4"><button type="button" class="add-subject-btn btn btn-default" onclick="addSubject(this)">Add Subject</button></div>')
    }
})();

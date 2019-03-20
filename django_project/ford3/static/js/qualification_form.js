let subjectList = 1;
let addSubject = (e) => {
     subjectList++;
     let $row = $(e).parent().parent().parent();
     let $clone = $row.clone();
     $row.parent().append($clone);
     console.log($clone.find('.col-form-label'));
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

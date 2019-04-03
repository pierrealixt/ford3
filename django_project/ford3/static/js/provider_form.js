$(document).ready(function() {
    innitiateRemoveCampusButtons();
})

function innitiateRemoveCampusButtons() {
    $('.remove-campus-button').click(function() {
        this_button_parrent_parent = $(this).parent().parent();
        this_button_parrent_parent.remove();
    })
 }

$(document).on("submit", "form", function(e) {
    if (confirm('Submitting data. Continue?')) {
        campus_name_elements = $('.campus_name').elements
       return true;
    }
    else {
       return false;
    }
})

$('#add-campus-name').click(
    function () {
        addCampusNameInput();
        innitiateRemoveCampusButtons();
    }
 )



function addCampusNameInput() {
    var campus_container = $('#campus-names-input-wrapper');
    var result_html = ('<div>' +
            '<div class="row mt1 campus-name-fade-in">' +
                '<div class="col-4 centerv npl">' +
                    'Campus Name ' +
                '</div>' +
                '<div class="col-7">' +
                    '<input name="campus_name" required class="campus_name" ' +
                    'type="text" placeholder="•••••••••••••••••"/>' +
                '</div>' +
                '<div class="col-1">' +
                    '<div class="remove-campus-button">' +
                    '<div class="remove-campus-button-inner ">X</div></div>' +
                '</div>' +
            '</div></div>')
    new_input = $.parseHTML(result_html);
    campus_container.append(new_input);

}

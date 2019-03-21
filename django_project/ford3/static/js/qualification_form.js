let interestSelectedHandler = (e, maxSelected, listSelected) => {
    let $div = $(e);
    let value = $div.data('value');
    let updateHiddenInputs = false;
    if ($div.hasClass('selected')) {
        $div.removeClass('selected');
        let index = $.inArray(value, listSelected);
        if (index !== -1) {
            listSelected.splice(index, 1);
        }
        updateHiddenInputs = true;
    } else {
        if (listSelected.length < maxSelected) {
            listSelected.push(value);
            $div.addClass('selected');
            updateHiddenInputs = true;
        }
    }

    if (updateHiddenInputs) {
        let $listSelectedDiv = $div.parent().find('.list-selected');
        let inputName = $listSelectedDiv.data('name');
        $listSelectedDiv.html('');
        for (let i = 0; i < listSelected.length; i++) {
            let selectedValue = listSelected[i];
            $listSelectedDiv.append('<input type="hidden" name="' + inputName + '" value="' + selectedValue + '">')
        }
    }
};

let interestList = [];

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
            $(selectDiv).attr('name', '');
            $(selectDiv).hide();
            $(selectDiv).parent().append('<div class="list-selected" data-name="' + inputName + '"></div>');
            // Get list of select
            let childrenIndex = 1;
            $(selectDiv).children().each(function () {
                let oddClass = '';
                if (childrenIndex % 2) {
                    oddClass = 'odd';
                }
                $(selectDiv).parent().append('<span onclick="interestSelectedHandler(this, 3, interestList)" class="multiple-select-square ' + backgroundColorClass + ' ' + oddClass + '" data-value="' + $(this).val() + '">' + $(this).text() + '</span>');
                childrenIndex++;
            });

        });
    }

})();

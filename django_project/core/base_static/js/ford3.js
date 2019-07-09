$(document).ready(function() {
    $('#sidebar-small-link').click(function () {
        let stm = $('.small-sidebar-menu');
        if (stm.hasClass('show-sidebar-menu')) {
            stm.removeClass('show-sidebar-menu')
        }
        else {
            stm.addClass('show-sidebar-menu');
        }
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})
$(function () {
    'use strict'

    $('[data-toggle="offcanvas"]').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    })
})

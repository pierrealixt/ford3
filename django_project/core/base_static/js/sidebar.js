const toggleSidebar = () => {
   const sidebar = document.getElementById('sidebar')
   sidebar.classList.toggle('active')
}

$(document).ready(function () {

        $('#sidebarCollapse').on('click', function () {
            $('#sidebar').toggleClass('active');
        });

});

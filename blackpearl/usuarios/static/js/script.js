$(document).ready(function () {
            $('#sidebarCollapse').on('click', function () {
                $('#sidebar').toggleClass('active');
            });
        });

$(document).ready(function() {
  $('#sidebar .nav-link').click(function() {
    // Recolhe todos os ul dentro do #sidebar
    $('#sidebar ul').slideUp();

    // Verifica se o próximo elemento é um ul
    if ($(this).next().is('ul')) {
      // Verifica se o ul está oculto
      if ($(this).next().is(':hidden')) {
        // Expande o ul
        $(this).next().slideDown();
      } else {
        // Recolhe o ul
        $(this).next().slideUp();
      }
    }
  });
});


/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    //
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


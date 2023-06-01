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

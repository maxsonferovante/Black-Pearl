$(document).ready(function() {
  $('#id_contratante').change(function() {
    var contratanteId = $(this).val();
    if (contratanteId) {
      $.ajax({
        type: 'GET',
        url: '/convenios/verificardependentes/',  // Certifique-se de usar uma barra inicial para a URL
        data: {'contratante_id': contratanteId},
        success: function(response) {
          if (response.has_dependents) {
            $('#dependente-message').text(' Incluir dependentes');
            $('#adicionar-dependente-btn').prop('disabled', false);

          } else {
            $('#dependente-message').text(' Cadastrar dependentes');
            $('#adicionar-dependente-btn').prop('disabled', true);
          }
        }
      });
    } else {
      $('#dependente-message').text('');
      $('#adicionar-dependente-btn').prop('disabled', true);
    }
  });
});


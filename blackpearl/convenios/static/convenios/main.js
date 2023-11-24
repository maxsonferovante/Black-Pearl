$('#div_id_dependentes').html('');

$(document).ready(function() {
  $('#id_contratante').change(function() {
    var contratanteId = $(this).val();
    var snapLoading = $('#snap-loading');
    if (contratanteId) {
        snapLoading.show();
      $.ajax({
        url: '/convenios/verificardependentes/',
        type: 'GET',
        data: {'contratante_id': contratanteId},
        success: function(response) {
            snapLoading.hide();
          if (response.has_dependents) {
            var dependentes = response.dependentes;
            var checkboxes = '';
            for (var i = 0; i < dependentes.length; i++) {
              checkboxes += '<div class="form-check">';
              checkboxes += '<input type="checkbox" name="dependentes" value="' + dependentes[i].id + '" id="id_dependentes_' + i + '" class="form-check-input">';
              checkboxes += '<label for="id_dependentes_' + i + '" class="form-check-label">' + dependentes[i].nomecompleto + '</label>';
              checkboxes += '</div>';
            }
            $('#div_id_dependentes').html(checkboxes);
          } else {
            $('#div_id_dependentes').html('');
          }
        }
      });
    } else {
      $('#div_id_dependentes').html('');
    }
  });
});



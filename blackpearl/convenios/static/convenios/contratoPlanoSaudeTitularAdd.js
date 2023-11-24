
$(document).ready(function() {
  $('.idade-atend-valor').change(function(event) {
    const planoSaude_id = $('#id_planoSaude').val();
    const contratante_id = $('#id_contratante').val();
    const atendDomiciliar = $('#id_atendimentoDomiciliar').val();
    var snapLoading = $('#snap-loading');

      if (planoSaude_id !== '' && contratante_id !== '' && atendDomiciliar !== '') {
        snapLoading.show();
          $.ajax({
          url: '/convenios/contratoplanosaude/consultafaixa/',
          data: {
            'planoSaude_id': planoSaude_id,
            'atendimentoDomiciliar': atendDomiciliar,
            'contratante_id': contratante_id
          },
          dataType: 'json',
          success: function(response) {
            snapLoading.hide();
            const faixa_id = response.faixa_id;
            const valor = response.valor;
            idadeMin = response.idadeMin;
            idadeMax = response.idadeMax;
            $('#id_valor').empty();
            $('#id_valor').val(valor);
            $('#id_faixa').empty();
            $('#id_faixa').append('<option value="' + faixa_id + '">' + idadeMin + ' a ' +  idadeMax + ' (anos)</option>');
          }
        });
      }
  });




  });
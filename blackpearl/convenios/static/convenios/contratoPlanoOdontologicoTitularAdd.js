
$(document).ready(function() {
  $('.plano-quant-valor').change(function (event) {

    var contratanteId = $('#id_contratante').val();

    var planoOdontologicoId = $('#id_planoOdontologico').val();

    console.log(contratanteId, planoOdontologicoId);

    if (contratanteId !=='' && planoOdontologicoId !=='') {
       $.ajax({
              url: '/convenios/contratoodontologica/verificarassociacao/',  // URL da sua view VerificarAssociacaoView
              type: 'GET',
              data: { 'contratante_id': contratanteId,
                      'plano_odontologico_id': planoOdontologicoId
               },
              dataType: 'json',
              success: function(response) {
                var novoValor = response.valor_total;
                console.log(novoValor);
                $('#id_valor').val(novoValor);
              },
              error: function(xhr, status, error) {
                console.log(error);
                console.log(status);
              }
            });
    }
  });
});

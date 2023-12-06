$(document).ready(function() {


$('#id_contratoPlanoSaude').change(function(event) {
                var contratoPlanoSaudeField = $('#id_contratoPlanoSaude').val();
                var valorField = $('#id_valorContratado').val();
                var snapLoading = $('#snap-loading');
                if (contratoPlanoSaudeField) {
                snapLoading.show();
                    $.ajax({
                        url: '/cobrancas/gerar/contrato/individual/consulta/valor',
                        data: {
                        'contratoPlanoSaude': contratoPlanoSaudeField,
                        },
                        dataType: 'json',
                        success: function(response) {
                            snapLoading.hide();
                            $('#id_valorContratado').val(response.valorContratado);
                        }
                        });
                }
          });

$('#id_contratoPlanoOdontologico').change(function(event) {
                var contratoPlanoOdontoField = $('#id_contratoPlanoOdontologico').val();
                var valorField = $('#id_valorContratado').val();
                var snapLoading = $('#snap-loading');
                if (contratoPlanoOdontoField) {
                snapLoading.show();
                    $.ajax({
                        url: '/cobrancas/gerar/contrato/individual/consulta/valor',
                        data: {
                        'contratoPlanoSaude': contratoPlanoOdontoField,
                        },
                        dataType: 'json',
                        success: function(response) {
                            snapLoading.hide();
                            $('#id_valorContratado').val(response.valorContratado);
                        }
                        });
                }
          });

});

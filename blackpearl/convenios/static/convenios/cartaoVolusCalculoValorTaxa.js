$(document).ready(function() {
$('#id_valor').change(function(event) {
                var valorField = $('#id_valor').val();
                var valorComTaxaField = $('#id_valorComTaxa').val();
                if(valorField){
                    $.ajax({
                    url: '/convenios/cartaovolus/consultataxa',
                    data: {
                            'valor': valorField,
                    },
                    dataType: 'json',
                    success: function(response) {
                    console.log(response);
                        var valorComTaxa = response.valorTaxa;
                        $('#id_valorComTaxa').empty();
                        $('#id_valorComTaxa').val(valorComTaxa);
                    }

                    });
                }
});
});

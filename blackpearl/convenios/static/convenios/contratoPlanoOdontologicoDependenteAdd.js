$(document).ready(function() {
    $('#id_valor').prop('disabled', true);
    $('#id_valorComTaxa').prop('disabled', true);
    $('#id_dependente').prop('disabled', true);

    $('#id_dependente').change(function () {
        var contratoValue = $('#id_contratoTitular').val();
        var dependenteValue = $('#id_dependente').val();
        var valor = $('#id_valor').val();
        var valorComTaxa = $('#id_valorComTaxa').val();
        var snapLoading = $('#snap-loading');

        if(dependenteValue){
        snapLoading.show();
        $.ajax({
            url: '/convenios/contratoondontologico/consultadosvalores/dependente/',
            method: 'GET',
            data:{
                contratoValue: contratoValue,
            },
            success: function (response) {
                snapLoading.hide();
                // Atualiza os campos id_faixa e id_valor com os dados obtidos
                $('#id_valor').val(response.valor);
                $('#id_valorComTaxa').val(response.valorComTaxa);
                $('#id_valor').prop('disabled', false);
                $('#id_valorComTaxa').prop('disabled', false);

            },
            error: function () {
                console.error('Erro ao obter dados do servidor.');
            }
        });
        }
        else{
            $('#id_valor').prop('disabled', true);
            $('#id_valorComTaxa').prop('disabled', true);
            $('#id_valor').val('');
            $('#id_valorComTaxa').val('');

        }
        });
    $('#id_contratoTitular').change(function () {
        var contratoValue = $(this).val();
        var snapLoading = $('#snap-loading');
        if(contratoValue){
            snapLoading.show();
            $.ajax({
                url: '/convenios/contratoondontologico/consultadosdependentes/',
                data:{
                        'contratoValue': contratoValue,
                },
                dataType: 'json',
                success: function (data) {
                            snapLoading.hide();
                            if(data.has_dependents){
                                $('#id_dependente').empty();
                                $('#id_dependente').append('<option value=""> ---------------- </option>');
                                $.each(data.dependentes, function (index, value) {
                                    $('#id_dependente').append('<option value="' + value.id + '">' + value.nomecompleto + '</option>');
                                });
                                $('#id_dependente').prop('disabled', false);
                            }
                            else{
                                $('#id_dependente').empty();
                                $('#id_dependente').append('<option value=""> Sem depedentes cadastrados </option>');
                                $('#id_dependente').prop('disabled', true);
                            }
               },
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }

            });
        }
        else{
            $('#id_dependente').empty();
            $('#id_dependente').append('<option value=""> Selecione o contrato </option>');
            $('#id_dependente').prop('disabled', true);
            $('#id_valor').val('');
            $('#id_valorComTaxa').val('');
        }

    });
});
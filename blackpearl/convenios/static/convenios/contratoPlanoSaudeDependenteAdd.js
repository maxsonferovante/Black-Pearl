


$(document).ready(function() {
      $('#id_dependente').prop('disabled', true);
      $('#id_faixa').prop('disabled', true);
      $('#id_atendimentoDomiciliar').prop('disabled', true);

    $('#id_dependente').change(function () {
    var snapLoading = $('#snap-loading');
	var dependenteValue = $(this).val();
	var contratoValue = $('#id_contrato').val();
	var atendimentoDomiciliarValue = $('#id_atendimentoDomiciliar').val();


    if(dependenteValue){
    snapLoading.show();
    $.ajax({
		url: '/convenios/contratoplanosaude/consultafaixa_dependente/',
		method: 'GET',
		data: { dependente: dependenteValue,
		    contrato: contratoValue,
            atendimentoDomiciliar: atendimentoDomiciliarValue
		 },
		success: function (response) {
		    snapLoading.hide();
			// Atualiza os campos id_faixa e id_valor com os dados obtidos

            $('#id_faixa').empty();
			$('#id_faixa').append(
			'<option value="' + response.faixa.id + '">' + response.faixa.idadeMin + ' a ' +  response.faixa.idadeMax + ' (anos)</option>'
			);

			$('#id_valor').val(response.faixa.valor);

			$('#id_valorTotal').val(response.valorComTaxa);

			$('#id_faixa').prop('disabled', false);
			$('#id_atendimentoDomiciliar').prop('disabled', false);
		},
		error: function () {
			console.error('Erro ao obter dados do servidor.');
		}
	});
    }
    else {
        $('#id_faixa').prop('disabled', true);
        $('#id_atendimentoDomiciliar').prop('disabled', true);
        $('#id_faixa').empty();
        $('#id_faixa').append('<option value=""> ---------------- </option>');
    }
    });
    $('#id_atendimentoDomiciliar').change(function () {
    var snapLoading = $('#snap-loading');
	var dependenteValue = $('#id_dependente').val();
	var contratoValue = $('#id_contrato').val();
	var atendimentoDomiciliarValue = $(this).val();

	if(dependenteValue){
	    snapLoading.show();
    $.ajax({
		url: '/convenios/contratoplanosaude/consultafaixa_dependente/',
		method: 'GET',
		data: { dependente: dependenteValue,
		    contrato: contratoValue,
            atendimentoDomiciliar: atendimentoDomiciliarValue
		 },
		success: function (response) {
		    snapLoading.hide();
			// Atualiza os campos id_faixa e id_valor com os dados obtidos

            $('#id_faixa').empty();
			$('#id_faixa').append(
			'<option value="' + response.faixa.id + '">' + response.faixa.idadeMin + ' a ' +  response.faixa.idadeMax + ' (anos)</option>'
			);

			$('#id_valor').val(response.faixa.valor);

			$('#id_valorTotal').val(response.valorComTaxa);

			$('#id_faixa').prop('disabled', false);
		},
		error: function () {
			console.error('Erro ao obter dados do servidor.');
		}
	});
    }
    else {
        $('#id_faixa').prop('disabled', true);
        $('#id_faixa').empty();
        $('#id_faixa').append('<option value=""> ---------------- </option>');
    }
    });

    $('#id_contrato').change(function() {
        var snapLoading = $('#snap-loading');
        var contratoValue = $(this).val();
        if (contratoValue) {
            snapLoading.show();
          $.ajax({

            url: '/convenios/contratoplanosaude/consultadependente/',
            data: {
              'contrato': contratoValue
            },
            dataType: 'json',
            success: function(response) {
                snapLoading.hide();
              if(response.has_dependents){
                  $('#id_dependente').empty();
                  $('#id_dependente').append('<option value="">Selecione o dependente</option>');
                  // Popula o select de dependentes com os dados relevantes
                  $.each(response.dependentes, function(index, value) {
                    $('#id_dependente').append('<option value="' + value.id + '">' + value.nomecompleto + '</option>');
                  });
              }
              else{
                  $('#id_dependente').empty();
                  $('#id_dependente').append('<option value="">Não há dependentes cadastrados</option>');
              }
                $('#id_dependente').prop('disabled', false);
            }
          });
        } else {
          $('#id_dependente').prop('disabled', true);
          $('#id_dependente').empty();
          $('#id_dependente').append('<option value="">Selecione o contrato</option>');
        }
      });
});
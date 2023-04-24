
const cepInput = document.querySelector('#cep');
const addressInput = document.querySelector('#address');
const regionInput = document.querySelector('#inputGroupSelectUF');
const cityInput = document.querySelector('#textCidade');
const neighborhoodInput = document.querySelector('#textBairro');
const numeroInput = document.querySelector('#textNumero');


cepInput.addEventListener('keypress', (e) => {
  const onlyNumbers = /[0-9]|\./;
  const key = String.fromCharCode(e.keyCode);

  if (!onlyNumbers.test(key)) {
    e.preventDefault();
    return;
  }
});

cepInput.addEventListener('keyup', (e) => {
  const inputValue = e.target.value;

  if (inputValue.length === 8) {
    getAddress(inputValue);
  }
});
function getAddress(cep) {
  const numeroInput = document.querySelector('#numeroInput');

  fetch(`https://viacep.com.br/ws/${cep}/json/`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.erro) {
        alert('CEP não encontrado');
        return;
      }

      addressInput.value = data.logradouro;
      regionInput.value = data.uf;
      cityInput.value = data.localidade;
      neighborhoodInput.value = data.bairro;
      numeroInput.focus();

      formInputs.forEach((input) => {
        if (input !== numeroInput) {
          input.setAttribute('disabled', 'disabled');
        }
      });
      numeroInput.removeAttribute('disabled');
    })
    .catch(error => console.log(error));
}


button.addEventListener('click', () => {
  const inputValue = cepInput.value.replace(/\D/g, '');
  if (inputValue.length !== 8) {
    alert('CEP inválido');
    return;
  }

  getAddress(inputValue);
});



const checkbox = document.getElementById("flexSwitchCheckChecked");
const select01 = document.getElementById("inputGroupSelect01");
const select02 = document.getElementById("inputGroupSelect02");

checkbox.addEventListener("change", function() {
  if (this.checked) {
    select01.disabled = false;
    select02.disabled = false;
    select01.selectedIndex = 0;
    select02.selectedIndex = 0;
  } else {
    select01.disabled = true;
    select02.disabled = true;
    select01.selectedIndex = 0;
    select02.selectedIndex = 0;
  }
});



// Obtém o elemento HTML do campo de texto do CPF
const cpfInput = document.getElementById("textcpf");

// Adiciona um ouvinte de eventos ao campo de texto para verificar a entrada do usuário
cpfInput.addEventListener("input", function() {
  // Remove todos os caracteres que não são números do valor do campo de texto
  const cpf = cpfInput.value.replace(/\D/g, "");

  // Verifica se o CPF tem 11 dígitos
  if (cpf.length !== 11) {
    cpfInput.setCustomValidity("O CPF deve ter 11 dígitos numéricos.");
  } else {
    cpfInput.setCustomValidity("");
    // Verifica se o CPF é válido usando o algoritmo de validação de CPF
    let sum = 0;
    let remainder;
    for (let i = 1; i <= 9; i++) {
      sum += parseInt(cpf.substring(i-1, i)) * (11 - i);
    }
    remainder = (sum * 10) % 11;
    if ((remainder == 10) || (remainder == 11)) {
      remainder = 0;
    }
    if (remainder != parseInt(cpf.substring(9, 10))) {
      cpfInput.setCustomValidity("O CPF é inválido.");
      return;
    }
    sum = 0;
    for (let i = 1; i <= 10; i++) {
      sum += parseInt(cpf.substring(i-1, i)) * (12 - i);
    }
    remainder = (sum * 10) % 11;
    if ((remainder == 10) || (remainder == 11)) {
      remainder = 0;
    }
    if (remainder != parseInt(cpf.substring(10, 11))) {
      cpfInput.setCustomValidity("O CPF é inválido.");
      return;
    }
  }
});



function validarDDD(ddd) {
  var dddsValidos = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "24", "27", "28", "31", "32", "33", "34", "35", "37", "38", "41", "42", "43", "44", "45", "46", "47", "48", "49", "51", "53", "54", "55", "61", "62", "63", "64", "65", "66", "67", "68", "69", "71", "73", "74", "75", "77", "79", "81", "82", "83", "84", "85", "86", "87", "88", "89", "91", "92", "93", "94", "95", "96", "97", "98", "99"];
  return dddsValidos.includes(ddd);
}

function validarCelular(celular) {
  var numeros = celular.match(/\d/g);
  return numeros && numeros.length === 9;
}


const dddInput = document.querySelector('#dddInput');
const telefoneInput = document.querySelector('#telefoneInput');

function validarTelefone() {
  const ddd = dddInput.value;
  const telefone = telefoneInput.value;

  // Validar o DDD
  if (!ddd.match(/^\d{2}$/) || parseInt(ddd) < 11 || parseInt(ddd) > 99) {
    dddInput.setCustomValidity('Por favor, insira um DDD válido');
  } else {
    dddInput.setCustomValidity('');
  }

  // Validar o telefone
  if (!telefone.match(/^\d{9}$/)) {
    telefoneInput.setCustomValidity('Por favor, insira um número de telefone válido com 9 dígitos');
  } else {
    telefoneInput.setCustomValidity('');
  }
}

dddInput.addEventListener('input', validarTelefone);
telefoneInput.addEventListener('input', validarTelefone);


 $("#datatable").DataTable({
            paging: true,
            pageLength: 10,
            lengthChange:true,
            autoWidth:true,
            searching: true,
            bInfo: true,
            bSort: true,
            language: {
            processing:     "Processando...",
            search:         "Pesquisar:",
            lengthMenu:     "Mostrar _MENU_ entradas",
            info:           "Mostrando _START_ até _END_ de _TOTAL_ entradas",
            infoEmpty:      "Mostrando 0 até 0 de 0 entradas",
            infoFiltered:   "(filtrado de _MAX_ entradas no total)",
            infoPostFix:    "",
            loadingRecords: "Carregando...",
            zeroRecords:    "Nenhum registro encontrado",
            emptyTable:     "Nenhum dado disponível na tabela",
            paginate: {
                first:      "Primeiro",
                previous:   "Anterior",
                next:       "Próximo",
                last:       "Último"
            },
            aria: {
                sortAscending:  ": ativar para classificar a coluna em ordem crescente",
                sortDescending: ": ativar para classificar a coluna em ordem decrescente"
            }
            }
            });
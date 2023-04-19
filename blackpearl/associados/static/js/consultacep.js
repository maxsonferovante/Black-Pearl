const button = document.querySelector('#button-addon2');
const cepInput = document.querySelector('#cep');
const addressInput = document.querySelector('#address');
const regionInput = document.querySelector('#inputGroupSelectUF');
const textUfInput = document.querySelector('#textUf');
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
      textUfInput.value = data.uf;
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


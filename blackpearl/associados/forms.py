from django import forms

from blackpearl.associados.models import Associado


class AssociadoForm(forms.Form):
    # Dados Pessoais e contatos
    nome = forms.CharField(label='Nome', widget=forms.TextInput())
    sobrenome = forms.CharField(label='Sobrenome', widget=forms.TextInput())
    dataNascimento = forms.DateField(label='Data de Nascimento', widget=forms.DateInput())

    cpf = forms.CharField(label='CPF', widget=forms.TextInput())

    email = forms.EmailField(label='e-mail', widget=forms.EmailInput())
    dddNumeroContato = forms.CharField(label='DDD', widget=forms.TextInput())
    numeroContato = forms.CharField(label='Celular', widget=forms.TextInput())

    # Endereço
    cep = forms.CharField(label='CEP', widget=forms.TextInput())
    logradouro = forms.CharField(label='Logradouro', widget=forms.TextInput())
    num = forms.IntegerField(label='Número', widget=forms.NumberInput())
    bairro = forms.CharField(label='Bairro', widget=forms.TextInput())
    cidade = forms.CharField(label='Cidade', widget=forms.TextInput())
    estado = forms.CharField(label='Estado (UF)', widget=forms.TextInput)


class AssociadoModelForm(forms.ModelForm):
    class Meta:
        model = Associado
        exclude = ['ativo']
        widgets = {'dataNascimento': forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                   'class': 'form-control'}
        ),
            'cpf': forms.TextInput(
                attrs={
                    'id': 'textcpf'
                }
            ),
            'cep': forms.TextInput(
                attrs={
                    'id': 'cep'
                }
            ),
            'logradouro': forms.TextInput(
                attrs={
                    'id': 'address'
                }
            ),
            'bairro': forms.TextInput(
                attrs={
                    'id': 'textBairro'
                }
            ),
            'cidade': forms.TextInput(
                attrs={
                    'id': 'textCidade'
                }
            ),
            'estado': forms.TextInput(
                attrs={
                    'id': 'inputGroupSelectUF'
                }
            ),
            'num': forms.TextInput(
                attrs={
                    'id': 'textNumero'
                }
            )
        }

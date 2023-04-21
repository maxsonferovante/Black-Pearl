from django import forms

from blackpearl.associados.models import Associado


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
                    'id': 'textcpf',
                   'class': 'form-control'
                }
            ),
            'cep': forms.TextInput(
                attrs={
                    'id': 'cep',
                   'class': 'form-control'
                }
            ),
            'logradouro': forms.TextInput(
                attrs={
                    'id': 'address',
                   'class': 'form-control'
                }
            ),
            'bairro': forms.TextInput(
                attrs={
                    'id': 'textBairro',
                   'class': 'form-control'
                }
            ),
            'cidade': forms.TextInput(
                attrs={
                    'id': 'textCidade',
                   'class': 'form-control'
                }
            ),
            'estado': forms.TextInput(
                attrs={
                    'id': 'inputGroupSelectUF',
                   'class': 'form-control'
                }
            ),
            'num': forms.TextInput(
                attrs={
                    'id': 'textNumero',
                   'class': 'form-control'
                }
            )

        }

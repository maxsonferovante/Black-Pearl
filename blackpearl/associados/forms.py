from datetime import timezone

from django import forms
from django.core.exceptions import ValidationError

from blackpearl.associados.models import Associado, FileUploadExcelModel, Dependente


class AssociadoModelForm(forms.ModelForm):
    class Meta:
        model = Associado
        exclude = ['ativo']
        fields = ['nomecompleto', 'dataNascimento', 'sexo', 'cpf', 'identidade', 'orgemissor', 'estadocivil',
                  'dataAssociacao', 'associacao', 'empresa', 'email', 'dddNumeroContato', 'numeroContato',
                  'cep', 'logradouro', 'num', 'bairro', 'cidade', 'estado', 'matricula']

        widgets = {
            'dataNascimento': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'dataAssociacao': forms.DateInput(
                attrs={
                    'type': 'date'
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


class DependenteModelForm(forms.ModelForm):
    class Meta:
        model = Dependente
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
            )
        }


class FileUploadExcelModelForm(forms.Form):
    class meta:
        model = FileUploadExcelModel
        fields = '__all__'
        widgets = {
            'arquivo': forms.FileField()
        }

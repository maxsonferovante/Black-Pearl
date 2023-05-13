import re
from datetime import timezone

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from widget_tweaks.templatetags.widget_tweaks import register

from django.utils.translation import gettext_lazy as _

from blackpearl.associados.models import Associado, FileUploadExcelModel, Dependente


class AssociadoModelForm(forms.ModelForm):
    class Meta:
        model = Associado
        exclude = ['ativo']
        fields = ['nomecompleto', 'dataNascimento', 'sexo', 'cpf', 'identidade', 'orgemissor', 'estadocivil',
                  'dataAssociacao', 'associacao', 'empresa', 'email', 'dddNumeroContato', 'numeroContato',
                  'cep', 'logradouro', 'num', 'bairro', 'cidade', 'estado', 'matricula']

        widgets = {
            'dataNascimento': DateInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': 'dd/mm/yyyy',
                    'data-mask': '00/00/0000',
                    'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'
                },
                format='%d/%m/%Y'
            ),
            'dataAssociacao': DateInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': 'dd/mm/yyyy',
                    'data-mask': '00/00/0000',
                    'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'
                },
                format='%d/%m/%Y'
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


    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dataNascimento'].label = _('Data de Nascimento')
        self.fields['dataNascimento'].widget.attrs.update({'placeholder': '__/__/____'})
        self.fields['dataAssociacao'].label = _('Data de Associação')
        self.fields['dataAssociacao'].widget.attrs.update({'placeholder': '__/__/____'})
    """
class DependenteModelForm(forms.ModelForm):
    class Meta:
        model = Dependente
        exclude = ['ativo']
        widgets = {
            'dataNascimento': DateInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': 'dd/mm/yyyy',
                    'data-mask': '00/00/0000',
                    'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'
                },
                format='%d/%m/%Y'
            ),
        }


"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dataNascimento'].label = _('Data de Nascimento')
        self.fields['dataNascimento'].widget.attrs.update({'placeholder': '__/__/____'})
"""
@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    return field.as_widget(attrs={"placeholder": text})





class FileUploadExcelModelForm(forms.Form):
    class meta:
        model = FileUploadExcelModel
        fields = '__all__'
        widgets = {
            'arquivo': forms.FileField()
        }

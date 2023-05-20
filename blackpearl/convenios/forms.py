from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import DateInput
from re import match

from blackpearl.associados.models import Associado, Dependente
from blackpearl.convenios.models import CartaoConvenioVolus, FaturaCartao,ContratacaoPlanoOdontologico
from widget_tweaks.templatetags.widget_tweaks import register


class CartaoConvenioVolusForm(forms.ModelForm):
    class Meta:
        model = CartaoConvenioVolus
        exclude = ['ativo']
        fields = ['titular', 'valorLimite', 'status']

    def __int__(self, *args, **kwargs):
        super.__init__( *args, **kwargs)
        self.fields['titular'].queryset = Associado.objects.none()

        if 'titular' in self.data:
            self.fields['titular'].queryset = Associado.objects.all()
        elif self.instance.pk:
            self.fields['titular'].queryset = Associado.objects.all().filter(
                pk = self.instance.pk)

class FaturaCartaoForm(forms.ModelForm):
    class Meta:
        model = FaturaCartao
        exclude = ['ativo']
        fields = ['cartao', 'valor', 'valorComTaxa', 'competencia']
        widgets = {
            'competencia': DateInput(
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
            'valor': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'oninput': 'calcular_valor_com_taxa()',
                }
            ),
            'valorComTaxa': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled',
                    'step': '0.01',
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        valor = cleaned_data.get('valor')
        cartao = cleaned_data.get('cartao')
        if valor and cartao:
            if float(valor) > float(cartao.valorLimite):
                raise forms.ValidationError('Valor da fatura não pode ser maior que o limite do cartão.')
        return cleaned_data


class ContratacaoPlanoOdontologicoForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=8, decimal_places=2,  required= False, disabled= True)
    dependentes = forms.ModelMultipleChoiceField(
        queryset= Dependente.objects.all(),
        widget= forms.CheckboxSelectMultiple(
            attrs={
                'class': 'chosen-select'
            }), required=False)
    class Meta:
        model = ContratacaoPlanoOdontologico
        fields = ['contratante', 'plano_odontologico', 'dependentes','valor']


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    return field.as_widget(attrs={"placeholder": text})

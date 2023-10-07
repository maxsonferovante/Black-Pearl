from django import forms

from django.template.defaultfilters import register
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico
from blackpearl.associados.models import Associado
from blackpearl.convenios.models.planoOdontologicoModels import PlanoOdontologico


class ContratoPlanoOdontologicoForm(forms.ModelForm):
    contratante = forms.ModelChoiceField(
        queryset=Associado.objects.filter(associacao__in=['ag', 'fiativo', 'fiaposent', 'func']).exclude(ativo=False),
        widget=forms.Select(attrs={'class': 'plano-quant-valor'}))

    dataInicio = forms.DateField(
        label='Data da Contratação',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'dd/mm/yyyy',
                'data-mask': '00/00/0000'
            }
        ))
    quantidadeDependententes = forms.IntegerField(
        label='Quantidade de Dependentes',
        initial= 0,
        required= False,
        widget=forms.NumberInput(
            attrs={

                'class': 'plano-quant-valor',

                'placeholder': 'Quantidade de Dependentes'}))

    planoOdontologico = forms.ModelChoiceField(
        label='Plano Odontológico',
        queryset=PlanoOdontologico.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'plano-quant-valor'}))

    class Meta:
        model = ContratoPlanoOdontologico
        fields = ['contratante', 'planoOdontologico', 'formaPagamento', 'dataInicio', 'valor', 'ativo', 'quantidadeDependententes']
        exclude = ['dataFim']


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    return field.as_widget(attrs={"placeholder": text})

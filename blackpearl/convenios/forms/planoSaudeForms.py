from django import forms
from django.template.defaultfilters import register
from blackpearl.associados.models import Dependente, Associado
from blackpearl.convenios.models.planoSaudeModels import PlanoSaude, ContratoPlanoSaude, ContratoPlanoSaudeDependente


class ContratoPlanoSaudeForm(forms.ModelForm):
    contratante = forms.ModelChoiceField(
        queryset=Associado.objects.filter(associacao__in=['ag', 'fiativo', 'fiaposent', 'func']).exclude(ativo=False),
        widget=forms.Select(attrs={'class': 'idade-atend-valor'})
    )

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
    planoSaude = forms.ModelChoiceField(
        label='Plano de Saúde',
        queryset=PlanoSaude.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'idade-atend-valor'})
    )
    atendimentoDomiciliar = forms.BooleanField(label='Atendimento Domiciliar', initial=False, required=False,
                                               widget=forms.Select(choices=[(True, 'Sim'), (False, 'Não')],
                                                                   attrs={'class': 'idade-atend-valor'}))
    ativo = forms.BooleanField(label_suffix='Status*', required=True, initial=True,
                               widget=forms.Select(choices=[(True, 'Sim'), (False, 'Não')],
                                                   attrs={'class': 'form-control'}))

    class Meta:
        model = ContratoPlanoSaude
        fields = ['contratante', 'planoSaude', 'faixa', 'formaPagamento', 'atendimentoDomiciliar', 'dataInicio',
                  'valor', 'ativo', 'faixa']
        exclude = ['dataFim']


class ContratoPlanoSaudeDependenteForm(forms.ModelForm):
    contrato = forms.ModelChoiceField(queryset=ContratoPlanoSaude.objects.filter(ativo=True))
    dependente = forms.ModelChoiceField(queryset=Dependente.objects.filter(ativo=True))
    ativo = forms.BooleanField(label_suffix='Status*', required=True, initial=True,
                               widget=forms.Select(choices=[(True, 'Sim'), (False, 'Não')],
                                                   attrs={'class': 'form-control'}))
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

    class Meta:
        model = ContratoPlanoSaudeDependente
        fields = ['contrato', 'dependente', 'atendimentoDomiciliar', 'dataInicio', 'valor', 'ativo', 'faixa' ,'valorTotal']
        exclude = ['dataFim']


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    return field.as_widget(attrs={"placeholder": text})

from django import forms
from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico, \
    CHOICES_SITUACAO

from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico


class FaturaCobrancaGeracaoContratoPlanoSaudeForm(forms.ModelForm):
    situacao = forms.Select(choices=CHOICES_SITUACAO, attrs={'class': 'form-control'})

    contratoPlanoSaude = forms.ModelChoiceField(
        label='Contrato Plano de Saúde',
        queryset=ContratoPlanoSaude.objects.filter(ativo=True))

    dataDoVencimento = forms.DateField(
        label='Data do Vencimento',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'dd/mm/yyyy',
                'data-mask': '0000/00/00'
            }
        ))

    class Meta:
        model = CobrancaPlanoSaude
        fields = ['contratoPlanoSaude', 'dataDoVencimento', 'situacao', 'valorContratado']
        exclude = ['valorPago', 'dataDoPagamento', 'juros', 'multa']


class FaturaCobrancaGeracaoContratoPlanoOdontologicoForm(forms.ModelForm):
    situacao = forms.Select(choices=CHOICES_SITUACAO, attrs={'class': 'form-control'})

    contratoPlanoOdontologico = forms.ModelChoiceField(
        label='Contrato Plano Odontológico',
        queryset=ContratoPlanoOdontologico.objects.filter(ativo=True))

    dataDoVencimento = forms.DateField(
        label='Data do Vencimento',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'dd/mm/yyyy',
                'data-mask': '0000/00/00'
            }
        ))

    class Meta:
        model = CobrancaPlanoOdontologico
        fields = ['contratoPlanoOdontologico', 'dataDoVencimento', 'situacao', 'valorContratado']
        exclude = ['valorPago', 'dataDoPagamento', 'juros', 'multa']

from django import forms
from django.forms import DateInput
from blackpearl.associados.models import Associado
from blackpearl.convenios.models import CartaoConvenioVolus, FaturaCartao, ContratoPlanoOdontologico
from widget_tweaks.templatetags.widget_tweaks import register


class CartaoConvenioVolusForm(forms.ModelForm):
    class Meta:
        model = CartaoConvenioVolus
        exclude = ['ativo']
        fields = ['titular', 'valorLimite', 'status']

    def __int__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.fields['titular'].queryset = Associado.objects.none()

        if 'titular' in self.data:
            self.fields['titular'].queryset = Associado.objects.all()
        elif self.instance.pk:
            self.fields['titular'].queryset = Associado.objects.all().filter(
                pk=self.instance.pk)


class FaturaCartaoForm(forms.ModelForm):


    class Meta:
        model = FaturaCartao
        exclude = ['ativo']
        fields = ['cartao', 'valor', 'valorComTaxa', 'competencia']
        widgets = {
            'competencia': DateInput(
                attrs={
                    'type': 'date',
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

class ContratoPlanoOdontologicoForm(forms.ModelForm):

    contratante = forms.ModelChoiceField(
        queryset=Associado.objects.filter(associacao__in=['ag', 'fiativo', 'fiaposent']).exclude(ativo=False)
    )
    ativo = forms.BooleanField(label='Ativo', required=False, initial=True)
    class Meta:
        model = ContratoPlanoOdontologico
        fields = ['contratante', 'planoOdontologico', 'dataInicio', 'valor', 'ativo']
        widget = {
            'dataInicio': forms.SelectDateWidget(
                attrs={
                    'label': 'Data da Contratação',
                    'data':'date'
                }
            )
        }

""" BOOL_CHOICES = [(True, 'Sim'), (False, 'Não')]
    is_dependentes_associado = forms.BooleanField(label='Inclua seus dependentes ?',
                                                  widget=forms.RadioSelect(
                                                      choices=BOOL_CHOICES), required=False,
                                                  initial=False
                                                  )
"""


"""
class ContratoPlanoOdontologicoDependenteFormStepTwo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        choice = kwargs.pop('choice', None)
        super(ContratoPlanoOdontologicoDependenteFormStepTwo, self).__init__(*args, **kwargs)

        if choice is not None:
            self.fields['dependente'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=choice,
                required=False
            )

    class Meta:
        model = ContratoPlanoOdontologicoDependete
        fields = ['dependente', 'datainclusao']
        widget = {'datainclusao': forms.SelectDateWidget(attrs={'label': 'Data da Inclusão'})}
"""

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    return field.as_widget(attrs={"placeholder": text})

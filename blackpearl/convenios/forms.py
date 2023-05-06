from django import forms
from blackpearl.convenios.models import CartaoConvenioVolus


class CartaoConvenioVolusForm(forms.ModelForm):
    class Meta:
        model = CartaoConvenioVolus
        exclude = ['ativo']
        fields = ['titular', 'valorLimite','status']

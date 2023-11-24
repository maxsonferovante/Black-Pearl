from django import forms

from django.template.defaultfilters import register

from blackpearl.convenios.models.cartaoVolusModels import CartaoConvenioVolus, FaturaCartao
from blackpearl.associados.models import Associado

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
        fields = ['cartao', 'valor', 'valorComTaxa', 'competencia', 'situacaoFatura']
        widgets = {
            'competencia': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }


            ),
            'valor': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
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

class FileUploadExcelFaturasForm(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs.update({'class': 'form-control-file'})
    arquivo.widget.attrs.update({'id': 'inputGroupFile'})
    arquivo.widget.attrs.update({'nome': 'arquivo'})
    class meta:

        fields = '__all__'
        widgets = {
            'arquivo': forms.FileField()
        }


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    return field.as_widget(attrs={"placeholder": text})

from django import forms
from .models import Diretor, Destinatario, Oficio
from django.db.models import Max
class DiretorForm(forms.ModelForm):
    class Meta:
        model = Diretor
        fields = '__all__'

class DestinatarioForm(forms.ModelForm):
    class Meta:
        model = Destinatario
        fields = '__all__'

class OficioForm(forms.ModelForm):

    class Meta:
        model = Oficio
        fields = ['numeracao', 'dataOficio', 'assunto', 'remetente', 'destinatario', 'texto']
        exclude = ['id']
        widgets = {
            'dataOficio': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_numeracao(self):
        numeracao = self.cleaned_data.get('numeracao')
        max_numeracao = Oficio.objects.aggregate(Max('numeracao'))['numeracao__max']

        if max_numeracao is not None and numeracao <= max_numeracao:
            raise forms.ValidationError('A numeração deve ser maior que a maior numeração armazenada.')

        return numeracao

    def __init__(self, *args, **kwargs):
        super(OficioForm, self).__init__(*args, **kwargs)
        max_numeracao = Oficio.objects.aggregate(Max('numeracao'))['numeracao__max']
        if max_numeracao is not None:
            self.fields['numeracao'].initial = max_numeracao + 1
        else:
            self.fields['numeracao'].initial = 1
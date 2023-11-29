from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude, ContratoPlanoSaudeDependente




@method_decorator(login_required, name='dispatch')
class HomeTemplateView(TemplateView):
    template_name = 'home_cob.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
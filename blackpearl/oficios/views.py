from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Oficio, Destinatario, Diretor
from .forms import OficioForm
# Create your views here.

@method_decorator(login_required, name='dispatch')
class OficioListView(ListView):
    model = Oficio
    template_name = 'oficios/oficio_list.html'
    context_object_name = 'list_objs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queyset = super().get_queryset()
        obj_pesquisado = self.request.GET.get('obj')
        if obj_pesquisado:
            queyset = queyset.filter(assunto__icontains=obj_pesquisado).order_by('numeracao')
        else:
            queyset = queyset.all().order_by('numeracao')
        return queyset
@method_decorator(login_required, name='dispatch')
class OficioDetailView(ListView):
    model = Oficio
    template_name = 'oficios/oficio_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OficioDetailView, self).get_context_data(**kwargs)
        oficio = Oficio.objects.get(id=self.kwargs['pk'])
        context['oficio'] = oficio
        return context
@method_decorator(login_required, name='dispatch')
class OficiosCreateView(CreateView):
    model = Oficio
    form_class = OficioForm
    template_name = 'oficios/oficio_form.html'
    success_url = reverse_lazy('listar_oficios')

@method_decorator(login_required, name='dispatch')
class OficiosUpdateView(UpdateView):
    model = Oficio
    form_class = OficioForm
    template_name = 'oficios/oficio_form.html'
    success_url = reverse_lazy('listar_oficios')
@method_decorator(login_required, name='dispatch')
class OficiosDeleteView(DeleteView):
    model = Oficio
    success_url = reverse_lazy('listar_oficios')

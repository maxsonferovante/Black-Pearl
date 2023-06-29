from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from io import BytesIO as BytesIo
import os

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

@method_decorator(login_required, name='dispatch')
class RenderToPdfOficioView(View):
    template_name = 'oficios/template_export_oficio.html'

    
    def get(self, request, *args, **kwargs):
        oficio = Oficio.objects.get(id=self.kwargs['pk'])

        context = {
            'oficio': oficio
        }
        nomeOficio = str(oficio.numeracao) +"/"+ str(oficio.dataOficio.year) +"-"+ oficio.assunto
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(nomeOficio)

        template = get_template(self.template_name)
        html = template.render(context)
        result = BytesIo()

        pdf = pisa.pisaDocument(BytesIo(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
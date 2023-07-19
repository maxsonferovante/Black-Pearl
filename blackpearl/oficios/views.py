from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from io import BytesIO as BytesIo
import os

from .models import Oficio, Destinatario, Diretor
from .forms import OficioForm, OficioUpdateForm


from weasyprint import HTML, CSS

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
    form_class = OficioUpdateForm
    template_name = 'oficios/oficio_form.html'
    success_url = reverse_lazy('listar_oficios')

@method_decorator(login_required, name='dispatch')
class OficiosDeleteView(DeleteView):
    model = Oficio
    success_url = reverse_lazy('listar_oficios')

def link_callback(uri, rel):
    """
                Convert HTML URIs to absolute system paths so xhtml2pdf can access those
                resources
                """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

@method_decorator(login_required, name='dispatch')
class RenderToPdfOficioView(View):
    template_name = 'oficios/template_export_oficio.html'

    def get(self, request, *args, **kwargs):
        oficio = Oficio.objects.get(id=self.kwargs['pk'])

        context = {
            'oficio': oficio
        }
        nomeOficio = str(oficio.numeracao) +" \ "+ str(oficio.dataOficio.year) +" - "+ oficio.assunto
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(nomeOficio)

        template = get_template(self.template_name)
        html = template.render(context)

        pdf = pisa.CreatePDF(html, dest=response, encoding='utf-8')

        if not pdf.err:
            return HttpResponse(response, content_type='application/pdf')
        else:
            return HttpResponse("Erro ao gerar PDF: {}".format(pdf.err))
        
@method_decorator(login_required, name='dispatch')
class PdfGeneration(View):
    template_name = 'oficios/template_export_oficio.html'

    def get(self, request, *args, **kargs):
        oficio = Oficio.objects.get(id=self.kwargs['pk'])

        context = {
            'oficio': oficio
        }
        nomeOficio = str(oficio.numeracao) +" \ "+ str(oficio.dataOficio.year) +" - "+ oficio.assunto
        

        html_template = get_template(self.template_name)
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{nomeOficio}.pdf"'
        return response
from io import BytesIO
import openpyxl
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from formtools.wizard.views import SessionWizardView
from reportlab.pdfgen import canvas

from .forms import CartaoConvenioVolusForm, FaturaCartaoForm
from .forms import ContratoPlanoOdontologicoFormStepOne, ContratoPlanoOdontologicoDependenteFormStepTwo

from .models import CartaoConvenioVolus, FaturaCartao, ContratoPlanoOdontologico, ContratoPlanoOdontologicoDependete
from ..associados.models import Associado, Dependente


@method_decorator(login_required, name='dispatch')
class HomeTemplateView(TemplateView):
    template_name = 'convenios/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class CartaoListView(ListView):
    template_name = 'convenios/listagemcartoes.html'

    def get_context_data(self, **kwargs):
        context = super(CartaoListView, self).get_context_data(**kwargs)

        return context

    def get(self, request, *args, **kwargs):
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            cartoes = CartaoConvenioVolus.objects.filter(titular__nomecompleto__icontains=nome_pesquisado).order_by(
                'titular')
        else:
            cartoes = CartaoConvenioVolus.objects.all()
        paramentro_page = self.request.GET.get('page', '1')
        paramentro_limit = self.request.GET.get('limit', '10')
        if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
            paramentro_limit = '10'
        cartoes_paginator = Paginator(cartoes, paramentro_limit)
        try:
            page = cartoes_paginator.page(paramentro_page)
        except (EmptyPage, PageNotAnInteger):
            page = cartoes_paginator.page(1)

        return render(request, self.template_name, {
            'list_objs': page
        })


@method_decorator(login_required, name='dispatch')
class CartaoCreateView(CreateView):
    model = CartaoConvenioVolus
    form_class = CartaoConvenioVolusForm
    template_name_suffix = "_criar_form"
    success_url = reverse_lazy('listagemcartoes')


@method_decorator(login_required, name='dispatch')
class CartaoUpdateView(UpdateView):
    model = CartaoConvenioVolus
    form_class = CartaoConvenioVolusForm
    template_name_suffix = "_criar_form"
    success_url = reverse_lazy('listagemcartoes')


@method_decorator(login_required, name='dispatch')
class CartaoDetailView(DetailView):
    template_name = 'convenios/cartao_detalhes.html'
    model = CartaoConvenioVolus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartao_pk = self.kwargs['pk']
        cartao = CartaoConvenioVolus.objects.get(pk=cartao_pk)
        context['cartao'] = cartao
        return context


@method_decorator(login_required, name='dispatch')
class CartaoDeleteView(DeleteView):
    model = CartaoConvenioVolus
    success_url = reverse_lazy('listagemcartoes')


@method_decorator(login_required, name='dispatch')
class FaturaCreateView(CreateView):
    model = FaturaCartao
    form_class = FaturaCartaoForm
    template_name_suffix = '_criar_form'

    def get_success_url(self):
        # Verifica a origem da solicitação na sessão
        origin = self.request.session.get('fatura_create_origin')
        if origin == 'listagemfaturas':
            return reverse_lazy('listagemfaturas')
        else:
            cartao_pk = self.object.cartao.pk
            return reverse('cartao_visualizar', kwargs={'pk': cartao_pk})


@method_decorator(login_required, name='dispatch')
class FaturaDeleteView(DeleteView):
    model = FaturaCartao
    success_url = reverse_lazy('listagemfaturas')


@method_decorator(login_required, name='dispatch')
class FaturaUpdateView(UpdateView):
    model = FaturaCartao
    form_class = FaturaCartaoForm
    template_name_suffix = "_criar_form"
    success_url = reverse_lazy('listagemfaturas')


@method_decorator(login_required, name='dispatch')
class FaturaListView(ListView):
    template_name = 'convenios/listagem_faturas.html'

    def get_context_data(self, **kwargs):
        context = super(FaturaListView, self).get_context_data(**kwargs)

        return context

    def get(self, request, *args, **kwargs):
        request.session['fatura_create_origin'] = 'listagemfaturas'
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            faturas = FaturaCartao.objects.filter(cartao__titular__nomecompleto__icontains=nome_pesquisado).order_by(
                'cartao')
        else:
            faturas = FaturaCartao.objects.filter().order_by('competencia')

        paramentro_page = self.request.GET.get('page', '1')
        paramentro_limit = self.request.GET.get('limit', '10')

        if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
            paramentro_limit = '10'

        fatura_paginator = Paginator(faturas, paramentro_limit)

        try:
            page = fatura_paginator.page(paramentro_page)
        except (EmptyPage, PageNotAnInteger):
            page = fatura_paginator.page(1)

        return render(request, self.template_name, {
            'list_objs': page
        })


def show_dependentes_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('is_dependentes_associado')


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoWizardView(SessionWizardView):
    form_list = [ContratoPlanoOdontologicoFormStepOne, ContratoPlanoOdontologicoDependenteFormStepTwo]
    template_name = 'convenios/contratacaoplanoodontologico_criar_form.html'
    condition_dict = {'1': show_dependentes_form}

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        stepIndex = self.get_step_index(step)
        if stepIndex == 1:
            contratante = self.get_cleaned_data_for_step('0')['contratante']
            print(contratante.id, type(contratante))

            choice = [(choice.pk, choice.nomecompleto) for choice in Dependente.objects.filter(
                titular_id=contratante.id
            )]
            print(choice)
            form = ContratoPlanoOdontologicoDependenteFormStepTwo(choice=choice, data=data)
        return form

    def done(self, form_list, **kwargs):
        contratante_form = form_list[0]
        if contratante_form.cleaned_data.get('is_dependentes_associado'):
            contratante = contratante_form.save()

            dependentes_form = form_list[1]
            dependentes = dependentes_form.save(commit=False)
            for form in dependentes:
                form.titular_contratante = contratante
                form.save()
        else:
            contratante_form.save()

        return redirect('listagemcontratoodontologica')


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoDetailView(DetailView):
    pass


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoUpdateView(UpdateView):
    model = ContratoPlanoOdontologico
    form_class = ContratoPlanoOdontologicoFormStepOne
    template_name = 'convenios/contratoplanoOdontologico_update_form.html'
    success_url = reverse_lazy('listagemcontratoodontologica')


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoDeleteView(DeleteView):
    model = ContratoPlanoOdontologico
    success_url = reverse_lazy('listagemcontratoodontologica')


@method_decorator(login_required, name='dispatch')
class ContratoOdontologicaListView(ListView):
    template_name = 'convenios/listagem_contratacaoodontologica.html'

    def get_context_data(self, **kwargs):
        context = super(ContratoOdontologicaListView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            contratos = ContratoPlanoOdontologico.objects.filter(
                contratante__nomecompleto__icontains=nome_pesquisado).order_by('contratante')
        else:
            contratos = ContratoPlanoOdontologico.objects.all()

        paramentro_page = self.request.GET.get('page', '1')
        paramentro_limit = self.request.GET.get('limit', '10')
        if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
            paramentro_limit = '10'

        contratos_paginator = Paginator(contratos, paramentro_limit)
        try:
            page = contratos_paginator.page(paramentro_page)
        except (EmptyPage, PageNotAnInteger):
            page = contratos_paginator.page(1)

        return render(request, self.template_name, {
            'list_objs': page
        })


class VerificarDependentesView(View):
    @csrf_exempt
    def get(self, request):
        contratante_id = self.request.GET.get('contratante_id')
        contratante_id = request.GET.get('contratante_id')
        try:
            contratante = Associado.objects.get(pk=contratante_id)
            dependentes = contratante.dependentes.all()
            dependentes_data = [{'id': dep.pk, 'nomecompleto': dep.nomecompleto} for dep in dependentes]
            return JsonResponse({'has_dependents': dependentes.exists(), 'dependentes': dependentes_data})
        except Associado.DoesNotExist:
            return JsonResponse({'has_dependents': False, 'dependentes': []})


def exportar(request):
    empresa_selecionada = request.GET.get('inputGroupSelectEmpresa')
    data_inicial = request.GET.get('start_date')
    data_final = request.GET.get('end_date')
    tipoArquivo_selecionado = request.GET.get('inputGroupSelectTipoArquivo')

    print(f"{empresa_selecionada}, {data_inicial}, {data_final}")

    if data_inicial and data_final and empresa_selecionada and tipoArquivo_selecionado:
        # Filtra as faturas pelo intervalo de datas e pelo nome da empresa
        if empresa_selecionada == '5':
            faturas = FaturaCartao.objects.filter(
                competencia__gte=data_inicial, competencia__lte=data_final
            ).order_by('competencia')

            nome_arq = 'faturas_{}_{}'.format(data_inicial, data_final)
        else:
            faturas = FaturaCartao.objects.filter(
                cartao__titular__empresa_id=empresa_selecionada,
                competencia__gte=data_inicial, competencia__lte=data_final
            ).order_by('competencia')
            nome_arq = 'fatura_{}_{}'.format(data_inicial, data_final)

        return exporttofile(faturas=faturas,
                            nome_arq=nome_arq,
                            tipoArquivo_selecionado=tipoArquivo_selecionado)

    return reverse_lazy('listagemfaturas')


def exporttofile(faturas, nome_arq, tipoArquivo_selecionado):
    filename = f"{nome_arq}"

    if tipoArquivo_selecionado == '1':
        quant_faturas = faturas.count()
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        y = 750  # Posição y inicial
        for fatura in faturas:
            if y <= 50:
                pdf.showPage()
                y = 750
            # Escreve o título da fatura
            pdf.drawString(100, y, "Titular do Cartão: {}".format(fatura.cartao.titular.nomecompleto))
            y -= 20  # Move para a próxima linha
            pdf.drawString(100, y, "Empresa: {}".format(fatura.cartao.titular.empresa.nome))
            y -= 20  # Move para a próxima linha
            # Escreve as informações da fatura
            pdf.drawString(100, y, "Competência: {}".format(fatura.competencia))
            y -= 20
            pdf.drawString(100, y, "Valor da fatura: {}".format(fatura.valor))
            y -= 20
            pdf.drawString(100, y, "Valor com a taxa administrativa: {}".format(fatura.valorComTaxa))
            y -= 40  # Move duas linhas para baixo

        pdf.save()
        # Define o nome do arquivo PDF
        filename = filename + ".pdf"
        # Envia o PDF para o navegador como um arquivo de download
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        buffer.seek(0)

        response.write(buffer.read())

        buffer.close()
    elif tipoArquivo_selecionado == '2':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = nome_arq
        # Escreve os dados da lista de faturas na planilha
        ws['A1'] = "Titular"
        ws['B1'] = "Empresa"
        ws['C1'] = "Competêcia"
        ws['D1'] = "Valor"
        ws['E1'] = "Valor com taxa"

        for i, fatura in enumerate(faturas):
            ws.cell(row=i + 2, column=1, value=fatura.cartao.titular.nomecompleto)
            ws.cell(row=i + 2, column=2, value=fatura.cartao.titular.empresa.nome)
            ws.cell(row=i + 2, column=3, value=fatura.competencia)
            ws.cell(row=i + 2, column=4, value=fatura.valor)
            ws.cell(row=i + 2, column=5, value=fatura.valorComTaxa)

        # Cria uma resposta HTTP com o arquivo XLSX
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename={nome_arq}.xlsx'
        wb.save(response)


    elif tipoArquivo_selecionado == '3':
        """faturas_txt = ''
        for fatura in faturas:
            matricula = str(fatura.cartao.titular.matricula).zfill(6)
            valorComTaxa = str(fatura.valorComTaxa)[:4].replace('.', '').zfill(12)
            faturas_txt += '{} {}\n'.format(matricula, valorComTaxa)

        response = HttpResponse(faturas_txt, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{nome_arq}.txt'"""

    return response

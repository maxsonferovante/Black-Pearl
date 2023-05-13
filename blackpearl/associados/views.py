from io import BytesIO

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas

from .importExcelToAssociados import import_excel_to_associado
from .forms import AssociadoModelForm, FileUploadExcelModelForm, DependenteModelForm
from .models import Associado, FileUploadExcelModel, Dependente


# Create your views here.

@login_required(login_url='login')
def home(request):
    associados = Associado.objects.all()


    context = {
        'associados': associados

    }
    return render(request, 'associados/home.html', context)


@login_required(login_url='login')
def cadastrardjango(request):
    # o formulario pode ou não ter dados, tem quando usuario usa do botão cadastar, não tem quando a pagina carrega

    if str(request.method) == 'POST':
        formDadosAsssociado = AssociadoModelForm(request.POST)
        if formDadosAsssociado.is_valid():
            nomecompleto = formDadosAsssociado.cleaned_data['nomecompleto']
            cpf = formDadosAsssociado.cleaned_data['cpf']
            try:
                associado_existente = Associado.objects.get(nomecompleto=nomecompleto, cpf=cpf)
                messages.warning(request, f'O associado "{nomecompleto}" já está cadastrado.')
                return render(request, 'associados/formsdjango.html', {'form': formDadosAsssociado})
            except ObjectDoesNotExist:
                assoc = formDadosAsssociado.save()
                messages.success(request, f'Dados de {assoc.nomecompleto} cadastrados com sucesso!')
                formDadosAsssociado = AssociadoModelForm()
        else:
            messages.error(request, 'Verifique os campos destacados.')
    else:
        formDadosAsssociado = AssociadoModelForm()
    context = {
        'form': formDadosAsssociado
    }
    return render(request, 'associados/formsdjango.html', context)

@login_required(login_url='login')
def cadastrardependentes(request):
    # o formulario pode ou não ter dados, tem quando usuario usa do botão cadastar, não tem quando a pagina carrega

    if str(request.method) == 'POST':
        form = DependenteModelForm(request.POST)
        if form.is_valid():
            nomecompleto = form.cleaned_data['nomecompleto']
            cpf = form.cleaned_data['cpf']

            try:
                associado_existente = Dependente.objects.get(nomecompleto=nomecompleto, cpf=cpf)
                messages.warning(request, f'O dependente "{nomecompleto}" já está cadastrado.')
                return render(request, 'associados/forms_dependente.html', {'form': form})
            except ObjectDoesNotExist:
                depent = form.save()
                messages.success(request, f'Dados de {depent.nomecompleto} cadastrados com sucesso!')
                form = DependenteModelForm()

        else:
            messages.error(request, 'Verifique os campos destacados.')

    else:
        form = DependenteModelForm()
    context = {
        'form': form
    }
    return render(request, 'associados/forms_dependente.html', context)


@login_required(login_url='login')
def visualizar(request, associado_id):
    associado = Associado.objects.get(pk = associado_id)

    dependentes = associado.dependentes.all()
    context = {
        'dependentes': dependentes

    }
    return render(request, 'associados/home.html', context)



@login_required(login_url='login')
def editar(request, associado_id):
    if request.method == 'POST':
        associado = Associado.objects.get(pk=associado_id)
        formAssociado = AssociadoModelForm(request.POST, instance=associado)
        if formAssociado.is_valid():
            assoc = formAssociado.save()

            messages.success(request, 'Dados de {} atualizados com sucesso!'.format(assoc.nomecompleto))

            return render(request, 'associados/editar.html', {
                'form': formAssociado
            })
    else:
        associado = Associado.objects.get(pk=associado_id)
        formAssociado = AssociadoModelForm(
            instance=associado
        )
    return render(request, 'associados/editar.html', {
        'form': formAssociado
    })


@login_required(login_url='login')
def excluir(request, associado_id):
    if request.method == 'POST':
        associado = Associado.objects.get(pk=associado_id)
        associado.delete()

    return HttpResponseRedirect(reverse('home_assoc'))


@login_required(login_url='login')
def importExcel(request):
    if request.method == 'POST':
        formUploadFile = FileUploadExcelModelForm(request.POST)
        if formUploadFile.is_valid():
            arq = request.FILES['files']
            obj = FileUploadExcelModel.objects.create(
                nome="teste",
                arquivo=arq
            )
            ## modulo importExcelToAssociado.py responsável pela migração dos dados
            import_excel_to_associado(obj)
            obj = FileUploadExcelModel.objects.get(arquivo=obj.arquivo)

            obj.delete()

            formUploadFile = FileUploadExcelModelForm()

            messages.success(request, 'Dados importados com sucesso!')

        else:
            messages.error(request, 'Verifique os campos destacados!')
    else:
        formUploadFile = FileUploadExcelModelForm()

    context = {
        'formUploadFile': formUploadFile
    }
    return render(request, 'associados/formsdimport_excel.html', context)


def export_pdf(request, assoc_id):
    assoc = Associado.objects.get(id=assoc_id)

    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "{} {}".format(assoc.nome, assoc.sobrenome))

    p.drawString(100, 730, "{} {}".format(assoc.dataNascimento, assoc.cpf))

    p.drawString(100, 710, "{()} {} - {}", assoc.dddNumeroContato, assoc.numeroContato, assoc.email)

    p.drawString(100, 690, "CEP: {} Logradouro: {} N: {}".format(assoc.cep, assoc.logradouro, assoc.num))

    p.drawString(100, 690, "Bairro: {} Cidade: {} Estado(UF): {}".format(assoc.bairro, assoc.cidade, assoc.estado))

    p.showPage()
    p.save()

    # Define o nome do arquivo PDF
    filename = f"cadastro_{assoc.id}.pdf"

    # Envia o PDF para o navegador como um arquivo de download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()
    return response


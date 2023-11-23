from datetime import datetime

from .models import Associado, FileUploadExcelModel, Empresa
import pandas as pd
from blackpearl.settings import BASE_DIR
from ..convenios.models.cartaoVolusModels import CartaoConvenioVolus, FaturaCartao


def import_excel_to_associado(objUploadFile):
    path = str(objUploadFile.arquivo)

    print(f' {BASE_DIR}/{path}')
    df = pd.read_excel(path)

    for index in df.index:
        associado = Associado(
            nomecompleto='Nome Completo do Associado',

            dataNascimento='1990-01-01',

            sexo= df.at[index, 'Sexo'],

            cpf=df.at[index, 'CPF'].zfill(11),

            identidade='',
            orgemissor='',
            estadocivil='S',  # ou 'C' para casado, 'D' para divorciado, 'V' para viúvo(a)

            dataAssociacao='2022-01-01',

            associacao='fiativo',

            matricula=df.at[index, 'Matricula'],
            empresa=Empresa.objects.filter(nome=df.at[index, 'Departamento']),

            email='associado@example.com',
            dddNumeroContato='99',
            numeroContato='999999999',
            cep='12345-678',
            logradouro='Rua do Associado',
            num=123,
            bairro='Bairro do Associado',
            cidade='Cidade do Associado',
            estado='PA'
        )

        associado.save()
        # Criando um CartaoConvenioVolus fictício
        cartao = CartaoConvenioVolus.objects.create(nome="Convênio Volus", titular=associado,
                                                    valorLimite=df.at[index, 'Limite Crédito'], status="ATIVO")
        cartao.save()

        # Criando uma FaturaCartao fictícia
        fatura = FaturaCartao.objects.create(cartao=cartao, valor=df.at[index, 'Valor'], competencia=datetime.now().date())

        fatura()
        # Salvar o associado no banco de dados
        print("Salvando no banco de dados {} ...".format(associado.nomecompleto))

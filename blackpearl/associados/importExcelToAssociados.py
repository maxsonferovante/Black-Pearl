from datetime import datetime

from .models import Associado, FileUploadExcelModel
import pandas as pd
from blackpearl.settings import BASE_DIR

def import_excel_to_associado(objUploadFile):
    path = str(objUploadFile.arquivo)

    print(f' {BASE_DIR}/{path}')
    df = pd.read_excel(path)

    for index in df.index:
        associado = Associado.objects.create(
            ativo=df.at[index, 'ativo'],
            nome=df.at[index, 'nome'],
            sobrenome=df.at[index, 'sobrenome'],
            dataNascimento= datetime.fromisoformat(str(df.at[index, 'dataNascimento'])).date(),
            cpf=df.at[index, 'cpf'],
            email=df.at[index, 'email'],
            dddNumeroContato=df.at[index, 'dddNumeroContato'],
            numeroContato=df.at[index, 'numeroContato'],
            cep=df.at[index, 'cep'],
            logradouro=df.at[index, 'logradouro'],
            num=int(df.at[index, 'num']),
            bairro=df.at[index, 'bairro'],
            cidade=df.at[index, 'cidade'],
            estado=df.at[index, 'estado']
        )

        print("Salvando no banco de dados {} ...".format(associado.nome))


from blackpearl.convenios.models.models import Base
from blackpearl.associados.models import ASSOCIACAO_CHOICES
class RelatoriosConvenios:
    def __init__(self, convenio: Base):
        self.convenio = convenio

    def ativosEInativos(self):
        resultado = {
            'ativos':self.convenio.objects.filter(ativo=True).count(),
            'inativos':self.convenio.objects.filter(ativo=False).count()
        }
        return resultado
    def total(self):
        resultado = {
            'total_associados':self.convenio.objects.all().count(),
            'total_dependentes': self.convenio.objects.filter(dependentes__isnull=False).count()
        }
        return resultado

    def totalPorAssociacao(self):
        resultado = {}

        if self.convenio.__name__ == 'CartaoConvenioVolus':
            for associacao in ASSOCIACAO_CHOICES:
                resultado[associacao[1]] = self.convenio.objects.filter(titular__associacao=associacao[0]).count()
            return resultado

        if self.convenio.__name__ == 'Associado':
            for associacao in ASSOCIACAO_CHOICES:
                resultado[associacao[1]] = self.convenio.objects.filter(associacao=associacao[0]).count()
            return resultado

        if self.convenio.__name__ == 'ContratoPlanoSaude':
            for associacao in ASSOCIACAO_CHOICES:
                resultado[associacao[1]] = self.convenio.objects.filter(contratante__associacao=associacao[0]).count()
            return resultado

        if self.convenio.__name__ == 'ContratoPlanoSaudeDependente':
            for associacao in ASSOCIACAO_CHOICES:
                resultado[associacao[1]] = self.convenio.objects.filter(contrato__contratante__associacao=associacao[0]).count()
            return resultado

        if self.convenio.__name__ == 'ContratoPlanoOdontologico':
            for associacao in ASSOCIACAO_CHOICES:
                resultado[associacao[1]] = self.convenio.objects.filter(contratante__associacao=associacao[0]).count()
            return resultado

        if self.convenio.__name__ == 'ContratoPlanoOdontologicoDependente':
            for associacao in ASSOCIACAO_CHOICES:
                resultado[associacao[1]] = self.convenio.objects.filter(contrato__contratante__associacao=associacao[0]).count()
            return resultado

        return resultado




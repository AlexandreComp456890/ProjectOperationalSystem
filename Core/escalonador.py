from typing import List
from .processo import Processo
from Interface.enums import PoliticaEscalonamento
from Algoritmos.fcfs import FCFS
from Algoritmos.round_robin import RoundRobin
from Algoritmos.prioridade import PrioridadePreemptivo


class Escalonador:
    def __init__(self, filaProntos: list[Processo], politica: PoliticaEscalonamento):
        self.__fila_de_prontos: List[Processo] = filaProntos
        self.__politica: PoliticaEscalonamento = politica
        self.__processo_atual: Processo | None = None
        self.__algoritmo = self._instanciar_algoritmo(politica)

    # GETTERS
    @property
    def fila_de_prontos(self) -> List[Processo]:
        return self.__fila_de_prontos

    @property
    def processo_atual(self) -> Processo:
        return self.__processo_atual

    @property
    def politica(self) -> PoliticaEscalonamento:
        return self.__politica
    @property
    def algoritmo(self):   
        return self.__algoritmo

    # SETTERS
    @fila_de_prontos.setter
    def fila_de_prontos(self, nova_fila: List[Processo]):
        self.__fila_de_prontos = nova_fila

    @politica.setter
    def politica(self, nova_politica: PoliticaEscalonamento):
        print(f"[Escalonador] Mudando política de {self.__politica.value} para {nova_politica.value}")
        self.__politica = nova_politica
        self.__algoritmo = self._instanciar_algoritmo(nova_politica)
    @algoritmo.setter
    def algoritmo(self, novo_algoritmo):
        self.__algoritmo = novo_algoritmo

    # MÉTODOS
    # MÉTODO INTERNO PARA INSTANCIAR O ALGORITMO CERTO
    def _instanciar_algoritmo(self, politica: PoliticaEscalonamento):
        if politica == PoliticaEscalonamento.FCFS:
            return FCFS()
        elif politica == PoliticaEscalonamento.RR:
            return RoundRobin(quantum=2)   # Quantum configurável
        elif politica == PoliticaEscalonamento.PRIORIDADE:
            return PrioridadePreemptivo(quantum=2)
        else:
            raise ValueError(f"Política {politica} não reconhecida!")

    # MÉTODOS
    def AdicionarProcesso(self, processo: Processo):
        if processo not in self.__fila_de_prontos:
            self.__fila_de_prontos.append(processo)

    def ObterProximoProcesso(self) -> Processo:
        if not self.__fila_de_prontos:
            self.__processo_atual = None
            return None

        # Agora quem decide é o algoritmo escolhido
        self.__processo_atual = self.__algoritmo.EscolherProximo(self.__fila_de_prontos)
        return self.__processo_atual

    def Preemptar(self):
        # implementada futuramente
        pass

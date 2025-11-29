from enum import Enum

class Estado(Enum):
    NOVO = "Novo"
    PRONTO = "Pronto"
    EXECUTANDO = "Executando"
    BLOQUEADO = "Bloqueado"
    TERMINADO = "Terminado"

class TipoRecurso(Enum):
    CPU = "CPU"
    ES = "Entrada/Saída"
    MEMORIA = "Memória"

class PoliticaEscalonamento(Enum):
    FCFS = "First Come First Serve"
    RR = "Round Robin"
    PRIORIDADE_PREEMPTIVO = "Prioridade Preemptivo"
    PRIORIDADE_NAO_PREEMPTIVO = "Prioridade Não Preemptivo"
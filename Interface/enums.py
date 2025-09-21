from enum import Enum

class EstadoProcesso(Enum):
    NOVO = "Novo"
    PRONTO = "Pronto"
    EXECUTANDO = "Executando"
    BLOQUEADO = "Bloqueado"
    TERMINADO = "Terminado"

class EstadoThread(Enum):
    NOVA = "Nova"
    EXECUTANDO = "Executando"
    BLOQUEADA = "Bloqueada"
    TERMINADA = "Terminada"

class TipoRecurso(Enum):
    CPU = "CPU"
    ES = "Entrada/Saída"
    MEMORIA = "Memória"

class PoliticaEscalonamento(Enum):
    FCFS = "First Come First Serve"
    RR = "Round Robin"
    PRIORIDADE = "Prioridade"

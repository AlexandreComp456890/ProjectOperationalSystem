from Core.processo import Processo
from Core.recurso import Recurso, TipoRecurso
from Core.escalonador import Escalonador
from Core.gerenciadorMemoria import GerenciadorMemoria
from Core.gerenciadorRecursos import GerenciadorRecursos
from Core.sistemaOperacional import SistemaOperacional
from Interface.enums import PoliticaEscalonamento

# Criação de recursos
recurso1 = Recurso(1, TipoRecurso.CPU)
recurso2 = Recurso(2, TipoRecurso.MEMORIA)

# Gerenciadores
memoria = GerenciadorMemoria(memoria_total=10, tamanho_pagina=1)
recursos = GerenciadorRecursos()
recursos.recursos = recurso1
recursos.recursos = recurso2

# Escalonador
escalonador = Escalonador([], PoliticaEscalonamento.RR)

# Sistema Operacional
so = SistemaOperacional(escalonador, memoria, recursos)

# Criação de processos
p1 = so.criarProcesso("P1", prioridade=1, tamanho_memoria=1, tipo_recurso=recurso1)
p2 = so.criarProcesso("P2", prioridade=1, tamanho_memoria=1, tipo_recurso=recurso2)

# Força deadlock real: P1 quer recurso2, P2 quer recurso1
recursos.requisitarRecurso(p1, recurso2)  # P1 bloqueia porque recurso2 ocupado por P2
recursos.requisitarRecurso(p2, recurso1)  # P2 bloqueia porque recurso1 ocupado por P1

print("\n=== SIMULANDO DEADLOCK REAL ===")
so.verificarDeadlock()

# Executa ciclos de CPU com deadlock persistente
for ciclo in range(1, 6):
    print(f"\n--- CICLO {ciclo} ---")
    so.verificarDeadlock()  # Detecta deadlock antes de cada ciclo
    so.escalonar()           # Executa processos (somente os que não estão bloqueados)
    so.mostrar_mapa_memoria()  # Mostra o mapa de memória

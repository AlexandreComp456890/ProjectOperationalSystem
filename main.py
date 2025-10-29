from Core.sistemaOperacional import SistemaOperacional
from Core.escalonador import Escalonador
from Core.gerenciadorMemoria import GerenciadorMemoria
from Core.gerenciadorRecursos import GerenciadorRecursos
from Interface.enums import PoliticaEscalonamento

# Inicializa os componentes principais
mem = GerenciadorMemoria(memoria_total=64, tamanho_pagina=8)
rec = GerenciadorRecursos()
esc = Escalonador([], PoliticaEscalonamento.FCFS)

so = SistemaOperacional(esc, mem, rec)

# Cria dois processos
p1 = so.criarProcesso("P1", prioridade=1, tamanho_memoria=20)
p2 = so.criarProcesso("P2", prioridade=2, tamanho_memoria=16)

so.mostrar_mapa_memoria()

# Simula execução
so.escalonar()

# Testa acesso de memória e falta de página
mem.acessar_endereco(p1, 2)
mem.acessar_endereco(p1, 5)  # tentativa inválida -> ERRO / falta de página

# Simula acessos de memória normais
mem.acessar_endereco(p1, 0)  # deve estar carregada
mem.acessar_endereco(p1, 1)  # deve estar carregada
mem.acessar_endereco(p1, 2)  # deve estar carregada

# Agora acessa uma página nova (válida mas ainda não carregada) -> gera falta real
mem.tabela_paginas[p1.id_processo].append(type(mem.tabela_paginas[p1.id_processo][0])(3, p1))
mem.acessar_endereco(p1, 3)  # falta de página real

# Finaliza um processo
so.finalizarProcesso(p1)

so.mostrar_mapa_memoria()
so.estatisticas_memoria()



# Simulação de Sistema Operacional

Linguagem a ser utilizada *Python*

## UML

<img src="Documentos/UML.jpg" alt="UML" width="800"/>

## Autores
 
- <a href="https://github.com/AlexandreComp456890"> Alexandre Rocha </a>  
- <a href="https://github.com/jhenifersgomes209"> Jhenifer Silva </a>
- <a href="https://github.com/YanSilva22"> Yan Silva </a> 

## Descrição Geral

Este projeto tem como objetivo simular os principais conceitos de um sistema operacional, com foco em *gerência de processos*, *escalonamento de CPU*, *prioridades*, *execução por quantum*, e uso de *threads*. A simulação é implementada em Python utilizando os princípios de POO (Programação Orientada a Objetos) e abstrações de interface.

## Objetivos do Projeto

- Simular a criação, execução, bloqueio e finalização de processos.
- Representar o funcionamento básico da CPU e da memória.
- Implementar três algoritmos de escalonamento:
  - *Round Robin*
  - *Shortest Job First (SJF)*
  - *Priority (com preempção)*
- Modelar threads de usuário e do sistema.

---

## Estrutura de Pastas

projeto_sistema_operacional/
│
├── escalonador/ # Módulos de escalonamento
│ ├── escalonados.py
│ ├── processo.py
│ ├── tabelaProcessos.py
│ ├── sistemaOperacional.py
│ ├── thread.py
│ └── threading_processo.py
│
├── Interface/ # Interfaces abstratas
│ └── IAlgorithmics.py
│
└── README.md # Este documento

## Componentes do Sistema

### Classe `SistemaOperacional`
Representa o sistema como um todo, com CPU e memória.

- `cpu`: Lista de booleanos indicando se as CPUs estão livres ou ocupadas.
- `memoria`: Memória disponível (float).

---

### Classe `Processo`
Classe abstrata que define o comportamento dos processos.

- Atributos:
  - `id_processo`: identificador único.
  - `prioridade`: valor numérico.
  - `tempo_exec`: tempo restante de execução.
  - `estado`: estado atual (NEW, READY, EXECUTED, BLOCKED, FINISHED).
  - `threads_filhas`: threads associadas.
- Métodos abstratos: `Criar()`, `Executar()`, `Bloquear()`, `Finalizar()`, `Threading()`.

---

### Classe `Thread` / `Threading`
Representam threads associadas a processos, podendo ser de usuário ou sistema.

- `id_thread`: identificador único.
- `euusuario`: booleano indicando se é de usuário (`True`) ou do sistema (`False`).

---

### Classe `TabelaProcessos`
Controla todos os processos no sistema.

- Métodos:
  - `AdicionarProcesso(processo)`
  - `RemoverProcesso(processo)`
  - `ListarProcessos()`

---

### Classe `Escalonador` (implements `IAlgorithmics`)
Responsável por implementar os algoritmos de escalonamento:

#### `round_robin()`
- Cada processo é executado por um tempo fixo (quantum).
- Se o processo não termina, ele retorna ao final da fila.
- Exibe mensagens de log sobre execução e finalização.

#### `shortest_job_first()`
- **Ainda não implementado**.
- Quando implementado, deve priorizar o processo com menor tempo restante de execução.

#### `priority()`
- Ordena os processos por prioridade (quanto menor o valor, maior a prioridade).
- Executa o processo de maior prioridade por um quantum.
- Se não terminar, volta para a fila.

---

## Interface `IAlgorithmics`

Define os métodos que os escalonadores devem implementar:

- `shortest_job_first()`
- `round_robin()`
- `priority()`

Isso permite a flexibilidade de troca de diferentes estratégias de escalonamento sem alterar o código de execução.
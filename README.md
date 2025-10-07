# 🖥️ Simulador de Sistema Operacional  

## 📌 Descrição  
Este projeto é um **simulador educacional de Sistema Operacional**, desenvolvido em **Python 3**, com foco em demonstrar conceitos fundamentais de:  
- **Processos e Threads**  
- **Escalonamento de CPU**  
- **Gerenciamento de Memória**  
- **Gerenciamento de Recursos e Deadlocks (não Implementado)**  
- **Entrada e Saída (não Implementado)**  
- **Sistema de Arquivos (não Implementado)**  

O simulador executa em **linha de comando** e tem como objetivo reproduzir, de forma didática, as principais funções de um Sistema Operacional.  

## UML

<img src="Documentos/UML.jpg" alt="UML" width="800"/>

## 📂 Estrutura do Projeto  

```plaintext
ProjectOperationalSystem/
│── Algoritmos/                 
│   ├── fcfs.py                 # FCFS
│   ├── prioridade.py           # Prioridade Preemptivo
│   ├── round_robin.py          # Round Robin
│
│── Core/                      
│   ├── processo.py             # Classe Processo (PCB simplificado)
│   ├── thread.py               # Classe Thread (TCB simplificado)
│   ├── roundrobin.py           # Algoritmo de escalonamento Round Robin
│   ├── prioridade_preemptivo.py# Algoritmo de escalonamento por prioridade
│   ├── fcfs.py                 # Algoritmo de escalonamento FCFS
│   ├── escalonador.py          # Gerencia a política de escalonamento
│   ├── gerenciadorMemoria.py   # Gerencia memória (a expandir com paginação)
│   ├── gerenciadorRecursos.py  # Gerencia recursos e deadlocks
│   ├── recurso.py              # Classe de recurso do sistema
│   ├── sistemaOperacional.py   # Classe principal do SO
│
│── Interface/                  
│   ├── IAlgorithmics.py        # Interface dos algoritmos de escalonamento
│   ├── enums.py                # Enumerações de estados, políticas, recursos
│
│── main.py                     # Arquivo principal para testes
│── README.md                   # Documentação do projeto
│── requirements.txt            # Dependências (se necessário)
```

## ⚙️ Funcionalidades Implementadas  

✅ **Processos (PCB simplificado)**  
- PID, prioridade, tempo de execução, estado, threads filhas, dependências.  
- Operações: `Executar`, `Bloquear`, `Pronto`, `Finalizar`.  

✅ **Threads (TCB simplificado)**  
- ID, tempo de execução, estado, processo pai.  

✅ **Escalonadores de CPU**  
- **FCFS (First Come, First Served)**  
- **Round Robin (com quantum configurável)**  
- **Prioridade Preemptiva**  
- Impressão em tabela do estado dos processos a cada rodada.  

✅ **Gerenciamento de Recursos**  
- Alocação e liberação de recursos.  
- Estrutura para detecção de deadlock (a ser expandida).  

✅ **Sistema Operacional (núcleo)**  
- Integra processos, escalonador, gerenciador de memória e recursos.  

## 🚧 Funcionalidades em Desenvolvimento  

- 🔄 **Paginação simples** (gerenciamento de memória)  
- 💾 **Sistema de Arquivos** (criação, leitura, escrita, exclusão, diretórios)  
- ⌨️ **Entrada/Saída** (simulação de dispositivos e interrupções)  
- 📊 **Métricas de desempenho** (turnaround, tempo de espera, throughput, utilização de CPU)  
- 📝 **Log textual** com clock lógico  
- ⚡ **Interface CLI** para configurar política de escalonamento, quantum, memória etc.  

## ▶️ Como Executar  

1. Clone o repositório:  
   ```bash
   git clone https://github.com/AlexandreComp456890/ProjectOperationalSystem
   cd ProjectOperationalSystem
2. Execute o programa principal:
   ```bash
   python main.py

## 🎮 Execução (`main.py`)

Ao rodar o arquivo `main.py`, o simulador inicia em modo de **linha de comando**, exibindo um menu interativo com três opções de política de escalonamento:

- **FCFS (First Come, First Served)**
- **Round Robin**
- **Prioridade Preemptiva**

<img src="Documentos/UML_SistemasOperacionais.svg" alt="menu" width="1000"/>

---

### 🧩 Funcionamento

1. O sistema gera automaticamente um conjunto de **processos aleatórios**, cada um contendo:
   - Um **identificador** (ex: `P1`, `P2`, `P3`)
   - Uma **prioridade aleatória** (de 1 a 5)
   - Um **tempo de execução aleatório**

2. Após selecionar o algoritmo de escalonamento desejado, ele é aplicado sobre essa fila de processos.

3. A cada rodada, o sistema exibe uma **tabela formatada**, mostrando:
   - 🆔 **ID do processo**
   - ⚙️ **Prioridade**
   - ⏱️ **Tempo restante de execução**
   - 📊 **Estado atual** (*Pronto*, *Executando* ou *Finalizado*)
   - ⌛ **Tempo executado na rodada**

FCFS:

<img src="Documentos/FCFS.PNG" alt="FCFS" width="500"/>

Rund Robin:

<img src="Documentos/RR.PNG" alt="RR" width="500"/>

Prioridade Preemptiva:

<img src="Documentos/PP.PNG" alt="PP" width="500"/>

4. O simulador repete esse ciclo até que **todos os processos sejam finalizados**, encerrando com a mensagem:

   ```bash
   [SO] Todos os processos foram finalizados!

## 📊 Progresso do Projeto

O grupo estima que o projeto atingiu aproximadamente **40% de conclusão**.  
As principais funcionalidades implementadas até o momento incluem:

- Criação e gerenciamento de processos e threads;  
- Implementação dos algoritmos de escalonamento **FCFS**, **Round Robin** e **Prioridade Preemptiva**;  
- Estrutura base do **Sistema Operacional**, integrando componentes centrais;  
- Impressão formatada da execução dos processos no terminal.

As próximas etapas incluem o desenvolvimento dos módulos de **memória**, **recursos**, **sistema de arquivos** e **entrada/saída**.

## Autores
 
- <a href="https://github.com/AlexandreComp456890"> Alexandre Rocha </a>  
- <a href="https://github.com/jhenifersgomes209"> Jhenifer Silva </a>
- <a href="https://github.com/YanSilva22"> Yan Silva </a> 
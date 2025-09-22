# 🖥️ Simulador de Sistema Operacional  

## 📌 Descrição  
Este projeto é um **simulador educacional de Sistema Operacional**, desenvolvido em **Python 3**, com foco em demonstrar conceitos fundamentais de:  
- **Processos e Threads**  
- **Escalonamento de CPU**  
- **Gerenciamento de Memória**  
- **Gerenciamento de Recursos e Deadlocks**  
- **Entrada e Saída**  
- **Sistema de Arquivos**  

O simulador executa em **linha de comando** e tem como objetivo reproduzir, de forma didática, as principais funções de um núcleo de Sistema Operacional.  

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

## Autores
 
- <a href="https://github.com/AlexandreComp456890"> Alexandre Rocha </a>  
- <a href="https://github.com/jhenifersgomes209"> Jhenifer Silva </a>
- <a href="https://github.com/YanSilva22"> Yan Silva </a> 
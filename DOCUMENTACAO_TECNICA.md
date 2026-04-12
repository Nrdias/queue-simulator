# Documentação Técnica - Simulador de Rede de Filas

## Estrutura do Projeto

```
queue-simulator/
├── main.py                    # Entrada principal - Define os cenários
├── queue_simulator.py         # Classe simuladora de fila
├── README.md                  # Documentação geral
├── RESPOSTAS_ATIVIDADE.md    # Respostas completas da atividade
├── RESULTADOS_SIMULACAO.txt  # Resultados brutos
└── DOCUMENTACAO_TECNICA.md   # Este arquivo
```

## Componentes

### 1. QueueSimulator (queue_simulator.py)

Classe que implementa a simulação de uma fila M/M (ou G/G com distribuição geral).

**Parâmetros:**
- `servers`: Número de servidores (c)
- `capacity`: Capacidade máxima do sistema (N)
- `arrival_min`, `arrival_max`: Intervalo para geração de tempos entre chegadas
- `service_min`, `service_max`: Intervalo para geração de tempos de serviço

**Métodos principales:**
- `run()`: Executa a simulação com 100.000 eventos
- `report()`: Exibe os resultados da simulação
- `generate_random_interval()`: Gera números aleatórios uniforme
- `schedule_event()`: Agenda eventos na fila de prioridade

### 2. Modelo de Simulação

O simulador utiliza:
- **Simulação de Eventos Discretos**: Processa eventos de chegada (A) e saída (D)
- **Fila de Prioridade**: Eventos ordenados pelo tempo de ocorrência
- **Distribuição Uniforme**: Tempos gerados aleatoriamente dentro dos intervalos

### 3. Rede de Filas (Tandem)

```
Exterior → [Fila 1: G/G/2/3] → [Fila 2: G/G/1/5] → Exterior
```

**Características:**
- Fila 1 recebe clientes do exterior
- 100% dos clientes que saem da Fila 1 vão para a Fila 2
- Fila 2 tem saída para o exterior

## Resultados Esperados

### Fila 1 (G/G/2/3)
- Capacidade: 3 clientes
- Servidores: 2
- Taxa de bloqueio baixa (aprox. 0.1%)
- Distribuição concentrada em estados 1-2

### Fila 2 (G/G/1/5)
- Capacidade: 5 clientes
- Servidor: 1
- Taxa de bloqueio moderada (aprox. 0.8%)
- Distribuição mais dispersa entre estados

## Algoritmo de Simulação

```
1. Inicializar: estado = 0, tempo = 0, fila_eventos = {}
2. Agendar primeiro evento de chegada em t=2.0
3. Enquanto eventos existirem:
   a. Pop primeiro evento (menor tempo)
   b. Atualizar tempo acumulado no estado atual
   c. Se evento é chegada (A):
      - Se fila < capacidade:
        * Incrementar fila
        * Se fila <= servidores:
          - Agendar saída com tempo de serviço
      - Senão: contar como cliente perdido
      - Agendar próxima chegada
   d. Se evento é saída (D):
      - Decrementar fila
      - Se fila >= servidores:
        * Agendar próxima saída
```

## Métricas Calculadas

- **Total time**: Tempo total de simulação
- **Lost customers**: Número de clientes bloqueados
- **State times**: Tempo acumulado em cada estado
- **Probabilities**: Probabilidade de cada estado (time/total_time)

## Requisitos de Execução

- Python 3.x (testado em 3.8+)
- Nenhuma dependência externa

## Como Executar

```bash
python main.py
```

Isso executará ambos os cenários e exibirá os resultados na saída padrão.

## Extensões Possíveis

1. Implementar múltiplas filas em rede complexa
2. Usar distribuições não-uniformes (exponencial, Poisson, etc.)
3. Adicionar prioridades de clientes
4. Implementar políticas de escalonamento (FIFO, LIFO, Round-Robin)
5. Adicionar coleta de dados para análise estatística


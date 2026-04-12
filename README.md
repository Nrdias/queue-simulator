# Queue Simulator - Segunda Etapa

Simulador de Rede de Filas desenvolvido em Python para a segunda etapa da disciplina.

## Requisitos

- Python 3.x

## Execução

Para executar o simulador e gerar os resultados das simulações:

```bash
python main.py
```

## Respostas da Atividade

### 1. Link para o código fonte do grupo:
```
/Users/natandias/workspace/queue-simulator
```

### 2. Fila 1 - G/G/2/3
**Parâmetros:** 2 servidores, capacidade 3, chegadas uniforme [1..4], atendimento uniforme [3..4]

```
Total time: 125080.0260
Lost customers: 98

State Distribution:
State 0: 2454.3680 (1.96%)
State 1: 70381.0888 (56.27%)
State 2: 48114.3733 (38.47%)
State 3: 4130.1960 (3.30%)
```

### 3. Fila 2 - G/G/1/5
**Parâmetros:** 1 servidor, capacidade 5, chegadas uniforme [1..4], atendimento uniforme [2..3]

```
Total time: 126176.8146
Lost customers: 853

State Distribution:
State 0: 2180.9755 (1.73%)
State 1: 22375.6919 (17.73%)
State 2: 32092.0771 (25.43%)
State 3: 32803.3817 (26.00%)
State 4: 28316.8062 (22.44%)
State 5: 8407.8822 (6.66%)
```

## Análise

- A Fila 1 (G/G/2/3) com 2 servidores e capacidade 3 apresenta uma taxa de perda de apenas 98 clientes em 100.000 tentativas.
- A Fila 2 (G/G/1/5) com 1 servidor e capacidade 5 apresenta uma taxa de perda significativamente maior (853 clientes), indicando que um único servidor não é suficiente para o fluxo de clientes.
- Na Fila 1, o sistema passa a maior parte do tempo nos estados 1 e 2 (94.74%), indicando que geralmente há clientes na fila.
- Na Fila 2, a distribuição é mais dispersa, com concentração nos estados 2 e 3 (51.43%), mostrando maior variabilidade nos estados do sistema.

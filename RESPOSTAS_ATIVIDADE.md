# RESPOSTAS - SEGUNDA ETAPA DA ATIVIDADE
## Simulador de Rede de Filas

---

## 1. Link para o código fonte do grupo:

```
https://github.com/[usuario]/queue-simulator
```

**Ou acesso local:**
```
/Users/natandias/workspace/queue-simulator
```

---

## 2. Simulação: Fila 1 - G/G/2/3

**Configuração:**
- Notação: G/G/2/3
- Número de servidores: 2
- Capacidade do sistema: 3
- Distribuição de chegadas: Uniforme entre 1 e 4
- Distribuição de atendimento: Uniforme entre 3 e 4
- Número de clientes simulados: 100.000

**Resultados:**

```
Total time: 125080.0260
Lost customers: 98

State Distribution (Tempo acumulado e Probabilidade):
┌───────┬────────────────┬──────────────┐
│ State │ Accumulated    │ Probability  │
│       │ Time           │              │
├───────┼────────────────┼──────────────┤
│   0   │ 2454.3680      │  1.96%       │
│   1   │ 70381.0888     │ 56.27%       │
│   2   │ 48114.3733     │ 38.47%       │
│   3   │ 4130.1960      │  3.30%       │
└───────┴────────────────┴──────────────┘
```

**Interpretação:**
- O sistema com 2 servidores apresenta uma taxa de bloqueio muito baixa (98 perdas em 100.000 tentativas = 0,098%)
- A maioria do tempo o sistema está em estado 1 (um cliente sendo atendido ou aguardando) com 56,27%
- A capacidade de 3 unidades é frequentemente utilizada (41,77% do tempo em estados 2 e 3)

---

## 3. Simulação: Fila 2 - G/G/1/5

**Configuração:**
- Notação: G/G/1/5
- Número de servidores: 1
- Capacidade do sistema: 5
- Distribuição de chegadas: Uniforme entre 1 e 4 (clientes provenientes da Fila 1)
- Distribuição de atendimento: Uniforme entre 2 e 3
- Número de clientes simulados: 100.000

**Resultados:**

```
Total time: 126176.8146
Lost customers: 853

State Distribution (Tempo acumulado e Probabilidade):
┌───────┬────────────────┬──────────────┐
│ State │ Accumulated    │ Probability  │
│       │ Time           │              │
├───────┼────────────────┼──────────────┤
│   0   │ 2180.9755      │  1.73%       │
│   1   │ 22375.6919     │ 17.73%       │
│   2   │ 32092.0771     │ 25.43%       │
│   3   │ 32803.3817     │ 26.00%       │
│   4   │ 28316.8062     │ 22.44%       │
│   5   │ 8407.8822      │  6.66%       │
└───────┴────────────────┴──────────────┘
```

**Interpretação:**
- O sistema com 1 servidor apresenta uma taxa de bloqueio significativamente maior (853 perdas em 100.000 = 0,853%)
- O sistema está com muita frequência em estados altos (2, 3, 4), indicando formação de fila
- O estado 3 é o mais provável (26,00%), mostrando que frequentemente há 3 clientes no sistema
- A capacidade de 5 é quase sempre utilizada, com 6,66% do tempo em estado pleno

---

## Considerações Finais

A rede de filas em tandem (Fila 1 → Fila 2) mostra claramente o impacto do número de servidores:

1. **Fila 1 (2 servidores)**: Sistema mais eficiente com taxa de bloqueio muy baixa
2. **Fila 2 (1 servidor)**: Sistema com maior congestionamento e taxa de bloqueio mais alta

Isso demonstra por que o uso de múltiplos servidores é importante para sistemas com alta demanda de entrada.


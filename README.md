# Queue Simulator - Simulador de Rede de Filas

> Desenvolvido por: Bruno Panizzi, Enzo Zortéa, Gustavo Amaro e Natan Dias

Simulador de filas com **eventos discretos** em Python, com suporte a:

- rede de filas com topologia arbitrária,
- roteamento probabilístico entre filas,
- laços de realimentação (fila voltando para ela mesma),
- saída do sistema,
- semente aleatória para resultados reprodutíveis,
- capacidade finita **ou infinita** (`capacity=None`).

---

## Requisitos

- Python 3.8+
- Nenhuma dependência externa

---

## Como executar

```bash
python main.py
```

O `main.py` atual está configurado com a topologia de 3 filas da atividade.

---

## Conceitos do simulador

### Tipos de evento internos

- `E`: chegada externa
- `A`: chegada roteada de outra fila
- `D`: término de serviço (saída da fila)
- `X`: evento de saída com destino (ou saída do sistema)

### Estado de cada fila

O estado é o número de clientes no sistema da fila (em serviço + esperando).

---

## Uso da classe `QueueSimulator`

## 1) Modo rede (recomendado)

### Assinatura relevante

```python
QueueSimulator(
    queues=...,                # obrigatório no modo rede
    routing=...,               # obrigatório no modo rede
    seed=None,
    max_random_numbers=100000,
    initial_external_arrival=2.0,
)
```

### Estrutura de `queues`

`queues` é um dicionário onde cada chave é o nome da fila (`"Q1"`, `"Q2"`, etc):

```python
queues = {
    "Q1": {
        "servers": 1,          # obrigatório
        "capacity": None,      # None => infinita | int >= 1 => finita
        "arrival_min": 2.0,    # opcional (se definido junto com arrival_max, gera chegadas externas)
        "arrival_max": 4.0,    # opcional
        "service_min": 1.0,    # obrigatório
        "service_max": 2.0,    # obrigatório
    },
    ...
}
```

### Estrutura de `routing`

`routing` define, para cada fila de origem, as probabilidades de destino após `D`:

```python
routing = {
    "Q1": {"Q2": 0.8, "Q3": 0.2},
    "Q2": {"Q1": 0.3, "Q3": 0.5, None: 0.2},
    "Q3": {"Q2": 0.7, None: 0.3},
}
```

Regras:

- A soma das probabilidades de cada fila **deve ser 1.0**.
- `None` significa saída do sistema.
- É permitido rotear para a própria fila (realimentação), ex: `"Q2": {"Q2": 0.1, None: 0.9}`.
- Destinos também podem ser informados como `"EXIT"`, `"exit"`, `"OUT"`, `"out"` (normalizados para `None`).

### Fontes externas

Uma fila é fonte externa se **ambos** estiverem definidos:

- `arrival_min`
- `arrival_max`

Se não estiverem, a fila recebe apenas chegadas roteadas de outras filas.

---

## Parâmetros importantes

- `seed`: fixa a sequência pseudoaleatória (execuções reprodutíveis)
- `max_random_numbers`: limite de números aleatórios usados na simulação
- `initial_external_arrival`: instante inicial da primeira chegada externa em cada fila fonte

---

## Capacidade infinita

Para modelar fila sem limite de buffer:

```python
"capacity": None
```

No relatório, aparece como `∞`.

---

## Saída do relatório

No modo rede, o relatório mostra:

- tempo total simulado,
- clientes que saíram do sistema,
- para cada fila:
  - perdas por capacidade (`Lost customers`),
  - atendimentos concluídos,
  - tempo acumulado por estado,
  - probabilidade empírica por estado.

---

## Observações de modelagem

- O simulador usa distribuição **uniforme** para intervalos de chegada/serviço (`min..max`).
- Probabilidades de roteamento são aplicadas com sorteio uniforme em `[0,1)` e verificação por faixa acumulada.
- A simulação termina quando acaba o orçamento de números aleatórios (`max_random_numbers`) ou não há mais eventos.

---

## Erros comuns

- Probabilidades de roteamento não somam 1.0 para alguma fila.
- Destino de roteamento aponta para fila inexistente.
- Fila sem parâmetros obrigatórios (`servers`, `service_min`, `service_max`).
- `capacity` inválida (deve ser `None` ou inteiro `>= 1`).

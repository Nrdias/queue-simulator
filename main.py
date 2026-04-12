
from queue_simulator import QueueSimulator

if __name__ == "__main__":
    print("=" * 60)
    print("SIMULADOR DE REDE DE FILAS - SEGUNDA ETAPA")
    print("=" * 60)
    print()
    
    # Fila 1: G/G/2/3 - 2 servidores, capacidade 3, chegadas entre 1..4, atendimento entre 3..4
    print("FILA 1: G/G/2/3")
    print("Parâmetros: 2 servidores, capacidade 3")
    print("Chegadas: uniforme entre 1 e 4")
    print("Atendimento: uniforme entre 3 e 4")
    print()
    scenario1 = QueueSimulator(servers=2, capacity=3, arrival_min=1.0, arrival_max=4.0, service_min=3.0, service_max=4.0)
    scenario1.run()
    scenario1.report()
    
    print()
    print("=" * 60)
    print()
    
    # Fila 2: G/G/1/5 - 1 servidor, capacidade 5, chegadas entre 1..4 (da Fila 1), atendimento entre 2..3
    print("FILA 2: G/G/1/5")
    print("Parâmetros: 1 servidor, capacidade 5")
    print("Chegadas: uniforme entre 1 e 4 (clientes da Fila 1)")
    print("Atendimento: uniforme entre 2 e 3")
    print()
    scenario2 = QueueSimulator(servers=1, capacity=5, arrival_min=1.0, arrival_max=4.0, service_min=2.0, service_max=3.0)
    scenario2.run()
    scenario2.report()
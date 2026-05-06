from queue_simulator import QueueSimulator

if __name__ == "__main__":
    print("=" * 70)
    print("SIMULADOR DE REDE DE FILAS - TOPOLOGIA COM 3 FILAS")
    print("=" * 70)
    print()

    queues = {
        "Q1": {
            "servers": 1,
            "capacity": None,  # capacidade infinita
            "arrival_min": 2.0,
            "arrival_max": 4.0,
            "service_min": 1.0,
            "service_max": 2.0,
        },
        "Q2": {"servers": 2, "capacity": 5, "service_min": 4.0, "service_max": 6.0},
        "Q3": {"servers": 2, "capacity": 10, "service_min": 5.0, "service_max": 15.0},
    }

    routing = {
        "Q1": {"Q2": 0.8, "Q3": 0.2},
        "Q2": {"Q1": 0.3, "Q3": 0.5, None: 0.2},
        "Q3": {"Q2": 0.7, None: 0.3},
    }

    simulator = QueueSimulator(
        queues=queues,
        routing=routing,
        max_random_numbers=100000,
        initial_external_arrival=2.0,
        # seed=42,  # para execuções consistentes
    )

    simulator.run()
    simulator.report()

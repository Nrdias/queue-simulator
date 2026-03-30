
from queue_simulator import QueueSimulator

if __name__ == "__main__":
    scenario1 = QueueSimulator(1, 5, 2.0, 5.0, 3.0, 5.0)
    scenario1.run()
    scenario1.report()

    scenario2 = QueueSimulator(2, 5, 2.0, 5.0, 3.0, 5.0)
    scenario2.run()
    scenario2.report()
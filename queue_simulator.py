import random

class QueueSimulator:
    def __init__(self, servers, capacity, arrival_min, arrival_max, service_min, service_max):
        self.servers = servers
        self.capacity = capacity
        self.arrival_min = arrival_min
        self.arrival_max = arrival_max
        self.service_min = service_min
        self.service_max = service_max

        self.randoms_left = 100000
        self.current_time = 0.0
        self.queue_length = 0
        self.loss_count = 0
        self.state_times = [0.0] * (capacity + 1)
        self.events = []

    def generate_random_interval(self, min_value, max_value):
        if self.randoms_left > 0:
            self.randoms_left -= 1
            value = random.random()
            return (max_value - min_value) * value + min_value
        return None

    def schedule_event(self, event_time, event_type):
        self.events.append((event_time, event_type))
        self.events.sort()

    def run(self):
        self.schedule_event(2.0, 'A')

        while self.randoms_left > 0 and self.events:
            event_time, event_type = self.events.pop(0)
            elapsed_time = event_time - self.current_time
            self.state_times[self.queue_length] += elapsed_time
            self.current_time = event_time

            if event_type == 'A':
                if self.queue_length < self.capacity:
                    self.queue_length += 1
                    if self.queue_length <= self.servers:
                        service_time = self.generate_random_interval(self.service_min, self.service_max)
                        if service_time is not None:
                            self.schedule_event(self.current_time + service_time, 'D')
                else:
                    self.loss_count += 1

                arrival_interval = self.generate_random_interval(self.arrival_min, self.arrival_max)
                if arrival_interval is not None:
                    self.schedule_event(self.current_time + arrival_interval, 'A')

            elif event_type == 'D':
                self.queue_length -= 1
                if self.queue_length >= self.servers:
                    service_time = self.generate_random_interval(self.service_min, self.service_max)
                    if service_time is not None:
                        self.schedule_event(self.current_time + service_time, 'D')

    def report(self):
        total_time = sum(self.state_times)
        print(f"--- Results G/G/{self.servers}/{self.capacity} ---")
        print(f"Total time: {total_time:.4f}")
        print(f"Lost customers: {self.loss_count}")
        print(f"{'State':<8} | {'Accumulated time':<18} | {'Probability'}")
        for state, time_in_state in enumerate(self.state_times):
            probability = (time_in_state / total_time) * 100 if total_time > 0 else 0
            print(f"{state:<8} | {time_in_state:<18.4f} | {probability:.2f}%")
        print("-" * 50)
import heapq
import random


class QueueSimulator:
    def __init__(
        self,
        servers=None,
        capacity=None,
        arrival_min=None,
        arrival_max=None,
        service_min=None,
        service_max=None,
        seed=None,
        *,
        queues=None,
        routing=None,
        max_random_numbers=100000,
        initial_external_arrival=2.0,
    ):
        self.rng = random.Random(seed)
        self.randoms_left = max_random_numbers
        self.current_time = 0.0
        self.initial_external_arrival = initial_external_arrival

        self._event_seq = 0
        self.events = []
        self._NO_SAMPLE = object()

        # Legacy single-queue mode (backward compatible)
        if queues is None:
            if None in (servers, service_min, service_max):
                raise ValueError(
                    "In single-queue mode, servers/service_min/service_max are required"
                )

            queues = {
                "Q1": {
                    "servers": servers,
                    "capacity": capacity,
                    "arrival_min": arrival_min,
                    "arrival_max": arrival_max,
                    "service_min": service_min,
                    "service_max": service_max,
                }
            }
            routing = {"Q1": {None: 1.0}}
            self._legacy_mode = True
        else:
            self._legacy_mode = False
            if routing is None:
                raise ValueError("In network mode, routing must be provided")

        self.queues = self._normalize_queues(queues)
        self.routing = self._normalize_routing(routing)
        self._validate_routing()

        self.queue_ids = list(self.queues.keys())
        self.queue_lengths = {qid: 0 for qid in self.queue_ids}
        self.loss_count_by_queue = {qid: 0 for qid in self.queue_ids}
        self.state_times = {}
        for qid in self.queue_ids:
            capacity = self.queues[qid]["capacity"]
            if capacity is None:
                self.state_times[qid] = {0: 0.0}
            else:
                self.state_times[qid] = [0.0] * (capacity + 1)

        self.completed_services = {qid: 0 for qid in self.queue_ids}
        self.exited_system = 0

        # Backward compatibility fields
        if self._legacy_mode:
            self.queue_length = 0
            self.loss_count = 0

    def _normalize_queues(self, queues):
        if not isinstance(queues, dict) or not queues:
            raise ValueError("queues must be a non-empty dict")

        normalized = {}
        for qid, cfg in queues.items():
            if not isinstance(cfg, dict):
                raise ValueError(f"Queue config for {qid} must be a dict")

            required = ["servers", "service_min", "service_max"]
            for key in required:
                if key not in cfg:
                    raise ValueError(f"Queue {qid} is missing required field: {key}")

            capacity = cfg.get("capacity")
            if capacity in ("inf", "INF", "infinite", "INFINITE"):
                capacity = None
            if capacity is not None:
                if not isinstance(capacity, int) or capacity < 1:
                    raise ValueError(
                        f"Queue {qid} capacity must be None (infinite) or integer >= 1"
                    )

            normalized[qid] = {
                "servers": cfg["servers"],
                "capacity": capacity,
                "arrival_min": cfg.get("arrival_min"),
                "arrival_max": cfg.get("arrival_max"),
                "service_min": cfg["service_min"],
                "service_max": cfg["service_max"],
            }
        return normalized

    def _normalize_routing(self, routing):
        if not isinstance(routing, dict):
            raise ValueError("routing must be a dict")

        normalized = {}
        for origin, rule in routing.items():
            if isinstance(rule, dict):
                items = list(rule.items())
            elif isinstance(rule, list):
                items = rule
            else:
                raise ValueError(
                    f"Routing rule for {origin} must be dict or list of (dest, prob)"
                )

            normalized[origin] = []
            for destination, probability in items:
                dest = self._normalize_destination(destination)
                normalized[origin].append((dest, float(probability)))

        return normalized

    def _normalize_destination(self, destination):
        if destination in (None, "EXIT", "exit", "OUT", "out"):
            return None
        return destination

    def _validate_routing(self):
        for qid in self.queues:
            if qid not in self.routing:
                raise ValueError(f"Missing routing rule for queue {qid}")

        for origin, options in self.routing.items():
            if origin not in self.queues:
                raise ValueError(f"Routing origin {origin} does not exist in queues")
            if not options:
                raise ValueError(f"Routing for {origin} cannot be empty")

            total = 0.0
            for destination, probability in options:
                if probability < 0:
                    raise ValueError(
                        f"Routing probability cannot be negative ({origin} -> {destination})"
                    )
                if destination is not None and destination not in self.queues:
                    raise ValueError(
                        f"Routing destination {destination} from {origin} does not exist"
                    )
                total += probability

            if abs(total - 1.0) > 1e-9:
                raise ValueError(
                    f"Routing probabilities for {origin} must sum to 1 (got {total})"
                )

    def _next_random(self):
        if self.randoms_left <= 0:
            return None
        self.randoms_left -= 1
        return self.rng.random()

    def generate_random_interval(self, min_value, max_value):
        if min_value is None or max_value is None:
            return None

        r = self._next_random()
        if r is None:
            return None
        return (max_value - min_value) * r + min_value

    def _sample_destination(self, origin_queue):
        r = self._next_random()
        if r is None:
            return self._NO_SAMPLE

        acc = 0.0
        options = self.routing[origin_queue]
        for destination, probability in options:
            acc += probability
            if r < acc:
                return destination

        # numerical guard (r can be very close to 1)
        return options[-1][0]

    def schedule_event(self, event_time, event_type, queue_id, destination=None):
        self._event_seq += 1
        heapq.heappush(
            self.events,
            (event_time, self._event_seq, event_type, queue_id, destination),
        )

    def _accumulate_state_times(self, elapsed_time):
        for qid in self.queue_ids:
            size = self.queue_lengths[qid]
            bucket = self.state_times[qid]
            if isinstance(bucket, list):
                bucket[size] += elapsed_time
            else:
                bucket[size] = bucket.get(size, 0.0) + elapsed_time

    def _attempt_arrival(self, queue_id):
        cfg = self.queues[queue_id]

        capacity = cfg["capacity"]
        if capacity is None or self.queue_lengths[queue_id] < capacity:
            self.queue_lengths[queue_id] += 1

            if self.queue_lengths[queue_id] <= cfg["servers"]:
                service_time = self.generate_random_interval(
                    cfg["service_min"], cfg["service_max"]
                )
                if service_time is not None:
                    self.schedule_event(
                        self.current_time + service_time,
                        "D",
                        queue_id,
                    )
        else:
            self.loss_count_by_queue[queue_id] += 1

    def _capacity_label(self, capacity):
        return "∞" if capacity is None else str(capacity)

    def _iter_states(self, queue_id):
        if self._legacy_mode and (
            isinstance(self.state_times, list)
            or (
                isinstance(self.state_times, dict)
                and (not self.state_times or isinstance(next(iter(self.state_times.keys())), int))
            )
        ):
            bucket = self.state_times
        else:
            bucket = self.state_times[queue_id]

        if isinstance(bucket, list):
            return list(enumerate(bucket))
        return sorted(bucket.items(), key=lambda x: x[0])

    def run(self):
        # schedule first external arrivals for queues that have exogenous arrivals
        for qid, cfg in self.queues.items():
            if cfg["arrival_min"] is not None and cfg["arrival_max"] is not None:
                self.schedule_event(self.initial_external_arrival, "E", qid)

        while self.randoms_left > 0 and self.events:
            event_time, _, event_type, queue_id, destination = heapq.heappop(self.events)

            elapsed_time = event_time - self.current_time
            self._accumulate_state_times(elapsed_time)
            self.current_time = event_time

            if event_type == "E":
                # external arrival into queue_id
                self._attempt_arrival(queue_id)

                # schedule next external arrival for this queue
                arrival_interval = self.generate_random_interval(
                    self.queues[queue_id]["arrival_min"],
                    self.queues[queue_id]["arrival_max"],
                )
                if arrival_interval is not None:
                    self.schedule_event(self.current_time + arrival_interval, "E", queue_id)

            elif event_type == "A":
                # routed arrival into queue_id
                self._attempt_arrival(queue_id)

            elif event_type == "D":
                # service completion in queue_id
                self.queue_lengths[queue_id] -= 1
                self.completed_services[queue_id] += 1

                if self.queue_lengths[queue_id] >= self.queues[queue_id]["servers"]:
                    service_time = self.generate_random_interval(
                        self.queues[queue_id]["service_min"],
                        self.queues[queue_id]["service_max"],
                    )
                    if service_time is not None:
                        self.schedule_event(
                            self.current_time + service_time,
                            "D",
                            queue_id,
                        )

                next_destination = self._sample_destination(queue_id)
                # Exit event includes destination (can be None/external or any queue, including itself)
                if next_destination is not self._NO_SAMPLE:
                    self.schedule_event(self.current_time, "X", queue_id, next_destination)

            elif event_type == "X":
                # route to destination or leave system
                if destination is None:
                    self.exited_system += 1
                else:
                    self.schedule_event(self.current_time, "A", destination)

        # Backward compatibility fields
        if self._legacy_mode:
            self.queue_length = self.queue_lengths["Q1"]
            self.loss_count = self.loss_count_by_queue["Q1"]
            self.state_times = self.state_times["Q1"]

    def report(self):
        if self._legacy_mode:
            states = self._iter_states("Q1")
            total_time = sum(time_in_state for _, time_in_state in states)
            capacity_label = self._capacity_label(self.queues["Q1"]["capacity"])
            print(f"--- Results G/G/{self.queues['Q1']['servers']}/{capacity_label} ---")
            print(f"Total time: {total_time:.4f}")
            print(f"Lost customers: {self.loss_count}")
            print(f"{'State':<8} | {'Accumulated time':<18} | {'Probability'}")
            for state, time_in_state in states:
                probability = (time_in_state / total_time) * 100 if total_time > 0 else 0
                print(f"{state:<8} | {time_in_state:<18.4f} | {probability:.2f}%")
            print("-" * 50)
            return

        print("--- Queue Network Results ---")
        print(f"Total simulated time: {self.current_time:.4f}")
        print(f"Customers exited system: {self.exited_system}")
        print()

        for qid in self.queue_ids:
            states = self._iter_states(qid)
            total_time = sum(time_in_state for _, time_in_state in states)

            print(
                f"Queue {qid} (G/G/{self.queues[qid]['servers']}/{self._capacity_label(self.queues[qid]['capacity'])})"
            )
            print(f"  Lost customers: {self.loss_count_by_queue[qid]}")
            print(f"  Completed services: {self.completed_services[qid]}")
            print(f"  {'State':<8} | {'Accumulated time':<18} | {'Probability'}")
            for state, time_in_state in states:
                probability = (time_in_state / total_time) * 100 if total_time > 0 else 0
                print(f"  {state:<8} | {time_in_state:<18.4f} | {probability:.2f}%")
            print("-" * 60)

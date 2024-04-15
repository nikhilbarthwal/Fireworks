import requests
import threading
import time
import numpy as np


url = "http://www.google.com"
concurrency = 10
requests_per_thread = 10
percentiles = [50, 75, 95, 99]


class LoadTestingThread:
    def __init__(self, count):
        self.count = count
        self.error = 0
        self.timing = []

    def start(self):
        for _ in range(self.count):
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            self.timing.append((end_time - start_time) * 1000)
            if (response.status_code >= 300) and (response.status_code < 200):
                self.error += 1


threads = []
loads = []
for _ in range(concurrency):
    loads.append(LoadTestingThread(requests_per_thread))

for i in range(concurrency):
    thread = threading.Thread(target=loads[i].start())
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

errors = sum(loads[i].error for i in range(concurrency))
latencies = [x for i in range(concurrency) for x in loads[i].timing]
for percentile in percentiles:
    x = np.percentile(latencies, percentile)
    print(percentile, x)

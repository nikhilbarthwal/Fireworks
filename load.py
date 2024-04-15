import requests
import threading
import time
import numpy as np
from jinja2 import Environment, FileSystemLoader


class LoadTestingThread:
    def __init__(self, url, count, sigma):
        self.url = url
        self.sigma = sigma
        self.count = count
        self.error = 0
        self.timing = []

    def start(self):
        for _ in range(self.count):
            time.sleep(np.random.normal(0, self.sigma)/1000)  # Adding Jitter
            start_time = time.time()
            response = requests.get(self.url)
            end_time = time.time()
            self.timing.append((end_time - start_time) * 1000)
            if (response.status_code >= 300) and (response.status_code < 200):
                self.error += 1


def main(url, concurrency, requests_per_thread, percentiles, std_deviation):
    threads = []
    loads = []
    for _ in range(concurrency):
        loads.append(LoadTestingThread(url, requests_per_thread, std_deviation))

    for i in range(concurrency):
        thread = threading.Thread(target=loads[i].start())
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = concurrency * requests_per_thread
    latencies = [x for i in range(concurrency) for x in loads[i].timing]

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    print(template.render({
        'url': url,
        'mean': np.mean(latencies),
        'concurrency': concurrency,
        'requests_per_thread': requests_per_thread,
        'std_deviation': std_deviation,
        'errors': (100 * (sum(loads[i].error for i in range(concurrency)))) / total,
        'percentiles': [(percentile, round(np.percentile(latencies, percentile)), 2)
                        for percentile in percentiles],
    }))


if __name__ == "__main__":
    main(
        url="http://www.google.com",
        concurrency=10,
        requests_per_thread=10,
        percentiles=[50, 75, 95, 99],
        std_deviation=0
    )

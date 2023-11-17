import multiprocessing
import requests
import time

BASE_URLS = ["http://localhost"]


def kv_store_client(operation, key, value=None):
    # Determine which server to use based on the key
    server_url = BASE_URLS[0]
    start_time = time.time()
    try:
        if operation == 'set':
            # response = requests.post(f'{server_url}/put?key={key}', json={'value': value})
            response = requests.post(f'{server_url}/put', params={'key': key}, json={'value': value})
        elif operation == 'get':
            # response = requests.get(f'{server_url}/get?key={key}')
            response = requests.get(f'{server_url}/get', params={'key': key})
        else:
            raise ValueError('Invalid operation')
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f'Error performing {operation} on {key}: {e}')
        return None

def worker(num_operations, latencies_queue, operation, process_index):
    for i in range(num_operations):
        key = f'key{process_index}_{i}'
        value = f'value{process_index}_{i}' if operation == 'set' else None
        latency = kv_store_client(operation, key, value)
        if latency is not None:
            latencies_queue.put(latency)

def benchmark(num_operations, num_processes):
    manager = multiprocessing.Manager()
    latencies_queue = manager.Queue()

    set_processes = [
        multiprocessing.Process(target=worker, args=(num_operations, latencies_queue, 'set', i))
        for i in range(num_processes)
    ]
    get_processes = [
        multiprocessing.Process(target=worker, args=(num_operations, latencies_queue, 'get', i))
        for i in range(num_processes)
    ]
    start_time = time.time()

    for p in set_processes:
        p.start()
    for p in set_processes:
        p.join()

    for p in get_processes:
        p.start()
    for p in get_processes:
        p.join()

    total_time = time.time() - start_time
    total_operations = num_operations * num_processes * 2  # Each process does num_operations SET and GET
    total_latencies = []

    while not latencies_queue.empty():
        total_latencies.append(latencies_queue.get())

    average_latency = sum(total_latencies) / len(total_latencies)
    print(f'Total Latency: {sum(total_latencies):.2f} second')
    print(f'Length of latencies: {len(total_latencies):.0f} latencies')
    throughput = total_operations / total_time
    print(f'Total Operation: {total_operations:.0f} operations')
    print(f'Average Latency: {average_latency:.5f} seconds per operation')
    print(f'Throughput: {throughput:.2f} operations per second')
    print(f'Total Benchmark Time: {total_time:.2f} seconds')

if __name__ == '__main__':
    num_operations_per_process = 100
    num_processes = 5
    benchmark(num_operations_per_process, num_processes)
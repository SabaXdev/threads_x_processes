import multiprocessing
import threading
import time
import requests
import concurrent.futures
import json

API_URLS = [
    f"https://dummyjson.com/products/{i}" for i in range(1, 101)
]


def fetch_product(url_index):  # value of url_index starts from 0 to 99
    url = API_URLS[url_index]
    process_name = multiprocessing.current_process().name
    thread_name = threading.current_thread().name
    start_time = time.perf_counter()

    print(f"Process: {process_name}, ThreadID: {url_index}...")

    response = requests.get(url)

    if response.status_code == 200:
        end_time = time.perf_counter()
        print(f"Process: {process_name}, ThreadID: {url_index}, Time taken: {end_time - start_time} seconds...")
        return response.json()
    else:
        print(f"Failed to fetch data from {url}")


def threads(process):
    thread_results = []
    with concurrent.futures.ThreadPoolExecutor() as thread_executor:
        products_info = list(thread_executor.map(fetch_product, range(process, process + 20)))
        thread_results.extend(products_info)
    return thread_results


def processes():
    processes_range = [0, 20, 40, 60, 80]
    start_time_process = time.perf_counter()

    # Create 5 processes and for each process 20 threads
    with concurrent.futures.ProcessPoolExecutor() as process_executor:
        products = list(process_executor.map(threads, processes_range))

    with open("products2.json", "w") as file:
        json.dump(products, file, indent=4)

    end_time_process = time.perf_counter()
    tot_time = end_time_process - start_time_process
    print(f"Total execution time = {tot_time} seconds")


if __name__ == "__main__":
    processes()

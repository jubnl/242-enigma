import multiprocessing
import queue
from multiprocessing import Queue, Event


def worker(input_queue, output_queue, stop_event, processed_event, total_tasks, processed_count_lock, processed_count):
    while not stop_event.is_set():
        try:
            task = input_queue.get(timeout=1)

            # terminate if no task is received (meaning that all tasks have been processed)
            if task is None:
                break

            func, kwargs = task
            result = func(**kwargs)
            output_queue.put(result)

            # increment processed_count and check if all tasks have been processed
            with processed_count_lock:
                processed_count.value += 1
                if processed_count.value == total_tasks:
                    processed_event.set()  # Signal that all tasks are processed

            # if a result is found, stop all workers
            if result is not None:
                stop_event.set()
        except queue.Empty:
            continue


def init_workers(
        input_queue: Queue,
        output_queue: Queue,
        stop_event: Event,
        proceed_event: Event,
        total_tasks: int,
        processed_count_lock: multiprocessing.Lock,
        processed_count: multiprocessing.Value
):
    # one worker per cpu core
    worker_amount = multiprocessing.cpu_count()
    processes = [
        multiprocessing.Process(target=worker, args=(
            input_queue,
            output_queue,
            stop_event,
            proceed_event,
            total_tasks,
            processed_count_lock,
            processed_count
        )) for _
        in
        range(worker_amount)
    ]

    # start all workers
    for p in processes:
        p.start()

    return worker_amount, processes

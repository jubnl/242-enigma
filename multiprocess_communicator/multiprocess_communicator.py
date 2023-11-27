import multiprocessing
import queue
import logging
import threading
import time
from collections import defaultdict
from typing import Callable, Any, Dict, List


class MultiprocessCommunicator:
    def __init__(self):
        self.message_queues: Dict[int, multiprocessing.Queue] = {}
        self.listeners: Dict[int, List[Callable]] = defaultdict(list)
        self.listener_threads: List[threading.Thread] = []
        self.stop_event = threading.Event()
        self.logger = logging.getLogger(self.__class__.__name__)

    def register_queue(self, priority_level: int, max_size: int = 0, redeclare: bool = False):
        if priority_level not in self.message_queues:
            # Consider limiting the queue size here
            self.message_queues[priority_level] = multiprocessing.Queue(maxsize=max_size)
            return
        if redeclare:
            self.message_queues[priority_level] = multiprocessing.Queue(maxsize=max_size)

    def _ensure_queue_exists(self, priority_level: int):
        if priority_level not in self.message_queues:
            self.logger.critical("")

    def send_message(self, message_type: str, data: Any, priority_level: int = 1):
        self._ensure_queue_exists(priority_level)
        message = {"type": message_type, "data": data}
        try:
            # Add a timeout to avoid blocking indefinitely
            self.message_queues[priority_level].put(message, timeout=1)
        except queue.Full:
            self.logger.warning(f"Queue full for priority {priority_level}")
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")

    def register_listener(self, priority_level: int, listener_function: Callable):
        self._ensure_queue_exists(priority_level)
        self.listeners[priority_level].append(listener_function)

    def start_listeners(self):
        for priority_level in self.message_queues:
            thread = threading.Thread(target=self._listener_thread, args=(priority_level,))
            thread.start()
            self.listener_threads.append(thread)

    def _listener_thread(self, priority_level: int):
        while not self.stop_event.is_set():
            try:
                message = self.message_queues[priority_level].get(timeout=1)
                for listener in self.listeners[priority_level]:
                    listener(message)
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in listener thread: {e}")

    def is_empty(self) -> bool:
        return all(q.empty() for q in self.message_queues.values())

    def close(self):
        self.stop_event.set()
        for q in self.message_queues.values():
            q.close()
        for thread in self.listener_threads:
            if thread.is_alive():
                thread.join()

    def join_thread(self):
        for q in self.message_queues.values():
            q.join_thread()

    def graceful_shutdown(self, keep_running_for: float = .1, timeout: float = None):
        if keep_running_for:
            time.sleep(keep_running_for)

        self.stop_event.set()
        for thread in self.listener_threads:
            thread.join(timeout)
            if thread.is_alive():
                self.logger.warning("Thread did not terminate within timeout")

        self.close()
        self.join_thread()

    def log_status(self):
        self.logger.info(f"Queue Status - Empty: {self.is_empty()}")


if __name__ == "__main__":
    def listener_one(message):
        print("Listener One received:", message)


    def listener_two(message):
        print("Listener Two received:", message)


    def listener_three(message):
        print("Listener Three received:", message)


    def listener_four(message):
        print("Listener Four received:", message)


    communicator = MultiprocessCommunicator()
    communicator.register_listener(1, listener_one)
    communicator.register_listener(2, listener_two)
    communicator.register_listener(3, listener_three)
    communicator.register_listener(3, listener_four)

    # Start background listener threads
    communicator.start_listeners()

    # Example: sending messages
    communicator.send_message("type1", "data for type1", priority_level=1)
    communicator.send_message("type2", "data for type2", priority_level=2)
    communicator.send_message("type3", "data for type3", priority_level=3)
    communicator.send_message("type3", "data for type3", priority_level=3)
    communicator.send_message("type3", "data for type3", priority_level=3)
    communicator.send_message("type3", "data for type3", priority_level=3)
    communicator.send_message("type3", True, priority_level=3)

    # The listener threads will automatically process these messages

    # When done, gracefully shutdown
    communicator.graceful_shutdown()

import multiprocessing
import queue
import string
import time
from itertools import permutations, product
import random
from typing import List, Optional

from enigma.machine import EnigmaMachine
from tabulate import tabulate

from multiprocessing_shit import init_workers


def get_machine(
        ring_settings: List[int] = None,
        rotors: str = "I V IV",
        plugboard_settings: str = "NX EC RV GP SU DK IT FY BL AZ",
        initial_position: str = "GYD",
        # key: str = "OCR"
) -> EnigmaMachine:
    """Create an EnigmaMachine instance
    :param ring_settings: ring settings
    :type ring_settings: List[int]
    :param rotors: Rotors used
    :type rotors: str
    :param plugboard_settings: Letters swaps
    :type plugboard_settings: str
    :param initial_position: Rotors initial position
    :type initial_position: str
    :rtype: EnigmaMachine
    :return: A new preconfigured EnigmaMachine instance
    """
    machine = EnigmaMachine.from_key_sheet(
        rotors=rotors,
        ring_settings=ring_settings if ring_settings is not None else [13, 15, 11],
        plugboard_settings=plugboard_settings,
    )
    machine.set_display(initial_position)
    # msg_key = machine.process_text(key)
    # machine.set_display(msg_key)
    return machine


def encode(plain_text: str, machine: Optional[EnigmaMachine] = None):
    if machine is None:
        # get machine with default parameters
        machine = get_machine()
    return machine.process_text(plain_text)


def decode(cipher: str, machine: Optional[EnigmaMachine] = None):
    if machine is None:
        # get machine with default parameters
        machine = get_machine()
    return machine.process_text(cipher)


def process_bruteforce(
        cipher: str = "",  # transform the function into kwargs
        initial_position: str = "",
        rotors: str = "",
        ring_settings: Optional[List[int]] = None,
        plugboard_settings: str = "GH QW TZ RO IP AL SJ DK CN YM",
        first_word: str = "METEOROLOGIE",
):
    # set default parameters
    if ring_settings is None:
        ring_settings = [19, 6, 8]

    machine = get_machine(
        rotors=rotors,
        ring_settings=ring_settings,
        plugboard_settings=plugboard_settings,
        initial_position=initial_position
    )

    deciphered = machine.process_text(cipher)

    if first_word in deciphered:
        return rotors, initial_position

    return None


def bruteforce(cipher: str, plugboard_settings: str = "GH QW TZ RO IP AL SJ DK CN YM",
               ring_settings: Optional[List[int]] = None, shuffle: bool = False, reverse: bool = False,
               first_word: str = "METEOROLOGIE"):
    if ring_settings is None:
        ring_settings = [19, 6, 8]

    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()
    processed_event = multiprocessing.Event()

    # Create a shared counter
    processed_count = multiprocessing.Value('i', 0)  # 'i' is the type code for integers
    processed_count_lock = multiprocessing.Lock()  # A lock to ensure thread-safe increments

    initial_positions = [''.join(combo) for combo in permutations(string.ascii_uppercase, 3)]
    possible_rotors = [" ".join(combo) for combo in permutations(["I", "II", "III", "IV", "V"], 3)]

    bruteforce_parameters = [{
        "cipher": cipher,
        "initial_position": initial_position,
        "rotors": rotors,
        "ring_settings": ring_settings,
        "plugboard_settings": plugboard_settings,
        "first_word": first_word
    } for (initial_position, rotors) in product(initial_positions, possible_rotors)]
    total_tasks = len(bruteforce_parameters)

    if shuffle:
        random.shuffle(bruteforce_parameters)

    if reverse:
        bruteforce_parameters = reversed(bruteforce_parameters)

    worker_amount, processes = init_workers(input_queue, output_queue, stop_event, processed_event, total_tasks,
                                            processed_count_lock, processed_count)

    # start bruteforce
    for params in bruteforce_parameters:
        input_queue.put((process_bruteforce, params))

    # termination signal if all data have been tested
    for _ in processes:
        input_queue.put(None)

    final_result = None
    start_time = time.time()

    while True:
        try:
            result = output_queue.get(timeout=1)
            if result is not None:
                final_result = result
                stop_event.set()
                break
        except queue.Empty:
            pass

        # Check if all tasks have been processed only if a result has not been found
        if processed_event.is_set() and final_result is None:
            break

    end_time = time.time()

    # Explicitly terminate all worker processes
    for p in processes:
        p.terminate()

    # Join all worker processes
    for p in processes:
        p.join()

    return final_result, end_time - start_time, processed_count.value


def print_bruteforce(data, plugboard_settings, ring_settings, first_word, cipher, cpu_infos):
    cores = cpu_infos["count"]
    table = [
        ["Status", "Failed" if data[0] is None else "Success"],
        ["Time to bruteforce (seconds)", data[1]],
        ["Total tries", data[2]],
        ["Tries by second", f"{data[2] / data[1]} ({data[2] / data[1] / cores} try/cpu core/second)"],
        ["CPU Name", cpu_infos["brand_raw"]],
        ["CPU Cores", cores],
        ["CPU Arch", cpu_infos["arch"]],
        ["CPU Bits", cpu_infos["bits"]],
        ["CPU GHz (actual/advertised)", cpu_infos["hz_actual_friendly"] + "/" + cpu_infos["hz_advertised_friendly"]],
        ["CPU Cycle amount per try", cpu_infos["hz_actual"][0] / (data[2] / data[1] / cores)],
        ["Rotors", "" if data[0] is None else data[0][0]],
        ["Initial position", "" if data[0] is None else data[0][1]],
        ["Plugboard settings", plugboard_settings],
        ["Ring settings", ", ".join([str(i) for i in ring_settings])],
        ["First word", first_word],
        ["Cipher", cipher],
        ["Deciphered", "" if data[0] is None else get_machine(
            ring_settings=ring_settings,
            plugboard_settings=plugboard_settings,
            initial_position=data[0][1],
            rotors=data[0][0],
        ).process_text(cipher)]
    ]

    return tabulate(table, tablefmt="rounded_grid")

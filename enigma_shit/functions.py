import multiprocessing
import queue
import random
import string
import time
from itertools import permutations, product
from typing import List, Optional, Union

from enigma.machine import EnigmaMachine
from tabulate import tabulate

from multiprocessing_shit import init_workers


def get_machine(
        ring_settings: Optional[Union[List[int], str]] = None,
        rotors: str = "I V IV",
        plugboard_settings: str = "NX EC RV GP SU DK IT FY BL AZ",
        initial_position: str = "GYD",
        # key: str = "OCR"
) -> EnigmaMachine:
    machine = EnigmaMachine.from_key_sheet(
        rotors=rotors,
        ring_settings=ring_settings if ring_settings is not None else [13, 15, 11],
        plugboard_settings=plugboard_settings,
    )
    machine.set_display(initial_position)
    # msg_key = machine.process_text(key)
    # machine.set_display(msg_key)
    return machine


def encode(plain_text: str, machine: Optional[EnigmaMachine] = None, separator: str = "X"):
    if machine is None:
        # get machine with default parameters
        machine = get_machine()
    return machine.process_text(plain_text, replace_char=separator)


def decode(cipher: str, machine: Optional[EnigmaMachine] = None, separator: str = "X"):
    return encode(cipher, machine=machine, separator=separator)


def process_bruteforce(
        cipher: str = "",  # transform the function into kwargs
        initial_position: str = "",
        rotors: str = "",
        ring_settings: Optional[List[int]] = None,
        plugboard_settings: str = "GH QW TZ RO IP AL SJ DK CN YM",
        first_word: str = "METEOROLOGIE",
        separator: str = "X",
):
    # small optimisation, only test for the 1st word
    cipher = cipher[0:len(first_word)]
    # set default parameters
    if ring_settings is None:
        ring_settings = [19, 6, 8]

    machine = get_machine(
        rotors=rotors,
        ring_settings=ring_settings,
        plugboard_settings=plugboard_settings,
        initial_position=initial_position,
    )

    deciphered = machine.process_text(cipher, replace_char=separator)

    if first_word == deciphered:
        return rotors, initial_position

    return None


def bruteforce(
        cipher: str,
        plugboard_settings: str = "GH QW TZ RO IP AL SJ DK CN YM",
        ring_settings: Optional[Union[List[int], str]] = None,
        shuffle: bool = False,
        reverse: bool = False,
        first_word: str = "METEOROLOGIE",
        separator: str = "X"
):
    assert separator in string.ascii_uppercase, "Separator must be an uppercase ascii letter"

    if ring_settings is None:
        ring_settings = [19, 6, 8]

    if not first_word.endswith(separator):
        first_word += separator

    # Create queues
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()
    processed_event = multiprocessing.Event()

    # Create a shared counter
    processed_count = multiprocessing.Value('i', 0)  # 'i' is the type code for integers
    processed_count_lock = multiprocessing.Lock()  # A lock to ensure thread-safe increments

    # generate all possible combinations
    # initial position can be AAA, AAB, ..., ZZZ, so 26^3 = 17'576 possibilities
    initial_positions = [''.join(p) for p in product(string.ascii_uppercase, repeat=3)]

    # rotors can be I, II, III, IV, V, but a rotor is unique. So 5 * 4 * 3 = 60 possibilities
    possible_rotors = [" ".join(combo) for combo in permutations(["I", "II", "III", "IV", "V"], 3)]

    # generate all bruteforce parameters. This will be the input of the workers (17'576 * 60 = 1'054'560 possibilities)
    bruteforce_parameters = [{
        "cipher": cipher,
        "initial_position": initial_position,
        "rotors": rotors,
        "ring_settings": ring_settings,
        "plugboard_settings": plugboard_settings,
        "first_word": first_word,
        "separator": separator,
    } for (rotors, initial_position) in product(possible_rotors, initial_positions)]
    total_tasks = len(bruteforce_parameters)

    # shuffle parameters. This will make (in theory) the bruteforce faster since it is never the 1st or the last
    # (again, in theory)
    if shuffle:
        random.shuffle(bruteforce_parameters)

    # reverse parameters
    if reverse:
        bruteforce_parameters = reversed(bruteforce_parameters)

    # init workers that listen to the input_queue and put the result in the output_queue
    worker_amount, processes = init_workers(
        input_queue,
        output_queue,
        stop_event,
        processed_event,
        total_tasks,
        processed_count_lock,
        processed_count
    )

    # put all bruteforce parameters in the input_queue
    for params in bruteforce_parameters:
        input_queue.put((process_bruteforce, params))

    # termination signal if all data have been tested
    for _ in processes:
        input_queue.put(None)

    final_result = None
    start_time = time.time()
    end_time = None

    # Wait for all tasks to be processed
    while True:
        try:
            result = output_queue.get(timeout=1)
            if result is not None:
                end_time = time.time()
                final_result = result
                stop_event.set()
                break
        except queue.Empty:
            pass

        # Check if all tasks have been processed only if a result has not been found
        if processed_event.is_set() and final_result is None:
            break

    if end_time is None:
        end_time = time.time()

    # Explicitly terminate all worker processes
    for p in processes:
        p.terminate()

    # Join all worker processes
    for p in processes:
        p.join()

    return final_result, end_time - start_time, processed_count.value, total_tasks, shuffle, reverse


def print_bruteforce(
        data,
        plugboard_settings,
        ring_settings,
        first_word,
        cipher,
        cpu_infos,
        is_new=False,
        separator="X"
):
    cores = cpu_infos["count"]

    # format data
    total_seconds = f"{data[1]:,.2f} seconds".replace(",", "'")
    tries = f"{data[2]:,}".replace(",", "'")
    total_tries = f"{data[3]:,}".replace(",", "'")
    tries_by_second = f"{(data[2] / data[1]):,.2f}".replace(",", "'")
    tries_by_second_by_core = f"{(data[2] / data[1] / cores):,.2f}".replace(",", "'")

    # create table and returns it
    table = [
        ["Status", "Failed" if data[0] is None else "Success"],
        ["Duration", total_seconds],
        ["Total tries (tried/total)", f"{tries}/{total_tries}"],
        ["Tries by second", f"{tries_by_second} ({tries_by_second_by_core} try/cpu core/second)"],
        ["Input randomized", data[4]],
        ["Input reversed", data[5]],
        # ["CPU Name", cpu_infos["brand_raw"]],
        # ["CPU Cores", cores],
        # ["CPU Arch", cpu_infos["arch"]],
        # ["CPU Bits", cpu_infos["bits"]],
        # ["CPU GHz (actual/advertised)", cpu_infos["hz_actual_friendly"] + "/" + cpu_infos["hz_advertised_friendly"]],
        # ["CPU Cycle amount per try", cpu_infos["hz_actual"][0] / (data[2] / data[1] / cores)],
        ["Rotors", "" if data[0] is None else data[0][0]],
        ["Initial position", "" if data[0] is None else data[0][1]],
        ["Plugboard settings", plugboard_settings],
        ["Ring settings", ", ".join([str(i) for i in ring_settings])],
        ["First word", first_word],
        ["Cipher", cipher],
        ["Deciphered", "" if data[0] is None else get_machine(
            ring_settings=ring_settings if not is_new else " ".join([str(i) for i in ring_settings]),
            plugboard_settings=plugboard_settings,
            initial_position=data[0][1],
            rotors=data[0][0],
        ).process_text(cipher, replace_char=separator)]
    ]

    return tabulate(table, tablefmt="rounded_grid")

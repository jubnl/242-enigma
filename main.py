import logging
import string
import time
from itertools import permutations, product
import random
from typing import Optional, List
from multiprocessing import Pool, Manager

from enigma.machine import EnigmaMachine
from tabulate import tabulate

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logging.addLevelName(25, "SUCCESS")
logging_success_level = 25

# Configure logger for successful attempts
success_logger = logging.getLogger("success_logger")

success_logger.setLevel(logging_success_level)  # Set to INFO to capture successful attempts
success_handler = logging.FileHandler('success.log')
success_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
success_logger.addHandler(success_handler)

# Configure enigma logger
enigma_logger = logging.getLogger("enigma")
enigma_logger.setLevel(logging.INFO)
enigma_handler = logging.FileHandler('enigma.log')
enigma_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
enigma_logger.addHandler(enigma_handler)


def get_machine(rotors: str = "I V IV", ring_settings: Optional[List[int]] = None,
                plugboard_settings: str = "NX EC RV GP SU DK IT FY BL AZ", initial_position: str = "GYD",
                key: str = "TSD"):
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
        machine = get_machine()
    return machine.process_text(plain_text)


def decode(cypher: str, machine: Optional[EnigmaMachine] = None):
    if machine is None:
        machine = get_machine()
    return machine.process_text(cypher, replace_char=None)


def process_combination(params):
    rotor, ring_settings, plugboard_settings, cypher, first_word, pos, found_event = params
    if found_event.is_set():
        return None
    machine = get_machine(
        rotors=rotor,
        ring_settings=ring_settings,
        plugboard_settings=plugboard_settings,
        initial_position=pos,
    )
    decoded = machine.process_text(cypher, replace_char="_")
    if first_word in decoded:
        success_logger.log(logging_success_level, f"Rotors: {rotor}, Initial pos: {pos}, Deciphered: {decoded}")
        found_event.set()  # Set the event to indicate a solution has been found
        return "Rotors:", rotor, "Initial pos", pos
    # failed_logger.error(f"Failed - Rotors: {rotor}, Initial pos: {pos}")
    return None


def bruteforce():
    plugboard_settings = "GH QW TZ RO IP AL SJ DK CN YM"
    ring_settings = [19, 6, 8]
    first_word = "meteorologie".upper()
    previous_cipher = "HUFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"
    cipher = "GRWYGBHCZRZKAOQDWJYKQSLNKGINIKUAHAUFKUKGRNVKUWOFTVNCKHDAYWKJBJYVWFFWNVXMLDGXARISRQJQOJGLEAYWNUWVDYUACPBMSJGRSOHAYRLINRHIPCBHJAZO"

    alphabet = string.ascii_uppercase
    initial_positions = [''.join(combo) for combo in permutations(alphabet, 3)]
    random.shuffle(initial_positions)
    # initial_positions = reversed(_initial_positions)
    possible_rotors = [" ".join(combo) for combo in permutations(["I", "II", "III", "IV", "V"], 3)]
    random.shuffle(possible_rotors)
    # possible_rotors = reversed(_possible_rotors)
    total_possibilities = len(possible_rotors) * len(initial_positions)
    enigma_logger.info(
        f"Rotor len: {len(possible_rotors)}, init pos len: {len(initial_positions)}, total possibilities: {total_possibilities}")

    with Manager() as manager:
        found_event = manager.Event()

        param_generator = ((rotor, ring_settings, plugboard_settings, cipher, first_word, pos, found_event)
                           for rotor, pos in product(possible_rotors, initial_positions))

        total_try = 0
        enigma_logger.info(f"New cipher      : {cipher}")
        enigma_logger.info("Starting new cipher bruteforce...")
        start = time.time()
        with Pool() as pool:
            results = pool.imap_unordered(process_combination, param_generator, chunksize=100)
            for _ in results:
                total_try += 1
                if found_event.is_set():
                    break
        end = time.time()
        total = end - start
        if not found_event.is_set():
            enigma_logger.error("Decipher was not successful, no match found.")
        enigma_logger.info(
            f"New : Took {total} seconds in {total_try} tries ({total_try / total} try/second)")

        found_event = manager.Event()

        param_generator = ((rotor, ring_settings, plugboard_settings, previous_cipher, first_word, pos, found_event)
                           for rotor, pos in product(possible_rotors, initial_positions))
        total_try = 0
        start = time.time()
        enigma_logger.info(f"Previous cipher : {previous_cipher}")
        enigma_logger.info("Starting previous cipher bruteforce...")
        with Pool() as pool:
            results = pool.imap_unordered(process_combination, param_generator, chunksize=100)
            for _ in results:
                total_try += 1
                if found_event.is_set():
                    break
        end = time.time()
        total = end - start
        if not found_event.is_set():
            enigma_logger.error("Decipher was not successful, no match found.")
        enigma_logger.info(f"Previous : Took {total} seconds in {total_try} tries ({total_try / total} try/second)")


if __name__ == "__main__":
    plain = 'Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir.'.upper()
    cypher = encode(plain)
    decoded = decode(cypher)

    table = tabulate(
        [
            ["Plain text:", plain],
            ["Ciphered text:", cypher],
            ["Deciphered text:", decoded],
        ],
        tablefmt="rounded_grid"
    )

    print(table)

    time.sleep(0.01)
    bruteforce()

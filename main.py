import multiprocessing
import os

from tabulate import tabulate

from enigma_shit import bruteforce, get_machine, encode, decode


def print_bruteforce(data, plugboard_settings, ring_settings, first_word, cipher):
    cores = multiprocessing.cpu_count()
    table = [
        ["Status", "Failed" if data[0] is None else "Success"],
        ["Time to bruteforce (seconds)", data[1]],
        ["Total tries", data[2]],
        ["Tries by second", f"{data[2] / data[1]} ({data[2] / data[1] / cores} try/cpu core/second)"],
        ["CPU Cores", cores],
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

    print(tabulate(table, tablefmt="rounded_grid"))


if __name__ == "__main__":
    plain = ('Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic '
             'radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir.').upper()

    ring_settings = [13, 15, 11]
    rotors = "I V IV"
    plugboard_settings = "NX EC RV GP SU DK IT FY BL AZ"
    initial_position = "GYD"

    encode_machine = get_machine(
        ring_settings=ring_settings,
        rotors=rotors,
        plugboard_settings=plugboard_settings,
        initial_position=initial_position,
    )
    decode_machine = get_machine(
        ring_settings=ring_settings,
        rotors=rotors,
        plugboard_settings=plugboard_settings,
        initial_position=initial_position,
    )

    cypher = encode(plain, machine=encode_machine)
    decoded = decode(cypher, machine=decode_machine)

    table = tabulate(
        [
            ["Plain text", plain],
            ["Ciphered text", cypher],
            ["Deciphered text", decoded],
        ],
        tablefmt="rounded_grid"
    )

    print(table)

    cipher1 = "HUFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"
    cipher2 = "GRWYGBHCZRZKAOQDWJYKQSLNKGINIKUAHAUFKUKGRNVKUWOFTVNCKHDAYWKJBJYVWFFWNVXMLDGXARISRQJQOJGLEAYWNUWVDYUACPBMSJGRSOHAYRLINRHIPCBHJAZO"
    plugboard_settings = "GH QW TZ RO IP AL SJ DK CN YM"
    ring_settings = [19, 6, 8]
    first_word = "METEOROLOGIE"
    data1 = bruteforce(
        cipher1,
        plugboard_settings=plugboard_settings,
        ring_settings=ring_settings,
        shuffle=True,
        first_word=first_word
    )

    data2 = bruteforce(
        cipher2,
        plugboard_settings=plugboard_settings,
        ring_settings=ring_settings,
        shuffle=True,
        first_word=first_word
    )

    print_bruteforce(data1, plugboard_settings, ring_settings, first_word, cipher1)
    print_bruteforce(data2, plugboard_settings, ring_settings, first_word, cipher2)

    # force exit because queues behave strangely
    os._exit(0)

import multiprocessing
import os

from tabulate import tabulate

from enigma_shit import bruteforce, get_machine, encode, decode

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

    cipher = "HUFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"
    # cipher = "GRWYGBHCZRZKAOQDWJYKQSLNKGINIKUAHAUFKUKGRNVKUWOFTVNCKHDAYWKJBJYVWFFWNVXMLDGXARISRQJQOJGLEAYWNUWVDYUACPBMSJGRSOHAYRLINRHIPCBHJAZO"
    plugboard_settings = "GH QW TZ RO IP AL SJ DK CN YM"
    ring_settings = [19, 6, 8]
    first_word = "METEOROLOGIE"
    data = bruteforce(
        cipher,
        plugboard_settings=plugboard_settings,
        ring_settings=ring_settings,
        shuffle=True,
        first_word=first_word
    )

    if data[0] is None:
        table = tabulate(
            [
                ["Bruteforce failed...", ""],
                ["Time to bruteforce (seconds)", data[1]],
                ["Total tries", data[2]],
                ["Tries by second", data[2] / data[1]],
                ["CPU Cores", multiprocessing.cpu_count()],
                ["Cipher", cipher]
            ],
            tablefmt="rounded_grid"
        )
        print(table)

        # force exit because queues behave strangely
        os._exit(0)

    table = tabulate(
        [
            ["Time to bruteforce (seconds)", data[1]],
            ["Total tries", data[2]],
            ["Tries by second", data[2] / data[1]],
            ["CPU Cores", multiprocessing.cpu_count()],
            ["rotors", data[0][0]],
            ["Initial position", data[0][1]],
            ["Plugboard settings", plugboard_settings],
            ["Ring settings", ", ".join([str(i) for i in ring_settings])],
            ["Cipher", cipher],
            ["Deciphered", get_machine(
                ring_settings=ring_settings,
                plugboard_settings=plugboard_settings,
                initial_position=data[0][1],
                rotors=data[0][0],
            ).process_text(cipher)]
        ],
        tablefmt="rounded_grid"
    )
    print(table)

    # force exit because queues behave strangely
    os._exit(0)

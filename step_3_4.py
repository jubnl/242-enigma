import os

from tabulate import tabulate

from enigma_shit import encode, decode, get_machine

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
            ["Rotors", rotors],
            ["Plugboard settings", plugboard_settings],
            ["Ring settings", ", ".join([str(i) for i in ring_settings])],
            ["Initial position", initial_position],
            ["Plain text", plain],
            ["Ciphered text", cypher],
            ["Deciphered text", decoded],
        ],
        tablefmt="rounded_grid"
    )

    with open("step_3-4.output.txt", "w", encoding="utf-8") as f:
        f.write(table)

    print("Output saved at :", os.path.abspath("./step_3-4.output.txt"))
    print(table)

    os._exit(os.EX_OK)

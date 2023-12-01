import os
import platform

from tabulate import tabulate

from enigma_shit import encode, decode, get_machine

if __name__ == "__main__":
    plain = ('Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic '
             'radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir.').upper()

    rotors = "I V IV"
    plugboard_settings = "NX EC RV GP SU DK IT FY BL AZ"
    initial_position = "GYD"
    ring_settings = "13 15 11"

    output_file_name = f"step_3_4.output.{platform.system()}.{platform.release()}.txt"

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
            ["Ring settings", ", ".join(ring_settings.split(" "))],
            ["Initial position", initial_position],
            ["Plain text", plain],
            ["Ciphered text", cypher],
            ["Deciphered text", decoded],
        ],
        tablefmt="rounded_grid"
    )

    print(table)
    with open(output_file_name, "w", encoding="utf-8") as f:
        f.write(table)

    print("Output saved at :", os.path.abspath(f"./{output_file_name}"))

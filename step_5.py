import os
import platform

from cpuinfo import get_cpu_info
from pathvalidate import sanitize_filename

from enigma_shit import bruteforce, print_bruteforce

if __name__ == "__main__":
    cipher = "GRWYGBHCZRZKAOQDWJYKQSLNKGINIKUAHAUFKUKGRNVKUWOFTVNCKHDAYWKJBJYVWFFWNVXMLDGXARISRQJQOJGLEAYWNUWVDYUACPBMSJGRSOHAYRLINRHIPCBHJAZO"
    plugboard_settings = "GH QW TZ RO IP AL SJ DK CN YM"
    ring_settings = "19 6 8"
    first_word = "METEOROLOGIE"
    separator = "X"

    cpu_infos = get_cpu_info()
    cores = cpu_infos["count"]
    output_file_name = sanitize_filename(
        f"step_5.output.{platform.system()}-{platform.release()}.{cores}-cores.txt",
        platform=os.name
    )

    data = bruteforce(
        cipher,
        plugboard_settings=plugboard_settings,
        ring_settings=ring_settings,
        shuffle=True,
        first_word=first_word,
        separator=separator
    )

    table = print_bruteforce(
        data,
        plugboard_settings,
        ring_settings,
        first_word,
        cipher,
        cpu_infos,
        separator=separator
    )
    with open(output_file_name, "w", encoding="utf-8") as f:
        f.write(table)
    print("Output saved at :", os.path.abspath(f"./{output_file_name}"))
    print(table)

    # Queues behaves strangely, if I don't kill python this way, the queues takes multiple minute to close out
    # completely.
    os._exit(os.EX_OK)

import os

from cpuinfo import get_cpu_info

from enigma_shit import bruteforce, print_bruteforce

if __name__ == "__main__":
    cipher = "HUFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"
    plugboard_settings = "GH QW TZ RO IP AL SJ DK CN YM"
    ring_settings = "19 6 8"
    first_word = "METEOROLOGIE"
    cpu_infos = get_cpu_info()

    data = bruteforce(
        cipher,
        plugboard_settings=plugboard_settings,
        ring_settings=ring_settings,
        shuffle=True,
        first_word=first_word
    )

    table = print_bruteforce(data, plugboard_settings, ring_settings, first_word, cipher, cpu_infos)
    with open("step_5-previous-cipher.output.txt", "w", encoding="utf-8") as f:
        f.write(table)
    print("Output saved at :", os.path.abspath("./step_5-previous-cipher.output.txt"))
    print(table)

    os._exit(os.EX_OK)
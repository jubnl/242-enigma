import string
from itertools import product, permutations

import dispy

from enigma_shit import process_bruteforce, get_machine


def job_status(job):  # executed at the client
    if job.status != dispy.DispyJob.Finished:
        return
    if not job.result:
        return

    print(job.result)
    for j in jobs:
        if j.status in [dispy.DispyJob.Created, dispy.DispyJob.Running,
                        dispy.DispyJob.ProvisionalResult, dispy.DispyJob.Abandoned]:
            cluster.cancel(j)


if __name__ == "__main__":
    jobs = []
    cluster = dispy.JobCluster(
        process_bruteforce,
        nodes=['192.168.65.14', '192.168.65.104', '192.168.65.145'],
        depends=[get_machine, job_status, jobs],
        job_status=job_status,
    )

    cipher = "GRWYGBHCZRZKAOQDWJYKQSLNKGINIKUAHAUFKUKGRNVKUWOFTVNCKHDAYWKJBJYVWFFWNVXMLDGXARISRQJQOJGLEAYWNUWVDYUACPBMSJGRSOHAYRLINRHIPCBHJAZO"
    plugboard_settings = "GH QW TZ RO IP AL SJ DK CN YM"
    ring_settings = "19 6 8"
    first_word = "METEOROLOGIE"
    separator = "X"

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
    for n, i in enumerate(bruteforce_parameters):
        job = cluster.submit(**i)
        if job is None:
            print('creating job %s failed!' % n)
            continue
        job.id = n
        jobs.append(job)

    cluster.wait()
    cluster.print_status()
    cluster.close()

import dispy

from enigma_shit import process_bruteforce, get_machine


if __name__ == "__main__":
    cluster = dispy.JobCluster(
        process_bruteforce,
        nodes=['192.168.65.49', '192.168.65.14', '192.168.65.104', '192.168.65.145'],
        depends=[get_machine],
    )
    
    

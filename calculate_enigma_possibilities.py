from math import factorial, pow


def calculate_enigma_possibilities(rotors_available, rotors_used, plugboard_pairs):
    # Rotor permutations
    rotor_permutations = factorial(rotors_available) / factorial(rotors_available - rotors_used)

    # Rotor settings (26 positions for each of the 3 rotors)
    rotor_settings = pow(26, rotors_used)

    # Plugboard combinations
    # 26! / ((26 - 20)! * 2^10 * 10!)
    plugboard_combinations = factorial(26) / (
                factorial(26 - plugboard_pairs * 2) * pow(2, plugboard_pairs) * factorial(plugboard_pairs))

    # Initial position possibilities (3 letters)
    initial_position_possibilities = pow(26, rotors_used)

    # Total possibilities
    total_possibilities = rotor_permutations * rotor_settings * plugboard_combinations * initial_position_possibilities

    return total_possibilities


# Execute the function and print the result
total_enigma_possibilities = calculate_enigma_possibilities(5, 3, 10)
print(f"Total Enigma Machine Possibilities: {total_enigma_possibilities}")

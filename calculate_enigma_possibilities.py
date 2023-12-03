from math import factorial, pow


def calculate_enigma_possibilities(rotors_available, rotors_used, plugboard_pairs):
    # Rotor permutations
    rotor_permutations = int(factorial(rotors_available) / factorial(rotors_available - rotors_used))

    # Rotor settings (26 positions for each of the rotors)
    rotor_settings = int(pow(26, rotors_used))

    # Plugboard combinations
    plugboard_combinations = int(factorial(26) / (
            factorial(26 - plugboard_pairs * 2) * pow(2, plugboard_pairs) * factorial(plugboard_pairs)))

    # Initial position possibilities (3 letters)
    initial_position_possibilities = int(pow(26, 3))

    # Total possibilities
    total_possibilities = rotor_permutations * rotor_settings * plugboard_combinations * initial_position_possibilities

    return f"{total_possibilities:,}".replace(",", "'")


total_enigma_possibilities = calculate_enigma_possibilities(5, 3, 10)
print(f'Total Enigma Machine Possibilities: {total_enigma_possibilities}')

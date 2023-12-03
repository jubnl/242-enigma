# Calculate all possibilities for enigma

## Theory
$P(n, r) = \frac{n!}{(n - r)!}$
1. Rotor Order Possibilities
$$rotorOrderPossibilities = P(nRotors, rUsed)$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{rUsed}$$
3. Initial Positions
$$initialPositions = 26^{rUsed}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{26!}{(26 - 2 \times plugboardAmount)! \times 2^{plugboardAmount} \times plugboardAmount!}$$
5. Total Possibilities
$$totalPossibilities = rotorOrderPossibilities \times ringSettingPossibilities \times initialPositions \times plugboardPossibilities$$\
$$totalPossibilities = P(nRotors, rUsed) \times \frac{26^{2 \times rUsed} \times 26!}{(26 - 2 \times plugboardAmount)! \times 2^{plugboardAmount} \times plugboardAmount!}$$

## Math application
$\text{let } nRotors = 5\text{, } rUsed = 3 \text{ and } plugboardAmount = 10$
1. Rotor Order Possibilities
$$rotorOrderPossibilities = \frac{5!}{(5 - 3)!} = 60$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{3} = 17576$$
3. Initial Positions
$$initialPositions = 26^{3} = 17576$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{26!}{(26-2 \times 10)! \times 2^{10} \times 10!} = 150738274937250$$
5. Total Possibilities
$$totalPossibilities = 60 \times 17576^2 \times 150738274937250 = 2793925870508516103360000$$

## Code Application

```python
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
```
Prints out: `Total Enigma Machine Possibilities: 2'793'925'870'508'516'103'360'000`
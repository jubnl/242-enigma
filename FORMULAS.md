# Calculate all possibilities for enigma

1. Rotor Order Possibilities
$$P(nRotors, rUsed) = \frac{nRotors!}{(nRotors - rUsed)!}$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = positionsPerRotor^{rUsed}$$
3. Initial Rotor Positions
$$initial\_rotor\_positions = positionsPerRotor^{rUsed}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{\prod\_{i=0}^{9} P(26 - 2i, 2)}{10!}$$
5. Total Possibilities
$$total\_possibilities = P(nRotors, rUsed) \times positionsPerRotor^{rUsed} \times \frac{\prod\_{i=0}^{9} P(26 - 2i, 2)}{10!} \times positionsPerRotor^{rUsed}$$

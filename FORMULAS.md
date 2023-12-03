# Calculate all possibilities for enigma

1. Rotor Order Possibilities
$$P({n\_rotors}, {r\_used}) = \frac{{n\_rotors}!}{({n\_rotors} - {r\_used})!}$$
2. Rotor Settings (Ring Setting Possibilities)
$$ring\_setting\_possibilities = positions\_per\_rotor^{r\_used}$$
3. Initial Rotor Positions
$$initial\_rotor\_positions = positions\_per\_rotor^{r\_used}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboard\_possibilities = \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!}$$
5. Total Possibilities
$$total\_possibilities = P({n\_rotors}, {r\_used}) \times positions\_per\_rotor^{r\_used} \times \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!} \times positions\_per\_rotor^{r\_used}$$
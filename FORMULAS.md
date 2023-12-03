# Calculate all possibilities for enigma

1. Rotor Order Possibilities
$$P(n_rotors, r_used) = \frac{n_rotors!}{(n_rotors - r_used)!}$$
2. Rotor Settings (Ring Setting Possibilities)
$$ring_setting_possibilities = positions_per_rotor^{r_used}$$
3. Initial Rotor Positions
$$initial_rotor_positions = positions_per_rotor^{r_used}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboard_possibilities = \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!}$$
5. Total Possibilities
$$total_possibilities = P(n_rotors, r_used) \times positions_per_rotor^{r_used} \times \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!} \times positions_per_rotor^{r_used}$$

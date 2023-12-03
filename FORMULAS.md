# Calculate all possibilities for enigma

1. Rotor Order Possibilities
$$P(\text{n\_rotors}, \text{r\_used}) = \frac{\text{n\_rotors}!}{(\text{n\_rotors} - \text{r\_used})!}$$
2. Rotor Settings (Ring Setting Possibilities)
$$\text{ring\_setting\_possibilities} = \text{positions\_per\_rotor}^{\text{r\_used}}$$
3. Initial Rotor Positions
$$\text{initial\_rotor\_positions} = \text{positions\_per\_rotor}^{\text{r\_used}}$$
4. Plugboard Settings (Plugboard Possibilities)
$$\text{plugboard\_possibilities} = \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!}$$
5. Total Possibilities
$$\text{total\_possibilities} = P(\text{n\_rotors}, \text{r\_used}) \times \text{positions\_per\_rotor}^{\text{r\_used}} \times \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!} \times \text{positions\_per\_rotor}^{\text{r\_used}}$$

# Calculate all possibilities for enigma

## Theory
1. Rotor Order Possibilities
$$P(nRotors, rUsed) = \frac{nRotors!}{(nRotors - rUsed)!}$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{rUsed}$$
3. Initial Rotor Positions
$$initialRotorPositions = 26^{rUsed}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!}$$
5. Total Possibilities
$$totalPossibilities = P(nRotors, rUsed) \times (26^{rUsed})^2 \times plugboardPossibilities$$

## Code Application

1. Rotor Order Possibilities
```python
def rotor_order_possibilities(n_rotors, r_used):
    return math.factorial(n_rotors) / math.factorial(n_rotors - r_used)
```

2. Rotor Settings (Ring Setting Possibilities)
```python
def ring_setting_possibilities(r_used):
    return math.perm(26, r_used)
```

3. Initial Rotor Positions
```python
def initial_rotor_positions(r_used):
    return math.perm(26, r_used)
```

4. Plugboard Settings (Plugboard Possibilities)
```python
def plugboard_possibilities():
    possibilities = [math.perm(26 - i * 2, 2) for i in range(10)]
    return math.prod(possibilities) / math.factorial(10)
```

5. Total Possibilities
```python
def total_possibilities(n_rotors, r_used):
    return rotor_order_possibilities(n_rotors, r_used) * math.pow(ring_setting_possibilities(r_used), 2) * plugboard_possibilities()
```
# Calculate all possibilities for enigma

## Theory
1. Rotor Order Possibilities
$$rotorOrderPossibilities = P(nRotors, rUsed)$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{rUsed}$$
3. Initial Rotor Positions
$$initialRotorPositions = 26^{rUsed}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{\prod_{i=0}^{9} P(26 - 2i, 2)}{10!}$$
5. Total Possibilities
$$totalPossibilities = rotorOrderPossibilities \times ringSettingPossibilities \times initialRotorPositions \times plugboardPossibilities$$

## Math application
$nRotors = 5$\
$rUsed = 3$\
$P(n, r) = \frac{n!}{(n - r)!}$\
1. Rotor Order Possibilities
$$rotorOrderPossibilities = \frac{5!}{(5 - 3)!} = 60$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{3} = 17576$$
3. Initial Rotor Positions
$$initialRotorPositions = 26^{3} = 17576$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{P(26, 2) \times P(24, 2) \times P(22, 2) \times P(20, 2) \times P(18, 2) \times P(16, 2) \times P(14, 2) \times P(12, 2) \times P(10, 2) \times P(8, 2)}{10!} = \frac{650 \times 552 \times 462 \times 380 \times 306 \times 240 \times 182 \times 132 \times 90 \times 56}{3628800} = 154355993535744000$$
5. Total Possibilities
$$totalPossibilities = 60 \times 17576^2 \times 154355993535744000 = 2860980091400720489840640000$$

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
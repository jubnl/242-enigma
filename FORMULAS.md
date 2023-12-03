# Calculate all possibilities for enigma

## Theory
$P(n, r) = \frac{n!}{(n - r)!}$
1. Rotor Order Possibilities
$$rotorOrderPossibilities = P(nRotors, rUsed)$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{rUsed}$$
3. Initial Rotor Positions
$$initialRotorPositions = 26^{rUsed}$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{26!}{(26 - plugboardAmount \times 2)! \times 2^plugboardAmount \times plugboardAmount!}$$
5. Total Possibilities
$$totalPossibilities = rotorOrderPossibilities \times ringSettingPossibilities \times initialRotorPositions \times plugboardPossibilities$$\
$$totalPossibilities = P(nRotors, rUsed) \times 26^{rUsed} \times 26^{rUsed} \times \frac{26!}{(26 - 2 \times plugboardAmount)! \times 2^plugboardAmount \times plugboardAmount!}$$

## Math application
$nRotors = 5$\
$rUsed = 3$\
$plugboardAmount = 10$
1. Rotor Order Possibilities
$$rotorOrderPossibilities = \frac{5!}{(5 - 3)!} = 60$$
2. Rotor Settings (Ring Setting Possibilities)
$$ringSettingPossibilities = 26^{3} = 17576$$
3. Initial Rotor Positions
$$initialRotorPositions = 26^{3} = 17576$$
4. Plugboard Settings (Plugboard Possibilities)
$$plugboardPossibilities = \frac{26!}{(26-2 \times 10)! \times 2^{10} \times 10!} = 150738274937250$$
5. Total Possibilities
$$totalPossibilities = 60 \times 17576^2 \times 150738274937250 = 2793925870508516103360000$$

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
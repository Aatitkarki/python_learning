"""01a: validated calculations and an interactive loop with injectable input/output."""
import math

def number(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('A finite number is required')
    return result

def calculate(a, operator, b):
    a, b = number(a), number(b)
    if operator == '+': result = a + b
    elif operator == '-': result = a - b
    elif operator == '*': result = a * b
    elif operator == '/': result = a / b
    else: raise ValueError('Choose +, -, *, or /')
    return number(result)

def temperature(value, source='C', target='F'):
    value = number(value)
    if source not in {'C', 'F'} or target not in {'C', 'F'}:
        raise ValueError('Units must be C or F')
    if source == target: return value
    return number(value * 9 / 5 + 32 if source == 'C' else (value - 32) * 5 / 9)

def profit(buy, sell, shares):
    buy, sell, shares = map(number, (buy, sell, shares))
    if min(buy, sell) < 0 or shares <= 0:
        raise ValueError('Prices must be nonnegative; shares positive')
    return number((sell - buy) * shares)

def bmi(mass_kg, height_m):
    mass_kg, height_m = number(mass_kg), number(height_m)
    if min(mass_kg, height_m) <= 0: raise ValueError('Positive measurements required')
    return mass_kg / height_m**2  # Arithmetic only; no medical interpretation.

def main(read=input, write=print):
    """Commands: calc 6 / 2; temp 20 C F; profit 100 110 5; quit."""
    write('Commands: calc A OP B | temp VALUE C F | profit BUY SELL SHARES | quit')
    while True:
        try: parts = read('> ').split()
        except EOFError: return
        if not parts: continue
        if parts == ['quit']: return
        try:
            if len(parts) == 4 and parts[0] == 'calc':
                result = calculate(parts[1], parts[2], parts[3])
            elif len(parts) == 4 and parts[0] == 'temp':
                result = temperature(parts[1], parts[2], parts[3])
            elif len(parts) == 4 and parts[0] == 'profit':
                result = profit(*parts[1:])
            else: raise ValueError('Unknown command or wrong number of arguments')
            write(str(result))
        except (ValueError, ZeroDivisionError) as exc:
            write('Input error: ' + str(exc))

if __name__ == '__main__': main()

def my_float(s):

    if not s:
        raise ValueError("Invalid number format")

    s = s.strip()
    if not s:
        raise ValueError("Invalid number format")

    sign = 1
    start = 0

    if s[0] == '-':
        sign = -1
        start = 1
    elif s[0] == '+':
        start = 1

    if start >= len(s):
        raise ValueError("Invalid number format")

    dot_pos = -1
    for i in range(start, len(s)):
        if s[i] == '.':
            dot_pos = i
            break

    if dot_pos == -1:
        integer_part = s[start:]
        fractional_part = ""
    else:
        integer_part = s[start:dot_pos]
        fractional_part = s[dot_pos + 1:]

    if not integer_part and not fractional_part:
        raise ValueError("Invalid number format")

    int_value = 0
    if integer_part:
        for char in integer_part:
            if char not in '0123456789':
                raise ValueError("Invalid number format")
            int_value = int_value * 10 + (ord(char) - ord('0'))

    frac_value = 0.0
    if fractional_part:
        for i, char in enumerate(fractional_part):
            if char not in '0123456789':
                raise ValueError("Invalid number format")
            frac_value += (ord(char) - ord('0')) / (10 ** (i + 1))

    result = sign * (int_value + frac_value)
    return result


def main():
    try:
        s = input()
        number = my_float(s)
        result = number * 2
        print(f"{result:.3f}")

    except ValueError:
        print("Invalid number format")
    except Exception:
        print("Invalid number format")


if __name__ == "__main__":
    main()
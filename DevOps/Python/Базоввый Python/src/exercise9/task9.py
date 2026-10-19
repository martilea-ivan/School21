def main():
    first_line = input().split()
    n = int(first_line[0])
    x0 = float(first_line[1])

    coefficients = []
    for _ in range(n + 1):
        coef = float(input())
        coefficients.append(coef)

    derivative = 0.0

    for power, coef in enumerate(coefficients):
        current_power = n - power
        if current_power > 0:
            derivative += current_power * coef * (x0 ** (current_power - 1))
    print(f"{derivative:.3f}")


if __name__ == "__main__":
    main()
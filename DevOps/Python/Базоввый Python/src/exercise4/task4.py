def print_pascal_triangle(n):
    if n <= 0:
        return

    previous_row = [1]

    for i in range(n):

        print(' '.join(map(str, previous_row)))

        next_row = [1]
        for j in range(len(previous_row) - 1):
            next_row.append(previous_row[j] + previous_row[j + 1])
        next_row.append(1)
        previous_row = next_row


def main():
    try:
        user_input = input().strip()
        if not user_input:
            print("Natural number was expected")
            return
        n = int(user_input)

        if n <= 0:
            print("Natural number was expected")
            return

        print_pascal_triangle(n)

    except ValueError:
        print("Natural number was expected")


if __name__ == "__main__":
    main()
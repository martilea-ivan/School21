def main():
    n = int(input())
    unique = set()

    for _ in range(n):
        num = int(input())
        unique.add(num)

    print(len(unique))

if __name__ == "__main__":
    main()
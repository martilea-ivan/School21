try:
    n = int(input())
except ValueError:
    print("Значение должно быть числом!")
    exit()

if n < 10:
    print(False)
else:
    original = n
    reversed_num = 0
    while n > 0:
        digit = n % 10
        reversed_num = reversed_num * 10 + digit
        n = n // 10
    print(original == reversed_num)
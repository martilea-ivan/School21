try:
    vector1 = list(map(float, input().split()))
    vector2 = list(map(float, input().split()))
    scalar = vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]
    print(scalar)
except ValueError:
    print("Значение должно быть числом!")
except IndexError:
    print("Входные данные должны иметь 3 числа!")
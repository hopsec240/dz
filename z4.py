import math

x = float(input("Введите длину палки x: "))
y_start = float(input("Введите начальное расстояние y: "))
y_end = float(input("Введите конечное расстояние y: "))
h = float(input("Введите шаг h: "))

print("Результаты:")
steps = int((y_end - y_start) / h) + 1

for i in range(steps):
    y = y_start + i * h

    if y <= x:
        alpha = math.degrees(math.acos(y / x))
        print("При y =", round(y, 2), "угол alpha =", round(alpha, 2))
    else:
        print("При y =", round(y, 2), "палка не достает до стены")
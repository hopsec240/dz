A = float(input("Введите ежемесячную стипендию A (руб): "))
B = float(input("Введите ежемесячные расходы B (руб): "))

stip = A * 10
ras = 0
tek = B

for month in range(1, 11):
    ras += tek
    tek *= 1.03

money = ras - stip

print("\nОбщая стипендия за 10 месяцев:", round(stip, 2), "руб.")
print("Общие расходы за 10 месяцев (с инфляцией):", round(ras, 2), "руб.")
print("Сумма, которую следует попросить у родителей:", round(max(0, money), 2), "руб.")
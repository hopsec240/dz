print("Возможные комбинации:")

for r in range(17):
    l_r = r * 4
    l_l = 64 - l_r
    if l_l >= 0 and l_l % 2 == 0:
        geese = l_l // 2
        print("Кроликов: ", r," Гусей: ", geese)
n = int(input("Введите n: "))

amoebas = 1
print("Начало: ", amoebas, " амеба")

for i in range(1, n+1):
    hours = i * 3
    amoebas *= 2
    print("Через ", hours," часов: ", amoebas, " амеб")
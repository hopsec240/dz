d = 10.0 
t = d

for day in range(2, 6):
    d *= 1.1 
    t += d

print("Суммарный путь за 5 дней: ", t, " км")
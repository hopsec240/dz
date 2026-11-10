print("Простые числа вида 2x^2 + 29:")

for x in range(29):
    chislo = 2 * (x**2) + 29
    
    prostoe = True 
    
    for i in range(2, chislo // 2 + 1):
        if chislo % i == 0:
            prostoe = False 
            break
            
    if prostoe:
        print("x = ", x," число = ", chislo)
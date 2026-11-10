print("Варианты покупки (Быки, Коровы, Телята):")

for bulls in range(11):
    for cows in range(21):
        tel = 100 - bulls - cows
        if tel >= 0:
            cost = (bulls * 10) + (cows * 5) + (tel * 0.5)
            if cost == 100:
                print(f"Быков: {bulls}, Коров: {cows}, Телят: {tel}")
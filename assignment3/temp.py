with open("big.txt", "r") as f1:
    with open("out4.txt", "r") as f2:
        d1 = f1.read().splitlines()
        d2 = f2.read().splitlines()
        for i in range(50000):
            if d1[i] != d2[i]:
                print(i)
                break
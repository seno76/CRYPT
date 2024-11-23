import CRYPT.lab1.gen_curve_1 as gen_curve_1
import random

def test_gen(k):
    with open("gen_curves.txt", "w", encoding="UTF-8") as f:
        for i in range(k):
            l = random.randint(10, 20)
            m = random.randint(10, 100)
            f.write(f"{i + 1}) {gen_curve_1.build_curve(l, m)}\n")

if __name__ == "__main__":
    k = 10_0
    test_gen(k)
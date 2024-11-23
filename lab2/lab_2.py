import random
import curve

def gen_curve(l, m):
    p, B, Q, r = curve.build_curve(l, m)
    return p, B, Q, r 

def check_point_in_curve(P, a, b, p):
    return P[1] ** 2 % p == (P[0] ** 3 + a * P[0] + b) % p

def gen_P(Q, p, a, b):
    l = random.randint(1, p - 1)
    P = curve.mul_scalar_(l, Q[0], Q[1], p)
    while not check_point_in_curve(P, a, b, p):
        l = random.randint(1, p - 1)
        P = curve.mul_scalar_(l, Q[0], Q[1], p)
    return l, P

def gen_k(l, r):
    k = random.randint(1, r - 1)
    k2 = k * l % r
    return k, k2

def write_k(k1, k2, file_name="k.txt"):
    with open(file_name, "w", encoding="UTF-8") as file:
        file.write(f"{k1} {k2}")

def read_k(file_name="k.txt"):
    with open(file_name, "r", encoding="UTF-8") as file:
        lst = file.readline().split()
        k = int(lst[0]) 
        k2 = int(lst[1])
    return k, k2

def write_R(R, file_name="R.txt"):
    with open(file_name, "w", encoding="UTF-8") as file:
        file.write(f"{R[0]} {R[1]}")

def read_R(file_name="R.txt"):
    with open(file_name, "r", encoding="UTF-8") as file:
        lst = file.readline().split()
        R = (int(lst[0]), int(lst[1]))
    return R

def write_bit(bit, file_name="bit.txt"):
    with open(file_name, "w", encoding="UTF-8") as file:
        file.write(f"{bit}")

def read_bit(file_name="bit.txt"):
    with open(file_name, "r", encoding="UTF-8") as file:
        bit = int(file.readline())
    return bit

def write_data_for_verificate(k, file_name="data_verificate.txt"):
    with open(file_name, "w", encoding="UTF-8") as file:
        file.write(str(k))

def read_data_for_verificate(file_name="data_verificate.txt"):
    with open(file_name, "r", encoding="UTF-8") as file:
        bit = int(file.readline())
    return bit

def write_l(l, P, file_name="l.txt"):
    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(f"{l} {P[0]} {P[1]}")

def read_l(file_name="l.txt"):
    with open(file_name, "r", encoding="UTF-8") as f:
        line = f.readline().split()
        l = int(line[0])
        P = (int(line[1]), int(line[2]))
    return l, P


def check_period(r, R, p):
    Q1, Q2 = R[0], R[1]
    k = 1
    while Q1 != -1:
        Q1, Q2 = curve.add_points(R[0], R[1], Q1, Q2, p)  # функция сложения двух точек
        k += 1
    print("Период", k)
    return k == r

def step_1(Q, P, l, r):
    k, k2 = gen_k(l, r)
    #print("k, k':", k, k2)
    write_k(k, k2)
    R = curve.mul_scalar_(k, P[0], P[1], p)
    #print(R)
    write_R(R)

def step_2(r, R, p):
    if check_period(r, R, p) and R != (-1, -1):
        bit = random.choice([1, 0])
        write_bit(bit)
        print("Верификатор убедился в периоде и точке R")
        print("Бит записан в файл bit.txt")
    else:
        print("На шаге 2: Получили несоответствие")
        raise "Ошибка при проверке"

def step_3(bit):
    k, k2 = read_k()
    if bit == 0:
        write_data_for_verificate(k)
    else:
        write_data_for_verificate(k2)

def step_4(R, Q, P, p):
    k, k2 = read_k()
    bit = read_bit()
    if bit == 0:
        return R == curve.mul_scalar_(k, P[0], P[1], p)
    else:
        return R == curve.mul_scalar_(k2, Q[0], Q[1], p)


if __name__ == "__main__":
    a, i = 0, 0
    while True:
        print("\nМеню:")
        print("1. Генерация эллиптической кривой")
        print("2. Генерация P и l")
        print("3. Шаг 1: Генерация k, k' и R")
        print("4. Шаг 2: Проверка верификатором r*R и генерация случайного бита")
        print("5. Шаг 3: Предъявление к или к' претендента")
        print("6. Шаг 4: Аутентификация пользователя")
        print("7. Выйти из программы")
        choice = input("Выберите действие (1-7): ")
        print()

        if choice == '1':

            print("Выбран режим: Генерация эллиптической кривой")
            l = int(input("Укажите количество бит: "))
            m = int(input("Укажите параметр сложности: "))
            p, b, Q, r  = gen_curve(l, m)
            print(f"Была сгенерирована следующая кривая: p = {p}, B = {b}, (x0, y0) = {Q}, r = {r}")
            with open("curve.txt", "w", encoding="UTF-8") as f:
                f.write(f"{p} {b} {Q[0]} {Q[1]} {r}")
            print("Кривая сохранена в файл curve.txt")
            
        elif choice == '2':

            print("Выбран режим: Генерация P и l")
            with open("curve.txt", "r", encoding="UTF-8") as f:
                line = f.readline().split()
                p = int(line[0])
                b = int(line[1])
                Q = (int(line[2]), int(line[3]))
                r = int(line[4])
            print(p, b, Q, r)
            l, P = gen_P(Q, p, a, b)
            print(f"l = {l}, P = {P}")
            write_l(l, P)
            print("l и P записаны в файл l.txt")

        elif choice == '3':
            i += 1
            print("Выбран режим: Генерация k, k' и R")
            l, P = read_l()
            with open("curve.txt", "r", encoding="UTF-8") as f:
                line = f.readline().split()
                p = int(line[0])
                b = int(line[1])
                Q = (int(line[2]), int(line[3]))
                r = int(line[4])
            step_1(Q, P, l, r)
            print("k и k' сохранены в файл k.txt")
            print("R сохранен в файл R.txt")

        elif choice == '4':

            print("Выбран режим: Проверка верификатором r*R и генерация случайного бита")
            with open("curve.txt", "r", encoding="UTF-8") as f:
                line = f.readline().split()
                p = int(line[0])
                b = int(line[1])
                Q = (int(line[2]), int(line[3]))
                r = int(line[4])
            R = read_R()
            step_2(r, R, p)

        elif choice == '5':

            print("Выбран режим: Предъявление к или к' претендента")
            bit = read_bit()
            step_3(bit)
            print("Данныые (k, k') записаны в файл data_verificate.txt")

        elif choice == '6':
            R = read_R()
            _, P = read_l()
            with open("curve.txt", "r", encoding="UTF-8") as f:
                line = f.readline().split()
                p = int(line[0])
                Q = (int(line[2]), int(line[3]))
            print(f"{i + 1}) Проверка:", step_4(R, Q, P, p))
        else:
            break

    # p, b, Q, r  = gen_curve(6, 10)
    # print(f"Была сгенерирована следующая кривая: p = {p}, B = {b}, (x0, y0) = {Q}, r = {r}")
    # # Параметры эллиптической кривой
    # k = 10
    # a = 0   # коэффициент a эллиптической кривой
    # l, P = gen_P(Q, p, a, b)
    
    # print("--------------------------", l, P)
    # write_l(l, P)
    # input()
    # print(l, P, curve.mul_scalar_(l, Q[0], Q[1], p))
    # for i in range(k):
    #     input()
    #     l, P = read_l()
    #     print("--------------------------", l, P)
    #     step_1(Q, P, l, r)
        
    #     R = read_R()
    #     step_2(r, R, p)

    #     bit = read_bit()
    #     step_3(bit)

    #     print(f"{i + 1}) Проверка:", step_4(R, Q, P, p))
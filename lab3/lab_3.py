import random
import curve
import hashlib

# Вычисление значения s (0 < s < r)
def compute_s_from_file(filename, r):
    with open(filename, "rb") as f:
        file_data = f.read()
    hash_object = hashlib.sha256(file_data)
    s = int(hash_object.hexdigest(), 16) % r
    with open("s.txt", "w") as f:
        f.write(str(s))
    return s

def read_curve(file_name="curve.txt"):
    with open(file_name, "r", encoding="UTF-8") as f:
        line = f.readline().split()
        p = int(line[0])
        b = int(line[1])
        Q = (int(line[2]), int(line[3]))
        r = int(line[4])
    return p, b, Q, r

def write_one_num(num, file_name):
    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(f"{num}")

def write_point(P, file_name):
    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(f"{P[0]} {P[1]}")

def read_point(file_name):
    with open(file_name, "r", encoding="UTF-8") as file:
        lst = file.readline().split()
        point = (int(lst[0]), int(lst[1]))
    return point

def read_one_num(file_name):
    with open(file_name, "r", encoding="UTF-8") as f:
        num = int(f.readline())
    return num

def check_point_in_curve(P, a, b, p):
    return P[1] ** 2 % p == (P[0] ** 3 + a * P[0] + b) % p

def check_params(file_name, len_=1):
    with open(file_name, "r", encoding="UTF-8") as f:
        params = f.readline().split()
    if not params or len(params) != len_:
        return False
    for par in params:
        if not par.strip().isdigit():
            return False 
    return True

def func(R):
    return R[0] + R[1]

if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1. Генерация эллиптической кривой E(k)")
        print("2. Вычисление по заданному числу l точку P = l * Q (Q - образующая точка порядка r)")
        print("3. Вычисление сообщения m, точки R, показателя k и s - подписи для m")
        print("4. Генерация k', R' и alpha")
        print("5. Вычисление показателя B")
        print("6. Вычисление новое сообщение m' и подпись s'")
        # print("7. Верификация подписи")
        print("7. Выйти из программы")
        choice = input("Выберите действие (1-7): ")
        print()

        if choice == '1':

            print("Выбран режим: Генерация эллиптической кривой E(k)")
            
            l = input("Укажите количество бит l: ").strip()
            while not l.isdigit():
                print("Ошибка: l должно быть числом!!!")
                l = input("Укажите количество бит l: ").strip()
            l = int(l)

            m = input("Укажите параметр сложности m: ").strip()
            while not m.isdigit():
                print("Ошибка: m должно быть числом!!!")
                m = input("Укажите параметр сложности m: ").strip()
            m = int(m)

            p, b, Q, r = curve.build_curve(l, m)
            print(f"Была сгенерирована следующая кривая: p = {p}, B = {b}, (x0, y0) = {Q}, r = {r}")
            with open("curve.txt", "w", encoding="UTF-8") as f:
                f.write(f"{p} {b} {Q[0]} {Q[1]} {r}")
            print("Кривая сохранена в файл curve.txt")
        
        elif choice == '2':

            print("Выбран режим: Вычисление по заданному числу l точки P = l * Q")

            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            p, b, Q, r = read_curve()
            l = input("Укажите число l: ")
            while not l.isdigit():
                print("Ошибка: l должно быть числом!!!")
                l = input("Укажите число l: ")
            l = int(l)
            P = curve.mul_scalar_(l, Q[0], Q[1], p)

            print(f"P = l * Q => P = {l} * {Q}")
            print("Сгенерированная точка P:", P)
            print("Принадлежность точки кривой E(k):", check_point_in_curve(P, 0, b, p))
            write_one_num(l, "l.txt")
            write_point(P, "P.txt")
            print("Данные записаны в файлы l.txt и P.txt")
        
        elif choice == '3':

            print("Выбран режим: Формирование подписи m")

            try:
                filename = input("Укажите подписываемый файл: ")
            except Exception as err:
                print(f"Ошибка при обращению к файлу {filename} !!!")
                print(f"Ошибка: {err}")
                break
            
            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("l.txt"):
                print("Значение лгоарифма l задано неправильно (проверьте значения файла l.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            
            p, b, Q, r = read_curve()
            k = random.randint(2, r - 2)
            R = curve.mul_scalar_(k, Q[0], Q[1], p)
            l = read_one_num("l.txt")
            s = compute_s_from_file(filename, r)
            m = (func(R) * l + k * s) % r
            write_point(R, "R.txt")
            write_one_num(m, "m.txt")
            write_one_num(s, "s.txt")
            write_one_num(k, "k.txt")

            print(f"Вычисленные значения: k = {k}, m = {m}, s = {s}, R = {R}")
            print(f"Данные записаны в файлы: k.txt, m.txt, s.txt и R.txt")


        elif choice == '4':

            print("Выбран режим: Генерация k, k' и R")

            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("k.txt"):
                print("Значение k задано неправильно (проверьте значения файла k.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("R.txt", 2):
                print("Значение точки R задано неправильно (проверьте значения файла R.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            p, b, Q, r = read_curve()
            alpha = random.randint(1, r - 1)
            k = read_one_num("k.txt")
            k_ = alpha * k % r
            R = read_point("R.txt")
            R_ = curve.mul_scalar_(alpha, R[0], R[1], p)

            print(f"Полученные значения alpha = {alpha}, k = {k}, k' = {k_}, R = {R}, R' = {R_}")
            print("Принадлежность точки кривой E(k):", check_point_in_curve(R, 0, b, p))
            
            write_one_num(k_, "k'.txt")
            write_one_num(alpha, "alpha.txt")
            write_point(R_, "R'.txt")

            print(f"Вычисленные значения: k' = {k_}, alpha = {alpha}, R' = {R_}")
            print("Данные записаны в файлы k'.txt, alpha.txt и R'.txt")
        
        elif choice == '5':

            print("Выбран режим: Вычисление показателя B")

            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break
        
            if not check_params("R.txt", 2):
                print("Значение точки R задано неправильно (проверьте значения файла R.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("R'.txt", 2):
                print("Значение точки R задано неправильно (проверьте значения файла R'.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break
            
            p, b, Q, r = read_curve()
            R_ = read_point("R'.txt")
            R = read_point("R.txt")
            f_R_ = func(R_)
            f_R = func(R)
            B = (f_R * pow(f_R_, -1, r)) % r

            write_one_num(B, "B.txt")
            print("Данные записаны в файл B.txt")
        
        elif choice == '6':

            print("Выбран режим: Вычисление новое сообщение m' и подпись s'")

            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break
            
            if not check_params("k'.txt"):
                print("Значение k' задано неправильно (проверьте значения файла k'.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("m.txt"):
                print("Значение m задано неправильно (проверьте значения файла m.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("B.txt"):
                print("Значение B задано неправильно (проверьте значения файла B.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("alpha.txt"):
                print("Значение alpha задано неправильно (проверьте значения файла alpha.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("s.txt"):
                print("Значение s задано неправильно (проверьте значения файла s.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("R'.txt", 2):
                print("Значение точки R задано неправильно (проверьте значения файла R'.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("l.txt"):
                print("Значение лгоарифма l задано неправильно (проверьте значения файла l.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            p, b, Q, r = read_curve()
            m = read_one_num("m.txt")
            B = read_one_num("B.txt")
            alpha = read_one_num("alpha.txt")
            s = read_one_num("s.txt")
            m_ = alpha * pow(B, -1, r) * m % r
            # m_ = B * m % r
            if m_ != 0:
                l = read_one_num("l.txt")
                k_ = read_one_num("k'.txt")
                R_ = read_point("R'.txt")
                f_R_ = func(R_)
                s_ = (l * f_R_ + k_ * m_) % r
                # s_ = pow(alpha, -1, p) * B * s % r
            else:
                print("m_ = 0")
                break

            print("Cообщение m' и подпись s':", m_, s_)
            write_one_num(m_, "m'.txt")
            write_one_num(s_, "s'.txt")
            print("Данные записаны в файлы m'.txt и s'.txt")
        
        elif choice == '7':

            print("Выбран режим: Верификация подписи")

            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("s'.txt"):
                print("Значение s' задано неправильно (проверьте значения файла s'.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("P.txt", 2):
                print("Значение точки P задано неправильно (проверьте значения файла P.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("R'.txt", 2):
                print("Значение точки R задано неправильно (проверьте значения файла R'.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            if not check_params("m'.txt"):
                print("Значение m' задано неправильно (проверьте значения файла m'.txt)!!")
                print("Нельзя проверить достоверность подписи!!")
                break

            p, b, Q, r = read_curve()
            s_ = read_one_num("s'.txt")
            P = read_point("P.txt")
            R_ = read_point("R'.txt")
            m_ = read_one_num("m'.txt")
            f_R_ = func(R_)
            f_R_P = curve.mul_scalar_(f_R_, P[0], P[1], p)
            m_R_ = curve.mul_scalar_(m_, R_[0], R_[1], p)
            left = curve.mul_scalar_(s_, Q[0], Q[1], p)
            right = curve.add_points(f_R_P[0], f_R_P[1], m_R_[0], m_R_[1], p)

            if left == right:
                print("Подпись подтверждена")
                print(f"Проверка: {left} = {right}")
            else:
                print("Подпись не прошла проверку")
                print(f"Проверка: {left} != {right}")
            
            # B = read_one_num("B.txt")
            # R = read_point("R.txt")
            # m = read_one_num("m.txt")
            # s = s_ * B % r


            # left = curve.mul_scalar_(s, Q[0], Q[1], p)
            # f_R = func(R)
            # f_R_P = curve.mul_scalar_(f_R, P[0], P[1], p)
            # m_R = curve.mul_scalar_(m, R[0], R[1], p)
            # right = f_R_P + m_R

            # if left == right:
            #     print("Проверка банком прошла успешно!!")
            # else:
            #     print("Проверка банком не прошла!")
        
        elif choice == '8':
            print("Выход из программы")
            break
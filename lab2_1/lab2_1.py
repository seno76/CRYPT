import random
import curve
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def check_point_in_curve(P, a, b, p):
    return P[1] ** 2 % p == (P[0] ** 3 + a * P[0] + b) % p

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

def read_curve(file_name="curve.txt"):
    with open(file_name, "r", encoding="UTF-8") as f:
        line = f.readline().split()
        p = int(line[0])
        b = int(line[1])
        Q = (int(line[2]), int(line[3]))
        r = int(line[4])
    return p, b, Q, r

def read_key():
    with open("z.txt", "r", encoding="UTF-8") as f:
        key = f.readline()
    return key

def check_period(r, R, p):
    Q1, Q2 = R[0], R[1]
    k = 1
    while Q1 != -1:
        Q1, Q2 = curve.add_points(R[0], R[1], Q1, Q2, p)
        k += 1
    print("Период", k)
    return k == r

# Функция для шифрования точки R
def encrypt_point(point, key):
    
    data = f"{point[0]} {point[1]}".encode('utf-8')
    data = pad(data, AES.block_size)

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    encrypted_data = cipher.encrypt(data)
    return iv + encrypted_data

# Запись зашифрованной точки в файл
def write_encrypted_point(encrypted_data, file_name="enc_R.txt"):
    with open(file_name, "w") as f:
        f.write(str(encrypted_data))

def read_key_as_bytes(key_int):
    key_bytes = key_int.to_bytes(16, byteorder='big')  # Преобразуем в 16-байтовый ключ
    return key_bytes

# Функция для чтения и расшифровки зашифрованной точки из файла
def decrypt_point(file_name, key):
    with open(file_name, "r") as f:
        encrypted_data = eval(f.read())


    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    x, y = map(int, decrypted_data.decode('utf-8').split())

    return (x, y)

def check_params(file_name, len_=1):
    with open(file_name, "r", encoding="UTF-8") as f:
        params = f.readline().split()
    if not params or len(params) != len_:
        return False
    for par in params:
        if not par.strip().isdigit():
            return False 
    return True


if __name__ == "__main__":
    lst_ver = [0.5]
    n = 1
    while True:
        print("\nМеню:")
        print("1. Генерация эллиптической кривой E(k)")
        print("2. Вычисление по заданному числу l точку P = l * Q (Q - образующая точка порядка r)")
        print("3. Шаг 1: Генерация k, k' и R")
        print("4. Шаг 2: Генерация случайного ключа z и зашифрование на этом ключе точку R")
        print("5. Шаг 3: Генерация бита и передача данных по каналам с0 с1")
        print("6. Шаг 4: Верификация претендента")
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

            p, b, Q, r  = curve.build_curve(l, m)
            print(f"Была сгенерирована следующая кривая: p = {p}, B = {b}, (x0, y0) = {Q}, r = {r}")
            with open("curve.txt", "w", encoding="UTF-8") as f:
                f.write(f"{p} {b} {Q[0]} {Q[1]} {r}")
            print("Кривая сохранена в файл curve.txt")
        
        elif choice == '2':
            
            print("Выбран режим: Вычисление по заданному числу l точки P = l * Q")
            a = 0
            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break
            p, b, Q, r = read_curve()
            print(f"p = {p}, b = {b}, Q = {Q}, r = {r}")

            l = input("Укажите число l (логарифм который хотим проверить): ")
            while not l.isdigit():
                print("Ошибка: l должно быть числом!!!")
                l = input("Укажите число l (логарифм который хотим проверить): ")
            
            l = int(l)

            P = curve.mul_scalar_(l, Q[0], Q[1], p)
            print(f"P = l * Q => P = {l} * {Q}")
            print("Сгенерированная точка P:", P)
            print("Принадлежность точки кривой E(k):", check_point_in_curve(P, a, b, p))

            # Запись данных в файл
            write_one_num(l, "l.txt")
            write_point(P, "P.txt")
            print("Данные записаны в файлы l.txt и P.txt")
            
        elif choice == '3':
            
            print("Выбран режим: Генерация k, k' и R")
        
            if not check_params("curve.txt", 5):
                print("Эллиптическая кривая E(k) задана неправильно (проверьте значения файла curve.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("l.txt"):
                print("Значение лгоарифма l задано неправильно (проверьте значения файла l.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("P.txt", 2):
                print("Значение точки P задано неправильно (проверьте значения файла P.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break
            
            a = 0
            p, b, Q, r = read_curve()
            l = read_one_num("l.txt")
            k = random.randint(2, r - 2)
            k_ = l * k % r
            P = read_point("P.txt")
            R = curve.mul_scalar_(k, P[0], P[1], p)
            print(f"Полученные значения k = {k}, k' = {k_}, R = {R}")
            print("Принадлежность точки кривой E(k):", check_point_in_curve(R, a, b, p))
            
            # Запись в файл
            write_one_num(k, "k.txt")
            write_one_num(k_, "k'.txt")
            write_point(R, "R.txt")

            print("Данные записаны в файлы k.txt, k'.txt и R.txt")
            
        elif choice == '4':

            print("Выбран режим: Генерация случайного ключа z и зашифрование на этом ключе точки R")
            
            if not check_params("R.txt", 2):
                print("Значение точки R задано неправильно (проверьте значения файла R.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            # Генерация 16-байтового ключа z для AES (128 бит)
            z = get_random_bytes(16)
            
            # Запись ключа z в файл для последующей расшифровки
            write_one_num(int.from_bytes(z, byteorder='big'), "z.txt")
            
            # Чтение точки R из файла
            R = read_point("R.txt")
            
            # Шифрование точки R с использованием ключа z
            encrypted_R = encrypt_point(R, z)
            
            # Запись зашифрованной точки в файл
            write_encrypted_point(encrypted_R, "enc_R.txt")
            print("Точка R зашифрована и записана в файл enc_R.txt")
            
        elif choice == '5':

            print("Выбран режим: Генерация бита и передача данных по каналам с0 с1")

            if not check_params("k.txt"):
                print("Значение k задано неправильно (проверьте значения файла k.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("k'.txt"):
                print("Значение k' задано неправильно (проверьте значения файла k'.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("z.txt"):
                print("Значение z задано неправильно (проверьте значения файла z.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            bit = random.choice([0, 1])
            write_one_num(bit, "bit.txt")
            k = read_one_num("k.txt")
            k_ = read_one_num("k'.txt")
            z = read_key()
            print(f"Бит: {bit}\nКлюч z: {z}\nk = {k}\nk'= {k_}\n")
            if bit == 0:
                write_point((z, k), "c0.txt")
                write_point((z, k_), "c1.txt")
            else:
                write_point((z, k_), "c0.txt")
                write_point((z, k), "c1.txt")
            print("Данные записаны в файлы: bit.txt, c0.txt и c1.txt")
            
        elif choice == '6':

            print("Выбран режим: Верификация претендента")

            if not check_params("P.txt", 2):
                print("Значение точки P задано неправильно (проверьте значения файла P.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("curve.txt", 5):
                print("Значения эллиптической кривой E(k) заданы неправильно (проверьте значения файла curve.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break
            
            if not check_params("bit.txt"):
                print("Значение передаваемого бита задано неправильно (проверьте значения файла bit.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("c0.txt", 2):
                print("Значения в канале c0 заданы неправильно (проверьте значения файла с0.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            if not check_params("c1.txt", 2):
                print("Значения в канале с1 заданы неправильно (проверьте значения файла с1.txt)!!")
                print("Знание логарифма претендентом не доказано!!")
                break

            # Загрузка необходимых данных
            P = read_point("P.txt")
            p, b, Q, r = read_curve()
            bit = read_one_num("bit.txt")
            if bit == 0:
                z, k = read_point("c0.txt")
                _, k_ = read_point("c1.txt")
            else:
                z, k_ = read_point("c0.txt")
                _, k = read_point("c1.txt")
            # print(z, k, k_)
            z = read_key_as_bytes(z)
            print("-------------------------->", z)
            # print(z)
            try:
                R = decrypt_point("enc_R.txt", z)

            except Exception:
                print("Ошибка при расшифровке точки R (ключ неправильный)")
                print("Знание логарифма претендентом не доказано!!")
                break
            # print("---------------------------", R)
            
            # Проверка, что R принадлежит кривой и имеет порядок r
            if not check_point_in_curve(R, 0, b, p):
                print("Ошибка: Точка R не принадлежит кривой E(k)")
                print("Знание логарифма претендентом не доказано!!")
                break
            else:
                print(f"Принадлежность точки R кривой: {True}")

            if not check_period(r, R, p):
                print(f"Точка R = {R} не имеет порядок r = {r}")
                print("Знание логарифма претендентом не доказано!!")
                break

            # Проверка условий протокола
            if bit == 0:
                
                expected_R = curve.mul_scalar_(k, P[0], P[1], p)
                if R == expected_R:
                    print("Проверка успешна: R = k * P")

                    print(f"Пользователь знает логарифм l с вероятность {lst_ver[-1]}")
                    lst_ver.append(1 - lst_ver[-1] / 2 ** n)
                    n += 1
                else:
                    print(f"Ошибка: R != k * P => {R} != {k} * {P} => {R} != {expected_R}")
                    print("Знание логарифма претендентом не доказано!!")
            else:
                expected_R = curve.mul_scalar_(k_, Q[0], Q[1], p)
                if R == expected_R:
                    print("Проверка успешна: R = k' * Q")
                    print(f"Пользователь знает логарифм l с вероятность {lst_ver[-1]}")
                    lst_ver.append(1 - lst_ver[-1] / 2 ** n)
                    n += 1
                else:
                    print(f"Ошибка: R != k' * Q => {R} != {k_} * {Q} => {R} != {expected_R}")
                    print("Знание логарифма претендентом не доказано!!")
            
        else:
            print("Выход из программы")
            break
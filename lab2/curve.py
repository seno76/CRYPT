import random 
import sys

sys.setrecursionlimit(20000)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def divider(n):
    s = 0
    q = n - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    return s, q

# a^((2^k)q) ≡ -1 (mod m) => -1 ≡ m - 1 (mod m)
def check(a, s, q, n):
    for i in range(s):
        if pow(a, pow(2, i) * q, n) == n - 1:
            return True
    return False

# Тест Робина-Миллера
def robin_miller(n, k=10):
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    else: 
        for _ in range(k):
            a = random.randint(2, n - 1)
            s, q = divider(n)
            if n % a != 0 and (pow(a, q, n) == 1 or check(a, s, q, n)):
                    continue
            else:
                return False
        return True 

def generate_prime_mod(l, n=20): 
    while True:
        p = random.getrandbits(n)
        if p < 2**(l-1):
            continue
        if robin_miller(p) and p % 6 == 1:
            return p

def gen_prime_mod_small(l, last_num):
    start = 2**(l - 1)
    end = 2**l
    if last_num != 0:
        start = last_num + 1
    for num in range(start, end):
        if robin_miller(num):
            if num % 6 == 1:
                return num
    return None

def gen_prime(n): 
    while True: 
        p = random.getrandbits(n) 
        if robin_miller(p): 
            return p

def legandre(a, n):
    a = a % n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    return t if n == 1 else 0        

def mod_sqrt(a, p):
    if legandre(a, p) != 1:
        return None
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return r
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legandre(z, p) != -1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        t_pow = t
        i = 0
        for i in range(1, m):
            t_pow = pow(t_pow, 2, p)
            if t_pow == 1:
                break
        b = pow(c, pow(2, (m - i - 1)), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r

def decompose_P_to_Z(p, D):
    if p == 1:
        return None, None
    
    if legandre(-D, p) != 1:
        return None, None
    
    u = mod_sqrt(-D % p, p)

    ui = [u]
    mi = [p]
    i = 0

    while True:
        mi.append((ui[i] ** 2 + D) // mi[i])
        ui.append(min(ui[i] % mi[i + 1], mi[i + 1] - ui[i] % mi[i + 1]))
        if mi[i + 1] == 1:
            break
        i += 1
       
    a = [0] * (i + 1)
    b = [0] * (i + 1)
    a[i] = ui[i]
    b[i] = 1

    while i != 0:
        divider = a[i] * a[i] + D * b[i] * b[i]

        if (ui[i - 1] * a[i] + D * b[i]) % divider == 0:
            a[i - 1] = (ui[i - 1] * a[i] + D * b[i]) // divider
        else:
            a[i - 1] = (-ui[i - 1] * a[i] + D * b[i]) // divider

        if (-a[i] + ui[i - 1] * b[i]) % divider == 0:
            b[i - 1] = (-a[i] + ui[i - 1] * b[i]) // divider
        else:
            b[i - 1] = (-a[i] - ui[i - 1] * b[i]) // divider

        i -= 1
    #print(a, b)

    return a[0], b[0] 

def is_cubic(a, p):
    if a % p == 0: return 0
    a %= p
    if pow(a, (p - 1) // 3, p) == 1: return 1
    else: return -1


def gen_point(p, N, r):
    while True:
        x0 = random.randint(1, p - 1)
        y0 = random.randint(1, p - 1)
        B = (pow(y0, 2) - pow(x0, 3)) % p
        if N == r:
            #print("1")
            if (legandre(B, p) != -1 or is_cubic(B, p) != -1):
                continue
        if N == 2 * r:
            #print("2")
            if (legandre(B, p) != -1 or is_cubic(B, p) != 1):
                continue
        if N == 3 * r:
            #print("3")
            if (legandre(B, p) != 1 or is_cubic(B, p) != -1):
                continue
        if N == 6 * r:
            #print("4")
            if (legandre(B, p) != 1 or is_cubic(B, p) != 1):
                continue
        break

    return x0, y0, B

def add_points(x0, y0, x1, y1, p):
    if x0 == -1:
        return (x1, y1)
    if x1 == -1:
        return (x0, y0)
    
    # Приведение координат к диапазону от 0 до p-1
    x0, y0 = x0 % p, y0 % p
    x1, y1 = x1 % p, y1 % p
    
    if x0 == x1 and y0 == y1:
        if y0 == 0:
            # Точка на бесконечности (удвоение точки, у которой y = 0)
            return -1, -1
        a = 0
        # Вычисление λ для удвоения точки
        numerator = (3 * x0 ** 2 + a) % p
        denominator = (2 * y0) % p
        lambda_ = (numerator * pow(denominator, -1, p)) % p
    else:

        if x0 == x1:
            # Если x0 = x1, а y0 != y1, то это точка на бесконечности
            return -1, -1
        
        numerator = (y1 - y0) % p
        denominator = (x1 - x0) % p
        lambda_ = (numerator * pow(denominator, -1, p)) % p

    x2 = (lambda_ ** 2 - x0 - x1) % p
    y2 = (lambda_ * (x0 - x2) - y0) % p
    
    return x2, y2

def mul_scalar_check(N, x0, y0, p):
    x1, y1 = x0, y0
    for i in range(N - 1):
        #print(f"{i + 1})", x1, y1)
        x1, y1 = add_points(x0, y0, x1, y1, p)
        #print(x1, y1)
    return x1 == -1
    

def mul_scalar_(N, x0, y0, p):
    x1, y1 = x0, y0
    for _ in range(N - 1):
        #print(f"{i + 1})", x1, y1)
        x1, y1 = add_points(x0, y0, x1, y1, p)
    return x1, y1

def build_curve(l, m, D=3, last=0):
    # Шаг 1 ------------------------
    if l < 5:
        p = gen_prime_mod_small(l, last)
        if p is None:
            print("Шаг 1: Для заданного l не удалось найти p")
            return None
    else: 
        p = generate_prime_mod(l)
    #print("--->", p)
    #print(p)
    # ------------------------------

    # Шаг 2 ------------------------
    c, d = decompose_P_to_Z(p, D)
    if c is None:
        print(f"Шаг 2: Нелья разложить число p = {p} в кольце")
        return None
    # print(c, d)
    # print(p, "=", c ** 2 + D * d ** 2)
    # ------------------------------

    # Шаг 3 ------------------------
    T = [
         c + 3 * d, -(c + 3 * d),
         c - 3 * d, -(c - 3 * d),
         2*c,-2*c
        ]
    flag = False
    
    for t in T:
        N = p + 1 + t
        # print("N = ", N)
        for multiplier in [1, 2, 3, 6]:
            if N % multiplier != 0:
                continue
            r = N // multiplier
            if robin_miller(r):
                r = int(r)
                flag = True
                #print("---->", p, N, r)
                break
        if flag:
            break

    if not flag:
        # print("Шаг 3")
        return build_curve(l, m)
    # --------------------------------

    # Шаг 4 --------------------------
    if p == r:
        return build_curve(l, m)
    
    for i in range(1, m + 1):
        if pow(p, i, r) == 1:
                print("Шаг 4: Необходимо вычислить новое p")
                return build_curve(l, m, last=p)
    # --------------------------------

    # Шаг 5 --------------------------
    x0, y0, B = gen_point(p, N, r)
    #print("x0, y0", x0, y0)
    # --------------------------------

    # Шаг 6 --------------------------
    while not mul_scalar_check(N, x0, y0, p):
        x0, y0, B = gen_point(p, N, r)
        #print(">>>>>>>> x0, y0", x0, y0)
    # -------------------------------- 

    # Шаг 7 --------------------------
    # print(N, r, N // r)
    Q = mul_scalar_(N // r, x0, y0, p)
    #print(c, d)
    # --------------------------------
    with open("points.txt", "w", encoding="UTF-8") as f:
        x1, x2 = Q[0], Q[1]          
        while x1 != -1:
                f.write(f"{x1, x2}\n")
                x1, x2 = add_points(x1, x2, Q[0], Q[1], p)
    # Шаг 8 --------------------------
    return p, B, Q, r 
    
 
if __name__ == "__main__": 
    print("Генерация эллиптической с нулевым инвариантом (j = 0)")
    flag1, flag2 = False, False
    while not flag1:
        l = input("Укажите длину характеристики поля l: ").strip()
        if l.isdigit():
            flag1 = True
            l = int(l)
        else:
            print("Введены некорректные данные!!!")
    while not flag2:
        m = input("Укажите параметр безопасности m: ").strip()
        if m.isdigit():
            flag2 = True
            m = int(m)
        else:
            print("Введены некорректные данные!!!")
    data = build_curve(l, m)
    if data is None:
        print("Ошибка во время генерации кривой!!")
    else:
        p, B, Q, r = build_curve(l, m)
        print(f"Была сгенерирована следующая кривая: p = {p}, B = {B}, (x0, y0) = {Q}, r = {r}")
        with open("curve.txt", "w", encoding="UTF-8") as f:
            f.write(f"{p}, {B}, {Q}, {r}")
        print("Результат был записан в файл curve.txt")
        #print("Точки были записаны в файл points.txt")
        # Генерация точек в файл
        with open("points.txt", "w", encoding="UTF-8") as f:
            x1, x2 = Q[0], Q[1]          
            while x1 != -1:
                    f.write(f"{x1, x2}\n")
                    x1, x2 = add_points(x1, x2, Q[0], Q[1], p)
        diagram_flag = input("Отобразить точки на граффике ? (1 - Да, 2 - Нет): ")
        print(f"Уравнение: y^2 = x^3 + B")
        print(f"Проверка: {Q[1]} ^ 2 (mod {p}) = {Q[0]} ^ 3 + {B} (mod {p})")
        print(f"Результат : {pow(Q[1], 2, p)} = {(pow(Q[0], 3, p) + B % p) % p}")
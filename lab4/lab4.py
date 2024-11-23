from sympy import isprime
import sys

class Tee:
    """Класс для дублирования вывода в терминал и файл."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def is_point_on_curve(x, y, p):
    return (y ** 2) % p == (x ** 3 + 2 * x + 1) % p

def check_discriminant(a, b):
    # Формула дискриминанта: -16 * (4 * a^3 + 27 * b^2)
    discriminant = -16 * (4 * a ** 3 + 27 * b ** 2)
    print(f"Вычисление дискриминанта: -16 * (4 * {a}^3 + 27 * {b}^2)")
    print(f"4 * {a}^3 = {4 * a ** 3}")
    print(f"27 * {b}^2 = {27 * b ** 2}")
    print(f"Дискриминант = {discriminant}")
    return discriminant != 0

def generate_points(p):
    points = []
    for x in range(p):
        for y in range(p):
            if is_point_on_curve(x, y, p):
                points.append((x, y))
    return points

def point_addition(P, Q, p):
    if P == "O":
        return Q
    if Q == "O":
        return P
    
    x1, y1 = P
    x2, y2 = Q
    
    if P != Q:
        if x1 == x2:
            return "O"
        slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    else:
        if y1 == 0:
            return "O"
        slope = ((3 * x1 ** 2 + 2) * pow(2 * y1, -1, p)) % p
    
    x3 = (slope ** 2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)

def create_addition_table(points, p):
    table = {}
    for P in points:
        table[P] = {}
        for Q in points:
            table[P][Q] = point_addition(P, Q, p)
    return table

def print_addition_table(table):
    # Форматированная печать таблицы сложения
    points = list(table.keys())
    cell_width = 10  # Ширина ячейки для выравнивания

    # Заголовок таблицы
    header = "".join(f"{str(P):^{cell_width}}" for P in points)
    print(f"{'':^{cell_width}}{header}")

    # Строки таблицы
    for P in points:
        row = "".join(f"{str(table[P][Q]):^{cell_width}}" for Q in points)
        print(f"{str(P):^{cell_width}}{row}")


def verify_group_properties(points, p):
    identity = "O"
    for P in points:
        print(f"\nПроверка точки: {P}")
        
        # Проверка наличия обратного элемента
        for Q in points:
            result = point_addition(P, Q, p)
            if result == identity:
                print(f"{P} + {Q} = {identity} (обратный элемент для {P} найден)")
                break
        
        # Проверка ассоциативности
        for Q in points:
            for R in points:
                left = point_addition(point_addition(P, Q, p), R, p)
                right = point_addition(P, point_addition(Q, R, p), p)
                print(f"({P} + {Q}) + {R} = {left}, {P} + ({Q} + {R}) = {right}")
                if left != right:
                    print("Ассоциативность нарушена.")
                    return False
    print("Все точки удовлетворяют свойствам группы.")
    return True

def add_points(x0, y0, x1, y1, p, a=0):
    if x0 == -1:
        return (x1, y1)
    if x1 == -1:
        return (x0, y0)
    
    # Приведение координат к диапазону от 0 до p-1
    x0, y0 = x0 % p, y0 % p
    x1, y1 = x1 % p, y1 % p
    if x0 == x1 and y0 == y1:
        
        if y0 == 0:
            print("x1 == x2, y1 == y2 == 0:")
            # Точка на бесконечности (удвоение точки, у которой y = 0)
            return -1, -1
        print("x1 == x2, y1 == y2 != 0:")
        # Вычисление λ для удвоения точки
        numerator = (3 * x0 ** 2 + a) % p
        denominator = (2 * y0) % p
        lambda_ = (numerator * pow(denominator, -1, p)) % p
        print(f"    l = (3x1**2 + a) / 2y1) mod (p) = (3*{x1} ** 2  + {a}) / 2 * {y1}) mod ({p}) = {lambda_}")
        
    else:

        if x0 == x1:
            # Если x0 = x1, а y0 != y1, то это точка на бесконечности
            return -1, -1
        print("x1 != x2:")
        numerator = (y1 - y0) % p
        denominator = (x1 - x0) % p
        lambda_ = (numerator * pow(denominator, -1, p)) % p
        print(f"    l = (y2 - y1 / x2 - x1) mod (p) = ({y1} - {y0} / {x1} - {x0}) mod ({p}) = {lambda_}")
        
        print(f"    l = {lambda_}")

    x2 = (lambda_ ** 2 - x0 - x1) % p
    y2 = (lambda_ * (x0 - x2) - y0) % p

    print(f"    x3 = l^2 - x1 - x2 (mod p) => {lambda_}^2 - {x0} - {x1} (mod {p})")
    print(f"    y3 = l*(x1 - x3) - y1 (mod p) => {lambda_}*({x0} - {x2}) - {y0} (mod {p})")
    print(f"    x3 = {x2}, y3 = {y2}")
    
    return x2, y2



def find_period_point(points, p, a):
    for i, point in enumerate(points):
        print(f"Точка {i + 1}: P = {point}")
        if point == 'O':
            print("Бесконечная точка не является образующим элементом!")
        else:
            x2 = point[0]
            y2 = point[1]
            count = 1  # Начинаем с 1, так как первая точка уже включена
            while (x2, y2) != (-1, -1):
                print(f"Шаг {count}: Точка P = {x2, y2} Вычислим {count + 1}*P = {x2, y2} + {point[0], point[1]}")
                x2, y2 = add_points(x2, y2, point[0], point[1], p, a)
                count += 1  # Правильное увеличение счетчика
            print("Порядок:", count, "\n")
            print("-------------------------------------------------------------------")


def check_cyclic_group(points, p):
    print("5) Проверка, является ли группа циклической и поиск образующего элемента.")
    for i, point in enumerate(points):
        generated_points = set()
        Q = point
        print(f"\nПроверка точки {point} как возможного образующего элемента:")
        
        while Q != "O":
            generated_points.add(Q)
            print(f"Рассматриваемая точка: {Q}")
            Q = point_addition(Q, point, p)
        
        if len(generated_points) == len(points) - 1:
            print(f"Группа циклическая. Порождающий элемент: {point}")
            return
    print("Группа не является циклической.")

if __name__ == "__main__":
    p = 5
    a, b = 2, 1  # Коэффициенты для уравнения кривой y^2 = x^3 + ax + b
    p = int(input("Укажите p (Z_p над многочленом): "))
    a = int(input("Укажите a для уравнения (y^2 = x^3 + ax + b): "))
    b = int(input("Укажите b для уравнения (y^2 = x^3 + ax + b): "))
    sys.stdout = Tee("report.txt")  # Дублирование вывода в файл report.txt
    if isprime(p):
        print("1) Проверка дискриминанта для существования эллиптической кривой.")
        if not check_discriminant(a, b):
            print("Это не эллиптическая кривая.")
        else:
            print("Дискриминант не равен нулю, эллиптическая кривая существует.")
            
            print("\n2) Поиск всех точек на кривой E над Z_5.")
            points = generate_points(p)
            points.append("O")
            print("Найденные точки:", points)
            
            print("\n3) Построение таблицы сложения всех точек.")
            addition_table = create_addition_table(points, p)
            print_addition_table(addition_table)
                
            
            print("\n4) Проверка свойств группы для найденных точек.")
            if not verify_group_properties(points, p):
                print("Найденные точки не образуют группу.")
            else:
                find_period_point(points, p, a)
                check_cyclic_group(points, p)
    else:
        print("Ошибка!!! (p - должно быть простым числом)")
import random
import curve


print(curve.mul_scalar_(7, 2, 5, 11, 5))
print(curve.add_points(2, 6, 2, 5, 11, 5))
# print(curve.add_points(3, 4, 2, 5, 11, 5))


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



def main(x1, y1, p, a):
    x2 = x1
    y2 = y1
    count = 1  # Начинаем с 1, так как первая точка уже включена
    
    while (x2, y2) != (-1, -1):
        print(f"Шаг {count}: Точка P = {x2, y2} Вычислим {count + 1}*P = {x2, y2} + {x1, y1}")
        x2, y2 = add_points(x2, y2, x1, y1, p, a)
        count += 1  # Правильное увеличение счетчика
    
    print("Порядок:", count)

main(3, 3, 5, 2)
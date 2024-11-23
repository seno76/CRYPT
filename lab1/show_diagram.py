import matplotlib.pyplot as plt
from sympy import jacobi_symbol as jacobi

# Извлечение квадратного корня в кольце вычетов
def mod_sqrt(a, p):
    if jacobi(a, p) != 1:
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
    while jacobi(z, p) != -1:
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


def find_points_on_curve(B, p):
    points = []
    
    # Для всех x в поле Z_p
    for x in range(p):
        # Вычисляем правую часть уравнения y^2 = x^3 + B (mod p)
        right_side = (x**3 + B) % p
        
        # Ищем квадратичный корень (если существует)
        y = mod_sqrt(right_side, p)
        
        # Если квадратичный корень существует, добавляем точки (x, y) и (x, p - y)
        if y is not None:
            points.append((x, y))
            if y != 0:
                points.append((x, p - y))
    
    return points

def plot_curve(B, p, point_to_highlight=None):
    points = find_points_on_curve(B, p)
    
    if not points:
        print("Не найдено точек на кривой")
        return

    # Разбиваем на координаты x и y для построения графика
    x_vals = [point[0] for point in points]
    y_vals = [point[1] for point in points]
    
    plt.figure(figsize=(6, 6))
    plt.scatter(x_vals, y_vals, color='blue', label='Точки на кривой')
    
    # Если точка для выделения задана
    if point_to_highlight is not None:
        hx, hy = point_to_highlight
        # Отображаем заданную точку красным цветом
        plt.scatter(hx, hy, color='red', s=100, label=f'Заданная точка ({hx}, {hy})')
    
    plt.title(f'Эллиптическая кривая $y^2 = x^3 + {B}$ над полем Z_{p}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Пример использования
    B = 22449  # Задаём значение B
    p = 57847  # Простое число p
    point_to_highlight = (2878, 14535)  # Заданная точка, которую нужно выделить красным цветом

    plot_curve(B, p, point_to_highlight)
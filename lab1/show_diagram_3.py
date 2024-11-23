import matplotlib.pyplot as plt

# Функция для чтения точек из файла
def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            # Убираем лишние символы и разбиваем строку на координаты
            line = line.strip().strip('()')
            x, y = map(int, line.split(', '))
            points.append((x, y))
    return points

def plot_curve_from_file(filename, B, p, point_to_highlight=None):
    points = read_points_from_file(filename)
    
    if not points:
        print("Не найдено точек в файле")
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
    
    plot_curve_from_file('points.txt', 210, 433, (343, 41))
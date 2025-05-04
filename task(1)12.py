import os
import math
import numpy as np
import matplotlib.pyplot as plt

# Параметры функции
A = 0
x_start = -5.12
x_end = 5.12
step = 0.01  

# Создаем директорию results, если ее нет
if not os.path.exists('results'):
    os.makedirs('results')

# Вычисляем значения функции
x_values = np.arange(x_start, x_end + step, step)
y_values = [-1 + (math.cos(12 * math.sqrt(x**2 + A**2))) / (0.5 * (x**2 + A**2) + 2) for x in x_values]

# Сохраняем результаты в файл
with open('results/function_results.txt', 'w') as file:
    for x, y in zip(x_values, y_values):
        file.write(f"{x:.4f}    {y:.10f}\n")

# Строим график
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label='f(x)')
plt.title('График функции f(x) = -1 + cos(12√(x²+A²))/(0.5(x²+A²)+2)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.savefig('results/function_plot.png')
plt.show()

print("Расчет завершен. Результаты сохранены в папке results.")
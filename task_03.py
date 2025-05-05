import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(x1, x2):
    numerator = np.cos(np.sin(np.abs(x1**2 - x2**2)))**2 - 0.5
    denominator = (1 + 0.001 * (x1**2 + x2**2))**2
    return 0.5 + numerator / denominator

# Параметры
x1_min, x1_max = -2.0, 2.0
x2_min, x2_max = -2.0, 2.0
x10, x20 = 0.0, 0.0  # тестовая точка

# Создание сетки
x1 = np.linspace(x1_min, x1_max, 100)
x2 = np.linspace(x2_min, x2_max, 100)
X1, X2 = np.meshgrid(x1, x2)
Y = f(X1, X2)

# Значение в тестовой точке
y_test = f(x10, x20)

# Создание фигуры с увеличенным размером и лучшим расположением
fig = plt.figure(figsize=(16, 12))
fig.suptitle(f'Графики функции. Тестовая точка: ({x10}, {x20}), f={y_test:.6f}', 
              fontsize=16, y=0.98)

# 1. 3D поверхность (изометрический вид)
ax1 = fig.add_subplot(221, projection='3d')
surf = ax1.plot_surface(X1, X2, Y, cmap='viridis', edgecolor='none', alpha=0.9)
ax1.set_xlabel('x1', labelpad=10)
ax1.set_ylabel('x2', labelpad=10)
ax1.set_zlabel('y = f(x1, x2)', labelpad=10)
ax1.set_title('1. 3D поверхность (изометрический вид)', pad=15)
ax1.view_init(elev=30, azim=45)  # Улучшенный угол обзора
fig.colorbar(surf, ax=ax1, shrink=0.6, aspect=10, pad=0.1)

# 2. Вид сверху (проекция на XOY)
ax2 = fig.add_subplot(222)
contour = ax2.contourf(X1, X2, Y, levels=20, cmap='viridis')
ax2.set_xlabel('x1', labelpad=10)
ax2.set_ylabel('x2', labelpad=10)
ax2.set_title('2. Вид сверху (проекция на плоскость XOY)', pad=15)
fig.colorbar(contour, ax=ax2, shrink=0.6, aspect=10, pad=0.1)

# 3. График y = f(x1) при x2 = x20
ax3 = fig.add_subplot(223)
y_x1 = f(x1, x20)
ax3.plot(x1, y_x1, 'b', linewidth=2, label=f'x2 = {x20}')
ax3.scatter(x10, y_test, color='red', s=100, zorder=5, label='Тестовая точка')
ax3.set_xlabel('x1', labelpad=10)
ax3.set_ylabel('y = f(x1, x2)', labelpad=10)
ax3.set_title(f'3. График y = f(x1) при x2 = {x20}', pad=15)
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.legend(loc='upper right')

# 4. График y = f(x2) при x1 = x10
ax4 = fig.add_subplot(224)
y_x2 = f(x10, x2)
ax4.plot(x2, y_x2, 'r', linewidth=2, label=f'x1 = {x10}')
ax4.scatter(x20, y_test, color='red', s=100, zorder=5, label='Тестовая точка')
ax4.set_xlabel('x2', labelpad=10)
ax4.set_ylabel('y = f(x1, x2)', labelpad=10)
ax4.set_title(f'4. График y = f(x2) при x1 = {x10}', pad=15)
ax4.grid(True, linestyle='--', alpha=0.7)
ax4.legend(loc='upper right')

# Улучшенное расположение подграфиков
plt.tight_layout(pad=3.0, h_pad=3.0, w_pad=3.0)
plt.subplots_adjust(top=0.92)  # Добавляем место для общего заголовка

plt.show()
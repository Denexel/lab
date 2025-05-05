import requests
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt
import json
import toml
from math import pi

class RCSCalculator:
    def __init__(self, D, fmin, fmax, num_points=1000):
        self.r = D / 2  # радиус сферы
        self.fmin = fmin
        self.fmax = fmax
        self.num_points = num_points
        self.frequencies = np.linspace(fmin, fmax, num_points)
        self.rcs_values = []
    
    def calculate_rcs(self):
        c = 3e8  # скорость света
        self.rcs_values = []
        
        for f in self.frequencies:
            lambda_ = c / f
            k = 2 * np.pi / lambda_
            kr = k * self.r
            
            sum_rcs = 0 + 0j  # Комплексная сумма
            
            # Вычисляем сумму до N=50 (достаточно для сходимости)
            for n in range(1, 50):
                # Сферические функции Бесселя первого и второго рода
                jn = spherical_jn(n, kr)
                yn = spherical_yn(n, kr)
                
                # Сферическая функция Ханкеля (третьего рода)
                hn = jn + 1j * yn
                
                # Производные функций
                jn_deriv = spherical_jn(n, kr, derivative=True)
                yn_deriv = spherical_yn(n, kr, derivative=True)
                hn_deriv = jn_deriv + 1j * yn_deriv
                
                # Коэффициент a_n
                an = spherical_jn(n, kr) / hn
                
                # Коэффициент b_n
                numerator = kr * spherical_jn(n-1, kr) - n * spherical_jn(n, kr)
                denominator = kr * (spherical_jn(n-1, kr) + 1j * spherical_yn(n-1, kr)) - n * hn
                bn = numerator / denominator
                
                # Добавляем к сумме
                sum_rcs += (-1)**n * (n + 0.5) * (bn - an)
            
            # Вычисляем ЭПР
            sigma = (lambda_**2 / pi) * np.abs(sum_rcs)**2
            self.rcs_values.append(sigma)
        
        return self.frequencies, self.rcs_values
    
    def plot_rcs(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.frequencies, self.rcs_values)
        plt.xlabel('Частота (Гц)')
        plt.ylabel('ЭПР (м²)')
        plt.title('Зависимость ЭПР идеально проводящей сферы от частоты')
        plt.grid(True)
        plt.show()

class ResultWriter:
    @staticmethod
    def write_toml(frequencies, rcs_values, filename):
        data = []
        c = 3e8  # скорость света
        
        for f, rcs in zip(frequencies, rcs_values):
            lambda_ = c / f
            data.append({
                "freq": float(f),
                "lambda": float(lambda_),
                "rcs": float(rcs)
            })
        
        with open(filename, 'w') as f:
            toml.dump({"data": data}, f)

def download_and_parse_task(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить файл: {response.status_code}")
    
    content = response.text
    
    # Парсим TOML файл (для варианта 12)
    try:
        data = toml.loads(content)
        variant_data = data.get('12', {})
        D = variant_data.get('D', 0.1)
        fmin = variant_data.get('fmin', 1e6)
        fmax = variant_data.get('fmax', 10e9)
        return D, fmin, fmax
    except Exception as e:
        raise Exception(f"Ошибка парсинга TOML файла: {e}")

def main():
    # Параметры для варианта 12
    task_url = "https://jenyay.net/uploads/Student/Modelling/task_rcs_02.toml"
    output_format = 3  # TOML для варианта 12
    output_filename = "result_12.toml"
    
    try:
        # Загружаем и парсим файл задания
        D, fmin, fmax = download_and_parse_task(task_url)
        print(f"Параметры сферы: D={D} м, fmin={fmin} Гц, fmax={fmax} Гц")
        
        # Создаем калькулятор и рассчитываем ЭПР
        calculator = RCSCalculator(D, fmin, fmax)
        frequencies, rcs_values = calculator.calculate_rcs()
        
        # Строим график
        calculator.plot_rcs()
        
        # Сохраняем результаты в файл
        if output_format == 3:  # TOML
            ResultWriter.write_toml(frequencies, rcs_values, output_filename)
            print(f"Результаты сохранены в {output_filename}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
import requests
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt
import json
from math import pi

class RCSCalculator:
    def __init__(self, D, fmin, fmax, num_points=1000):
        self.r = D / 2
        self.fmin = fmin
        self.fmax = fmax
        self.num_points = num_points
        self.frequencies = np.linspace(fmin, fmax, num_points)
        self.rcs_values = []
    
    def calculate_rcs(self):
        c = 3e8
        self.rcs_values = []
        
        for f in self.frequencies:
            lambda_ = c / f
            k = 2 * np.pi / lambda_
            kr = k * self.r
            
            sum_rcs = 0 + 0j
            
            for n in range(1, 50):
                jn = spherical_jn(n, kr)
                yn = spherical_yn(n, kr)
                hn = jn + 1j * yn
                
                jn_deriv = spherical_jn(n, kr, derivative=True)
                yn_deriv = spherical_yn(n, kr, derivative=True)
                hn_deriv = jn_deriv + 1j * yn_deriv
                
                an = jn / hn
                numerator = kr * spherical_jn(n-1, kr) - n * jn
                denominator = kr * (spherical_jn(n-1, kr) + 1j * spherical_yn(n-1, kr)) - n * hn
                bn = numerator / denominator
                
                sum_rcs += (-1)**n * (n + 0.5) * (bn - an)
            
            sigma = (lambda_**2 / pi) * np.abs(sum_rcs)**2
            self.rcs_values.append(sigma)
        
        return self.frequencies, self.rcs_values
    
    def plot_rcs(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.frequencies, self.rcs_values)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('RCS (m²)')
        plt.title('RCS of Perfectly Conducting Sphere vs Frequency')
        plt.grid(True)
        plt.show()  # Важно: добавить это для отображения графика

class ResultWriter:
    @staticmethod
    def write_json(frequencies, rcs_values, filename):
        c = 3e8
        data = {
            "freq": [float(f) for f in frequencies],
            "lambda": [float(c/f) for f in frequencies],
            "rcs": [float(rcs) for rcs in rcs_values]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

def download_and_parse_task(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    
    content = response.text
    
    try:
        import toml
        data = toml.loads(content)
        variant_data = data.get('12', {})
        D = float(variant_data.get('D', "70e-3").strip('"'))
        fmin = float(variant_data.get('fmin', "0.01e9").strip('"'))
        fmax = float(variant_data.get('fmax', "25e9").strip('"'))
        return D, fmin, fmax
    except Exception as e:
        raise Exception(f"Error parsing task file: {e}")

def main():
    task_url = "https://jenyay.net/uploads/Student/Modelling/task_rcs_02.toml"
    output_filename = "result_12.json"
    
    try:
        D, fmin, fmax = download_and_parse_task(task_url)
        print(f"Sphere parameters: D={D} m, fmin={fmin} Hz, fmax={fmax} Hz")
        
        calculator = RCSCalculator(D, fmin, fmax, num_points=200)  # Можно уменьшить кол-во точек для быстрого теста
        frequencies, rcs_values = calculator.calculate_rcs()
        
        calculator.plot_rcs()  # Теперь график точно появится
        
        ResultWriter.write_json(frequencies, rcs_values, output_filename)
        print(f"Results saved to {output_filename}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
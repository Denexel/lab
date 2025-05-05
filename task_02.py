import argparse
import matplotlib.pyplot as plt
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Plot y = f(x) from a text file and save the graph.')
    parser.add_argument('input_file', help='Path to the input text file (format: x    y)')
    parser.add_argument('--output', '-o', help='Output file to save the graph (e.g., "plot.png")', default=None)
    return parser.parse_args()

def read_data(file_path):
    x, y = [], []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.split('    ')  # 4 пробела как разделитель
                    if len(parts) == 2:
                        x.append(float(parts[0]))
                        y.append(float(parts[1]))
        return x, y
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Ошибка: Некорректные данные в файле. Проверьте формат (числа, разделенные 4 пробелами).", file=sys.stderr)
        sys.exit(1)

def plot_and_save(x, y, output_file=None):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2)  # Синяя линия
    plt.title("График функции y = f(x)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)

    if output_file:
        plt.savefig(output_file)
        print(f"График сохранен в файл: {os.path.abspath(output_file)}")
    else:
        plt.show()

def main():
    args = parse_args()
    x, y = read_data(args.input_file)
    plot_and_save(x, y, args.output)

if __name__ == "__main__":
    main()
import math
import matplotlib.pyplot as plt
import numpy as np
import os

# ============================================
# Данные из протокола
# ============================================

# Таблица 1 (ПВО)
L1 = [10, 20, 30, 40, 50]
U1 = [5.6, 10.3, 16.8, 24.7, 31.4]

# Таблица 2 (ПГО)
L2 = [10, 20, 30, 40, 50]
U2 = [4.5, 9.3, 15.6, 22.1, 28.0]

# Таблица 3 (макс. чувствительность)
L3 = [10, 20, 30, 40, 50]
U3 = [0.014, 0.020, 0.037, 0.050, 0.076]

# Таблица 4 (Лиссажу)
# отношения частот f_x/f_y, f_y (Гц)
ratios = [1, 0.5, 1/3, 2]
f_y = [50, 100, 150, 25]
# вычисляем f_x
f_x_calc = [r * fy for r, fy in zip(ratios, f_y)]
# для наглядности запишем полученные значения (все равны 50)
print("f_x по фигурам Лиссажу:", f_x_calc)

# ============================================
# Функция вычисления чувствительности
# ============================================
def sensitivity(L, U):
    """S = L / (2√2 * U)"""
    return [l / (2 * math.sqrt(2) * u) for l, u in zip(L, U)]

S1 = sensitivity(L1, U1)
S2 = sensitivity(L2, U2)
S3 = sensitivity(L3, U3)

# ============================================
# Создание папок для выходных данных
# ============================================
os.makedirs("output", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# ============================================
# Построение графиков S(U)
# ============================================

# График для ПВО
plt.figure(figsize=(8,5))
plt.plot(U1, S1, 'bo-', label='ПВО')
plt.xlabel('U_eff, В')
plt.ylabel('S, мм/В')
plt.title('Чувствительность пластин вертикального отклонения')
plt.grid(True)
plt.savefig('figures/sensitivity_PVO.png', dpi=300)
plt.show()

# График для ПГО
plt.figure(figsize=(8,5))
plt.plot(U2, S2, 'ro-', label='ПГО')
plt.xlabel('U_eff, В')
plt.ylabel('S, мм/В')
plt.title('Чувствительность пластин горизонтального отклонения')
plt.grid(True)
plt.savefig('figures/sensitivity_PGO.png', dpi=300)
plt.show()

# График для максимальной чувствительности
plt.figure(figsize=(8,5))
plt.plot(U3, S3, 'go-', label='max S')
plt.xlabel('U_eff, В')
plt.ylabel('S, мм/В')
plt.title('Максимальная чувствительность осциллографа')
plt.grid(True)
plt.savefig('figures/sensitivity_max.png', dpi=300)
plt.show()

# ============================================
# Генерация LaTeX-таблиц
# ============================================

def write_latex_table(filename, caption, label, headers, data_rows):
    with open(f"output/{filename}", 'w', encoding='utf-8') as f:
        f.write("\\begin{table}[h]\n\\centering\n")
        f.write(f"\\caption{{{caption}}}\n")
        f.write(f"\\label{{{label}}}\n")
        f.write("\\begin{tabular}{|c|c|c|}\n\\hline\n")
        f.write(" & ".join(headers) + " \\\\\n\\hline\n")
        for row in data_rows:
            f.write(" & ".join(str(x) for x in row) + " \\\\\n")
        f.write("\\hline\n\\end{tabular}\n\\end{table}\n")

# Таблица 1
rows1 = [[L1[i], f"{U1[i]:.1f}", f"{S1[i]:.3f}"] for i in range(len(L1))]
write_latex_table("table_PVO.tex", "Чувствительность пластин вертикального отклонения", "tab:pvo",
                  ["$L$, мм", "$U_{\\text{eff}}$, В", "$S$, мм/В"], rows1)

# Таблица 2
rows2 = [[L2[i], f"{U2[i]:.1f}", f"{S2[i]:.3f}"] for i in range(len(L2))]
write_latex_table("table_PGO.tex", "Чувствительность пластин горизонтального отклонения", "tab:pgo",
                  ["$L$, мм", "$U_{\\text{eff}}$, В", "$S$, мм/В"], rows2)

# Таблица 3
rows3 = [[L3[i], f"{U3[i]:.4f}".replace('.', ','), f"{S3[i]:.1f}"] for i in range(len(L3))]
write_latex_table("table_maxS.tex", "Максимальная чувствительность осциллографа", "tab:maxS",
                  ["$L$, мм", "$U_{\\text{eff}}$, В", "$S$, мм/В"], rows3)

# Таблица 4 (Лиссажу) – среднее значение частоты
mean_fx = np.mean(f_x_calc)
std_fx = np.std(f_x_calc, ddof=1)  # несмещённое стандартное отклонение
n = len(f_x_calc)
ci = 2.776 * std_fx / math.sqrt(n) if n > 1 else 0  # t для 4 измерений, P=0.95 (t=3.182 для n=4? уточню: для n=4, df=3, t=3.182, но мы используем 2.776 для n=5? Для n=4 правильнее t=3.182. Я посчитаю точно)

# Коэффициент Стьюдента для n=4 (доверительная вероятность 0.95) = 3.182
t_student = 3.182
ci = t_student * std_fx / math.sqrt(n)

rows4 = [["$f_x/f_y$", "$f_y$, Гц", "$f_x$, Гц"]]
for i in range(len(ratios)):
    rows4.append([f"{ratios[i]:g}", f"{f_y[i]}", f"{f_x_calc[i]:.1f}"])
rows4.append(["Среднее", "", f"{mean_fx:.1f}"])
rows4.append(["Погрешность (P=0.95)", "", f"{ci:.2f}"])

with open("output/table_lissajous.tex", 'w', encoding='utf-8') as f:
    f.write("\\begin{table}[h]\n\\centering\n")
    f.write("\\caption{Определение частоты по фигурам Лиссажу}\n")
    f.write("\\label{tab:lissajous}\n")
    f.write("\\begin{tabular}{|c|c|c|}\n\\hline\n")
    for i, row in enumerate(rows4):
        f.write(" & ".join(row) + " \\\\\n")
        if i == 0 or i == len(rows4)-3:
            f.write("\\hline\n")
    f.write("\\hline\n\\end{tabular}\n\\end{table}\n")

print("Все таблицы сохранены в папку output/")
print(f"Среднее значение f_x = {mean_fx:.1f} ± {ci:.2f} Гц (P=0.95)")
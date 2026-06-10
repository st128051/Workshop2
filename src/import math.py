import math
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats   # для линейной регрессии

# Данные из протокола
L1 = [10, 20, 30, 40, 50]
U1 = [5.6, 10.3, 16.8, 24.7, 31.4]

L2 = [10, 20, 30, 40, 50]
U2 = [14.5, 18.3, 22.0, 25.6, 28.0]

L3 = [10, 20, 30, 40, 50]
U3 = [0.040, 0.020, 0.010, 0.005, 0.0046]

# Лиссажу
ratios = [1, 0.5, 1/3, 2]
f_y = [50, 100, 150, 25]
f_x_calc = [r * fy for r, fy in zip(ratios, f_y)]
print("f_x по фигурам Лиссажу:", f_x_calc)

# Расчёт чувствительности S = L / (2√2 * U)
def sensitivity(L, U):
    return [l / (2 * math.sqrt(2) * u) for l, u in zip(L, U)]

S1 = sensitivity(L1, U1)
S2 = sensitivity(L2, U2)
S3 = sensitivity(L3, U3)

# Погрешности
L_err = 0.5          # погрешность длины, мм
U_rel_err = 0.01     # относительная погрешность напряжения 1%

def compute_errors(L, U, S):
    U_err = [u * U_rel_err for u in U]
    S_err = []
    for i in range(len(S)):
        rel_err = math.sqrt((L_err / L[i])**2 + U_rel_err**2)
        S_err.append(S[i] * rel_err)
    return U_err, S_err

U1_err, S1_err = compute_errors(L1, U1, S1)
U2_err, S2_err = compute_errors(L2, U2, S2)
U3_err, S3_err = compute_errors(L3, U3, S3)

# Одинаковые погрешности (средние)
U1_err_mean = np.mean(U1_err)
S1_err_mean = np.mean(S1_err)
U2_err_mean = np.mean(U2_err)
S2_err_mean = np.mean(S2_err)
U3_err_mean = np.mean(U3_err)
S3_err_mean = np.mean(S3_err)

# Создаём папки
os.makedirs("output", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# ---------- График 1: ПВО (с линейной регрессией и доверительной полосой) ----------
plt.figure(figsize=(8,5))
plt.errorbar(U1, S1, xerr=U1_err_mean, yerr=S1_err_mean, fmt='bo',
             markersize=4, markeredgewidth=0.5, capsize=4, ecolor='red',
             label='Экспериментальные точки')

# Линейная регрессия (МНК)
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(U1, S1)
U_fit = np.linspace(min(U1), max(U1), 100)
S_fit1 = slope1 * U_fit + intercept1
plt.plot(U_fit, S_fit1, 'b-', linewidth=1.5, label=f'Линейная регрессия: S = {slope1:.3f}·U + {intercept1:.3f}')

# Доверительный интервал для среднего (95%)
n1 = len(U1)
residuals1 = np.array(S1) - (slope1 * np.array(U1) + intercept1)
s_err1 = np.sqrt(np.sum(residuals1**2) / (n1-2))
mean_U1 = np.mean(U1)
t_val1 = stats.t.ppf(0.975, n1-2)   # 95% доверительный интервал
se_fit1 = s_err1 * np.sqrt(1/n1 + (U_fit - mean_U1)**2 / np.sum((np.array(U1)-mean_U1)**2))
ci1 = t_val1 * se_fit1
plt.fill_between(U_fit, S_fit1 - ci1, S_fit1 + ci1, color='blue', alpha=0.2, label='95% доверительный интервал')

plt.xlabel('U_eff, В')
plt.ylabel('S, мм/В')
plt.title('Чувствительность пластин вертикального отклонения')
plt.grid(True)
plt.legend()
plt.savefig('figures/sensitivity_PVO.png', dpi=300)
plt.show()

# ---------- График 2: ПГО (с линейной регрессией и доверительной полосой) ----------
plt.figure(figsize=(8,5))
plt.errorbar(U2, S2, xerr=U2_err_mean, yerr=S2_err_mean, fmt='ro',
             markersize=4, markeredgewidth=0.5, capsize=4, ecolor='red',
             label='Экспериментальные точки')

slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(U2, S2)
S_fit2 = slope2 * U_fit + intercept2
plt.plot(U_fit, S_fit2, 'r-', linewidth=1.5, label=f'Линейная регрессия: S = {slope2:.3f}·U + {intercept2:.3f}')

n2 = len(U2)
residuals2 = np.array(S2) - (slope2 * np.array(U2) + intercept2)
s_err2 = np.sqrt(np.sum(residuals2**2) / (n2-2))
mean_U2 = np.mean(U2)
t_val2 = stats.t.ppf(0.975, n2-2)
se_fit2 = s_err2 * np.sqrt(1/n2 + (U_fit - mean_U2)**2 / np.sum((np.array(U2)-mean_U2)**2))
ci2 = t_val2 * se_fit2
plt.fill_between(U_fit, S_fit2 - ci2, S_fit2 + ci2, color='red', alpha=0.2, label='95% доверительный интервал')

plt.xlabel('U_eff, В')
plt.ylabel('S, мм/В')
plt.title('Чувствительность пластин горизонтального отклонения')
plt.grid(True)
plt.legend()
plt.savefig('figures/sensitivity_PGO.png', dpi=300)
plt.show()

# ---------- График 3: максимальная чувствительность (без регрессии, только точки) ----------
plt.figure(figsize=(8,5))
plt.errorbar(U3, S3, xerr=U3_err_mean, yerr=S3_err_mean, fmt='go',
             markersize=4, markeredgewidth=0.5, capsize=4, ecolor='red',
             label='max S')
plt.xlabel('U_eff, В')
plt.ylabel('S, мм/В')
plt.title('Максимальная чувствительность осциллографа')
plt.grid(True)
plt.legend()
plt.savefig('figures/sensitivity_max.png', dpi=300)
plt.show()

# ---------- Генерация LaTeX-таблиц (без изменений) ----------
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

rows1 = [[L1[i], f"{U1[i]:.1f}", f"{S1[i]:.3f}"] for i in range(len(L1))]
write_latex_table("table_PVO.tex", "Чувствительность пластин вертикального отклонения", "tab:pvo",
                  ["$L$, мм", "$U_{\\text{eff}}$, В", "$S$, мм/В"], rows1)

rows2 = [[L2[i], f"{U2[i]:.1f}", f"{S2[i]:.3f}"] for i in range(len(L2))]
write_latex_table("table_PGO.tex", "Чувствительность пластин горизонтального отклонения", "tab:pgo",
                  ["$L$, мм", "$U_{\\text{eff}}$, В", "$S$, мм/В"], rows2)

rows3 = [[L3[i], f"{U3[i]:.4f}".replace('.', ','), f"{S3[i]:.1f}"] for i in range(len(L3))]
write_latex_table("table_maxS.tex", "Максимальная чувствительность осциллографа", "tab:maxS",
                  ["$L$, мм", "$U_{\\text{eff}}$, В", "$S$, мм/В"], rows3)

# Таблица Лиссажу
mean_fx = np.mean(f_x_calc)
std_fx = np.std(f_x_calc, ddof=1)
n = len(f_x_calc)
t_student = 3.182   # для n=4, P=0.95
ci = t_student * std_fx / math.sqrt(n) if n > 1 else 0

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
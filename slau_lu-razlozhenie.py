import re

VAR = r'[a-zA-Z]\d*'
NUM = r'\d+(?:\.\d+)?'

# шаблон одного члена уравнения
TERM = re.compile(
    rf'(?P<sign>[+\-])?\s*'
    rf'(?:'
    rf'(?:(?P<coef>{NUM})\s*\*?\s*)?(?P<name>{VAR})'
    rf'|'
    rf'(?P<const>{NUM})'
    rf')'
)

#--------------------------------------------------------
def main():
    w = int(input("Решение СЛАУ методом LU-разложения\n"
                  "Чтобы задать систему уравнений нажмите '1';\n"
                  "Чтобы задать матрицу нажмите '2';\n"
                  "(После ввода числа нажмите 'Enter')\n"
                  "Ваш выбор: "))
    match w:
        case 1:
            print("--------------------------------------------------------------------------------")
            n = int(input("Введите количество уравнений: "))
        case 2:
            print("--------------------------------------------------------------------------------")
            n = int(input("Введите порядок квадратной матрицы: "))
        #---------------------------------------------------------
        case 0:
            n = 5 # исходные данные к задаче

    matr = [[0.0 for j in range(n+1)] for i in range(n)]
    l = [[0.0 for j in range(n)] for i in range(n)]
    u = [[0.0 for j in range(n)] for i in range(n)]
    x = [0.0 for q in range(n)]
    y = [0.0 for p in range(n)]
    st = ['' for i in range(n)]

    #--------------------------------------------------------
    if (w == 1):
        raw = input("Введите через пробел имена переменных, которые Вы хотите использовать при вводе уравнений: ").strip()
        var_names = raw.split()
        
        if (not var_names):
            print("Список переменных пуст")
            return
            
        if (len(set(var_names)) != len(var_names)):
            print("Имена переменных не должны повторяться")
            return
        
        if (len(var_names) != n):
            print(f"Введите {n} переменных")
            return
        
        equa = []
        for o in range(n):
            line = input(f"Введите уравнение {o+1}: ").strip()
            coeffs, rhs = equation(line, var_names)
            equa.append([coeffs.get(v, 0.0) for v in var_names] + [rhs])
            matr = equa
    #--------------------------------------------------------
    if (w == 2):
        print(f"Введите расширенную матрицу размерностью {n}x{n+1}\n"
              "(Вводите построчно с пробелом после каждого числа и 'Enter' после строки): ")
        for b in range(n):
            row = list(map(float, input(f"Строка {b+1}: ").split()))
            matr[b] = row
    #--------------------------------------------------------
    if (w == 0): # исходные данные к задаче
        matr[0][0] = 3
        matr[0][1] = 4
        matr[0][2] = 4
        matr[0][3] = 5
        matr[0][4] = 6
        matr[0][5] = 22

        matr[1][0] = 7
        matr[1][1] = 3
        matr[1][2] = 7
        matr[1][3] = 2
        matr[1][4] = 1
        matr[1][5] = 20
    
        matr[2][0] = 6
        matr[2][1] = 5
        matr[2][2] = 7
        matr[2][3] = 4
        matr[2][4] = 4
        matr[2][5] = 26
    
        matr[3][0] = 4
        matr[3][1] = 7
        matr[3][2] = 7
        matr[3][3] = 6
        matr[3][4] = 7
        matr[3][5] = 31
    
        matr[4][0] = 8
        matr[4][1] = 4
        matr[4][2] = 7
        matr[4][3] = 5
        matr[4][4] = 5
        matr[4][5] = 29
        
    #--------------------------------------------------------
    print("--------------------------------------------------------------------------------")
    print("Исходная матрица: \n")
    for t in range(n):
        for e in range(n):
            print(format(matr[t][e], "10.4f"), end = "  ")
        print(end = "|")
        for d in range(n, n+1):
            print(format(matr[t][d], "10.4f"), end = "")
        print()
        
    x = lu(n, matr, l, u, y, x)
    
    if (w == 0):
        # вывод решений к задаче
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ, полученные методом LU-разложения: \n")
        for k in range(n):
            print(f"x{k} = {x[k]:.4f}")
    #--------------------------------------------------------
    if (w == 1):
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ: \n")
        for name, val in zip(var_names, x):
            print(f"{name} = {val:.4f}")
    #--------------------------------------------------------
    if (w == 2):
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ: \n")
        for h in range(n):
            print(format(x[h], "10.4f"))
#--------------------------------------------------------
def pars(s, var_names):
    """Разбирает выражение без знака '=' и возвращает словарь коэффициентов и свободный член."""
    coeffs = {}
    const = 0.0

    # убрать все пробельные символы
    s = re.sub(r'\s+', '', s)
    pos = 0

    while (pos < len(s)):
        m = TERM.match(s, pos)
        if (not m):
            raise ValueError(f"Некорректный член уравнения около: {s[pos:]}")

        sign = -1.0 if (m.group('sign') == '-') else 1.0

        if (m.group('name')):
            name = m.group('name')
            if (name not in var_names):
                raise ValueError(f"Неизвестная переменная: {name}")

            coef = float(m.group('coef')) if (m.group('coef')) else 1.0
            coeffs[name] = coeffs.get(name, 0.0) + sign * coef
        else:
            const += sign * float(m.group('const'))

        pos = m.end()

        # после каждого члена должен идти знак '+' или '-' либо конец строки
        if ((pos < len(s)) and (s[pos] not in '+-')):
            raise ValueError(f"Ожидался знак '+' или '-' перед: {s[pos:]}")

    return coeffs, const
#--------------------------------------------------------
def equation(line, var_names):
    """Преобразует уравнение вида '2*x1 - x2 = 3' в строку расширенной матрицы."""
    left, sep, right = line.partition('=')
    if (not sep):
        right = '0'

    cl, kl = pars(left, var_names)
    cr, kr = pars(right, var_names)

    coeffs = {k: cl.get(k, 0.0) - cr.get(k, 0.0)
              for k in set(cl) | set(cr)}
    const = kr - kl
    return coeffs, const
#--------------------------------------------------------
def lu(n, matr, l, u, y, x):
    #первичное заполнение массивов l и u
    for i in range(n):
        for j in range(n):
            l[i][j] = 0
            if (i == j):
                u[i][j] = 1
            else:
                u[i][j] = 0
    
    #слой 0
    for i in range(n):
        l[i][0] = matr[i][0]
    for j in range(1, n):
        u[0][j] = matr[0][j] / l[0][0]

    #пересчёт остальных слоёв
    for k in range(1, n):
        
        #пересчёт l(i, k)
        for i in range(k, n):
            l[i][k] = matr[i][k]
            for m in range(k):
                l[i][k] = l[i][k] - l[i][m] * u[m][k]

        #пересчёт u(k, j)
        if (k < n-1):
            for j in range(k+1, n):
                u[k][j] = matr[k][j]
                for m in range(k):
                    u[k][j] = u[k][j] - l[k][m] * u[m][j]
                u[k][j] = u[k][j] / l[k][k]

    #вывод матриц l и u
    print("\n--------------------------------------------------------------------------------")
    print("Матрица L: \n")
    for i in range(n):
        for j in range(n):
            print(format(l[i][j], "10.4f"), end = "  ")
        print()

    print("\n--------------------------------------------------------------------------------")
    print("Матрица U: \n")
    for i in range(n):
        for j in range(n):
            print(format(u[i][j], "10.4f"), end = "  ")
        print()

    #ычисление y
    y[0] = matr[0][n] / l[0][0]
    for k in range(1, n):
        y[k] = matr[k][n]
        for m in range(k):
            y[k] = y[k] - l[k][m] * y[m]
        y[k] = y[k] / l[k][k]

    #вывод y
    print("\n--------------------------------------------------------------------------------")
    print("Вектор Y: \n")
    for k in range(n):
        print(format(y[k], "10.4f"), end = "  ")
    print()

    #вычисление x
    x[n-1] = y[n-1]
    for k in range(n-2, -1, -1):
        x[k] = y[k]
        for m in range(k+1, n):
            x[k] = x[k] - u[k][m] * x[m]
    
    return x
#--------------------------------------------------------
if (__name__ == "__main__"):
    main()

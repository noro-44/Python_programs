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
    w = int(input("Решение СЛАУ методом простых итераций / Зейделя\n"
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
    x = [0.0 for y in range(n)]
    xo = [0.0 for y in range(n)]
    xn = [0.0 for y in range(n)]
    st = ['' for u in range(n)]

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
        matr[0][0] = 26
        matr[0][1] = 2
        matr[0][2] = 3
        matr[0][3] = 2
        matr[0][4] = 2
        matr[0][5] = 45

        matr[1][0] = 4
        matr[1][1] = 23
        matr[1][2] = 3
        matr[1][3] = 2
        matr[1][4] = 1
        matr[1][5] = 64
    
        matr[2][0] = 4
        matr[2][1] = 2
        matr[2][2] = 46
        matr[2][3] = 1
        matr[2][4] = 4
        matr[2][5] = 152
    
        matr[3][0] = 5
        matr[3][1] = 4
        matr[3][2] = 2
        matr[3][3] = 35
        matr[3][4] = 4
        matr[3][5] = 93
    
        matr[4][0] = 1
        matr[4][1] = 5
        matr[4][2] = 3
        matr[4][3] = 5
        matr[4][4] = 49
        matr[4][5] = 79
        
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
        
    if (w == 0):
        print("\n--------------------------------------------------------------------------------")
        print("Метод простых итераций: ")
        print("--------------------------------------------------------------------------------", end = '')
        x = prostye_iteratsii(n, matr, xo, xn)
        
        # вывод решений к задаче
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ, полученные методом простых итерций: \n")
        for l in range(n):
            print(f"x{l} = {x[l]:.4f}")

        print("\n--------------------------------------------------------------------------------")
        print("Метод Зейделя: ")
        print("--------------------------------------------------------------------------------", end = '')
        x = zeydel(n, matr, xo, xn)
        
        # вывод решений к задаче
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ, полученные методом Зейделя: \n")
        for l in range(n):
            print(f"x{l} = {x[l]:.4f}")
    else:
        print("\n--------------------------------------------------------------------------------")
        v = int(input("Метод решения СЛАУ:\n"
                  "Чтобы выбрать метод простых итераций нажмите '1';\n"
                  "Чтобы выбрать метод Зейделя нажмите '2';\n"
                  "(После ввода числа нажмите 'Enter')\n"
                  "Ваш выбор: "))
        print("--------------------------------------------------------------------------------", end = '')
        match v:
            case 1:
                x = prostye_iteratsii(n, matr, xo, xn)
            case 2:
                x = zeydel(n, matr, xo, xn)  
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
        print()
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
def prostye_iteratsii(n, matr, xo, xn):
    k = 0
    for y in range(n):
        xo[y] = 0
    while (True):
        k += 1
        for i in range(n):
            xn[i] = matr[i][n]
            for j in range(n):
                if (j != i):
                    xn[i] = xn[i] - matr[i][j] * xo[j]
            xn[i] = xn[i] / matr[i][i]
        h = 0
        for i in range(n):
            if (abs(xo[i] - xn[i]) < 1e-13):
                h += 1
            xo[i] = xn[i]
        if (h == n):
            break

        #вывод
        print(format(f"\nИтерация k = {k}:"), end = " ")
        for i in range(n):
            print(format(xo[i], "10.4f"), end = "  ")
        print()
        
    return xn
#--------------------------------------------------------
def zeydel(n, matr, xn, xo):
    k = 0
    for i in range(n):
        xo[i] = 0.1
    while (True):
        k += 1
        for i in range(n):
            xn[i] = matr[i][n]
            for j in range(n):
                if (j < i):
                    xn[i] = xn[i] - matr[i][j] * xn[j]
                else:
                   if (j > i):
                       xn[i] = xn[i] - matr[i][j] * xo[j]
            xn[i] = xn[i] / matr[i][i]
        h = 0
        for i in range(n):
            if (abs(xo[i] - xn[i]) < 1e-13):
                h += 1
            xo[i] = xn[i]
        if (h == n):
            break

        #вывод
        print(format(f"\nИтерация k = {k}: "), end = "")
        for i in range(n):
            print(format(xo[i], "10.4f"), end = "  ")
        print()

    return xn
#--------------------------------------------------------
if (__name__ == "__main__"):
    main()


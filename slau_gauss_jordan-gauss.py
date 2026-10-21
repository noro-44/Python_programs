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
    w = int(input("Решение СЛАУ методом Гаусса / Жордана-Гаусса\n"
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
        matr[0][0] = -9.41
        matr[0][1] = -8.58
        matr[0][2] = 0.93
        matr[0][3] = -9.09
        matr[0][4] = 0.04
        matr[0][5] = 4.18

        matr[1][0] = 6.32
        matr[1][1] = 4.39
        matr[1][2] = 1.32
        matr[1][3] = -7.73
        matr[1][4] = 8.5
        matr[1][5] = 8.14
    
        matr[2][0] = 2.02
        matr[2][1] = -2.23
        matr[2][2] = -6.24
        matr[2][3] = -3.25
        matr[2][4] = 5.58
        matr[2][5] = 9.22
    
        matr[3][0] = -1.71
        matr[3][1] = 1.02
        matr[3][2] = -3.58
        matr[3][3] = 5.98
        matr[3][4] = 4.58
        matr[3][5] = 2.37
    
        matr[4][0] = 0.63
        matr[4][1] = -6.18
        matr[4][2] = 3.5
        matr[4][3] = 6.49
        matr[4][4] = 1.66
        matr[4][5] = -2.2
        
    #--------------------------------------------------------
    print("--------------------------------------------------------------------------------")
    print("Исходная матрица: \n")
    # вывод матрицы после к итерации
    for r in range(n):
        for e in range(n+1):
            print(format(matr[r][e], "10.4f"), end = "  ")
        print()
        
    if (w == 0):
        print("\n--------------------------------------------------------------------------------")
        print("Метод Гаусса: ")
        print("--------------------------------------------------------------------------------", end = '')
        x = gauss(n, matr, x)
        
        # вывод решений к задаче
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ, полученные методом Гаусса: \n")
        for l in range(n):
            print(f"x{l} = {x[l]:.4f}")

        print("\n--------------------------------------------------------------------------------")
        print("Метод Жордана-Гаусса: ")
        print("--------------------------------------------------------------------------------", end = '')
        x = jordan_gauss(n, matr, x)
        
        # вывод решений к задаче
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ, полученные методом Жордана-Гаусса: \n")
        for l in range(n):
            print(f"x{l} = {x[l]:.4f}")
    else:
        print("\n--------------------------------------------------------------------------------")
        v = int(input("Метод решения СЛАУ:\n"
                  "Чтобы выбрать метод Гаусса нажмите '1';\n"
                  "Чтобы выбрать метод Жордана-Гаусса нажмите '2';\n"
                  "(После ввода числа нажмите 'Enter')\n"
                  "Ваш выбор: "))
        print("--------------------------------------------------------------------------------", end = '')
        match v:
            case 1:
                x = gauss(n, matr, x)
            case 2:
                x = jordan_gauss(n, matr, x)  
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
def gauss(n, matr, x):
    for k in range(n):
        if (abs(matr[k][k]) < 0.0000000001):
            m = k + 1
            while ((m < n) and (abs(matr[m][k]) < 0.0000000001)):
                m += 1
            
            for j in range(n+1):
                temp = matr[k][j]
                matr[k][j] = matr[m][j]
                matr[m][j] = temp
            
        for i in range(k+1, n):
            for j in range(k+1, n+1):
                matr[i][j] = (matr[i][j] * matr[k][k] -  matr[k][j] * matr[i][k]) / matr[k][k]

        for i in range(k+1, n):
            matr[i][k] = 0.0
        
        for j in range(n, k-1, -1):
            matr[k][j] = matr[k][j] / matr[k][k]
        
        # вывод матрицы после каждой итерации
        print(f"\nПосле итерации k = {k + 1}: \n")
        for p in range(n):
            for q in range(n+1):
                print(format(matr[p][q], "10.4f"), end = "  ")
            print()
        
    # вычисление х
    x[n-1] = matr[n-1][n]
    for k in range(n-2, -1, -1):
        x[k] = matr[k][n]
        for m in range(n-1, k, -1):
            x[k] -= matr[k][m] * x[m]
            
    return x
#--------------------------------------------------------
def jordan_gauss(n, matr, x):
    for k in range(n):
        if (abs(matr[k][k]) < 0.0000000001):
            m = k + 1
            while ((m < n) and (abs(matr[m][k]) < 0.0000000001)):
                m += 1
            
            for j in range(n+1):
                temp = matr[k][j]
                matr[k][j] = matr[m][j]
                matr[m][j] = temp
            
        for i in range(n):
            for j in range(k+1, n+1):
                if (i != k):
                    matr[i][j] = (matr[i][j] * matr[k][k] -  matr[k][j] * matr[i][k]) / matr[k][k]

        for i in range(n):
            if (i != k):
                matr[i][k] = 0.0
        
        for j in range(n, k-1, -1):
            matr[k][j] = matr[k][j] / matr[k][k]
        
        # вывод матрицы после каждой итерации
        print(f"\nПосле итерации k = {k + 1}: \n")
        for p in range(n):
            for q in range(n+1):
                print(format(matr[p][q], "10.4f"), end = "  ")
            print()
        
    # вычисление х
    for k in range(n):
        x[k] = matr[k][n]
        
    return x
#--------------------------------------------------------
if (__name__ == "__main__"):
    main()

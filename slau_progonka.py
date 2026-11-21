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
    w = int(input("Решение СЛАУ методом прогонки\n"
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
    c = [0.0 for y in range(n)]
    l = [0.0 for y in range(n)]
    r = [0.0 for y in range(n)]
    q = [0.0 for y in range(n)]
    p = [0.0 for y in range(n)]
    x = [0.0 for y in range(n)]
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
        matr[0][0] = 4
        matr[0][1] = 5
        matr[0][2] = 0
        matr[0][3] = 0
        matr[0][4] = 0
        matr[0][5] = 9

        matr[1][0] = 9
        matr[1][1] = 6
        matr[1][2] = 6
        matr[1][3] = 0
        matr[1][4] = 0
        matr[1][5] = 21
    
        matr[2][0] = 0
        matr[2][1] = 6
        matr[2][2] = 3
        matr[2][3] = 5
        matr[2][4] = 0
        matr[2][5] = 14
    
        matr[3][0] = 0
        matr[3][1] = 0
        matr[3][2] = 9
        matr[3][3] = 5
        matr[3][4] = 6
        matr[3][5] = 20
    
        matr[4][0] = 0
        matr[4][1] = 0
        matr[4][2] = 0
        matr[4][3] = 4
        matr[4][4] = 6
        matr[4][5] = 10
        
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
        
    #проверка матрицы на трёхдиагональность
    if (not tri_diagonal(n, matr)):
        print("\n--------------------------------------------------------------------------------")
        print("Матрица не является трёхдиагональной")
        return

    x = progonka(n, matr, c, l, r, q, p, x)
    
    if (w == 0):
        # вывод решений к задаче
        print("\n--------------------------------------------------------------------------------")
        print("Решения СЛАУ, полученные методом прогонки: \n")
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
def progonka(n, matr, c, l, r, q, p, x):
    #заполнение векторов
    for k in range(n):
        
        if (k >= 1):
            l[k] = matr[k][k-1]
                       
        c[k] = matr[k][k]
        
        if (k <= n-2):
            r[k] = matr[k][k+1]
            
        p[k] = 0
        q[k] = 0
        x[k] = 0

    #вывод вектора l
    print("\n--------------------------------------------------------------------------------")
    print("Вектор L: \n")
    for i in range(n):
        print(format(l[i], "10.4f"), end = "  ")
    print()

    #вывод вектора c
    print("\n--------------------------------------------------------------------------------")
    print("Вектор C: \n")
    for i in range(n):
        print(format(c[i], "10.4f"), end = "  ")
    print()
    
    #вывод вектора r
    print("\n--------------------------------------------------------------------------------")
    print("Вектор R: \n")
    for i in range(n):
        print(format(r[i], "10.4f"), end = "  ")
    print()

    #вычисление p и q
    p[0] = matr[0][n] / c[0]
    q[0] = r[0] / c[0]
    for k in range(1, n):
        p[k] = (matr[k][n] - l[k] * p[k-1]) / (c[k] - l[k] * q[k-1])
        q[k] = r[k] / (c[k] - l[k] * q[k-1])

    #вывод p
    print("\n--------------------------------------------------------------------------------")
    print("Вектор P: \n")
    for i in range(n):
        print(format(p[i], "10.4f"), end = "  ")
    print()
    
    #вывод q
    print("\n--------------------------------------------------------------------------------")
    print("Вектор Q: \n")
    for i in range(n):
        print(format(q[i], "10.4f"), end = "  ")
    print()

    #вычисление x
    x[n-1] = p[n-1]
    for k in range(n-2, -1, -1):
        x[k] = p[k] - q[k] * x[k+1]
    
    return x
#--------------------------------------------------------
def tri_diagonal(n, matr):
    for i in range(n):
        for j in range(n):
            if (abs(i - j) > 1):
                if (abs(matr[i][j]) > 1e-13):
                    return 0
    return 1
#--------------------------------------------------------
if (__name__ == "__main__"):
    main()



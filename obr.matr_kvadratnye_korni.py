def main():
    w = int(input("Нахождение обратной матрицы методом Холецкого (методом квадраных корней)\n"
                  "Введите порядок квадратной матрицы: "))
    match w:
        #---------------------------------------------------------
        case 0:
            n = 5 # исходные данные к задаче
        case _:
            n = w

    matr = [[0.0 for j in range(n)] for i in range(n)]
    l = [[0.0 for j in range(n)] for i in range(n)]
    y = [[0.0 for j in range(n)] for i in range(n)]
    invert = [[0.0 for j in range(n)] for i in range(n)]
    st = ['' for i in range(n)]

    #--------------------------------------------------------
    if (w == 0): # исходные данные к задаче
        matr[0][0] = 5
        matr[0][1] = 1
        matr[0][2] = 1
        matr[0][3] = 3
        matr[0][4] = 3

        matr[1][0] = 1
        matr[1][1] = 6
        matr[1][2] = 2
        matr[1][3] = 6
        matr[1][4] = 2
    
        matr[2][0] = 1
        matr[2][1] = 2
        matr[2][2] = 9
        matr[2][3] = 1
        matr[2][4] = 5
    
        matr[3][0] = 3
        matr[3][1] = 6
        matr[3][2] = 1
        matr[3][3] = 9
        matr[3][4] = 1
    
        matr[4][0] = 3
        matr[4][1] = 2
        matr[4][2] = 5
        matr[4][3] = 2
        matr[4][4] = 9
    #--------------------------------------------------------
    else:
        print(f"Введите матрицу размерностью {n}x{n}\n"
              "(Вводите построчно с пробелом после каждого числа и 'Enter' после строки): ")
        for b in range(n):
            row = list(map(float, input(f"Строка {b+1}: ").split()))
            matr[b] = row
        
    #--------------------------------------------------------
    print("--------------------------------------------------------------------------------")
    print("Исходная матрица: \n")
    for t in range(n):
        for e in range(n):
            print(format(matr[t][e], "10.4f"), end = "  ")
        print()
        
    #проверка матрицы на симметричность и положительную определённость
    if (not spo(n, matr)):
        print("\n--------------------------------------------------------------------------------")
        print("Матрица не является симметричной положительно определённой")
        return

    invert = holetskiy(n, matr, l, y, invert)
    
    # вывод решений к задаче
    print("\n--------------------------------------------------------------------------------")
    print("Обратная матрица: \n")
    for h in range(n):
        for g in range(n):
            print(format(invert[h][g], "10.4f"), end = "  ")
        print()
#--------------------------------------------------------
def holetskiy(n, matr, l, y, invert):
    #заполнение матрицы l
    l[0][0] = pow(matr[0][0], 0.5)
    for i in range(1, n):
        l[i][0] = matr[i][0] / l[0][0]
    for k in range(1, n):
        ks = 0
        for m in range(k):
            ks = ks + l[k][m] * l[k][m]
        l[k][k] = pow((matr[k][k] - ks), 0.5)
        if (k < n-1):
            for i in range(k+1, n):
                ps = 0
                for m in range(k):
                    ps = ps + l[i][m] * l[k][m]
                l[i][k] = (matr[i][k] - ps) / l[k][k]
    
    #вывод матрицы l
    print("\n--------------------------------------------------------------------------------")
    print("Матрица L: \n")
    for i in range(n):
        for j in range(n):
            print(format(l[i][j], "10.4f"), end = "  ")
        print()
        
    #заполнение матрицы y
    for i in range(n):
        for j in range(n):
            if (j > i):
                y[i][j] = 0
            elif (j == i):
                y[i][j] = 1 / l[i][i]
            elif (j < i):
                y[i][j] = 0
                for m in range(j, i):
                    y[i][j] = y[i][j] + l[i][m] * y[m][j]
                y[i][j] = y[i][j] / (-l[i][i])

    #вывод матрицы y
    print("\n--------------------------------------------------------------------------------")
    print("Матрица Y: \n")
    for i in range(n):
        for j in range(n):
            print(format(y[i][j], "10.4f"), end = "  ")
        print()

    #вычисление обратной матрицы
    for i in range(n):
        for j in range(n):
            invert[i][j] = 0
            for m in range(n):
                invert[i][j] = invert[i][j] + y[m][i] * y[m][j]
    
    return invert
#--------------------------------------------------------
def opredelitel(n, matr):
    d = 1.0
    m = [[0.0 for j in range(n+1)] for i in range(n)]
    
    for u in range(n):
        for z in range(n):
            m[u][z] = matr[u][z]
            
    for k in range(n):
        p = max(range(k, n), key = lambda i :abs(m[i][k]))
        if (abs(m[p][k]) <= 1e-13):
            return 0.0
        if (p != k):
            m[k], m[p] = m[p], m[k]
            d = -d
        d *= m[k][k]
        for i in range(k+1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n):
                m[i][j] -= f * m[k][j]
    return d
#--------------------------------------------------------
def spo(n, matr):
    simm = 0 #симметричность
    pol_opr = 0 #положительная определённость

    #проверка на симметричность
    for i in range(n):
        for j in range(n):
            if (matr[i][j] == matr[j][i]):
                simm = 1
            else:
                simm = 0

    #проверка на положительную определённость
    for k in range(1, n+1):
        minor = [[matr[i][j] for j in range(k)] for i in range(k)]
        if (opredelitel(k, minor) <= 1e-13):
            pol_opr = 0
        else:
            pol_opr = 1

    
    if ((simm == 1) and (pol_opr == 1)):
        return 1
    else:
        return 0
#--------------------------------------------------------
if (__name__ == "__main__"):
    main()



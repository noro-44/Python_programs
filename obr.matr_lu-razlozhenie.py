def main():
    w = int(input("Нахождение обратной матрицы методом LU-разложения\n"
                  "Введите порядок квадратной матрицы: "))
    match w:
        #---------------------------------------------------------
        case 0:
            n = 5 # исходные данные к задаче
        case _:
            n = w

    matr = [[0.0 for j in range(n)] for i in range(n)]
    l = [[0.0 for j in range(n)] for i in range(n)]
    u = [[0.0 for j in range(n)] for i in range(n)]
    y = [[0.0 for j in range(n)] for i in range(n)]
    x = [[0.0 for j in range(n)] for i in range(n)]
    invert = [[0.0 for j in range(n)] for i in range(n)]
    st = ['' for i in range(n)]

    #--------------------------------------------------------
    if (w == 0): # исходные данные к задаче
        matr[0][0] = 1
        matr[0][1] = 1
        matr[0][2] = 6
        matr[0][3] = 2
        matr[0][4] = 5

        matr[1][0] = 6
        matr[1][1] = 9
        matr[1][2] = 2
        matr[1][3] = 8
        matr[1][4] = 3
    
        matr[2][0] = 8
        matr[2][1] = 9
        matr[2][2] = 3
        matr[2][3] = 3
        matr[2][4] = 9
    
        matr[3][0] = 6
        matr[3][1] = 9
        matr[3][2] = 3
        matr[3][3] = 6
        matr[3][4] = 5
    
        matr[4][0] = 6
        matr[4][1] = 5
        matr[4][2] = 3
        matr[4][3] = 5
        matr[4][4] = 6
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

    invert = lu(n, matr, l, u, y, x, invert)
    
    # вывод решений к задаче
    print("\n--------------------------------------------------------------------------------")
    print("Обратная матрица: \n")
    for h in range(n):
        for g in range(n):
            print(format(invert[h][g], "10.4f"), end = "  ")
        print()
#--------------------------------------------------------
def lu(n, matr, l, u, y, x, invert):
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
        if (k <= n-2):
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
    for i in range(n):
        for j in range(n):
            if (j > i):
                y[i][j] = 0
            elif (j == i):
                y[i][j] = 1 / l[i][i]
            elif (j < i):
                y[i][j] = 0
                for m in range(j, i):
                    y[i][j] = y[i][j] - l[i][m] * y[m][j]
                y[i][j] = y[i][j] / l[i][i]

    #вывод матрицы y
    print("\n--------------------------------------------------------------------------------")
    print("Матрица Y: \n")
    for i in range(n):
        for j in range(n):
            print(format(y[i][j], "10.4f"), end = "  ")
        print()

    #вычисление x
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if (j < i):
                x[i][j] = 0
            elif (j == i):
                x[i][j] = 1
            elif (j > i):
                x[i][j] = 0
                for m in range(i+1, j+1):
                    x[i][j] = x[i][j] - u[i][m] * x[m][j]
    
    #вывод матрицы x
    print("\n--------------------------------------------------------------------------------")
    print("Матрица X: \n")
    for i in range(n):
        for j in range(n):
            print(format(x[i][j], "10.4f"), end = "  ")
        print()
    
    #вычисление обратной матрицы
    for i in range(n):
        for j in range(n):
            invert[i][j] = 0
            for m in range(n):
                invert[i][j] = invert[i][j] + x[i][m] * y[m][j]
    
    return invert
#--------------------------------------------------------
if (__name__ == "__main__"):
    main()

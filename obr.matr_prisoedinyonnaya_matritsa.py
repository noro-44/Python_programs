def main():
    w = int(input("Нахождение обратной матрицы методом присоединённой матрицы\n"
                  "Введите порядок квадратной матрицы: "))
    match w:
        #---------------------------------------------------------
        case 0:
            n = 5 # исходные данные к задаче
        case _:
            n = w

    matr = [[0.0 for j in range(n*2)] for i in range(n)]
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
            while (True):
                row = list(map(float, input(f"Строка {b+1}: ").split()))
                for d in range(n):
                    matr[b][d] = row[d]
                break
    #--------------------------------------------------------
    for i in range(n):
        matr[i][n + i] = 1.0
        
    #--------------------------------------------------------
    print("--------------------------------------------------------------------------------")
    print("Исходная матрица: \n")
    for t in range(n):
        for e in range(n):
            print(format(matr[t][e], "10.4f"), end = "  ")
        print()
        
    #проверка на невырожденность
    if (opredelitel(n, matr) == 0.0):
        print("\n--------------------------------------------------------------------------------")
        print("Матрица является вырожденной")
        return
    
    invert = prisoed_matr(n, matr, invert)
    
    # вывод решений к задаче
    print("\n--------------------------------------------------------------------------------")
    print("Обратная матрица: \n")
    for h in range(n):
        for g in range(n):
            print(format(invert[h][g], "10.4f"), end = "  ")
        print()
#--------------------------------------------------------
def prisoed_matr(n, matr, invert):
    for k in range(n):
        if (abs(matr[k][k]) < 1e-13):
            m = 0
            while (True):
                if ((abs(matr[m][k]) > 1e-13) and (m != k)):
                    break
                m += 1
            
            for j in range(n*2):
                matr[k][j] = matr[k][j] + matr[m][j]
            
        for i in range(n):
            for j in range(k+1, n*2):
                if (i != k):
                    matr[i][j] = (matr[i][j] * matr[k][k] - matr[k][j] * matr[i][k]) / matr[k][k]

        for i in range(n):
            if (i != k):
                matr[i][k] = 0.0
        
        for j in range((n*2)-1, k-1, -1):
            matr[k][j] = matr[k][j] / matr[k][k]
        
        # вывод матрицы после каждой итерации
        print(f"\nПосле итерации k = {k + 1}: \n")
        for p in range(n):
            for q in range(n):
                print(format(matr[p][q], "10.4f"), end = "  ")   
            print(end = "|")
            for d in range(n, n*2):
                print(format(matr[p][d], "10.4f"), end = "")
            print()
    
    #вычисление обратной матрицы
    for i in range(n):
        for j in range(n):
            invert[i][j] = matr[i][j+n]
    
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
if (__name__ == "__main__"):
    main()

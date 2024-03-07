# Operações_com_matrizes 1.0 - desenvolvido por Gabriel Jonathan de Matos - agradecimento especial à Professora Ana Carolina Camargo Francisco.
import copy
import math
def Mult():
    def mult_matriz_bi(arrayA,arrayB):
        if len(arrayA[0]) != len(arrayB):
            return
        colunas = [[x[cont] for x in arrayB] for cont in range(len(arrayB[0]))]
        mat_final = []
        soma = 0
        for linha in arrayA:                               
            linha_mat= []
            for coluna in colunas:
                for num1,num2 in zip(linha,coluna):
                    soma += num1 * num2
                linha_mat.append(soma)
                soma = 0
            mat_final.append(linha_mat)
        return (mat_final)
    emenda = False
    try:
        if emenda == False:
            print('Defina as dimensões da primeira matriz:')
            linhas,colunas = map(int,input().split())
            print('Insira os elementos da primeira matriz uma linha de cada vez:')
            matriz1 = [list(map(int,input().split())) for _ in range(linhas)]
            print('Defina as dimensões da segunda matriz:')
            linhas,colunas = map(int,input().split())
            print('Insira os elementos da segunda matriz uma linha de cada vez:')
            matriz2 = [list(map(int,input().split())) for _ in range(linhas)]
            mat_final = mult_matriz_bi(matriz1,matriz2)
            try:
                for ele in mat_final:
                    print(ele)
                print('resultado da multiplicação obtido com sucesso!')
            except:
                print('impossivel multiplicar as matrizes descritas!')
                pass
            resp = input('Deseja multiplicar a matriz resultado por outra?')
            if resp.upper() == 'S' or resp.upper() == 'SIM':
                emenda = True
        else:
            print('Defina as dimensões da segunda matriz:')
            linhas,colunas = map(int,input().split())
            print('Insira os elementos da segunda matriz uma linha de cada vez:')
            matriz2 = [list(map(int,input().split())) for _ in range(linhas)]
            mat_final = mult_matriz_bi(mat_final,matriz2)
            try:
                for ele in mat_final:
                    print(ele)
                print('resultado da multiplicação obtido com sucesso!')
            except:
                print('impossivel multiplicar as matrizes descritas!')
                emenda = False
                pass
            resp = input('Deseja multiplicar a matriz resultado por outra?')
            if resp.upper() != 'S' or resp.upper() != 'SIM':
                emenda = False
    except EOFError:
        pass
def CalculaInversa():
    def MatrizId(i):
        return [[1 if cont == j else 0 for cont in range(i)] for j in range(i)]
    def TrocaLinha(matriz,i,j,max_lin,subindo):
        aux = []
        if subindo:
            for cont in range(i + 1):
                if matriz[i - cont][j] != 0:
                    aux = matriz[i]
                    matriz[i] = matriz[i - cont]
                    matriz[i - cont] = aux
                    return
        else:
            for cont in range(max_lin - i):
                if matriz[i + cont][j] != 0:
                    aux = matriz[i]
                    matriz[i] = matriz[i + cont]
                    matriz[i + cont] = aux
                    return
        return -1
    print('Defina as dimensões da matriz separadas por espaço:')
    linhas,colunas = map(int,input().split())
    iD = MatrizId(linhas)
    matriz = [list(map(int,input('Informe os elementos da próxima linha da matriz separados por espaço:').split())) for _ in range(linhas)]
    matrizAlong = []
    for lin1, lin2 in zip(matriz, iD):
        linha = lin1 + lin2
        matrizAlong.append(linha)
    iPvt, jPvt = 0, 0
    primeiraVez = True
    subindo = False
    deuPau = False
    while not (iPvt == jPvt == 0 and primeiraVez == False):
        primeiraVez = False
        if iPvt == linhas - 1 and jPvt == colunas - 1:
            subindo = True
        if subindo:
            incremento = -1
            if matrizAlong[iPvt][jPvt] == 0:
                resultado = TrocaLinha(matrizAlong,iPvt,jPvt,linhas,True)
                if resultado != None:
                    print('A matriz informada não é imversível')
                    deuPau = True
                    break
            while iPvt + incremento >= 0:
                fator = -matrizAlong[iPvt + incremento][jPvt] / matrizAlong[iPvt][jPvt]
                matrizAlong[iPvt + incremento] = [fator * x + y for x,y in zip(matrizAlong[iPvt],matrizAlong[iPvt + incremento])]
                incremento -= 1
            iPvt -= 1
            jPvt -= 1
        else:
            incremento = 1
            if matrizAlong[iPvt][jPvt] == 0:
                resultado = TrocaLinha(matrizAlong,iPvt,jPvt,linhas,False)
                if resultado != None:
                    print('A matriz informada não é imversível!')
                    deuPau = True
                    break
            while iPvt + incremento < linhas:
                fator = -matrizAlong[iPvt + incremento][jPvt] / matrizAlong[iPvt][jPvt]
                matrizAlong[iPvt + incremento] = [fator * x + y for x,y in zip(matrizAlong[iPvt],matrizAlong[iPvt + incremento])]
                incremento += 1
            iPvt += 1
            jPvt += 1
    if deuPau:
        pass
    inverter = False
    for ele in matrizAlong:
        indx = matrizAlong.index(ele)
        if matrizAlong[indx][indx] != 1:
            inverter = True
            break
    try:
        if inverter:
            for ele in matrizAlong:
                indx = matrizAlong.index(ele)
                matrizAlong[indx] = [1/matrizAlong[indx][indx] * x for x in matrizAlong[indx]]
    except:
        print('A matriz informada não é inversível!')
        pass
    print('Exibindo a matriz inversa da informada:')
    for ele in matrizAlong:
        print(ele[linhas:])
def Descriptografar():
    def MultiplicarMatrizes(arrayA,arrayB):
        if len(arrayA[0]) != len(arrayB):
            return -1
        colunas = [[x[cont] for x in arrayB] for cont in range(len(arrayB[0]))]
        mat_final = []
        soma = 0
        for linha in arrayA:                               
            linha_mat= []
            for coluna in colunas:
                for num1,num2 in zip(linha,coluna):
                    soma += num1 * num2
                linha_mat.append(soma)
                soma = 0
            mat_final.append(linha_mat)
        return mat_final
    def InverterMatriz(matriz):
        def MatrizId(i):
            return [[1 if cont == j else 0 for cont in range(i)] for j in range(i)]
        def TrocaLinha(matriz,i,j,max_lin,subindo):
            aux = []
            if subindo:
                for cont in range(i + 1):
                    if matriz[i - cont][j] != 0:
                        aux = matriz[i]
                        matriz[i] = matriz[i - cont]
                        matriz[i - cont] = aux
                        return
            else:
                for cont in range(max_lin - i):
                    if matriz[i + cont][j] != 0:
                        aux = matriz[i]
                        matriz[i] = matriz[i + cont]
                        matriz[i + cont] = aux
                        return
            return -1
        linhas = len(matriz)
        colunas = len(matriz[0])
        iD = MatrizId(linhas)
        matrizAlong = []
        for lin1, lin2 in zip(matriz, iD):
            linha = lin1 + lin2
            matrizAlong.append(linha)
        iPvt, jPvt = 0, 0
        primeiraVez = True
        subindo = False
        deuPau = False
        while not (iPvt == jPvt == 0 and primeiraVez == False):
            primeiraVez = False
            if iPvt == linhas - 1 and jPvt == colunas - 1:
                subindo = True
            if subindo:
                incremento = -1
                if matrizAlong[iPvt][jPvt] == 0:
                    resultado = TrocaLinha(matrizAlong,iPvt,jPvt,linhas,True)
                    if resultado != None:
                        print('A matriz informada não é inversível')
                        deuPau = True
                        break
                while iPvt + incremento >= 0:
                    fator = -matrizAlong[iPvt + incremento][jPvt] / matrizAlong[iPvt][jPvt]
                    matrizAlong[iPvt + incremento] = [fator * x + y for x,y in zip(matrizAlong[iPvt],matrizAlong[iPvt + incremento])]
                    incremento -= 1
                iPvt -= 1
                jPvt -= 1
            else:
                incremento = 1
                if matrizAlong[iPvt][jPvt] == 0:
                    resultado = TrocaLinha(matrizAlong,iPvt,jPvt,linhas,False)
                    if resultado != None:
                        print('A matriz informada não é inversível!')
                        deuPau = True
                        break
                while iPvt + incremento < linhas:
                    fator = -matrizAlong[iPvt + incremento][jPvt] / matrizAlong[iPvt][jPvt]
                    matrizAlong[iPvt + incremento] = [fator * x + y for x,y in zip(matrizAlong[iPvt],matrizAlong[iPvt + incremento])]
                    incremento += 1
                iPvt += 1
                jPvt += 1
        if deuPau:
            return -1
        inverter = False
        for ele in matrizAlong:
            indx = matrizAlong.index(ele)
            if matrizAlong[indx][indx] != 1:
                inverter = True
                break
        try:
            if inverter:
                for ele in matrizAlong:
                    indx = matrizAlong.index(ele)
                    matrizAlong[indx] = [1/matrizAlong[indx][indx] * x for x in matrizAlong[indx]]
        except:
            print('A matriz informada não é inversível!')
            return -1
        for ele in matrizAlong:
            matrizAlong[matrizAlong.index(ele)] = ele[linhas:]
        return matrizAlong
    alpha = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
    i,j = map(int,input('Informe as dimensões da matriz criptografada:').split())
    matCript = []
    for _ in range(i):
        lin = list(map(float,input('Informe a Próxima linha da matriz separando os elementos por espaço').split()))
        matCript.append(lin)
    i,j = map(int,input('Informe as dimensões da matriz multiplicadora:').split())
    while i != j:
            i,j = map(int,input('Informe as dimensões de um matriz quadrada:').split())
    matMult = []
    for _ in range(i):
        lin = list(map(float,input('Informe a próxima linha da matriz separando os elementos por espaço').split()))
        matMult.append(lin)
    matChave = InverterMatriz(matMult)
    matMens = MultiplicarMatrizes(matChave,matCript)
    mensagem = ''
    for linha in matMens:
        for num in linha:
            mensagem += alpha.get(round(num))
    print('Exibindo mensagem descriptografada:')
    print(mensagem)
def Transpor():
    matOrig = []
    i,j = map(int,input('Informe as dimensões da matriz original:').split())
    for _ in range(i):
        linha = list(map(int,input('Informe os elementos da próxima linha da matriz separados por espaço:').split()))
        matOrig.append(linha)
    transposta = []
    for cont in range(j):
        novaLinha = []
        for linha in matOrig:
            novaLinha.append(linha[cont])
        transposta.append(novaLinha)
    print('Exibindo matriz transposta:')
    for ele in transposta:
        print(ele)
def CalcularDeterminante():
    i,j = map(int,input('Informe as dimensões da matriz:').split())
    matriz = []
    for _ in range(i):                                                                                                  
        linha = list(map(int,input('Informe os elementos da próxima linha da matriz separados por espaço:').split()))
        matriz.append(linha)
    if i == 0 or j == 0 or i != j:
        return

    def det(matriz):
        if len(matriz) == 1:
            return matriz[0][0]
        else:
            soma = 0
            for l in range(len(matriz[0])):                                      
                matResult = [row[:l] + row[l+1:] for row in matriz[1:]]
                soma += matriz[0][l] * ((-1) ** l) * det(matResult)
            return soma

    print()
    print('Determinante =', det(matriz))
    print()
while True:
    print('Digite 1 para multiplicar matrizes, 2 para calcular a matriz inversa, 3 para descriptografar uma mensagem, 4 para transpor uma matriz ou 5 para calcular determinante:')
    resposta = int(input())
    if resposta == 1:
        Mult()
    elif resposta == 2:
        CalculaInversa()
    elif resposta == 3:
        Descriptografar()
    elif resposta== 4:
        Transpor()
    else:
        CalcularDeterminante()

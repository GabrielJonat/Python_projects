import random
rejeitados = 0
def Sorteio():
    def sortear(stop):
        start = 1
        stop += 1
        step = 1
        ran_num = random.randrange(start,stop,step)
        return ran_num
    try:
        numAlunos = int(input('Digite o numero de alunos: '))
    except:
        print('Entrada inválida!')
        print()
        return
    try:
        maxAlunos = int(input('\nQuantos alunos desejas sortear? '))
    except:
        print('Entrada inválida!')
        print()
        return
    if maxAlunos >= numAlunos:
        print('Sorteio inválido! ')
        print()
        return
    jafoi = []
    sorteados = []
    while len(sorteados) < maxAlunos:                              
        aluno = sortear(numAlunos)
        if aluno not in jafoi:
            sorteados.append(aluno)
            jafoi.append(aluno)
        else:
            while aluno in jafoi:
                aluno = sortear(numAlunos)
            sorteados.append(aluno)
            jafoi.append(aluno)
    print('\nAlunos Sorteados:')
    print(sorteados)
    lista_negra = []
    rejeitados = 0
    def resorteio(lista_negra):
        print('\nDesejas sortear novamente algum aluno? (\'s\',\'n\')')
        resp = input().upper()
        if resp == 'S' or resp == 'SIM':
            print('\nInforme os alunos a serem sorteados novamente separando-os por espaço:')
            try:
                listaResort = list(map(int,input().split()))
            except:
                print('Entrada de dados inválida!')
                print()
                return
            resort = len(listaResort)
            global rejeitados
            rejeitados += resort
            if rejeitados > numAlunos - maxAlunos:
                print('\nNão há alunos o suficiente para o sorteio')
                print()
                return -1
            if resort > len(sorteados):
                print('Sorteio inválido!')
                print()
                return -1
            lista_negra += listaResort
            for ele in listaResort:
                try:
                    sorteados.remove(ele)
                except:
                    print('Erro: aluno inexistente!')
                    print()
                    return -1
            for _ in range(resort):
                aluno = sortear(numAlunos)
                while aluno in listaResort or aluno in sorteados or aluno in lista_negra:
                    aluno = sortear(numAlunos)
                sorteados.append(aluno)
            print('\nNovo sorteio:')
            print('Alunos anteriores:',sorteados[:resort + 1])
            print('Alunos resorteados:',sorteados[resort+1:])
            return 0
        else:
            return -1
    loop = resorteio(lista_negra)
    while loop != -1:
        loop = resorteio(lista_negra)
resp = 'S'
while resp == 'S' or resp == 'SIM':
    rejeitados = 0
    Sorteio()
    resp = input('\nDesejas fazer um novo sorteio? (\'s\', \'n\')').upper()
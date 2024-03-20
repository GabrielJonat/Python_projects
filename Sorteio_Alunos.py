import random
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
        return
    try:
        maxAlunos = int(input('Quantos alunos desejas sortear? '))
    except:
        print('Entrada inválida!')
        return
    if maxAlunos >= numAlunos:
        print('Sorteio inválido!')
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
    print('Alunos Sorteados:')
    print(sorteados)
    print('Desejas sortear novamente algum aluno? (\'s\',\'n\')')
    resp = input().upper()
    if resp == 'S' or resp == 'SIM':
        print('Informe os alunos a serem sorteados novamente separando-os por espaço:')
        try:
            listaResort = list(map(int,input().split()))
        except:
            print('Entrada de dados inválida!')
            return
        resort = len(listaResort)
        if resort >= len(sorteados):
            print('Sorteio inválido!')
            return
        for ele in listaResort:
            try:
                sorteados.remove(ele)
            except:
                print('Erro: aluno inexistente!')
                return
        for _ in range(resort):
            aluno = sortear(numAlunos)
            while aluno in listaResort:
                aluno = sortear(numAlunos)
            sorteados.append(aluno)
        print('Novo sorteio:')
        print(sorteados)
resp = 'S'
while resp == 'S' or resp == 'SIM':
    Sorteio()
    resp = input('Deseja fazer um novo sorteio? (\'s\', \'n\')').upper()

  

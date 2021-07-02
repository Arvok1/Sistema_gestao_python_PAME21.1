from logging import raiseExceptions
from os import system, name
from sys import exit
from time import sleep
from model import session, professores_materias, Aluno_turma, Pessoa, Professor, Aluno, Materia, Turma


def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
#função visual apenas
def line_break():
    print("\n--------------------------------------\n")


#faz um "login" bem básico e sem muita funcionalidade
def login_inicial():
    clear()
    line_break()
    login_nao_realizado=True
    while login_nao_realizado:
        try:
            login = str(input("digite seu login:"))
            senha = str(input("Digite sua senha:"))
            
            if login=="admin" and senha=="admin":
                login_nao_realizado = False
                print(f'Olá {login}, login realizado com sucesso')
                sleep(1)
                menu_home()

            else:
                login_nao_realizado=True
                print('Login ou senha inválidos')
                
        except:
            login_nao_realizado=True
            pass

        print("as informações precisam ser uma string")

#menu-inicial
#a utilização de try except dentro de um loop serve para que a pergunta siga sendo feita até que uma opção válida seja fornecida
def menu_home():
    clear()
    line_break()
    print("Escolha uma das opções abaixo:")
    line_break()
    print("1 - Cadastrar nova matéria\n")
    print("2 - Cadastrar novo professor\n")
    print("3 - Cadastrar novo aluno\n")
    print("4 - Mostrar todas as matérias\n")
    print("5 - Mostrar todos os professores\n")
    print("6 - Mostrar todos os alunos\n")
    print("7 - Abrir Menu de Turmas\n")
    print("0 - Sair do programa")
    opcao_nao_valida = True
    while opcao_nao_valida == True:
        try:
            option = int(input('Opção desejada:\n'))
            if option == 0:
                opcao_nao_valida = False
                exit()

            elif option == 1:
                opcao_nao_valida = False
                cadastrar_materia()
                
            elif option == 2:
                opcao_nao_valida = False
                cadastrar_professor()

            elif option == 3:
                opcao_nao_valida = False
                cadastrar_aluno()

            elif option == 4:        
                mostrar_materias()

            elif option == 5:
                mostrar_professores()

            elif option == 6:
                mostrar_alunos()
            
            elif option == 7:
                menu_turmas()
                
        except:
            print('Infelizmente essa não é uma opção válida')
            menu_home()
            pass

def cadastrar_materia():
    clear()
    line_break()
    print("Para cadastrar uma nova matéria, precisamos de: Código/Nome")
    codigo=str(input("Código:\n"))
    print("\n")
    nome=str(input("Nome:\n"))
    print("\n")
    print(f'Cadastrando a matéria {nome} com o código {codigo}?')
    materia_existente=session.query(Materia).filter_by(codigo=codigo).first()
    if materia_existente:
        print("Essa Materia já existe")
        sleep(1)
        cadastrar_materia()
    else:
        materia = Materia(codigo=codigo, nome=nome)
        session.add(materia)
        session.commit()
        print(f'Materia {codigo} cadastrada com sucesso, voltando ao menu')
        sleep(1)
        menu_home()

    
def cadastrar_professor():
    clear()
    line_break()
    print("Para cadastrar um novo professor, precisamos de: nome/sobrenome/cpf/email/niveldeformacao")
    nome=str(input("Nome:\n"))
    print("\n")
    sobrenome=str(input("Sobrenome:\n"))
    print("\n")
    cpf=str(input("CPF:\n"))
    print("\n")
    email=str(input("email:\n"))
    print("\n")
    niveldeformacao=str(input("Nível de formação:\n"))
    print("\n")
    print(f'Cadastrando o professor {nome} com o cpf {cpf}?')
    pessoa_existente = session.query(Pessoa).filter_by(cpf=cpf).first()
    if pessoa_existente:
        print("Essa pessoa já existe")
        sleep(1)
        cadastrar_professor()
    else:
        pessoa_professor = Pessoa(forename=nome, surname=sobrenome, cpf=cpf)
        session.add(pessoa_professor)
        professor = Professor(pessoa=pessoa_professor, email=email, niveldeformacao=niveldeformacao)
        session.add(professor)
        session.commit()
        print(f'Professor {nome} cadastrada com sucesso')
        sleep(1)
        menu_home()

def cadastrar_aluno():
    clear()
    line_break()
    print("Para cadastrar um novo professor, precisamos de: nome/sobrenome/cpf/email/niveldeformacao")
    nome=str(input("Nome:\n"))
    print("\n")
    sobrenome=str(input("Sobrenome:\n"))
    print("\n")
    cpf=str(input("CPF:\n"))
    print("\n")
    email=str(input("email:\n"))
    print("\n")
    print(f'Cadastrando o professor {nome} com o cpf {cpf}?')
    pessoa_aluno = Pessoa(forename=nome, surname=sobrenome, cpf=cpf)
    session.add(pessoa_aluno)
    aluno = Aluno(pessoa=pessoa_aluno, email=email)
    session.add(aluno)
    session.commit()
    print(f'Professor {nome} cadastrada com sucesso')
    sleep(1)
    menu_home()

def mostrar_materias():
    clear()
    line_break()
    print("AS matérias são:")
    materias = session.query(Materia).all()
    print("ID/Código/nome")
    line_break()
    #professores conterá uma lista com todos os professores, ou seja, um elemento iterável, cada objeto dentro do elemento corresponde a um professor
    for materia in materias:
        print(f'{materia.id}/{materia.codigo}/{materia.nome}\n')
    print('Opções:\n')
    print(' Digite o id do professor que você deseja ver as turmas ou 0 para voltar ao menu principal\n')

def mostrar_professores():
    clear()
    line_break()
    print("Os professores são:")
    professores = session.query(Professor).all()
    print("ID/Primeiro Nome/Segundo Nome/Email/Nível de Formação")
    line_break()
    #professores conterá uma lista com todos os professores, ou seja, um elemento iterável, cada objeto dentro do elemento corresponde a um professor
    for professor in professores:
        pessoa = session.query(Pessoa).filter_by(id=professor.id).first()
        print(f'{professor.id}/{pessoa.forename}/{pessoa.surname}/{professor.email}/{professor.niveldeformacao}/{professor.materias}\n')
    print('Opções:\n')
    print(' Digite o id do professor que você deseja ver as turmas ou 0 para voltar ao menu principal\n')


    try:
        option = int(input('Opção desejada:\n'))
        professor=session.query(Professor).filter_by(id=option).first()
        if option == 0:
            menu_home()

        elif professor:
            clear()
            line_break()
            print(f'O professor {professor.forename}{professor.surname} é professor das seguintes matérias nas seguintes turmas:')
            line_break()
            for turma in professor.turmas:
                print(f'Turma: {turma.codigo} da matéria {turma.materia}')

            print('Pressione 0 para voltar ao menu anterior ou 1 para voltar ao menu principal')
            try:
                option = int(input('Opção desejada:\n'))
                if option == 0:
                    #valid_option = True
                    mostrar_professores()

                if option == 1:
                    #valid_option = True
                    menu_home()
                else:
                    #valid_option = False
                    pass
            except:
                pass
        else:
            #valid_option = False
            pass

    except:
        print('Infelizmente essa não é uma opção válida')
        mostrar_professores()#valid_option = False
        pass
           
def mostrar_alunos():
    clear()
    line_break()
    print("Os alunos são:")
    alunos = session.query(Aluno).all()
    print("ID/Primeiro Nome/Segundo Nome/Email")
    line_break()
    #alunos conterá uma lista com todos os professores, ou seja, um elemento iterável, cada objeto dentro do elemento corresponde a um professor
    for aluno in alunos:
        pessoa = session.query(Pessoa).filter_by(id=aluno.id).first()
        print(f'{aluno.id}/{pessoa.forename}/{pessoa.surname}/{aluno.email}\n')
    print('Opções:\n')
    print(' Digite o id do aluno que você deseja ver as turmas ou 0 para voltar ao menu principal\n')

## ainda não implementada##

    try:
        option = int(input('Opção desejada:\n'))
        if option == 0:
            menu_home()

    except:
        print('Infelizmente essa não é uma opção válida')
        mostrar_alunos()#valid_option = False
        pass

def sair_do_programa():
    print("O programa fechará em 1 segundo")
    exit(0)


def menu_turmas():
    clear()
    line_break()
    print("Escolha uma das opções abaixo:")
    line_break()
    print("1 - Cadastrar nova turma\n")
    print("2 - Designar professor para turma\n")
    print("3 - Adicionar alunos a turma\n")
    print("4 - Remover alunos de turma\n")
    print("5 - Dar a nota final a alunos de turma\n")
    print("6 - Mostrar todos os alunos de uma turma\n")
    print("7 - Mostrar todas as turmas cadastradas\n")
    print("0 - Voltar ao menu principal")
    opcao_nao_valida = True
    while opcao_nao_valida == True:
        try:
            option = int(input('Opção desejada:\n'))
            if option == 0:
                opcao_nao_valida = False
                menu_home()

            elif option == 1:
                opcao_nao_valida = False
                cadastrar_turma()
                
            elif option == 2:
                opcao_nao_valida = False
                designar_professor()

            elif option == 3:
                opcao_nao_valida = False
                designar_aluno()

            elif option == 4:        
                remover_aluno()

            elif option == 5:
                aplicar_notas()

            elif option == 6:
                mostrar_alunos_turma()
            
            elif option == 7:
                menu_turmas()
                
        except:
            print('Infelizmente essa não é uma opção válida')
            menu_home()
            pass

def cadastrar_turma():
    clear()
    line_break()
    print("Para cadastrar uma nova turma, insira o código da mesma")
    codigo=str(input("Código:\n"))
    print("\n")
    turma_existente = session.query(Turma).filter_by(codigo=codigo).first()
    if turma_existente:
        print("Essa turma já existe")
        sleep(1)
        cadastrar_turma()
    else:
        print(f'Cadastrando a turma com o código {codigo}')
        turma = Turma(codigo=codigo)
        session.add(turma)
        session.commit()
        print(f'Turma com código {codigo} cadastrada com sucesso')
        sleep(1)
        menu_turmas()

def designar_professor():
    clear()
    line_break()
    print("Qual turma deseja modificar?")
    print("\n")
    turmas = session.query(Turma).all()
    print("ID/Código")
    line_break()
    #professores conterá uma lista com todos os professores, ou seja, um elemento iterável, cada objeto dentro do elemento corresponde a um professor
    for turma in turmas:
        print(f'{turma.id}/{turma.codigo}\n')
    print("Pressione 0 para voltar ao menu anterior ou o id da turma desejada")
    try:
        option = int(input('Opção desejada:\n'))
        turma = session.query(Turma).filter_by(id=option).first()
        if option == 0:
            #valid_option = True
            menu_turmas()
        elif turma:
            print("Qual desses professores você gostaria de adicionar a turma?")
            print("Os professores são:")
            professores = session.query(Professor).all()
            print("ID/Primeiro Nome/Segundo Nome/Email/Nível de Formação")
            line_break()
            #professores conterá uma lista com todos os professores, ou seja, um elemento iterável, cada objeto dentro do elemento corresponde a um professor
            for professor in professores:
                pessoa = session.query(Pessoa).filter_by(id=professor.id).first()
                print(f'{professor.id}/{pessoa.forename}/{pessoa.surname}/{professor.email}/{professor.niveldeformacao}/{professor.materias}\n')
            
            prof_option=int(input('Opção desejada:\n'))
            professor = session.query(Professor).filter_by(id=prof_option)
            if professor:
                setattr(turma, 'professor_id', professor.id) #atualiza o atributo professor_id da tabela turma
                session.commit()
                print(f'professor {professor.nome} adicionado a turma {turma.codigo}')
                menu_turmas()
            else:
                pass
    except:
        menu_turmas()

'''
def designar_aluno():

def remover_aluno():

def aplicar_nota():

def mostrar_alunos_turma():

def mostrar_turmas():
'''
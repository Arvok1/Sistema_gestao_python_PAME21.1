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
                
        except:
            pass    

        print('Infelizmente essa não é uma opção válida')


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
        cadastrar_materia()
    else:
        materia = Materia(codigo=codigo, nome=nome)
        session.add(materia)
        session.commit()
        print(f'Materia {codigo} cadastrada com sucesso, voltando ao menu')
        sleep(10)

    
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
    else:
        pessoa_professor = Pessoa(forename=nome, surname=sobrenome, cpf=cpf)
        session.add(pessoa_professor)
        professor = Professor(pessoa=pessoa_professor, email=email, niveldeformacao=niveldeformacao)
        session.add(professor)
        session.commit()
        print(f'Professor {nome} cadastrada com sucesso')
        sleep(10)

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
    sleep(10)

def mostrar_materias():
    print("As matérias são:")

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

    valid_option = False
    while valid_option == False:
        try:
            option = int(input('Opção desejada:\n'))
            professor=Professor.find_by_id(id=option)
            if option == 0:
                return menu_home()

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
                        valid_option = True
                        mostrar_professores()

                    if option == 1:
                        valid_option = True
                        menu_home()
                    else:
                        valid_option = False
                        print('Infelizmente essa não é uma opção válida')
                        pass
                except:
                    pass
            else:
                valid_option = False
                print('Infelizmente essa não é uma opção válida')
                pass

        except:
            print('Infelizmente essa não é uma opção válida')
            valid_option = False
            pass
           


def sair_do_programa():
    print("O programa fechará em 1 segundo")
    exit(0)

'''
def menu_turmas():

def designar_professor():

def adicionar_aluno():

def remover_aluno():

def aplicar_nota():

def mostrar_turmas():
'''
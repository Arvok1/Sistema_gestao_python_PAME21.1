from logging import raiseExceptions
from sqlalchemy.sql.schema import ForeignKey
from SQLAlchemy import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from os import system, name
from time import sleep

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# define our clear function
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

#Relação many to many, um professor pode ensinar várias matérias e uma matéria pode ter vários professores
professores_materias = Table('professores_materias', Base.metadata,
Column('professores_id', Integer, ForeignKey('professor.id')),
Column('materias_id', Integer, ForeignKey('materia.id'))
)

class Aluno_turma(Base):
    __tablename__ = 'aluno_turma'
    turma_id = Column(Integer, ForeignKey('turma.id'), primary_key=True)
    aluno_id = Column(Integer, ForeignKey('aluno.id'), primary_key=True)
    nota = Float
    Aluno = relationship("Aluno")


class Pessoa(Base):
    __tablename__='pessoa'

    id=Column(Integer, primary_key=True, autoincrement= True)
    forename = Column(String(16))
    surname= Column(String(64))
    cpf= Column(String(13))

    memberships = relationship('Membership', backref='pessoa')

class Professor(Base):
    __tablename__='professor'
    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True )
    pessoa = relationship('Pessoa')
    email = Column(String(120))
    niveldeformacao = Column(String(20))
    turmas = relationship("Turma") #one to many, um professor pode ter várias turmas, mas cada turma só tem um professor
    materias = relationship("Materia", secondary=professores_materias, back_populates="professores")

class Aluno(Base):
    __tablename__='professor'
    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True )
    pessoa = relationship('Pessoa')
    email = Column(String(120))


class Materia(Base):
    __tablename__='materia'
    id=Column(Integer, primary_key=True, autoincrement= True)
    codigo=Column(String(6))
    nome = Column(String(30))
    professores = relationship("Professor", secondary=professores_materias, back_populates="materias")
    turmas =  relationship("Turma")

class Turma(Base):
    __tablename__='turma'
    professor_id=Column(Integer, ForeignKey('professor.id')) #one to many relationship
    materia_id=Column(Integer, ForeignKey('materia.id'))
    alunos = relationship("Aluno_turma")



def line_break():
    print("\n--------------------------------------\n")


def login_inicial():

def menu_home():
    clear()
    line_break()
    print("Escolha uma das opções abaixo:")
    line_break()
    print("1 - Cadastrar nova matéria\n")
    print("2 - Cadastrar novo professor\n")
    print("3 - Cadastrar novo aluno\n")
    try:
        option = int(input('Opção desejada:\n'))
        if option == 0:
            menu_home()

        elif option == 1:
            clear()
            line_break()
            


    except:
        print('Infelizmente essa não é uma opção válida')    
def cadastrar_professor():
    print("Para cadastrar um novo professor, precisamos de:")

def cadastrar_aluno():
    print("Para cadastrar um novo aluno, precisamos de:")

def mostrar_materias():
    print("As matérias são:")

def mostrar_professores():
    print("Os professores são:")
    professores = Professor.query.all()
    print("ID/Primeiro Nome/Segundo Nome/Email/Nível de Formação")
    line_break
    for professor in professores:
        pessoa = Pessoa.query.filter_by(id=professor.id)
        print(f'{professor.id}/{pessoa.forename}/{pessoa.surname}/{professor.email}/{professor.niveldeformacao}/{professor.materias}\n')
    print('Opções:\n')
    print(' Digite o id do professor que você deseja ver as turmas ou 0 para voltar ao menu principal\n')

    valid_option = False
    while valid_option == False:
        try:
            option = int(input('Opção desejada:\n'))
            professor=Professor.query.filter_by(id=option)
            if option == 0:
                return menu_home()

            elif professor:
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
            else:
                valid_option = False
                print('Infelizmente essa não é uma opção válida')
                pass

        except:
            print('Infelizmente essa não é uma opção válida')
            valid_option = False
            pass   

def sair_do_programa():

def menu_turmas():

def designar_professor():

def adicionar_aluno():

def remover_aluno():

def aplicar_nota():

def mostrar_turmas():


from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

professores_materias = Table('professores_materias', Base.metadata,
Column('professores_id', Integer, ForeignKey('professor.id')),
Column('materias_id', Integer, ForeignKey('materia.id'))
)

#Objeto relacional de uma relação many-to-many, visto que vários alunos podem ser vinculados a várias turmas e uma relação aluno-turma terá uma nota
class Aluno_turma(Base):
    __tablename__ = 'aluno_turma'
    turma_id = Column(Integer, ForeignKey('turma.id'), primary_key=True)
    aluno_id = Column(Integer, ForeignKey('aluno.id'), primary_key=True)
    nota = Float
    Aluno = relationship("Aluno")

'''
Por dificultar o processo de criar classes filhas, como seriam Aluno e Professor da classe Pessoa, optei aqui por apenas vinculá-las no Banco de Dados
Dessa maneira, ao se criar um Professor ou um Aluno, será criada uma entrada na tabela Pessoa, que possuirá as informações que são comuns as duas classes:
cpf, nome e sobrenome.
'''
class Pessoa(Base):
    __tablename__='pessoa'

    id=Column(Integer, primary_key=True, autoincrement= True)
    forename = Column(String(16))
    surname= Column(String(64))
    cpf= Column(String(13))

   

    @classmethod
    def find_by_id(session, id):
        return session.query(Pessoa).filter_by(id=id).first()
    
    @classmethod
    def query_all(session):
        return session.query(Pessoa).all()

class Professor(Base):
    __tablename__='professor'
    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True )
    pessoa = relationship('Pessoa')
    email = Column(String(120))
    niveldeformacao = Column(String(20))
    turmas = relationship("Turma") #one to many, um professor pode ter várias turmas, mas cada turma só tem um professor
    materias = relationship("Materia", secondary=professores_materias, back_populates="professores")

    @classmethod
    def find_by_id(session, id):
        return session.query(Professor).filter_by(id=id).first()
    
    @classmethod
    def query_all(session):
        return session.query(Professor).all()

class Aluno(Base):
    __tablename__='aluno'
    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True )
    pessoa = relationship('Pessoa')
    email = Column(String(120))

    @classmethod
    def find_by_id(session, id):
        return session.query(Aluno).filter_by(id=id).first()
    
    @classmethod
    def query_all(session):
        return session.query(Aluno).all()

class Materia(Base):
    __tablename__='materia'
    id=Column(Integer, primary_key=True, autoincrement= True)
    codigo=Column(String(6), unique=True)
    nome = Column(String(30))
    professores = relationship("Professor", secondary=professores_materias, back_populates="materias")
    turmas =  relationship("Turma")

    @classmethod
    def find_by_id(session, id):
        return session.query(Materia).filter_by(id=id).first()
    
    @classmethod
    def query_all(session):
        return session.query(Materia).all()

    @classmethod
    def query_by_cod(session, cod):
        return session.query(Materia).filter_by(codigo=cod).first()

class Turma(Base):
    __tablename__='turma'
    id=Column(Integer, primary_key=True, autoincrement= True)
    professor_id=Column(Integer, ForeignKey('professor.id')) #one to many relationship
    materia_id=Column(Integer, ForeignKey('materia.id'))
    alunos = relationship("Aluno_turma")

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(Turma).filter_by(id=id).first()

    @classmethod
    def query_all(cls, session):
        return session.query(Turma).all()
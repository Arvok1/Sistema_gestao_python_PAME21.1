
from model import Base, engine, session
from functions import login_inicial
from model import professores_materias, Aluno_turma, Pessoa, Professor, Aluno, Materia, Turma




def init_db():
    Base.metadata.create_all(bind=engine) 
    #cria as tabelas no banco de dados
    session.commit()    #"commita" as modificações


def main():
    login_inicial()


if __name__ == "__main__":
    init_db()
    main()
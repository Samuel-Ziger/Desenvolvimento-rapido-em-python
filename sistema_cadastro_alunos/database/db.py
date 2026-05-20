"""
Módulo de gerenciamento do banco de dados SQLite.
Responsável por criar a conexão, inicializar as tabelas e fornecer
um context manager para uso seguro do banco.
"""
import sqlite3
import os
from contextlib import contextmanager

# Caminho do arquivo do banco - fica na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sistema_alunos.db")


@contextmanager
def get_connection():
    """
    Context manager que retorna uma conexão SQLite com row_factory configurada
    para retornar resultados como dicionários (sqlite3.Row).
    Garante commit em sucesso e rollback em erro.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Habilita verificação de chaves estrangeiras (vem desabilitado por default no SQLite)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """
    Cria as tabelas se ainda não existirem.
    Modelo conforme especificação:
      ALUNO     (MATRICULA PK, NOME, DT_NASCIMENTO)
      DISCIPLINA(ID PK, NOME, TURNO, SALA, PROFESSOR)
      NOTA      (VALOR, MATRICULA FK, DISCIPLINA_ID FK) - PK composta
    """
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS aluno (
                matricula     TEXT PRIMARY KEY,
                nome          TEXT NOT NULL,
                dt_nascimento TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS disciplina (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      TEXT NOT NULL,
                turno     TEXT NOT NULL,
                sala      TEXT NOT NULL,
                professor TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS nota (
                valor         REAL NOT NULL,
                matricula     TEXT NOT NULL,
                disciplina_id INTEGER NOT NULL,
                PRIMARY KEY (matricula, disciplina_id),
                FOREIGN KEY (matricula)    REFERENCES aluno(matricula)   ON DELETE CASCADE,
                FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)    ON DELETE CASCADE
            )
        """)


if __name__ == "__main__":
    init_db()
    print(f"Banco inicializado em: {DB_PATH}")

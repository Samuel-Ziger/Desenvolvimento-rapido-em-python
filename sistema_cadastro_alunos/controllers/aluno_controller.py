"""
Controller de Aluno - CRUD via SQLite.
"""
from typing import List, Optional
from database.db import get_connection
from models.aluno import Aluno


class AlunoController:

    @staticmethod
    def listar(filtro: str = "") -> List[Aluno]:
        """Lista alunos. Se filtro for informado, busca por matrícula ou nome."""
        with get_connection() as conn:
            cur = conn.cursor()
            if filtro:
                like = f"%{filtro}%"
                cur.execute(
                    "SELECT * FROM aluno WHERE matricula LIKE ? OR nome LIKE ? ORDER BY nome",
                    (like, like),
                )
            else:
                cur.execute("SELECT * FROM aluno ORDER BY nome")
            return [Aluno.from_row(row) for row in cur.fetchall()]

    @staticmethod
    def buscar(matricula: str) -> Optional[Aluno]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM aluno WHERE matricula = ?", (matricula,))
            row = cur.fetchone()
            return Aluno.from_row(row) if row else None

    @staticmethod
    def incluir(aluno: Aluno) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO aluno (matricula, nome, dt_nascimento) VALUES (?, ?, ?)",
                (aluno.matricula, aluno.nome, aluno.dt_nascimento),
            )

    @staticmethod
    def alterar(aluno: Aluno) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE aluno SET nome = ?, dt_nascimento = ? WHERE matricula = ?",
                (aluno.nome, aluno.dt_nascimento, aluno.matricula),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Aluno com matrícula {aluno.matricula} não encontrado.")

    @staticmethod
    def excluir(matricula: str) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM aluno WHERE matricula = ?", (matricula,))
            if cur.rowcount == 0:
                raise ValueError(f"Aluno com matrícula {matricula} não encontrado.")

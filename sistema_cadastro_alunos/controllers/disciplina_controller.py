"""
Controller de Disciplina - CRUD via SQLite.
"""
from typing import List, Optional
from database.db import get_connection
from models.disciplina import Disciplina


class DisciplinaController:

    @staticmethod
    def listar(filtro: str = "") -> List[Disciplina]:
        with get_connection() as conn:
            cur = conn.cursor()
            if filtro:
                like = f"%{filtro}%"
                cur.execute(
                    """SELECT * FROM disciplina
                       WHERE nome LIKE ? OR professor LIKE ? OR sala LIKE ?
                       ORDER BY nome""",
                    (like, like, like),
                )
            else:
                cur.execute("SELECT * FROM disciplina ORDER BY nome")
            return [Disciplina.from_row(row) for row in cur.fetchall()]

    @staticmethod
    def buscar(disciplina_id: int) -> Optional[Disciplina]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM disciplina WHERE id = ?", (disciplina_id,))
            row = cur.fetchone()
            return Disciplina.from_row(row) if row else None

    @staticmethod
    def incluir(disciplina: Disciplina) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO disciplina (nome, turno, sala, professor) VALUES (?, ?, ?, ?)",
                (disciplina.nome, disciplina.turno, disciplina.sala, disciplina.professor),
            )
            return cur.lastrowid

    @staticmethod
    def alterar(disciplina: Disciplina) -> None:
        if disciplina.id is None:
            raise ValueError("ID da disciplina é obrigatório para alteração.")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """UPDATE disciplina
                   SET nome = ?, turno = ?, sala = ?, professor = ?
                   WHERE id = ?""",
                (disciplina.nome, disciplina.turno, disciplina.sala,
                 disciplina.professor, disciplina.id),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Disciplina id={disciplina.id} não encontrada.")

    @staticmethod
    def excluir(disciplina_id: int) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM disciplina WHERE id = ?", (disciplina_id,))
            if cur.rowcount == 0:
                raise ValueError(f"Disciplina id={disciplina_id} não encontrada.")

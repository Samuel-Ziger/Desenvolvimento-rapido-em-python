"""
Controller de Nota - CRUD via SQLite.
Chave composta: (matricula, disciplina_id).
"""
from typing import List, Optional, Dict, Any
from database.db import get_connection
from models.nota import Nota


class NotaController:

    @staticmethod
    def listar(filtro: str = "") -> List[Dict[str, Any]]:
        """
        Retorna notas com JOIN para mostrar nome do aluno e disciplina.
        Cada item é um dict (não Nota) para facilitar exibição.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            sql_base = """
                SELECT n.valor, n.matricula, n.disciplina_id,
                       a.nome AS aluno_nome,
                       d.nome AS disciplina_nome
                FROM nota n
                JOIN aluno a      ON a.matricula = n.matricula
                JOIN disciplina d ON d.id = n.disciplina_id
            """
            if filtro:
                like = f"%{filtro}%"
                cur.execute(
                    sql_base + " WHERE a.nome LIKE ? OR d.nome LIKE ? OR n.matricula LIKE ? ORDER BY a.nome, d.nome",
                    (like, like, like),
                )
            else:
                cur.execute(sql_base + " ORDER BY a.nome, d.nome")
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def buscar(matricula: str, disciplina_id: int) -> Optional[Nota]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM nota WHERE matricula = ? AND disciplina_id = ?",
                (matricula, disciplina_id),
            )
            row = cur.fetchone()
            return Nota.from_row(row) if row else None

    @staticmethod
    def incluir(nota: Nota) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO nota (valor, matricula, disciplina_id) VALUES (?, ?, ?)",
                (nota.valor, nota.matricula, nota.disciplina_id),
            )

    @staticmethod
    def alterar(nota: Nota) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE nota SET valor = ? WHERE matricula = ? AND disciplina_id = ?",
                (nota.valor, nota.matricula, nota.disciplina_id),
            )
            if cur.rowcount == 0:
                raise ValueError("Nota não encontrada.")

    @staticmethod
    def excluir(matricula: str, disciplina_id: int) -> None:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM nota WHERE matricula = ? AND disciplina_id = ?",
                (matricula, disciplina_id),
            )
            if cur.rowcount == 0:
                raise ValueError("Nota não encontrada.")

    @staticmethod
    def boletim_aluno(matricula: str) -> Dict[str, Any]:
        """
        Retorna boletim do aluno: dados + lista de notas + média.
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM aluno WHERE matricula = ?", (matricula,))
            aluno_row = cur.fetchone()
            if not aluno_row:
                return {}

            cur.execute(
                """SELECT n.valor, d.nome AS disciplina_nome, d.professor, d.turno
                   FROM nota n
                   JOIN disciplina d ON d.id = n.disciplina_id
                   WHERE n.matricula = ?
                   ORDER BY d.nome""",
                (matricula,),
            )
            notas = [dict(r) for r in cur.fetchall()]
            media = round(sum(n["valor"] for n in notas) / len(notas), 2) if notas else 0.0
            return {
                "matricula": aluno_row["matricula"],
                "nome": aluno_row["nome"],
                "dt_nascimento": aluno_row["dt_nascimento"],
                "notas": notas,
                "media": media,
                "situacao": "APROVADO" if media >= 7 else ("RECUPERAÇÃO" if media >= 4 else "REPROVADO"),
            }

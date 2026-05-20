"""
Model Aluno - representa um aluno do sistema.
"""
from dataclasses import dataclass, asdict


@dataclass
class Aluno:
    matricula: str
    nome: str
    dt_nascimento: str  # formato ISO: YYYY-MM-DD

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row) -> "Aluno":
        """Cria Aluno a partir de uma sqlite3.Row ou dict."""
        return Aluno(
            matricula=row["matricula"],
            nome=row["nome"],
            dt_nascimento=row["dt_nascimento"],
        )

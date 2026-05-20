"""
Model Disciplina.
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Disciplina:
    nome: str
    turno: str       # Manhã / Tarde / Noite
    sala: str
    professor: str
    id: Optional[int] = None  # AUTOINCREMENT

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row) -> "Disciplina":
        return Disciplina(
            id=row["id"],
            nome=row["nome"],
            turno=row["turno"],
            sala=row["sala"],
            professor=row["professor"],
        )

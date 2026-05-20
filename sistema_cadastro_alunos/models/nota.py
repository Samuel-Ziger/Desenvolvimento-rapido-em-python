"""
Model Nota - chave composta por (matricula, disciplina_id).
"""
from dataclasses import dataclass, asdict


@dataclass
class Nota:
    valor: float
    matricula: str
    disciplina_id: int

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_row(row) -> "Nota":
        return Nota(
            valor=row["valor"],
            matricula=row["matricula"],
            disciplina_id=row["disciplina_id"],
        )

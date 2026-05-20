"""
Validações de entrada utilizadas pelas views/controllers.
Cada função retorna (valido: bool, mensagem: str).
"""
import re
from datetime import datetime


def validar_matricula(matricula: str) -> tuple[bool, str]:
    """Matrícula: 4 a 12 caracteres alfanuméricos."""
    matricula = (matricula or "").strip()
    if not matricula:
        return False, "Matrícula é obrigatória."
    if not re.fullmatch(r"[A-Za-z0-9]{4,12}", matricula):
        return False, "Matrícula deve conter 4 a 12 caracteres alfanuméricos."
    return True, ""


def validar_nome(nome: str, campo: str = "Nome") -> tuple[bool, str]:
    """Nome: 2 a 80 caracteres, letras, espaços e acentuação."""
    nome = (nome or "").strip()
    if not nome:
        return False, f"{campo} é obrigatório."
    if len(nome) < 2 or len(nome) > 80:
        return False, f"{campo} deve ter entre 2 e 80 caracteres."
    if not re.fullmatch(r"[A-Za-zÀ-ÿ\s\.\-']+", nome):
        return False, f"{campo} contém caracteres inválidos."
    return True, ""


def validar_data(data: str) -> tuple[bool, str]:
    """
    Aceita data no formato YYYY-MM-DD ou DD/MM/YYYY.
    Retorna válido + mensagem. Caso queira a data normalizada, use normalizar_data().
    """
    data = (data or "").strip()
    if not data:
        return False, "Data de nascimento é obrigatória."
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            d = datetime.strptime(data, fmt)
            if d > datetime.now():
                return False, "Data não pode ser futura."
            if d.year < 1900:
                return False, "Data inválida (ano anterior a 1900)."
            return True, ""
        except ValueError:
            continue
    return False, "Data inválida. Use DD/MM/AAAA ou AAAA-MM-DD."


def normalizar_data(data: str) -> str:
    """Converte qualquer formato aceito para YYYY-MM-DD (ISO)."""
    data = data.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(data, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Data em formato inválido: {data}")


def formatar_data_br(data_iso: str) -> str:
    """Converte YYYY-MM-DD para DD/MM/YYYY para exibição."""
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return data_iso or ""


def validar_nota(valor) -> tuple[bool, str]:
    """Nota: numérico entre 0 e 10."""
    if valor is None or str(valor).strip() == "":
        return False, "Valor da nota é obrigatório."
    try:
        v = float(str(valor).replace(",", "."))
    except ValueError:
        return False, "Nota deve ser um número."
    if v < 0 or v > 10:
        return False, "Nota deve estar entre 0 e 10."
    return True, ""


def validar_turno(turno: str) -> tuple[bool, str]:
    turnos_validos = {"Manhã", "Tarde", "Noite", "Integral"}
    if not turno or turno not in turnos_validos:
        return False, f"Turno deve ser um de: {', '.join(sorted(turnos_validos))}."
    return True, ""


def validar_texto(texto: str, campo: str, minimo: int = 1, maximo: int = 50) -> tuple[bool, str]:
    """Validação genérica de texto."""
    texto = (texto or "").strip()
    if len(texto) < minimo:
        return False, f"{campo} deve ter no mínimo {minimo} caractere(s)."
    if len(texto) > maximo:
        return False, f"{campo} deve ter no máximo {maximo} caracteres."
    return True, ""

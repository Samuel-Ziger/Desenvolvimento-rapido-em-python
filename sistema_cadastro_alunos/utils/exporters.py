"""
Exportação de dados para arquivos JSON, CSV e TXT.
Atende ao requisito da especificação de persistir dados em arquivo
(além do banco SQLite).
"""
import json
import csv
import os
from typing import List, Dict


def exportar_json(caminho: str, dados: List[Dict]) -> None:
    """Exporta lista de dicts para JSON com indentação."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def exportar_csv(caminho: str, dados: List[Dict]) -> None:
    """Exporta lista de dicts para CSV. Se vazio, cria arquivo vazio."""
    if not dados:
        # cria CSV vazio sem cabeçalho
        open(caminho, "w", encoding="utf-8").close()
        return
    campos = list(dados[0].keys())
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(dados)


def exportar_txt(caminho: str, dados: List[Dict], titulo: str = "") -> None:
    """Exporta lista de dicts em TXT amigável (legível por humanos)."""
    with open(caminho, "w", encoding="utf-8") as f:
        if titulo:
            f.write(f"=== {titulo} ===\n\n")
        if not dados:
            f.write("(nenhum registro)\n")
            return
        for i, item in enumerate(dados, start=1):
            f.write(f"--- Registro {i} ---\n")
            for chave, valor in item.items():
                f.write(f"  {chave}: {valor}\n")
            f.write("\n")


def exportar_todos(diretorio: str, nome_base: str, dados: List[Dict], titulo: str = "") -> Dict[str, str]:
    """
    Exporta nos três formatos (JSON, CSV, TXT).
    Retorna dict com os caminhos finais de cada arquivo gerado.
    """
    os.makedirs(diretorio, exist_ok=True)
    caminhos = {
        "json": os.path.join(diretorio, f"{nome_base}.json"),
        "csv":  os.path.join(diretorio, f"{nome_base}.csv"),
        "txt":  os.path.join(diretorio, f"{nome_base}.txt"),
    }
    exportar_json(caminhos["json"], dados)
    exportar_csv(caminhos["csv"], dados)
    exportar_txt(caminhos["txt"], dados, titulo=titulo or nome_base)
    return caminhos

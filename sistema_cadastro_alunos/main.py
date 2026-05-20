"""
Sistema de Cadastro de Alunos
Trabalho de Desenvolvimento Rápido em Python - Estácio
Tecnologias: Python + Tkinter + SQLite

Como executar:
    python main.py
"""
import os
import sys

# Garante que o diretório do projeto está no sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db import init_db
from views.main_window import MainWindow


def main():
    init_db()
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()

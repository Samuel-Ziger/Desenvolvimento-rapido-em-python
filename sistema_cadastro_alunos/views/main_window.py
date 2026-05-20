"""
Janela principal - menu de navegação para as funcionalidades.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os

from views.aluno_window import AlunoWindow
from views.disciplina_window import DisciplinaWindow
from views.nota_window import NotaWindow
from views.relatorio_window import RelatorioWindow
from controllers.aluno_controller import AlunoController
from controllers.disciplina_controller import DisciplinaController
from controllers.nota_controller import NotaController
from utils.exporters import exportar_todos


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro de Alunos - Estácio")
        self.geometry("520x520")
        self.minsize(520, 520)
        self.resizable(True, True)
        self._fullscreen = False
        self.configure(bg="#f0f4f8")
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._sair_fullscreen)
        self._build_ui()

    def _toggle_fullscreen(self, event=None):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)
        return "break"

    def _sair_fullscreen(self, event=None):
        if self._fullscreen:
            self._fullscreen = False
            self.attributes("-fullscreen", False)

    def _build_ui(self):
        # Cabeçalho
        header = tk.Frame(self, bg="#1f4e79", height=90)
        header.pack(fill="x")
        tk.Label(
            header, text="Sistema de Cadastro de Alunos",
            font=("Segoe UI", 18, "bold"), fg="white", bg="#1f4e79",
        ).pack(pady=(18, 0))
        tk.Label(
            header, text="Trabalho de Desenvolvimento Rápido em Python",
            font=("Segoe UI", 10), fg="#cfe2f3", bg="#1f4e79",
        ).pack()

        # Container de botões
        body = tk.Frame(self, bg="#f0f4f8")
        body.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            body, text="Selecione uma opção:",
            font=("Segoe UI", 11, "bold"), bg="#f0f4f8", fg="#333",
        ).pack(anchor="w", pady=(0, 12))

        botoes = [
            ("Aluno",      "#2e86ab", self.abrir_alunos),
            ("Disciplina", "#2e86ab", self.abrir_disciplinas),
            ("Nota",       "#2e86ab", self.abrir_notas),
            ("Relatório / Boletim", "#5cb85c", self.abrir_relatorio),
            ("Exportar Todos os Dados (JSON/CSV/TXT)", "#f0ad4e", self.exportar_tudo),
            ("Sair", "#d9534f", self.destroy),
        ]
        for texto, cor, comando in botoes:
            btn = tk.Button(
                body, text=texto, command=comando,
                bg=cor, fg="white", font=("Segoe UI", 11, "bold"),
                relief="flat", cursor="hand2", height=2, width=40,
            )
            btn.pack(pady=4)

        # Rodapé
        footer = tk.Frame(self, bg="#f0f4f8")
        footer.pack(fill="x", side="bottom", pady=8)
        tk.Label(
            footer, text="Python • Tkinter • SQLite",
            font=("Segoe UI", 8), fg="#888", bg="#f0f4f8",
        ).pack()

    def abrir_alunos(self):
        AlunoWindow(self)

    def abrir_disciplinas(self):
        DisciplinaWindow(self)

    def abrir_notas(self):
        NotaWindow(self)

    def abrir_relatorio(self):
        RelatorioWindow(self)

    def exportar_tudo(self):
        """Exporta as três entidades nos três formatos para a pasta /exports."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            export_dir = os.path.join(base_dir, "exports")

            alunos = [a.to_dict() for a in AlunoController.listar()]
            disciplinas = [d.to_dict() for d in DisciplinaController.listar()]
            notas = NotaController.listar()

            exportar_todos(export_dir, "alunos", alunos, "Alunos Cadastrados")
            exportar_todos(export_dir, "disciplinas", disciplinas, "Disciplinas Cadastradas")
            exportar_todos(export_dir, "notas", notas, "Notas Lançadas")

            messagebox.showinfo(
                "Exportação concluída",
                f"Arquivos JSON, CSV e TXT gerados em:\n{export_dir}",
            )
        except Exception as e:
            messagebox.showerror("Erro ao exportar", str(e))

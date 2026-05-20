"""
Janela de Relatório - Boletim por Aluno.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from controllers.aluno_controller import AlunoController
from controllers.nota_controller import NotaController
from utils.validators import formatar_data_br


class RelatorioWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatório - Boletim do Aluno")
        self.geometry("720x520")
        self.configure(bg="#f0f4f8")
        self.grab_set()

        self._mapa = {}
        self._build_ui()
        self._carregar_alunos()

    def _build_ui(self):
        top = tk.Frame(self, bg="#f0f4f8")
        top.pack(fill="x", padx=10, pady=10)

        tk.Label(top, text="Selecione o aluno:", bg="#f0f4f8",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        self.cmb = ttk.Combobox(top, width=50, state="readonly")
        self.cmb.pack(side="left", padx=8)
        tk.Button(top, text="Gerar Boletim", bg="#2e86ab", fg="white",
                  command=self.gerar).pack(side="left", padx=4)

        # Info aluno
        self.info = tk.LabelFrame(self, text="Aluno", bg="#f0f4f8",
                                  font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        self.info.pack(fill="x", padx=10)
        self.lbl_dados = tk.Label(self.info, text="(nenhum aluno selecionado)", bg="#f0f4f8",
                                  justify="left", anchor="w")
        self.lbl_dados.pack(fill="x")

        # Notas
        list_frame = tk.Frame(self, bg="#f0f4f8")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("disciplina", "professor", "turno", "valor")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        for c, t, w in zip(cols,
                           ["Disciplina", "Professor", "Turno", "Nota"],
                           [240, 220, 80, 80]):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center" if c in ("turno", "valor") else "w")
        self.tree.pack(fill="both", expand=True)

        # Rodapé com média
        self.footer = tk.Frame(self, bg="#f0f4f8")
        self.footer.pack(fill="x", padx=10, pady=10)
        self.lbl_resultado = tk.Label(self.footer, text="", bg="#f0f4f8",
                                      font=("Segoe UI", 12, "bold"))
        self.lbl_resultado.pack()

    def _carregar_alunos(self):
        alunos = AlunoController.listar()
        self._mapa = {f"{a.matricula} - {a.nome}": a.matricula for a in alunos}
        self.cmb["values"] = list(self._mapa.keys())

    def gerar(self):
        chave = self.cmb.get()
        if not chave:
            messagebox.showwarning("Atenção", "Selecione um aluno.", parent=self)
            return
        matricula = self._mapa[chave]
        boletim = NotaController.boletim_aluno(matricula)
        if not boletim:
            messagebox.showerror("Erro", "Aluno não encontrado.", parent=self)
            return

        self.lbl_dados.config(text=(
            f"Matrícula: {boletim['matricula']}    "
            f"Nome: {boletim['nome']}    "
            f"Nascimento: {formatar_data_br(boletim['dt_nascimento'])}"
        ))

        for it in self.tree.get_children():
            self.tree.delete(it)
        for n in boletim["notas"]:
            self.tree.insert("", "end", values=(
                n["disciplina_nome"], n["professor"], n["turno"], f"{n['valor']:.2f}",
            ))

        cor = {"APROVADO": "#2e7d32", "RECUPERAÇÃO": "#ef6c00", "REPROVADO": "#c62828"}.get(
            boletim["situacao"], "#333"
        )
        if boletim["notas"]:
            self.lbl_resultado.config(
                text=f"Média: {boletim['media']:.2f}   |   Situação: {boletim['situacao']}",
                fg=cor,
            )
        else:
            self.lbl_resultado.config(text="Aluno sem notas lançadas.", fg="#888")

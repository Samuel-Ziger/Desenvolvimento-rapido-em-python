"""
Janela CRUD de Alunos.
Operações: Listar, Incluir, Alterar, Excluir + Busca/filtro.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from controllers.aluno_controller import AlunoController
from models.aluno import Aluno
from utils.validators import (
    validar_matricula, validar_nome, validar_data,
    normalizar_data, formatar_data_br,
)


class AlunoWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Aluno")
        self.geometry("760x520")
        self.configure(bg="#f0f4f8")
        self.grab_set()  # modal

        self._build_ui()
        self.carregar_alunos()

    def _build_ui(self):
        # ----- Frame de formulário -----
        form = tk.LabelFrame(self, text="Dados do Aluno", bg="#f0f4f8",
                             font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Matrícula:", bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.ent_matricula = tk.Entry(form, width=20)
        self.ent_matricula.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Nome:", bg="#f0f4f8").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.ent_nome = tk.Entry(form, width=40)
        self.ent_nome.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Data Nascimento:", bg="#f0f4f8").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.ent_data = tk.Entry(form, width=20)
        self.ent_data.grid(row=1, column=1, sticky="w", padx=4, pady=4)
        tk.Label(form, text="(DD/MM/AAAA)", bg="#f0f4f8", fg="#888",
                 font=("Segoe UI", 8)).grid(row=1, column=2, sticky="w")

        # ----- Botões CRUD -----
        botoes = tk.Frame(self, bg="#f0f4f8")
        botoes.pack(fill="x", padx=10)

        tk.Button(botoes, text="Incluir", bg="#5cb85c", fg="white",
                  width=12, command=self.incluir).pack(side="left", padx=2)
        tk.Button(botoes, text="Alterar", bg="#f0ad4e", fg="white",
                  width=12, command=self.alterar).pack(side="left", padx=2)
        tk.Button(botoes, text="Excluir", bg="#d9534f", fg="white",
                  width=12, command=self.excluir).pack(side="left", padx=2)
        tk.Button(botoes, text="Limpar", bg="#777", fg="white",
                  width=12, command=self.limpar).pack(side="left", padx=2)

        # ----- Filtro -----
        filtro_frame = tk.Frame(self, bg="#f0f4f8")
        filtro_frame.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(filtro_frame, text="Buscar:", bg="#f0f4f8").pack(side="left")
        self.ent_filtro = tk.Entry(filtro_frame, width=40)
        self.ent_filtro.pack(side="left", padx=4)
        self.ent_filtro.bind("<KeyRelease>", lambda e: self.carregar_alunos())

        # ----- Listagem -----
        list_frame = tk.Frame(self, bg="#f0f4f8")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("matricula", "nome", "dt_nascimento")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
        self.tree.heading("matricula", text="Matrícula")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("dt_nascimento", text="Data Nascimento")
        self.tree.column("matricula", width=120, anchor="center")
        self.tree.column("nome", width=380)
        self.tree.column("dt_nascimento", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    # ---------- Operações ----------
    def carregar_alunos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        filtro = self.ent_filtro.get().strip()
        for aluno in AlunoController.listar(filtro):
            self.tree.insert(
                "", "end",
                values=(aluno.matricula, aluno.nome, formatar_data_br(aluno.dt_nascimento)),
            )

    def selecionar(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        valores = self.tree.item(sel[0])["values"]
        self.ent_matricula.delete(0, tk.END); self.ent_matricula.insert(0, valores[0])
        self.ent_nome.delete(0, tk.END);      self.ent_nome.insert(0, valores[1])
        self.ent_data.delete(0, tk.END);      self.ent_data.insert(0, valores[2])

    def _ler_form(self):
        return (
            self.ent_matricula.get().strip(),
            self.ent_nome.get().strip(),
            self.ent_data.get().strip(),
        )

    def _validar(self, matricula, nome, data):
        for ok, msg in (
            validar_matricula(matricula),
            validar_nome(nome),
            validar_data(data),
        ):
            if not ok:
                messagebox.showwarning("Validação", msg, parent=self)
                return False
        return True

    def incluir(self):
        matricula, nome, data = self._ler_form()
        if not self._validar(matricula, nome, data):
            return
        try:
            aluno = Aluno(matricula=matricula, nome=nome,
                          dt_nascimento=normalizar_data(data))
            AlunoController.incluir(aluno)
            messagebox.showinfo("Sucesso", "Aluno incluído.", parent=self)
            self.limpar()
            self.carregar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível incluir.\n{e}", parent=self)

    def alterar(self):
        matricula, nome, data = self._ler_form()
        if not self._validar(matricula, nome, data):
            return
        try:
            aluno = Aluno(matricula=matricula, nome=nome,
                          dt_nascimento=normalizar_data(data))
            AlunoController.alterar(aluno)
            messagebox.showinfo("Sucesso", "Aluno alterado.", parent=self)
            self.limpar()
            self.carregar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível alterar.\n{e}", parent=self)

    def excluir(self):
        matricula = self.ent_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Atenção", "Selecione um aluno para excluir.", parent=self)
            return
        if not messagebox.askyesno("Confirmar", f"Excluir aluno {matricula}?\n"
                                                "Notas vinculadas também serão removidas.",
                                   parent=self):
            return
        try:
            AlunoController.excluir(matricula)
            messagebox.showinfo("Sucesso", "Aluno excluído.", parent=self)
            self.limpar()
            self.carregar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir.\n{e}", parent=self)

    def limpar(self):
        self.ent_matricula.delete(0, tk.END)
        self.ent_nome.delete(0, tk.END)
        self.ent_data.delete(0, tk.END)
        for s in self.tree.selection():
            self.tree.selection_remove(s)

"""
Janela CRUD de Notas - usa Combobox para escolher aluno e disciplina.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from controllers.aluno_controller import AlunoController
from controllers.disciplina_controller import DisciplinaController
from controllers.nota_controller import NotaController
from models.nota import Nota
from utils.validators import validar_nota


class NotaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Nota")
        self.geometry("840x540")
        self.configure(bg="#f0f4f8")
        self.grab_set()

        self._mapa_alunos = {}      # display -> matricula
        self._mapa_disciplinas = {} # display -> id

        self._build_ui()
        self._recarregar_combos()
        self.carregar()

    def _build_ui(self):
        form = tk.LabelFrame(self, text="Lançamento de Nota", bg="#f0f4f8",
                             font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Aluno:", bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.cmb_aluno = ttk.Combobox(form, width=50, state="readonly")
        self.cmb_aluno.grid(row=0, column=1, columnspan=3, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Disciplina:", bg="#f0f4f8").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.cmb_disciplina = ttk.Combobox(form, width=50, state="readonly")
        self.cmb_disciplina.grid(row=1, column=1, columnspan=3, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Valor (0-10):", bg="#f0f4f8").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        self.ent_valor = tk.Entry(form, width=10)
        self.ent_valor.grid(row=2, column=1, sticky="w", padx=4, pady=4)

        # Botões
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
        tk.Button(botoes, text="Atualizar listas", bg="#5bc0de", fg="white",
                  width=16, command=self._recarregar_combos).pack(side="left", padx=2)

        # Filtro
        filtro_frame = tk.Frame(self, bg="#f0f4f8")
        filtro_frame.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(filtro_frame, text="Buscar:", bg="#f0f4f8").pack(side="left")
        self.ent_filtro = tk.Entry(filtro_frame, width=40)
        self.ent_filtro.pack(side="left", padx=4)
        self.ent_filtro.bind("<KeyRelease>", lambda e: self.carregar())

        # Lista
        list_frame = tk.Frame(self, bg="#f0f4f8")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        cols = ("matricula", "aluno", "disciplina_id", "disciplina", "valor")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
        for c, t, w in zip(cols,
                           ["Matrícula", "Aluno", "Disc. ID", "Disciplina", "Nota"],
                           [110, 240, 80, 240, 80]):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center" if c in ("matricula", "disciplina_id", "valor") else "w")
        # Esconde colunas de chave para usuário focar nos nomes
        self.tree.column("disciplina_id", width=70, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    def _recarregar_combos(self):
        # Alunos
        alunos = AlunoController.listar()
        self._mapa_alunos = {f"{a.matricula} - {a.nome}": a.matricula for a in alunos}
        self.cmb_aluno["values"] = list(self._mapa_alunos.keys())

        # Disciplinas
        discs = DisciplinaController.listar()
        self._mapa_disciplinas = {f"{d.id} - {d.nome}": d.id for d in discs}
        self.cmb_disciplina["values"] = list(self._mapa_disciplinas.keys())

    # ---------- Operações ----------
    def carregar(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        for n in NotaController.listar(self.ent_filtro.get().strip()):
            self.tree.insert("", "end", values=(
                n["matricula"], n["aluno_nome"], n["disciplina_id"],
                n["disciplina_nome"], f"{n['valor']:.2f}",
            ))

    def selecionar(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        matricula, nome_aluno, disc_id, nome_disc, valor = vals
        # Encontra strings nos combos
        chave_aluno = next((k for k, v in self._mapa_alunos.items() if v == str(matricula)), "")
        chave_disc  = next((k for k, v in self._mapa_disciplinas.items() if str(v) == str(disc_id)), "")
        self.cmb_aluno.set(chave_aluno)
        self.cmb_disciplina.set(chave_disc)
        self.ent_valor.delete(0, tk.END)
        self.ent_valor.insert(0, str(valor).replace(",", "."))

    def _ler_form(self):
        chave_aluno = self.cmb_aluno.get()
        chave_disc  = self.cmb_disciplina.get()
        valor = self.ent_valor.get().strip().replace(",", ".")
        matricula = self._mapa_alunos.get(chave_aluno)
        disc_id   = self._mapa_disciplinas.get(chave_disc)
        return matricula, disc_id, valor

    def incluir(self):
        matricula, disc_id, valor = self._ler_form()
        if not matricula:
            messagebox.showwarning("Validação", "Selecione um aluno.", parent=self); return
        if not disc_id:
            messagebox.showwarning("Validação", "Selecione uma disciplina.", parent=self); return
        ok, msg = validar_nota(valor)
        if not ok:
            messagebox.showwarning("Validação", msg, parent=self); return
        try:
            NotaController.incluir(Nota(valor=float(valor),
                                        matricula=matricula,
                                        disciplina_id=int(disc_id)))
            messagebox.showinfo("Sucesso", "Nota lançada.", parent=self)
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao incluir.\n"
                                          f"Verifique se já não existe nota deste aluno nesta disciplina.\n{e}",
                                 parent=self)

    def alterar(self):
        matricula, disc_id, valor = self._ler_form()
        if not (matricula and disc_id):
            messagebox.showwarning("Atenção", "Selecione uma nota da lista.", parent=self); return
        ok, msg = validar_nota(valor)
        if not ok:
            messagebox.showwarning("Validação", msg, parent=self); return
        try:
            NotaController.alterar(Nota(valor=float(valor),
                                        matricula=matricula,
                                        disciplina_id=int(disc_id)))
            messagebox.showinfo("Sucesso", "Nota alterada.", parent=self)
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao alterar.\n{e}", parent=self)

    def excluir(self):
        matricula, disc_id, _ = self._ler_form()
        if not (matricula and disc_id):
            messagebox.showwarning("Atenção", "Selecione uma nota da lista.", parent=self); return
        if not messagebox.askyesno("Confirmar", "Excluir esta nota?", parent=self):
            return
        try:
            NotaController.excluir(matricula, int(disc_id))
            messagebox.showinfo("Sucesso", "Nota excluída.", parent=self)
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir.\n{e}", parent=self)

    def limpar(self):
        self.cmb_aluno.set("")
        self.cmb_disciplina.set("")
        self.ent_valor.delete(0, tk.END)
        for s in self.tree.selection():
            self.tree.selection_remove(s)

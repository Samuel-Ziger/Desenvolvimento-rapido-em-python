"""
Janela CRUD de Disciplinas.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from controllers.disciplina_controller import DisciplinaController
from models.disciplina import Disciplina
from utils.validators import validar_nome, validar_turno, validar_texto


class DisciplinaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Disciplina")
        self.geometry("820x540")
        self.configure(bg="#f0f4f8")
        self.grab_set()

        self._build_ui()
        self.carregar()

    def _build_ui(self):
        form = tk.LabelFrame(self, text="Dados da Disciplina", bg="#f0f4f8",
                             font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="ID:", bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.ent_id = tk.Entry(form, width=10, state="readonly")
        self.ent_id.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Nome:", bg="#f0f4f8").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.ent_nome = tk.Entry(form, width=40)
        self.ent_nome.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Turno:", bg="#f0f4f8").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.cmb_turno = ttk.Combobox(
            form, width=15, state="readonly",
            values=["Manhã", "Tarde", "Noite", "Integral"],
        )
        self.cmb_turno.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Sala:", bg="#f0f4f8").grid(row=1, column=2, sticky="e", padx=4, pady=4)
        self.ent_sala = tk.Entry(form, width=20)
        self.ent_sala.grid(row=1, column=3, sticky="w", padx=4, pady=4)

        tk.Label(form, text="Professor:", bg="#f0f4f8").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        self.ent_professor = tk.Entry(form, width=50)
        self.ent_professor.grid(row=2, column=1, columnspan=3, sticky="w", padx=4, pady=4)

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

        cols = ("id", "nome", "turno", "sala", "professor")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
        for c, t, w in zip(cols,
                           ["ID", "Nome", "Turno", "Sala", "Professor"],
                           [50, 240, 80, 100, 240]):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="center" if c in ("id", "turno", "sala") else "w")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

    # ---------- Operações ----------
    def carregar(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        for d in DisciplinaController.listar(self.ent_filtro.get().strip()):
            self.tree.insert("", "end", values=(d.id, d.nome, d.turno, d.sala, d.professor))

    def selecionar(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self._set_id(str(vals[0]))
        self.ent_nome.delete(0, tk.END);      self.ent_nome.insert(0, vals[1])
        self.cmb_turno.set(vals[2])
        self.ent_sala.delete(0, tk.END);      self.ent_sala.insert(0, vals[3])
        self.ent_professor.delete(0, tk.END); self.ent_professor.insert(0, vals[4])

    def _set_id(self, valor: str):
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, valor)
        self.ent_id.config(state="readonly")

    def _ler_form(self):
        return (
            self.ent_id.get().strip(),
            self.ent_nome.get().strip(),
            self.cmb_turno.get().strip(),
            self.ent_sala.get().strip(),
            self.ent_professor.get().strip(),
        )

    def _validar(self, nome, turno, sala, professor):
        for ok, msg in (
            validar_nome(nome, "Nome da disciplina"),
            validar_turno(turno),
            validar_texto(sala, "Sala", 1, 20),
            validar_nome(professor, "Professor"),
        ):
            if not ok:
                messagebox.showwarning("Validação", msg, parent=self)
                return False
        return True

    def incluir(self):
        _id, nome, turno, sala, professor = self._ler_form()
        if not self._validar(nome, turno, sala, professor):
            return
        try:
            DisciplinaController.incluir(Disciplina(
                nome=nome, turno=turno, sala=sala, professor=professor,
            ))
            messagebox.showinfo("Sucesso", "Disciplina incluída.", parent=self)
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao incluir.\n{e}", parent=self)

    def alterar(self):
        _id, nome, turno, sala, professor = self._ler_form()
        if not _id:
            messagebox.showwarning("Atenção", "Selecione uma disciplina.", parent=self)
            return
        if not self._validar(nome, turno, sala, professor):
            return
        try:
            DisciplinaController.alterar(Disciplina(
                id=int(_id), nome=nome, turno=turno, sala=sala, professor=professor,
            ))
            messagebox.showinfo("Sucesso", "Disciplina alterada.", parent=self)
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao alterar.\n{e}", parent=self)

    def excluir(self):
        _id = self.ent_id.get().strip()
        if not _id:
            messagebox.showwarning("Atenção", "Selecione uma disciplina.", parent=self)
            return
        if not messagebox.askyesno("Confirmar",
                                   f"Excluir disciplina {_id}?\nNotas vinculadas serão removidas.",
                                   parent=self):
            return
        try:
            DisciplinaController.excluir(int(_id))
            messagebox.showinfo("Sucesso", "Disciplina excluída.", parent=self)
            self.limpar()
            self.carregar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir.\n{e}", parent=self)

    def limpar(self):
        self._set_id("")
        self.ent_nome.delete(0, tk.END)
        self.cmb_turno.set("")
        self.ent_sala.delete(0, tk.END)
        self.ent_professor.delete(0, tk.END)
        for s in self.tree.selection():
            self.tree.selection_remove(s)

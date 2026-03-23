import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import os
from datetime import datetime

# ──────────────────────────────────────────────
# BANCO DE DADOS
# ──────────────────────────────────────────────
DB_FILE = "escola.db"
JSON_FILE = "escola_backup.json"

def get_conn():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS ALUNO (
            MATRICULA TEXT PRIMARY KEY,
            NOME      TEXT NOT NULL,
            DT_NASCIMENTO TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS DISCIPLINA (
            ID        INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME      TEXT NOT NULL,
            TURNO     TEXT NOT NULL,
            SALA      TEXT NOT NULL,
            PROFESSOR TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS NOTA (
            VALOR         REAL NOT NULL,
            MATRICULA     TEXT NOT NULL,
            DISCIPLINA_ID INTEGER NOT NULL,
            PRIMARY KEY (MATRICULA, DISCIPLINA_ID),
            FOREIGN KEY (MATRICULA)     REFERENCES ALUNO(MATRICULA),
            FOREIGN KEY (DISCIPLINA_ID) REFERENCES DISCIPLINA(ID)
        );
    """)
    conn.commit()
    conn.close()

# ──────────────────────────────────────────────
# PERSISTÊNCIA JSON
# ──────────────────────────────────────────────
def export_json():
    conn = get_conn()
    c = conn.cursor()
    data = {
        "alunos":      [dict(zip(["matricula","nome","dt_nascimento"], r))
                        for r in c.execute("SELECT * FROM ALUNO")],
        "disciplinas": [dict(zip(["id","nome","turno","sala","professor"], r))
                        for r in c.execute("SELECT * FROM DISCIPLINA")],
        "notas":       [dict(zip(["valor","matricula","disciplina_id"], r))
                        for r in c.execute("SELECT * FROM NOTA")],
    }
    conn.close()
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ──────────────────────────────────────────────
# HELPERS DE UI
# ──────────────────────────────────────────────
CORES = {
    "bg":       "#1e1e2e",
    "surface":  "#2a2a3e",
    "accent":   "#7c3aed",
    "accent2":  "#a855f7",
    "success":  "#10b981",
    "danger":   "#ef4444",
    "text":     "#e2e8f0",
    "subtext":  "#94a3b8",
    "border":   "#3f3f5a",
    "entry_bg": "#16162a",
}

def styled_button(parent, text, command, color=None, **kw):
    color = color or CORES["accent"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white", relief="flat",
        font=("Segoe UI", 9, "bold"),
        padx=12, pady=6, cursor="hand2",
        activebackground=CORES["accent2"], activeforeground="white",
        **kw
    )
    return btn

def label_entry(parent, text, row, var=None, width=30):
    tk.Label(parent, text=text, bg=CORES["surface"], fg=CORES["subtext"],
             font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=4, padx=8)
    e = tk.Entry(parent, textvariable=var, width=width,
                 bg=CORES["entry_bg"], fg=CORES["text"],
                 insertbackground=CORES["text"], relief="flat",
                 font=("Segoe UI", 10), bd=4)
    e.grid(row=row, column=1, pady=4, padx=8, sticky="ew")
    return e

def label_combo(parent, text, row, values, var=None, width=28):
    tk.Label(parent, text=text, bg=CORES["surface"], fg=CORES["subtext"],
             font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=4, padx=8)
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      width=width, state="readonly", font=("Segoe UI", 10))
    cb.grid(row=row, column=1, pady=4, padx=8, sticky="ew")
    return cb

def make_treeview(parent, cols, col_names, heights=12):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=CORES["surface"],
                    foreground=CORES["text"],
                    fieldbackground=CORES["surface"],
                    rowheight=26,
                    font=("Segoe UI", 9))
    style.configure("Custom.Treeview.Heading",
                    background=CORES["accent"],
                    foreground="white",
                    font=("Segoe UI", 9, "bold"))
    style.map("Custom.Treeview", background=[("selected", CORES["accent2"])])

    frame = tk.Frame(parent, bg=CORES["bg"])
    frame.pack(fill="both", expand=True, padx=10, pady=6)

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")
    tree = ttk.Treeview(frame, columns=cols, show="headings",
                        height=heights, style="Custom.Treeview",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    for col, name in zip(cols, col_names):
        tree.heading(col, text=name)
        tree.column(col, width=140, anchor="center")
    return tree

# ──────────────────────────────────────────────
# ABA ALUNO
# ──────────────────────────────────────────────
class AbaAluno(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=CORES["bg"])
        self._build()
        self.refresh()

    def _build(self):
        # ── Formulário
        form = tk.LabelFrame(self, text=" Dados do Aluno ", bg=CORES["surface"],
                             fg=CORES["accent2"], font=("Segoe UI", 10, "bold"),
                             bd=1, relief="groove", labelanchor="nw")
        form.pack(fill="x", padx=10, pady=(10, 4))
        form.columnconfigure(1, weight=1)

        self.v_mat  = tk.StringVar()
        self.v_nome = tk.StringVar()
        self.v_dt   = tk.StringVar()

        label_entry(form, "Matrícula *",       0, self.v_mat)
        label_entry(form, "Nome *",            1, self.v_nome)
        label_entry(form, "Dt. Nascimento *\n(DD/MM/AAAA)", 2, self.v_dt)

        # ── Botões
        btn_frame = tk.Frame(self, bg=CORES["bg"])
        btn_frame.pack(fill="x", padx=10, pady=4)

        styled_button(btn_frame, "➕ Incluir",  self.incluir,  CORES["success"]).pack(side="left", padx=4)
        styled_button(btn_frame, "✏️ Alterar",  self.alterar,  CORES["accent"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑️ Excluir",  self.excluir,  CORES["danger"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Limpar",   self.limpar,   CORES["border"]).pack(side="left", padx=4)

        # ── Treeview
        self.tree = make_treeview(self,
            cols=("mat", "nome", "dt"),
            col_names=("Matrícula", "Nome", "Dt. Nascimento"))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_conn()
        for r in conn.execute("SELECT MATRICULA, NOME, DT_NASCIMENTO FROM ALUNO ORDER BY NOME"):
            self.tree.insert("", "end", values=r)
        conn.close()
        export_json()

    def _on_select(self, _=None):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])["values"]
        self.v_mat.set(v[0]); self.v_nome.set(v[1]); self.v_dt.set(v[2])

    def _validate(self):
        if not self.v_mat.get().strip():
            messagebox.showwarning("Atenção", "Matrícula é obrigatória."); return False
        if not self.v_nome.get().strip():
            messagebox.showwarning("Atenção", "Nome é obrigatório."); return False
        try:
            datetime.strptime(self.v_dt.get().strip(), "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Atenção", "Data inválida. Use DD/MM/AAAA."); return False
        return True

    def incluir(self):
        if not self._validate(): return
        try:
            conn = get_conn()
            conn.execute("INSERT INTO ALUNO VALUES (?,?,?)",
                         (self.v_mat.get().strip(), self.v_nome.get().strip(), self.v_dt.get().strip()))
            conn.commit(); conn.close()
            self.refresh(); self.limpar()
            messagebox.showinfo("Sucesso", "Aluno incluído com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Matrícula já cadastrada.")

    def alterar(self):
        if not self._validate(): return
        conn = get_conn()
        conn.execute("UPDATE ALUNO SET NOME=?, DT_NASCIMENTO=? WHERE MATRICULA=?",
                     (self.v_nome.get().strip(), self.v_dt.get().strip(), self.v_mat.get().strip()))
        conn.commit(); conn.close()
        self.refresh()
        messagebox.showinfo("Sucesso", "Aluno alterado com sucesso!")

    def excluir(self):
        mat = self.v_mat.get().strip()
        if not mat:
            messagebox.showwarning("Atenção", "Selecione um aluno."); return
        if not messagebox.askyesno("Confirmar", f"Excluir aluno {mat}?"):
            return
        conn = get_conn()
        conn.execute("DELETE FROM NOTA  WHERE MATRICULA=?", (mat,))
        conn.execute("DELETE FROM ALUNO WHERE MATRICULA=?", (mat,))
        conn.commit(); conn.close()
        self.refresh(); self.limpar()
        messagebox.showinfo("Sucesso", "Aluno excluído.")

    def limpar(self):
        self.v_mat.set(""); self.v_nome.set(""); self.v_dt.set("")

# ──────────────────────────────────────────────
# ABA DISCIPLINA
# ──────────────────────────────────────────────
class AbaDisciplina(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=CORES["bg"])
        self._build()
        self.refresh()

    def _build(self):
        form = tk.LabelFrame(self, text=" Dados da Disciplina ", bg=CORES["surface"],
                             fg=CORES["accent2"], font=("Segoe UI", 10, "bold"),
                             bd=1, relief="groove", labelanchor="nw")
        form.pack(fill="x", padx=10, pady=(10, 4))
        form.columnconfigure(1, weight=1)

        self.v_id   = tk.StringVar()
        self.v_nome = tk.StringVar()
        self.v_turno = tk.StringVar()
        self.v_sala  = tk.StringVar()
        self.v_prof  = tk.StringVar()

        label_entry(form, "ID (auto)",   0, self.v_id)
        label_entry(form, "Nome *",      1, self.v_nome)
        label_combo(form, "Turno *",     2, ["Manhã","Tarde","Noite"], self.v_turno)
        label_entry(form, "Sala *",      3, self.v_sala)
        label_entry(form, "Professor *", 4, self.v_prof)

        btn_frame = tk.Frame(self, bg=CORES["bg"])
        btn_frame.pack(fill="x", padx=10, pady=4)

        styled_button(btn_frame, "➕ Incluir",  self.incluir,  CORES["success"]).pack(side="left", padx=4)
        styled_button(btn_frame, "✏️ Alterar",  self.alterar,  CORES["accent"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑️ Excluir",  self.excluir,  CORES["danger"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Limpar",   self.limpar,   CORES["border"]).pack(side="left", padx=4)

        self.tree = make_treeview(self,
            cols=("id","nome","turno","sala","prof"),
            col_names=("ID","Nome","Turno","Sala","Professor"))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def refresh(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        conn = get_conn()
        for r in conn.execute("SELECT ID,NOME,TURNO,SALA,PROFESSOR FROM DISCIPLINA ORDER BY NOME"):
            self.tree.insert("", "end", values=r)
        conn.close(); export_json()

    def _on_select(self, _=None):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0])["values"]
        self.v_id.set(v[0]); self.v_nome.set(v[1]); self.v_turno.set(v[2])
        self.v_sala.set(v[3]); self.v_prof.set(v[4])

    def _validate(self):
        if not self.v_nome.get().strip():
            messagebox.showwarning("Atenção", "Nome é obrigatório."); return False
        if not self.v_turno.get():
            messagebox.showwarning("Atenção", "Selecione o turno."); return False
        if not self.v_sala.get().strip():
            messagebox.showwarning("Atenção", "Sala é obrigatória."); return False
        if not self.v_prof.get().strip():
            messagebox.showwarning("Atenção", "Professor é obrigatório."); return False
        return True

    def incluir(self):
        if not self._validate(): return
        conn = get_conn()
        conn.execute("INSERT INTO DISCIPLINA (NOME,TURNO,SALA,PROFESSOR) VALUES (?,?,?,?)",
                     (self.v_nome.get().strip(), self.v_turno.get(),
                      self.v_sala.get().strip(), self.v_prof.get().strip()))
        conn.commit(); conn.close()
        self.refresh(); self.limpar()
        messagebox.showinfo("Sucesso", "Disciplina incluída!")

    def alterar(self):
        if not self.v_id.get():
            messagebox.showwarning("Atenção", "Selecione uma disciplina."); return
        if not self._validate(): return
        conn = get_conn()
        conn.execute("UPDATE DISCIPLINA SET NOME=?,TURNO=?,SALA=?,PROFESSOR=? WHERE ID=?",
                     (self.v_nome.get().strip(), self.v_turno.get(),
                      self.v_sala.get().strip(), self.v_prof.get().strip(), self.v_id.get()))
        conn.commit(); conn.close()
        self.refresh()
        messagebox.showinfo("Sucesso", "Disciplina alterada!")

    def excluir(self):
        if not self.v_id.get():
            messagebox.showwarning("Atenção", "Selecione uma disciplina."); return
        if not messagebox.askyesno("Confirmar", "Excluir esta disciplina?"):
            return
        conn = get_conn()
        conn.execute("DELETE FROM NOTA        WHERE DISCIPLINA_ID=?", (self.v_id.get(),))
        conn.execute("DELETE FROM DISCIPLINA  WHERE ID=?", (self.v_id.get(),))
        conn.commit(); conn.close()
        self.refresh(); self.limpar()
        messagebox.showinfo("Sucesso", "Disciplina excluída.")

    def limpar(self):
        self.v_id.set(""); self.v_nome.set(""); self.v_turno.set("")
        self.v_sala.set(""); self.v_prof.set("")

# ──────────────────────────────────────────────
# ABA NOTA
# ──────────────────────────────────────────────
class AbaNota(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=CORES["bg"])
        self._build()
        self.refresh()

    def _get_alunos(self):
        conn = get_conn()
        rows = conn.execute("SELECT MATRICULA, NOME FROM ALUNO ORDER BY NOME").fetchall()
        conn.close()
        return rows

    def _get_disciplinas(self):
        conn = get_conn()
        rows = conn.execute("SELECT ID, NOME FROM DISCIPLINA ORDER BY NOME").fetchall()
        conn.close()
        return rows

    def _build(self):
        form = tk.LabelFrame(self, text=" Lançamento de Nota ", bg=CORES["surface"],
                             fg=CORES["accent2"], font=("Segoe UI", 10, "bold"),
                             bd=1, relief="groove", labelanchor="nw")
        form.pack(fill="x", padx=10, pady=(10, 4))
        form.columnconfigure(1, weight=1)

        self.v_aluno = tk.StringVar()
        self.v_disc  = tk.StringVar()
        self.v_valor = tk.StringVar()

        self.aluno_data = self._get_alunos()
        self.disc_data  = self._get_disciplinas()

        label_combo(form, "Aluno *",       0,
                    [f"{m} – {n}" for m,n in self.aluno_data], self.v_aluno)
        label_combo(form, "Disciplina *",  1,
                    [f"{i} – {n}" for i,n in self.disc_data],  self.v_disc)
        label_entry(form, "Valor (0-10) *", 2, self.v_valor)

        btn_frame = tk.Frame(self, bg=CORES["bg"])
        btn_frame.pack(fill="x", padx=10, pady=4)

        styled_button(btn_frame, "➕ Incluir",  self.incluir,  CORES["success"]).pack(side="left", padx=4)
        styled_button(btn_frame, "✏️ Alterar",  self.alterar,  CORES["accent"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑️ Excluir",  self.excluir,  CORES["danger"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Atualizar listas", self._reload_combos, CORES["border"]).pack(side="left", padx=4)

        self.tree = make_treeview(self,
            cols=("mat","aluno","disc","valor"),
            col_names=("Matrícula","Aluno","Disciplina","Nota"))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _reload_combos(self):
        self.aluno_data = self._get_alunos()
        self.disc_data  = self._get_disciplinas()
        # Atualiza os widgets Combobox
        for widget in self.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox):
                        if "–" in (child.get() or ""):
                            pass
        # Re-build rápido: destrói e reconstrói
        for w in self.winfo_children():
            w.destroy()
        self._build()
        self.refresh()

    def refresh(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        conn = get_conn()
        sql = """
            SELECT N.MATRICULA, A.NOME, D.NOME, N.VALOR
            FROM NOTA N
            JOIN ALUNO A      ON A.MATRICULA    = N.MATRICULA
            JOIN DISCIPLINA D ON D.ID           = N.DISCIPLINA_ID
            ORDER BY A.NOME, D.NOME
        """
        for r in conn.execute(sql):
            self.tree.insert("", "end", values=r)
        conn.close(); export_json()

    def _on_select(self, _=None):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0])["values"]
        mat, aluno_nome, disc_nome, valor = v
        # Setar combo aluno
        for m, n in self.aluno_data:
            if m == mat:
                self.v_aluno.set(f"{m} – {n}"); break
        # Setar combo disciplina
        conn = get_conn()
        d_id = conn.execute("SELECT ID FROM DISCIPLINA WHERE NOME=?", (disc_nome,)).fetchone()
        conn.close()
        if d_id:
            self.v_disc.set(f"{d_id[0]} – {disc_nome}")
        self.v_valor.set(str(valor))

    def _parse_sel(self):
        a = self.v_aluno.get()
        d = self.v_disc.get()
        if not a or not d:
            messagebox.showwarning("Atenção", "Selecione aluno e disciplina."); return None, None
        mat   = a.split(" – ")[0].strip()
        disc_id = d.split(" – ")[0].strip()
        return mat, disc_id

    def _parse_valor(self):
        try:
            v = float(self.v_valor.get().replace(",","."))
            if not 0 <= v <= 10:
                raise ValueError
            return v
        except ValueError:
            messagebox.showwarning("Atenção", "Nota deve ser um número entre 0 e 10.")
            return None

    def incluir(self):
        mat, disc_id = self._parse_sel()
        if mat is None: return
        valor = self._parse_valor()
        if valor is None: return
        try:
            conn = get_conn()
            conn.execute("INSERT INTO NOTA VALUES (?,?,?)", (valor, mat, disc_id))
            conn.commit(); conn.close()
            self.refresh()
            messagebox.showinfo("Sucesso", "Nota incluída!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nota já cadastrada para este aluno/disciplina. Use Alterar.")

    def alterar(self):
        mat, disc_id = self._parse_sel()
        if mat is None: return
        valor = self._parse_valor()
        if valor is None: return
        conn = get_conn()
        conn.execute("UPDATE NOTA SET VALOR=? WHERE MATRICULA=? AND DISCIPLINA_ID=?",
                     (valor, mat, disc_id))
        conn.commit(); conn.close()
        self.refresh()
        messagebox.showinfo("Sucesso", "Nota alterada!")

    def excluir(self):
        mat, disc_id = self._parse_sel()
        if mat is None: return
        if not messagebox.askyesno("Confirmar", "Excluir esta nota?"): return
        conn = get_conn()
        conn.execute("DELETE FROM NOTA WHERE MATRICULA=? AND DISCIPLINA_ID=?", (mat, disc_id))
        conn.commit(); conn.close()
        self.refresh()
        messagebox.showinfo("Sucesso", "Nota excluída.")

# ──────────────────────────────────────────────
# JANELA PRINCIPAL
# ──────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro de Alunos – Estácio")
        self.geometry("820x600")
        self.configure(bg=CORES["bg"])
        self.resizable(True, True)
        init_db()
        self._build_ui()

    def _build_ui(self):
        # ── Header
        header = tk.Frame(self, bg=CORES["accent"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🎓  Sistema de Cadastro de Alunos",
                 bg=CORES["accent"], fg="white",
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(header, text="Estácio", bg=CORES["accent"], fg="#d8b4fe",
                 font=("Segoe UI", 10)).pack(side="right", padx=20)

        # ── Notebook
        style = ttk.Style()
        style.configure("TNotebook",         background=CORES["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",     background=CORES["surface"],
                        foreground=CORES["subtext"],
                        font=("Segoe UI", 10, "bold"), padding=[14,6])
        style.map("TNotebook.Tab",
                  background=[("selected", CORES["accent"])],
                  foreground=[("selected", "white")])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.aba_aluno      = AbaAluno(nb)
        self.aba_disciplina = AbaDisciplina(nb)
        self.aba_nota       = AbaNota(nb)

        nb.add(self.aba_aluno,      text="  👤 Alunos  ")
        nb.add(self.aba_disciplina, text="  📚 Disciplinas  ")
        nb.add(self.aba_nota,       text="  📝 Notas  ")

        # ── Status bar
        status = tk.Frame(self, bg=CORES["surface"], height=24)
        status.pack(fill="x", side="bottom")
        tk.Label(status, text=f"💾 Banco: {DB_FILE}   |   📄 Backup JSON: {JSON_FILE}",
                 bg=CORES["surface"], fg=CORES["subtext"],
                 font=("Segoe UI", 8)).pack(side="left", padx=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()

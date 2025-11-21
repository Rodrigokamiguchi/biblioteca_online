# tela.py
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, timedelta
import pandas as pd

# -------------------------
# Config / Cores / Consts
# -------------------------
SIDEBAR_BG = "#2E3B55"    # cinza escuro azulado
SIDEBAR_BTN_BG = "#3A4A6A"
PRINCIPAL_BG = "#FFFFFF"
BTN_OK_BG = "#1976D2"     # azul
BTN_REPORT_BG = "#9C27B0"  # roxo para relatórios
TOOLTIP_BG = "#FFFFFF"
TOOLTIP_FG = "#333333"
TOOLTIP_DELAY = 400  # ms

# -------------------------
# Helper: PlaceholderEntry
# -------------------------
class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg = self['fg'] if 'fg' in self.keys() else 'black'
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, END)
            self['fg'] = self.default_fg

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

# -------------------------
# Tooltip class (discreto e moderno)
# -------------------------
class Tooltip:
    def __init__(self, widget, text, delay=TOOLTIP_DELAY):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._id = None
        self.tw = None
        widget.bind("<Enter>", self._on_enter, add='+')
        widget.bind("<Leave>", self._on_leave, add='+')
        widget.bind("<ButtonPress>", self._on_leave, add='+')

    def _on_enter(self, event=None):
        self._schedule()

    def _on_leave(self, event=None):
        self._unschedule()
        self._hide()

    def _schedule(self):
        self._unschedule()
        self._id = self.widget.after(self.delay, self._show)

    def _unschedule(self):
        if self._id:
            try:
                self.widget.after_cancel(self._id)
            except Exception:
                pass
            self._id = None

    def _show(self):
        if self.tw:
            return
        # create tooltip window
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        frm = Frame(self.tw, bg=TOOLTIP_BG, bd=1, relief=SOLID)
        frm.pack()
        lbl = Label(frm, text=self.text, justify=LEFT, bg=TOOLTIP_BG, fg=TOOLTIP_FG,
                    font=("Arial", 9), wraplength=300)
        lbl.pack(padx=8, pady=6)

    def _hide(self):
        if self.tw:
            try:
                self.tw.destroy()
            except Exception:
                pass
            self.tw = None

# -------------------------
# Banco de Dados e esquema
# -------------------------
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    sobrenome TEXT,
    endereco TEXT,
    email TEXT,
    telefone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    autor TEXT,
    editora TEXT,
    ano INTEGER,
    isbn TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    id_livro INTEGER,
    data_emprestimo TEXT,
    data_limite TEXT,
    data_devolucao TEXT,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY(id_livro) REFERENCES livros(id)
)
""")
conn.commit()

# add 'status' column to livros if missing (Disponível / Emprestado)
def ensure_livros_status_column():
    cursor.execute("PRAGMA table_info(livros)")
    cols = [r[1] for r in cursor.fetchall()]
    if "status" not in cols:
        cursor.execute("ALTER TABLE livros ADD COLUMN status TEXT DEFAULT 'Disponível'")
        conn.commit()

ensure_livros_status_column()

# -------------------------
# Funções DB básicas
# -------------------------
def get_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    return cursor.fetchall()

def get_livros():
    cursor.execute("SELECT id, titulo, autor, editora, ano, isbn, status FROM livros")
    return cursor.fetchall()

def get_emprestimos_all():
    cursor.execute("""
    SELECT e.id, l.titulo, u.nome || ' ' || u.sobrenome AS usuario,
           e.data_emprestimo, e.data_limite, e.data_devolucao
    FROM emprestimos e
    JOIN livros l ON e.id_livro = l.id
    JOIN usuarios u ON e.id_usuario = u.id
    """)
    return cursor.fetchall()

# -------------------------
# Utilidades de data
# -------------------------
def parse_date_flexible(s):
    if not s:
        return None
    s = str(s).strip()
    formatos = [
        "%Y-%m-%d", "%Y/%m/%d",
        "%d-%m-%Y", "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S",
        "%d-%m-%y", "%d/%m/%y"
    ]
    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    parts = None
    if "/" in s:
        parts = s.split()[0].split("/")
    elif "-" in s:
        parts = s.split()[0].split("-")
    if parts and len(parts) == 3:
        try:
            # heuristic: dd/mm/yyyy vs yyyy/mm/dd
            if len(parts[0]) <= 2:
                d = int(parts[0]); m = int(parts[1]); y = int(parts[2])
            else:
                y = int(parts[0]); m = int(parts[1]); d = int(parts[2])
            return date(y, m, d)
        except Exception:
            return None
    return None

# -------------------------
# UI helpers
# -------------------------
def limpar_frame():
    for w in frameDireita.winfo_children():
        w.destroy()

def botao_hover(widget, color_on="#5670A8", color_off=None):
    if color_off is None:
        color_off = widget['bg']
    def on(e): widget.config(bg=color_on)
    def off(e): widget.config(bg=color_off)
    widget.bind("<Enter>", on)
    widget.bind("<Leave>", off)

def show_help_box(title, text):
    messagebox.showinfo(title, text)

# -------------------------
# Telas / Ações
# -------------------------
def tela_inicio():
    limpar_frame()
    lbl_title = Label(frameDireita, text="📊 Painel de Controle", font=("Verdana", 16, "bold"), bg=PRINCIPAL_BG)
    lbl_title.pack(pady=12)
    cursor.execute("SELECT COUNT(*) FROM usuarios"); total_usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM livros"); total_livros = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE data_devolucao IS NULL"); total_emprestados = cursor.fetchone()[0]
    Label(frameDireita, text=f"Usuários cadastrados: {total_usuarios}", font=("Arial",12), bg=PRINCIPAL_BG).pack(pady=4)
    Label(frameDireita, text=f"Livros cadastrados: {total_livros}", font=("Arial",12), bg=PRINCIPAL_BG).pack(pady=4)
    Label(frameDireita, text=f"Livros atualmente emprestados: {total_emprestados}", font=("Arial",12), bg=PRINCIPAL_BG).pack(pady=4)

    # Checar se há atrasados - mostra aviso resumido
    cursor.execute("""
    SELECT e.id, l.titulo, u.nome || ' ' || u.sobrenome AS usuario, e.data_limite
    FROM emprestimos e
    JOIN livros l ON e.id_livro = l.id
    JOIN usuarios u ON e.id_usuario = u.id
    WHERE e.data_devolucao IS NULL
    """)
    rows = cursor.fetchall()
    hoje = date.today()
    atrasos = []
    for idemp, titulo, usuario, data_lim in rows:
        dt_lim = parse_date_flexible(data_lim)
        if dt_lim and hoje > dt_lim:
            dias = (hoje - dt_lim).days
            atrasos.append(f"{titulo} — {usuario} ({dias} dia(s) atrasado)")

    if atrasos:
        aviso_frame = Frame(frameDireita, bd=1, relief=SOLID, padx=8, pady=8, bg="#fff6f6")
        aviso_frame.pack(pady=10, fill=X, padx=12)
        Label(aviso_frame, text="⚠️ Atrasos detectados:", font=("Arial",12,"bold"), bg="#fff6f6").pack(anchor="w")
        for a in atrasos[:3]:
            Label(aviso_frame, text=a, anchor="w", bg="#fff6f6").pack(fill=X)
        if len(atrasos) > 3:
            Label(aviso_frame, text=f"... e mais {len(atrasos)-3} atraso(s). Verifique em 'Atrasos'.", bg="#fff6f6").pack(anchor="w")

# ---- Usuários ----
def tela_novo_usuario():
    limpar_frame()
    Label(frameDireita, text="👤 Novo Usuário", font=("Verdana", 14, "bold"), bg=PRINCIPAL_BG).pack(pady=8)

    def make_row(parent, placeholder, help_text):
        row = Frame(parent, bg=PRINCIPAL_BG); row.pack(fill=X, pady=3, padx=8)
        ent = PlaceholderEntry(row, placeholder=placeholder)
        ent.pack(side=LEFT, fill=X, expand=True)
        # tooltip on entry
        Tooltip(ent, help_text)
        return ent

    e_nome = make_row(frameDireita, "Nome", "Digite o primeiro nome do usuário. Ex: João")
    e_sob = make_row(frameDireita, "Sobrenome", "Digite o sobrenome do usuário. Ex: Silva")
    e_end = make_row(frameDireita, "Endereço", "Endereço opcional. Ex: Rua A, 123")
    e_email = make_row(frameDireita, "Email", "Email opcional. Ex: usuario@dominio.com")
    e_tel = make_row(frameDireita, "Telefone", "Telefone opcional. Ex: 11999998888")

    def salvar():
        nome = e_nome.get().strip()
        sobrenome = e_sob.get().strip()
        endereco = e_end.get().strip()
        email = e_email.get().strip()
        telefone = e_tel.get().strip()
        placeholders = {e_nome.placeholder, e_sob.placeholder, e_end.placeholder, e_email.placeholder, e_tel.placeholder}
        vals = [nome, sobrenome, endereco, email, telefone]
        vals = [None if v in placeholders or v == "" else v for v in vals]
        if not vals[0] or not vals[1]:
            messagebox.showwarning("Erro", "Nome e Sobrenome são obrigatórios.")
            return
        cursor.execute("INSERT INTO usuarios (nome,sobrenome,endereco,email,telefone) VALUES (?,?,?,?,?)", tuple(vals))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário adicionado.")
        tela_inicio()

    Button(frameDireita, text="Salvar", command=salvar, bg=BTN_OK_BG, fg="white").pack(pady=8)

def tela_ver_usuarios():
    limpar_frame()
    Label(frameDireita, text="📋 Usuários", font=("Verdana", 14, "bold"), bg=PRINCIPAL_BG).pack(pady=8)

    cols = ("ID","Nome","Sobrenome","Endereço","Email","Telefone")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=8, pady=6)
    for u in get_usuarios():
        tree.insert("", END, values=u)

    frame_rel = Frame(frameDireita, bg=PRINCIPAL_BG); frame_rel.pack(pady=6)
    id_entry = PlaceholderEntry(frame_rel, placeholder="ID do Usuário"); id_entry.grid(row=0, column=0, padx=3)
    Tooltip(id_entry, "Informe o ID numérico do usuário que aparece na tabela.")
    name_entry = PlaceholderEntry(frame_rel, placeholder="Ou digite o nome do usuário (opcional)"); name_entry.grid(row=0, column=1, padx=3)
    Tooltip(name_entry, "Digite parte do nome ou sobrenome para buscar.")

    def gerar():
        idv = id_entry.get().strip()
        namev = name_entry.get().strip()
        if idv and idv.isdigit():
            gerar_relatorio_usuario_por_id(int(idv))
        elif namev and namev != name_entry.placeholder:
            gerar_relatorio_usuario_por_nome(namev)
        else:
            messagebox.showwarning("Erro", "Informe ID válido ou nome do usuário.")

    def remover_selecionado():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Erro", "Selecione um usuário na tabela.")
            return
        vals = tree.item(sel[0], "values")
        uid = vals[0]
        if messagebox.askyesno("Confirmação", f"Remover usuário ID {uid}?"):
            cursor.execute("DELETE FROM usuarios WHERE id=?", (uid,))
            conn.commit()
            messagebox.showinfo("Removido", "Usuário removido.")
            tela_inicio()

    Button(frame_rel, text="Gerar Relatório (Excel)", command=gerar, bg=BTN_REPORT_BG, fg="white").grid(row=0, column=2, padx=6)
    Button(frame_rel, text="Remover Selecionado", command=remover_selecionado, bg="#E53935", fg="white").grid(row=0, column=3, padx=6)

# ---- Livros ----
def tela_novo_livro():
    limpar_frame()
    Label(frameDireita, text="📘 Novo Livro", font=("Verdana",14,"bold"), bg=PRINCIPAL_BG).pack(pady=8)

    def make_row(parent, placeholder, help_text):
        row = Frame(parent, bg=PRINCIPAL_BG); row.pack(fill=X, pady=3, padx=8)
        ent = PlaceholderEntry(row, placeholder=placeholder)
        ent.pack(side=LEFT, fill=X, expand=True)
        Tooltip(ent, help_text)
        return ent

    e_titulo = make_row(frameDireita, "Título", "Digite o título do livro.")
    e_autor = make_row(frameDireita, "Autor", "Nome do autor.")
    e_editora = make_row(frameDireita, "Editora", "Editora (opcional).")
    e_ano = make_row(frameDireita, "Ano", "Ano de publicação (somente números).")
    e_isbn = make_row(frameDireita, "ISBN", "ISBN codigo de numeração do livro padrão.")

    def salvar():
        titulo = e_titulo.get().strip()
        autor = e_autor.get().strip()
        editora = e_editora.get().strip()
        ano = e_ano.get().strip()
        isbn = e_isbn.get().strip()
        if titulo == "" or titulo == e_titulo.placeholder:
            messagebox.showwarning("Erro", "Título obrigatório.")
            return
        try:
            ano_int = int(ano) if ano and ano != e_ano.placeholder else None
        except:
            ano_int = None
        cursor.execute("INSERT INTO livros (titulo,autor,editora,ano,isbn,status) VALUES (?,?,?,?,?,?)",
                       (titulo, autor if autor != e_autor.placeholder else None,
                        editora if editora != e_editora.placeholder else None,
                        ano_int, isbn if isbn != e_isbn.placeholder else None, "Disponível"))
        conn.commit()
        messagebox.showinfo("Sucesso", "Livro adicionado.")
        tela_inicio()

    Button(frameDireita, text="Salvar", command=salvar, bg=BTN_OK_BG, fg="white").pack(pady=8)

def tela_ver_livros():
    limpar_frame()
    Label(frameDireita, text="📚 Livros", font=("Verdana",14,"bold"), bg=PRINCIPAL_BG).pack(pady=8)

    cols = ("ID","Título","Autor","Editora","Ano","ISBN","Status")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings", height=14)
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=8, pady=6)
    for l in get_livros():
        tree.insert("", END, values=l)

# ---- Empréstimos ----
def tela_emprestimo():
    limpar_frame()
    Label(frameDireita, text="🔁 Realizar Empréstimo", font=("Verdana",14,"bold"), bg=PRINCIPAL_BG).pack(pady=8)

    def make_row(parent, placeholder, help_text):
        row = Frame(parent, bg=PRINCIPAL_BG); row.pack(fill=X, pady=3, padx=8)
        ent = PlaceholderEntry(row, placeholder=placeholder)
        ent.pack(side=LEFT, fill=X, expand=True)
        Tooltip(ent, help_text)
        return ent

    e_id_usuario = make_row(frameDireita, "ID do Usuário", "Informe o ID numérico do usuário (visível na tabela de Usuários).")
    e_id_livro = make_row(frameDireita, "ID do Livro", "Informe o ID numérico do livro (visível na tabela de Livros).")
    e_prazo = make_row(frameDireita, "Prazo em dias (padrão 7)", "Quantos dias a pessoa pode ficar com o livro (padrão 7).")

    def salvar():
        idu = e_id_usuario.get().strip()
        idl = e_id_livro.get().strip()
        prazo_txt = e_prazo.get().strip()
        if not idu.isdigit() or not idl.isdigit():
            messagebox.showwarning("Erro", "Informe IDs numéricos válidos.")
            return
        # verifica usuário existe
        cursor.execute("SELECT id FROM usuarios WHERE id=?", (int(idu),))
        if not cursor.fetchone():
            messagebox.showwarning("Erro", "Usuário não encontrado.")
            return
        # verifica livro e disponibilidade
        cursor.execute("SELECT status FROM livros WHERE id=?", (int(idl),))
        r = cursor.fetchone()
        if not r:
            messagebox.showwarning("Erro", "Livro não encontrado.")
            return
        status_livro = r[0] if r[0] else "Disponível"
        if status_livro != "Disponível":
            messagebox.showwarning("Erro", f"Livro não disponível (status: {status_livro}).")
            return

        prazo = 7
        try:
            if prazo_txt and prazo_txt != e_prazo.placeholder:
                prazo = int(prazo_txt)
        except:
            prazo = 7
        data_emp = date.today()
        data_lim = data_emp + timedelta(days=prazo)
        cursor.execute("INSERT INTO emprestimos (id_usuario,id_livro,data_emprestimo,data_limite,data_devolucao) VALUES (?,?,?,?,NULL)",
                       (int(idu), int(idl), data_emp.strftime("%d-%m-%Y"), data_lim.strftime("%d-%m-%Y")))
        cursor.execute("UPDATE livros SET status=? WHERE id=?", ("Emprestado", int(idl)))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Empréstimo registrado. Devolver até {data_lim.strftime('%d-%m-%Y')}")
        tela_inicio()

    Button(frameDireita, text="Emprestar", command=salvar, bg=BTN_OK_BG, fg="white").pack(pady=8)

def tela_ver_emprestimos():
    limpar_frame()
    Label(frameDireita, text="📖 Empréstimos", font=("Verdana",14,"bold"), bg=PRINCIPAL_BG).pack(pady=8)

    cols = ("ID","Livro","Usuário","Data Empréstimo","Data Limite","Data Devolução","Status")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings", height=14)
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=8, pady=6)

    emprestimos = get_emprestimos_all()
    hoje = date.today()
    for e in emprestimos:
        idemp, titulo, usuario, data_emp, data_lim, data_dev = e
        dt_lim = parse_date_flexible(data_lim)
        status = "Emprestado" if (not data_dev or data_dev == "") else "Devolvido"
        if status == "Emprestado" and dt_lim and hoje > dt_lim:
            status_display = f"{status} (ATRASADO)"
        else:
            status_display = status
        tree.insert("", END, values=(idemp, titulo, usuario, data_emp, data_lim, data_dev if data_dev else "", status_display))

# ---- Devolução ----
def tela_devolucao():
    limpar_frame()
    Label(frameDireita, text="📦 Registrar Devolução", font=("Verdana",14,"bold"), bg=PRINCIPAL_BG).pack(pady=8)

    row = Frame(frameDireita, bg=PRINCIPAL_BG); row.pack(fill=X, pady=3, padx=8)
    e_id_emprestimo = PlaceholderEntry(row, placeholder="ID do Empréstimo"); e_id_emprestimo.pack(side=LEFT, fill=X, expand=True)
    Tooltip(e_id_emprestimo, "Informe o ID do empréstimo (visível na tabela de Empréstimos).")

    row2 = Frame(frameDireita, bg=PRINCIPAL_BG); row2.pack(fill=X, pady=3, padx=8)
    e_data_dev = PlaceholderEntry(row2, placeholder="Data de Devolução (DD-MM-AAAA) - opcional"); e_data_dev.pack(side=LEFT, fill=X, expand=True)
    Tooltip(e_data_dev, "Se não informar, será usada a data de hoje. Formato recomendado: DD-MM-AAAA.")

    def salvar_devolucao():
        idemp = e_id_emprestimo.get().strip()
        if not idemp.isdigit():
            messagebox.showwarning("Erro", "ID do empréstimo inválido.")
            return
        data_dev_txt = e_data_dev.get().strip()
        if not data_dev_txt or data_dev_txt == e_data_dev.placeholder:
            data_dev_txt = date.today().strftime("%d-%m-%Y")
        # verifica se existe e qual livro
        cursor.execute("SELECT id_livro, data_devolucao FROM emprestimos WHERE id=?", (int(idemp),))
        r = cursor.fetchone()
        if not r:
            messagebox.showwarning("Erro", "Empréstimo não encontrado.")
            return
        id_livro, existing_devolucao = r
        if existing_devolucao and existing_devolucao.strip() != "":
            messagebox.showinfo("Info", "Esse empréstimo já foi devolvido.")
            tela_inicio()
            return
        cursor.execute("UPDATE emprestimos SET data_devolucao=? WHERE id=?", (data_dev_txt, int(idemp)))
        # atualiza status do livro para Disponível
        cursor.execute("UPDATE livros SET status=? WHERE id=?", ("Disponível", int(id_livro)))
        conn.commit()
        messagebox.showinfo("Sucesso", "Devolução registrada e livro marcado como Disponível.")
        tela_inicio()

    Button(frameDireita, text="Registrar Devolução", command=salvar_devolucao, bg="#FFC107").pack(pady=8)

# ---- Verificar Atrasos (tela específica) ----
def verificar_atrasos():
    limpar_frame()
    Label(frameDireita, text="⏰ Atrasos", font=("Verdana",14,"bold"), bg=PRINCIPAL_BG).pack(pady=8)

    cols = ("ID","Livro","Usuário","Data Emprestimo","Data Limite","Atrasado?")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings", height=14)
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=8, pady=6)

    cursor.execute("""
    SELECT e.id, l.titulo, u.nome || ' ' || u.sobrenome AS usuario,
           e.data_emprestimo, e.data_limite
    FROM emprestimos e
    JOIN livros l ON e.id_livro = l.id
    JOIN usuarios u ON e.id_usuario = u.id
    WHERE e.data_devolucao IS NULL
    """)
    rows = cursor.fetchall()
    hoje = date.today()
    for idemp, titulo, usuario, data_emp, data_lim in rows:
        dt_lim = parse_date_flexible(data_lim)
        atrasado = dt_lim and hoje > dt_lim
        tree.insert("", END, values=(idemp, titulo, usuario, data_emp, data_lim, "SIM" if atrasado else "NÃO"))

# ---- Relatórios ----
def gerar_relatorio_usuario_por_id(id_usuario):
    cursor.execute("""
    SELECT u.nome || ' ' || u.sobrenome AS usuario,
           l.titulo, l.autor,
           e.data_emprestimo, e.data_limite, e.data_devolucao
    FROM emprestimos e
    JOIN usuarios u ON e.id_usuario = u.id
    JOIN livros l ON e.id_livro = l.id
    WHERE e.id_usuario = ?
    """, (id_usuario,))
    dados = cursor.fetchall()
    if not dados:
        messagebox.showinfo("Relatório", "Nenhum empréstimo encontrado para esse usuário.")
        return
    rows = []
    for usuario, titulo, autor, data_emp, data_lim, data_dev in dados:
        status = "Devolvido" if data_dev and data_dev.strip() != "" else "Emprestado"
        rows.append({
            "Usuário": usuario,
            "Título": titulo,
            "Autor": autor,
            "Data Empréstimo": data_emp,
            "Data Limite": data_lim,
            "Data Devolução": data_dev if data_dev else "",
            "Status": status
        })
    df = pd.DataFrame(rows)
    nome_usuario = dados[0][0].replace(" ", "_")
    fname = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=f"relatorio_{nome_usuario}.xlsx",
                                         filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if fname:
        df.to_excel(fname, index=False)
        messagebox.showinfo("Relatório", f"Relatório salvo como '{fname}'")
        tela_inicio()

def gerar_relatorio_usuario_por_nome(nome_usuario):
    cursor.execute("""
    SELECT u.id, u.nome || ' ' || u.sobrenome AS usuario
    FROM usuarios u
    WHERE (u.nome || ' ' || u.sobrenome) LIKE ?
    """, (f"%{nome_usuario}%",))
    found = cursor.fetchall()
    if not found:
        messagebox.showinfo("Relatório", "Nenhum usuário encontrado com esse nome.")
        return
    id_usuario = found[0][0]
    gerar_relatorio_usuario_por_id(id_usuario)

# -------------------------
# Janela principal / Layout
# -------------------------
janela = Tk()
janela.title("📚 Sistema de Biblioteca")
janela.geometry("1000x600")
janela.config(bg=PRINCIPAL_BG)

# frames
frameEsquerda = Frame(janela, width=220, bg=SIDEBAR_BG)
frameEsquerda.pack(side=LEFT, fill=Y)
frameDireita = Frame(janela, bg=PRINCIPAL_BG)
frameDireita.pack(side=RIGHT, fill=BOTH, expand=True)

# Botão util
def make_side_button(text, cmd, bg=SIDEBAR_BTN_BG):
    b = Button(frameEsquerda, text=text, command=cmd, bg=bg, fg="white", relief=FLAT, anchor="w", padx=12)
    b.pack(pady=6, padx=8, fill=X)
    botao_hover(b)
    return b

# menu lateral com emojis (ícones simples embutidos)
make_side_button("🏠  Dashboard", tela_inicio)
make_side_button("👤  Novo Usuário", tela_novo_usuario)
make_side_button("📋  Ver Usuários", tela_ver_usuarios)
make_side_button("📘  Novo Livro", tela_novo_livro)
make_side_button("📚  Ver Livros", tela_ver_livros)
make_side_button("🔁  Emprestar", tela_emprestimo)
make_side_button("📦  Devolução", tela_devolucao)
make_side_button("📖  Ver Empréstimos", tela_ver_emprestimos)
make_side_button("⏰  Atrasos", verificar_atrasos)

# inicializa na tela inicial
tela_inicio()

janela.mainloop()

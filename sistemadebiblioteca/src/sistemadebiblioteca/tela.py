# tela.py
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime, date, timedelta
import pandas as pd

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
        # Ao entrar no campo, limpa todo texto (placeholder ou não) para o usuário digitar
        self.delete(0, END)
        self['fg'] = self.default_fg

    def _add_placeholder(self, event=None):
        # Se vazio, coloca o placeholder
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

# -------------------------
# Banco de Dados
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

# -------------------------
# Funções DB básicas
# -------------------------
def get_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    return cursor.fetchall()

def get_livros():
    cursor.execute("SELECT * FROM livros")
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
# Utilidades de data (robusta)
# -------------------------
def parse_date_flexible(s):
    """Tenta converter string para date. Retorna date ou None."""
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
    # tentativa simples de normalizar "2025/5/1" -> "2025/05/01"
    parts = None
    if "/" in s:
        parts = s.split()[0].split("/")
    elif "-" in s:
        parts = s.split()[0].split("-")
    if parts and len(parts) == 3:
        try:
            y = int(parts[0]); m = int(parts[1]); d = int(parts[2])
            return date(y, m, d)
        except Exception:
            return None
    return None

# -------------------------
# Funções das telas
# -------------------------
def limpar_frame():
    for w in frameDireita.winfo_children():
        w.destroy()

# ---- Usuários ----
def tela_novo_usuario():
    limpar_frame()
    Label(frameDireita, text="Novo Usuário", font=("Verdana", 14, "bold")).pack(pady=8)

    e_nome = PlaceholderEntry(frameDireita, placeholder="Nome"); e_nome.pack(pady=3)
    e_sob = PlaceholderEntry(frameDireita, placeholder="Sobrenome"); e_sob.pack(pady=3)
    e_end = PlaceholderEntry(frameDireita, placeholder="Endereço"); e_end.pack(pady=3)
    e_email = PlaceholderEntry(frameDireita, placeholder="Email"); e_email.pack(pady=3)
    e_tel = PlaceholderEntry(frameDireita, placeholder="Telefone"); e_tel.pack(pady=3)

    def salvar():
        nome = e_nome.get().strip()
        sobrenome = e_sob.get().strip()
        endereco = e_end.get().strip()
        email = e_email.get().strip()
        telefone = e_tel.get().strip()
        # se placeholders não foram substituídos, eles estarão com o texto do placeholder; consideramos vazio
        placeholders = {e_nome.placeholder, e_sob.placeholder, e_end.placeholder, e_email.placeholder, e_tel.placeholder}
        vals = [nome, sobrenome, endereco, email, telefone]
        vals = [None if v in placeholders or v == "" else v for v in vals]
        if not vals[0] or not vals[1]:
            messagebox.showwarning("Erro", "Nome e Sobrenome são obrigatórios.")
            return
        cursor.execute("INSERT INTO usuarios (nome,sobrenome,endereco,email,telefone) VALUES (?,?,?,?,?)", tuple(vals))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário adicionado.")
        tela_ver_usuarios()

    Button(frameDireita, text="Salvar", command=salvar, bg="#4CAF50", fg="white").pack(pady=6)

def tela_ver_usuarios():
    limpar_frame()
    Label(frameDireita, text="Usuários", font=("Verdana", 14, "bold")).pack(pady=8)

    cols = ("ID","Nome","Sobrenome","Endereço","Email","Telefone")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)
    for u in get_usuarios():
        tree.insert("", END, values=u)

    # Gerar relatório por ID ou nome (o usuário pediu que o nome do arquivo seja o nome do usuário)
    frame_rel = Frame(frameDireita); frame_rel.pack(pady=6)
    id_entry = PlaceholderEntry(frame_rel, placeholder="ID do Usuário"); id_entry.grid(row=0, column=0, padx=3)
    name_entry = PlaceholderEntry(frame_rel, placeholder="Ou digite o nome do usuário (opcional)"); name_entry.grid(row=0, column=1, padx=3)

    def chamar_relatorio():
        idv = id_entry.get().strip()
        namev = name_entry.get().strip()
        # preferir ID se informado numericamente
        if idv and idv.isdigit():
            gerar_relatorio_usuario_por_id(int(idv))
        elif namev and namev != name_entry.placeholder:
            gerar_relatorio_usuario_por_nome(namev)
        else:
            messagebox.showwarning("Erro", "Informe ID válido ou nome do usuário.")

    Button(frame_rel, text="Gerar Relatório (Excel)", command=chamar_relatorio, bg="#9C27B0", fg="white").grid(row=0, column=2, padx=6)

# ---- Livros ----
def tela_novo_livro():
    limpar_frame()
    Label(frameDireita, text="Novo Livro", font=("Verdana",14,"bold")).pack(pady=8)

    e_titulo = PlaceholderEntry(frameDireita, placeholder="Título"); e_titulo.pack(pady=3)
    e_autor = PlaceholderEntry(frameDireita, placeholder="Autor"); e_autor.pack(pady=3)
    e_editora = PlaceholderEntry(frameDireita, placeholder="Editora"); e_editora.pack(pady=3)
    e_ano = PlaceholderEntry(frameDireita, placeholder="Ano"); e_ano.pack(pady=3)
    e_isbn = PlaceholderEntry(frameDireita, placeholder="ISBN"); e_isbn.pack(pady=3)

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
        cursor.execute("INSERT INTO livros (titulo,autor,editora,ano,isbn) VALUES (?,?,?,?,?)",
                       (titulo, autor if autor != e_autor.placeholder else None, editora if editora != e_editora.placeholder else None, ano_int, isbn if isbn != e_isbn.placeholder else None))
        conn.commit()
        messagebox.showinfo("Sucesso", "Livro adicionado.")
        tela_ver_livros()

    Button(frameDireita, text="Salvar", command=salvar, bg="#4CAF50", fg="white").pack(pady=6)

def tela_ver_livros():
    limpar_frame()
    Label(frameDireita, text="Livros", font=("Verdana",14,"bold")).pack(pady=8)

    cols = ("ID","Título","Autor","Editora","Ano","ISBN")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)
    for l in get_livros():
        tree.insert("", END, values=l)

# ---- Empréstimo ----
def tela_emprestimo():
    limpar_frame()
    Label(frameDireita, text="Realizar Empréstimo", font=("Verdana",14,"bold")).pack(pady=8)

    e_id_usuario = PlaceholderEntry(frameDireita, placeholder="ID do Usuário"); e_id_usuario.pack(pady=3)
    e_id_livro = PlaceholderEntry(frameDireita, placeholder="ID do Livro"); e_id_livro.pack(pady=3)
    e_prazo = PlaceholderEntry(frameDireita, placeholder="Prazo em dias (padrão 7)"); e_prazo.pack(pady=3)

    def salvar():
        idu = e_id_usuario.get().strip()
        idl = e_id_livro.get().strip()
        prazo_txt = e_prazo.get().strip()
        if not idu.isdigit() or not idl.isdigit():
            messagebox.showwarning("Erro", "Informe IDs numéricos válidos.")
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
                       (int(idu), int(idl), data_emp.strftime("%Y-%m-%d"), data_lim.strftime("%Y-%m-%d")))
        conn.commit()
        # marcar livro como emprestado (opcional: você também pode manter status na tabela livros)
        messagebox.showinfo("Sucesso", f"Empréstimo registrado. Devolver até {data_lim}")
        tela_ver_emprestimos()

    Button(frameDireita, text="Emprestar", command=salvar, bg="#2196F3", fg="white").pack(pady=6)

# ---- Devolução ----
def tela_devolucao():
    limpar_frame()
    Label(frameDireita, text="Registrar Devolução", font=("Verdana",14,"bold")).pack(pady=8)

    e_id_emprestimo = PlaceholderEntry(frameDireita, placeholder="ID do Empréstimo"); e_id_emprestimo.pack(pady=3)
    e_data_dev = PlaceholderEntry(frameDireita, placeholder="Data de Devolução (DD-MM-AAAA) - opcional"); e_data_dev.pack(pady=3)

    def salvar():
        idemp = e_id_emprestimo.get().strip()
        if not idemp.isdigit():
            messagebox.showwarning("Erro", "ID do empréstimo inválido.")
            return
        # se data não preenchida, usar hoje
        data_dev_txt = e_data_dev.get().strip()
        if not data_dev_txt or data_dev_txt == e_data_dev.placeholder:
            data_dev_txt = date.today().strftime("%d-%m-%Y")
        # atualizar
        cursor.execute("SELECT id_livro FROM emprestimos WHERE id=?", (int(idemp),))
        r = cursor.fetchone()
        if not r:
            messagebox.showwarning("Erro", "Empréstimo não encontrado.")
            return
        cursor.execute("UPDATE emprestimos SET data_devolucao=? WHERE id=?", (data_dev_txt, int(idemp)))
        conn.commit()
        messagebox.showinfo("Sucesso", "Devolução registrada.")
        tela_ver_emprestimos()

    Button(frameDireita, text="Registrar Devolução", command=salvar, bg="#FFC107").pack(pady=6)

# ---- Ver Empréstimos ----
def tela_ver_emprestimos():
    limpar_frame()
    Label(frameDireita, text="Empréstimos", font=("Verdana",14,"bold")).pack(pady=8)

    cols = ("ID","Livro","Usuário","Data Empréstimo","Data Limite","Data Devolução","Status")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)

    emprestimos = get_emprestimos_all()
    hoje = date.today()
    for e in emprestimos:
        idemp, titulo, usuario, data_emp, data_lim, data_dev = e
        dt_lim = parse_date_flexible(data_lim)
        dt_emp = parse_date_flexible(data_emp)
        status = "Emprestado" if (not data_dev or data_dev == "") else "Devolvido"
        # marcar atraso se emprestado e hoje > limite
        if status == "Emprestado" and dt_lim and hoje > dt_lim:
            status_display = f"{status} (ATRASADO)"
        else:
            status_display = status
        tree.insert("", END, values=(idemp, titulo, usuario, data_emp, data_lim, data_dev if data_dev else "", status_display))

# ---- Verificar Atrasos (apenas emprestados) ----
def verificar_atrasos():
    limpar_frame()
    Label(frameDireita, text="Empréstimos Emprestados (verificação de atraso)", font=("Verdana",14,"bold")).pack(pady=8)

    cols = ("ID","Livro","Usuário","Data Emprestimo","Data Limite","Atrasado?")
    tree = ttk.Treeview(frameDireita, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)

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
        atrasado = False
        if dt_lim and hoje > dt_lim:
            atrasado = True
        tree.insert("", END, values=(idemp, titulo, usuario, data_emp, data_lim, "SIM" if atrasado else "NÃO"))

# ---- Relatórios (Excel) ----
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
    # montar DataFrame incluindo status por linha
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
    # nome do arquivo usando o nome do usuário (limpo)
    nome_usuario = dados[0][0].replace(" ", "_")
    nome_arquivo = f"relatorio_{nome_usuario}.xlsx"
    df.to_excel(nome_arquivo, index=False)
    messagebox.showinfo("Relatório", f"Relatório salvo como '{nome_arquivo}'")

def gerar_relatorio_usuario_por_nome(nome_usuario):
    # buscar por correspondência
    cursor.execute("""
    SELECT u.id, u.nome || ' ' || u.sobrenome AS usuario
    FROM usuarios u
    WHERE (u.nome || ' ' || u.sobrenome) LIKE ?
    """, (f"%{nome_usuario}%",))
    found = cursor.fetchall()
    if not found:
        messagebox.showinfo("Relatório", "Nenhum usuário encontrado com esse nome.")
        return
    # se múltiplos encontrados, pegar primeiro (pode expandir)
    id_usuario = found[0][0]
    gerar_relatorio_usuario_por_id(id_usuario)

# -------------------------
# Interface Principal
# -------------------------
janela = Tk()
janela.title("📚 Sistema de Biblioteca")
janela.geometry("1000x600")
janela.config(bg="#e9edf5")

frameEsquerda = Frame(janela, width=220, bg="#333")
frameEsquerda.pack(side=LEFT, fill=Y)

frameDireita = Frame(janela, bg="#f7f7f7")
frameDireita.pack(side=RIGHT, fill=BOTH, expand=True)

# Carregar imagens dos botões (se não existirem, botão fica com texto)
def carregar_imagem(nome, tamanho=(20,20)):
    try:
        img = Image.open(nome)
        img = img.resize(tamanho, Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

imgs = {
    'usuario': carregar_imagem("pessoa.png"),
    'livro': carregar_imagem("livros.png"),
    'emprestimo': carregar_imagem("emprestado.png"),
    'devolver': carregar_imagem("devolver.png"),
    'atraso': carregar_imagem("atraso.png"),
    'relatorio': carregar_imagem("relatorio.png"),
}

# Botões laterais
def make_side_button(text, img, cmd):
    if img:
        b = Button(frameEsquerda, text="  "+text, image=img, compound=LEFT, anchor="w", command=cmd)
    else:
        b = Button(frameEsquerda, text=text, command=cmd)
    b.pack(pady=6, padx=6, fill=X)
    return b

make_side_button("Novo Usuário", imgs['usuario'], tela_novo_usuario)
make_side_button("Ver Usuários", imgs['usuario'], tela_ver_usuarios)
make_side_button("Novo Livro", imgs['livro'], tela_novo_livro)
make_side_button("Ver Livros", imgs['livro'], tela_ver_livros)
make_side_button("Emprestar", imgs['emprestimo'], tela_emprestimo)
make_side_button("Devolução", imgs['devolver'], tela_devolucao)
make_side_button("Ver Empréstimos", imgs['emprestimo'], tela_ver_emprestimos)
make_side_button("Atrasos (emprestados)", imgs['atraso'], verificar_atrasos)
make_side_button("Relatórios (por usuário)", imgs['relatorio'], tela_ver_usuarios)

# Tela inicial: mostra contadores
def tela_inicio():
    limpar_frame()
    Label(frameDireita, text="Painel Inicial", font=("Verdana", 16, "bold")).pack(pady=8)
    # contagens simples
    cursor.execute("SELECT COUNT(*) FROM usuarios"); total_usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM livros"); total_livros = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE data_devolucao IS NULL"); total_emprestados = cursor.fetchone()[0]
    Label(frameDireita, text=f"Usuários cadastrados: {total_usuarios}", font=("Arial",12)).pack(pady=4)
    Label(frameDireita, text=f"Livros cadastrados: {total_livros}", font=("Arial",12)).pack(pady=4)
    Label(frameDireita, text=f"Livros atualmente emprestados: {total_emprestados}", font=("Arial",12)).pack(pady=4)

tela_inicio()

janela.mainloop()

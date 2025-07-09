from tkinter import ttk
from tkinter .ttk import *
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import date
from datetime import datetime

# importando as funções da view
from view import *

# cores --------------------------------

co0 = "#2e2d2b" #Preta
co1 = "#feffff" #branca
co2 = "#4fa882" #verde
co3 = "#38576b" #valor
co4 = "#403d3d" #letra
co5 = "#e06636"
co6 = "#E9A178"
co7 = "#3fbfb9" #verde
co8 = "#263238" # + verde
co9 = "#e9edf5"
co10 = "#6e8faf"
co11 = "#f2f4f2"


# Criando janela ----------------------------
janela = Tk()
janela.title("")
janela.geometry("770x330")
janela.config(background=co1)
janela.resizable(width=FALSE, height=FALSE)

style = Style(janela)
style.theme_use("clam")

# Frames ------------------------------------

frameCima = Frame(janela, width=770, height=50, bg=co6, relief="flat")
frameCima.grid(row=0, column=0, columnspan=2, sticky=NSEW)

frameEsquerda = Frame(janela, width=150, height=265, bg=co4, relief="solid")
frameEsquerda.grid(row=1, column=0, sticky=NSEW)

frameDireita = Frame(janela, width=600, height=265, bg=co1, relief="solid")
frameDireita.grid(row=1, column=1, sticky=NSEW)


# Logo ---------------------------------------

# abrindo a imagem
app_img = Image.open('logo.png')
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, width=1000, compound=LEFT, padx=5, anchor=NW, bg=co6, fg=co1)
app_logo.place(x=5, y=0)

app = Label(frameCima, text="Gerenciamento de Livros", compound=LEFT, padx=5, anchor=NW, font=("Verdana 15 bold"), bg=co6, fg=co1)
app.place(x=50, y=7)

app_linha = Label(frameCima, width=770, height=1, padx=5, anchor=NW, font=("Verdana 1"), bg=co3, fg=co1)
app_linha.place(x=0, y=47)

# Novo Usuario
def novo_usuario():

    global img_salvar

    def add():
        first_name = e_nome.get()
        last_name = e_sobrenome.get()
        address = e_endereco.get()
        email = e_email.get()
        phone = e_telefone.get()

        lista = [first_name, last_name, address, email, phone]

        # Verificando caso algum campo esteja vazio
        for i in lista:
            if i == "":
                messagebox.showerror("Erro", "Prencha todos os campos")
                return
        # Inserindo os dados no banco de dados
        insert_users(first_name, last_name, address, email, phone)

        messagebox.showinfo("Sucesso", "Usuário inserido com sucesso")

        # limpando os campos de entradas
        e_nome.delete(0,END)
        e_sobrenome.delete(0,END)
        e_endereco.delete(0,END)
        e_email.delete(0,END)
        e_telefone.delete(0,END)

    app = Label(frameDireita, text=" Novo usuário", width=50, compound=LEFT, padx=5, pady=10, font=("Verdana 12"), bg=co1, fg=co4)
    app.grid(row=0, column=0, columnspan=4, sticky=NSEW)

    app_linha = Label(frameDireita, width=700, height=1, anchor=NW, font=("Verdana 1"), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=4, sticky=NSEW)

    l_nome = Label(frameDireita, text="Primeiro nome", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_nome.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

    e_nome = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_nome.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)

    l_sobrenome = Label(frameDireita, text="Sobrenome", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_sobrenome.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

    e_sobrenome = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_sobrenome.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)

    l_endereco = Label(frameDireita, text="Endereço do usuário", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_endereco.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)

    e_endereco = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_endereco.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

    l_email = Label(frameDireita, text="Email do usuário", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_email.grid(row=5, column=0, padx=5, pady=5, sticky=NSEW)

    e_email = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_email.grid(row=5, column=1, padx=5, pady=5, sticky=NSEW)

    l_telefone = Label(frameDireita, text="Telefone do usuário", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_telefone.grid(row=6, column=0, padx=5, pady=5, sticky=NSEW)

    e_telefone = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_telefone.grid(row=6, column=1, padx=5, pady=5, sticky=NSEW)  

    # Salvar
    img_salvar = Image.open('salvar.png')
    img_salvar = img_salvar.resize((18,18))
    img_salvar = ImageTk.PhotoImage(img_salvar)
    b_salvar = Button(frameDireita, command=add, image=img_salvar, compound=LEFT, anchor=NW, text=" Salvar Usuário", bg=co1, fg=co4, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
    b_salvar.grid(row=7, column=1, pady=5, sticky=NSEW) 

# Exbir Usuario
def ver_usuarios():

    app_ = Label(frameDireita,text="Todos os usuários",width=50,compound=LEFT, padx=5,pady=10, relief=FLAT, anchor=NW, font=('Verdana 12'),bg=co1, fg=co4)
    app_.grid(row=0, column=0, columnspan=3, sticky=NSEW)
    l_linha = Label(frameDireita, width=400, height=1,anchor=NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    dados = get_users()

    # creating a treeview with dual scrollbars
    list_header = ['ID', "Nome", "Endereço", "Email", "Telefone"]
    
    global tree

    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    
    # vertical scrollbar
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew')
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, sticky='ew')
    frameDireita.grid_rowconfigure(0, weight=12)

    hd=["nw","nw","nw","nw","nw","nw"]
    h=[20,80,80,120,120,76,100]
    n=0

    for col in list_header:
        tree.heading(col, text=col, anchor='nw')
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in dados:
        tree.insert('', 'end', values=item)

# Novo Livro
def novo_livro():

    global img_salvar

    def add():

        title = e_title.get()
        author = e_autor.get()
        publisher = e_editora.get()
        year = e_a_publicado.get()
        isbn = e_isbn.get()

        lista = [title, author, publisher, year, isbn]

         # Verificando caso algum campo esteja vazio
        for i in lista:
            if i == "":
                messagebox.showerror("Erro", "Prencha todos os campos")
                return
        # Inserindo os dados no banco de dados
        insert_book(title, author, publisher, year, isbn)

        messagebox.showinfo("Sucesso", "Livro inserido com sucesso")

        # limpando os campos de entradas
        e_title.delete(0,END)
        e_autor.delete(0,END)
        e_editora.delete(0,END)
        e_a_publicado.delete(0,END)
        e_isbn.delete(0,END)

    app = Label(frameDireita, text=" Inserir Novo Livro", width=50, compound=LEFT, padx=5, pady=10, font=("Verdana 12"), bg=co1, fg=co4)
    app.grid(row=0, column=0, columnspan=3, sticky=NSEW)

    app_linha = Label(frameDireita, width=700, height=1, anchor=NW, font=("Verdana 1"), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    l_title = Label(frameDireita, text="Título", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_title.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

    e_title = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_title.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)

    l_autor = Label(frameDireita, text="Autor", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_autor.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)

    e_autor = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_autor.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

    l_editora = Label(frameDireita, text="Editora", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_editora.grid(row=5, column=0, padx=5, pady=5, sticky=NSEW)

    e_editora = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_editora.grid(row=5, column=1, padx=5, pady=5, sticky=NSEW)

    l_a_publicado = Label(frameDireita, text="Ano Publicado", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_a_publicado.grid(row=6, column=0, padx=5, pady=5, sticky=NSEW)

    e_a_publicado = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_a_publicado.grid(row=6, column=1, padx=5, pady=5, sticky=NSEW)

    l_isbn = Label(frameDireita, text="ISBN", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_isbn.grid(row=7, column=0, padx=5, pady=5, sticky=NSEW)

    e_isbn = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_isbn.grid(row=7, column=1, padx=5, pady=5, sticky=NSEW)

    # Salvar
    img_salvar = Image.open('salvar.png')
    img_salvar = img_salvar.resize((18,18))
    img_salvar = ImageTk.PhotoImage(img_salvar)
    b_salvar = Button(frameDireita, command=add, image=img_salvar, compound=LEFT, anchor=NW, text=" Salvar Livro", bg=co1, fg=co4, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
    b_salvar.grid(row=8, column=1, pady=5, sticky=NSEW)

# Exibir Livros
def ver_livro():
     
    app_ = Label(frameDireita,text="Todos os Livros",width=50,compound=LEFT, padx=5,pady=10, relief=FLAT, anchor=NW, font=('Verdana 12'),bg=co1, fg=co4)
    app_.grid(row=0, column=0, columnspan=3, sticky=NSEW)
    l_linha = Label(frameDireita, width=400, height=1,anchor=NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    dados = exibir_livros()

    # creating a treeview with dual scrollbars
    list_header = ['ID', "Título", "Autor", "Editora", "Ano", "ISBN"]
    
    global tree

    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    
    # vertical scrollbar
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew')
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, sticky='ew')
    frameDireita.grid_rowconfigure(0, weight=12)

    hd=["nw","nw","nw","nw","nw","nw"]
    h=[20,165,110,100,50,50,100]
    n=0

    for col in list_header:
        tree.heading(col, text=col, anchor='nw')
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in dados:
        tree.insert('', 'end', values=item)

# Realizar emprestimo
def emprestar_livro():

    global img_salvar

    def add():
        user_id = e_id_usuario.get()
        book_id = e_id_livro.get()

        lista = [user_id, book_id]

        for i in lista:
            if i == "":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

        data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_loan(user_id, book_id, data_emprestimo, None)

        messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso")

        e_id_usuario.delete(0, END)
        e_id_livro.delete(0, END)

        

    app = Label(frameDireita, text=" Realizar um emprestimo", width=50, compound=LEFT, padx=5, pady=10, font=("Verdana 12"), bg=co1, fg=co4)
    app.grid(row=0, column=0, columnspan=3, sticky=NSEW)

    app_linha = Label(frameDireita, width=700, height=1, anchor=NW, font=("Verdana 1"), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    l_id_usuario = Label(frameDireita, text="ID do usuário", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_id_usuario.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

    e_id_usuario = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_id_usuario.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)

    l_id_livro = Label(frameDireita, text="ID do livro", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_id_livro.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)

    e_id_livro = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_id_livro.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

    
    # Salvar
    img_salvar = Image.open('salvar.png')
    img_salvar = img_salvar.resize((18,18))
    img_salvar = ImageTk.PhotoImage(img_salvar)
    b_salvar = Button(frameDireita, command=add, image=img_salvar, compound=LEFT, anchor=NW, text=" Emprestimo", bg=co1, fg=co4, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
    b_salvar.grid(row=8, column=1, pady=5, sticky=NSEW)

# Exibir livros emprestados
def mostrar_livro():
         
    app_ = Label(frameDireita,text="Livros Emprestados",width=50,compound=LEFT, padx=5,pady=10, relief=FLAT, anchor=NW, font=('Verdana 12'),bg=co1, fg=co4)
    app_.grid(row=0, column=0, columnspan=3, sticky=NSEW)
    
    l_linha = Label(frameDireita, width=400, height=1,anchor=NW, font=('Verdana 1 '), bg=co3, fg=co1)
    l_linha.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    dados =  []

    book_on_load = get_books_on_load()

    for book in book_on_load:
        dado = [ f"{book[0]}", f"{book[1]}", f"{book[2]} {book[3]}", f"{book[4]}", f"{book[5]}"]

        dados.append(dado)

    # creating a treeview with dual scrollbars
    list_header = ["ID","Título", "Nome do Usuario", "Data Emprestimo", "Data Devolução"]
    
    global tree

    tree = ttk.Treeview(frameDireita, selectmode="extended", columns=list_header, show="headings")
    
    # vertical scrollbar
    vsb = ttk.Scrollbar(frameDireita, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=2, sticky='nsew')
    vsb.grid(column=1, row=2, sticky='ns')
    hsb.grid(column=0, row=3, sticky='ew')
    frameDireita.grid_rowconfigure(0, weight=12)

    hd=["center", "nw", "nw", "ne", "ne"]
    h=[50, 175, 120, 90, 90]
    n=0

    for col in list_header:
        tree.heading(col, text=col, anchor='nw')
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in dados:
        tree.insert('', 'end', values=item)

# Devolver livro
def devolver_livro():
   
    global img_salvar

    def add():
        loan_id = e_id_emprestimo.get()
        return_date = e_data_return.get()

        lista = [loan_id, return_date]

        for i in lista:
            if i == "":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return

        update_loan_return_date(loan_id, return_date)

        messagebox.showinfo("Sucesso", "Livro devolvido")

        e_id_emprestimo.delete(0, END)
        e_data_return.delete(0, END)

    app = Label(frameDireita, text=" Devolver o Livro", width=50, compound=LEFT, padx=5, pady=10, font=("Verdana 12"), bg=co1, fg=co4)
    app.grid(row=0, column=0, columnspan=3, sticky=NSEW)

    app_linha = Label(frameDireita, width=700, height=1, anchor=NW, font=("Verdana 1"), bg=co3, fg=co1)
    app_linha.grid(row=1, column=0, columnspan=3, sticky=NSEW)

    l_id_emprestimo = Label(frameDireita, text="ID do Emprestimo", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_id_emprestimo.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

    e_id_emprestimo = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_id_emprestimo.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)

    l_data_return = Label(frameDireita, text="Nova data de devolução (formato AAAA-MM-DD)", anchor=NW, font=("iVY 10"), bg=co1, fg=co4)
    l_data_return.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)

    e_data_return = Entry(frameDireita, width=25, justify="left", relief="solid")
    e_data_return.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

    
    # Salvar
    img_salvar = Image.open('salvar.png')
    img_salvar = img_salvar.resize((18,18))
    img_salvar = ImageTk.PhotoImage(img_salvar)
    b_salvar = Button(frameDireita, command=add, image=img_salvar, compound=LEFT, anchor=NW, text=" Devolver", bg=co1, fg=co4, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
    b_salvar.grid(row=8, column=1, pady=5, sticky=NSEW)


# Função para controlar o menu ---------------------------------

def control(i):
    
    # novo usuario
    if i == "novo_usuario":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função novo usuario
        novo_usuario()

    # ver usuario
    if i == "ver_usuarios":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função ver usuario
        ver_usuarios()

    # Novo livro
    if i == "novo_livro":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função novo livro
        novo_livro()
    
    # Ver Livro
    if i == "ver_livro":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função ver livro
        ver_livro()

    # Realizar emprestimo do livro
    if i == "emprestar_livro":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função emprestar livro
        emprestar_livro()

    
    # Realizar mostrar livros emprestados
    if i == "mostrar_livro":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função mostrar livros emprestados
        mostrar_livro()
    
    # Realizar devolução do livro
    if i == "devolver_livro":
        for widget in frameDireita.winfo_children():
            widget.destroy()

        # Chamando a função devolver livro
        devolver_livro()

# Menu ----------------------------------------------------------

# Novo usuario
img_usuario = Image.open('adicionar.png')
img_usuario = img_usuario.resize((18,18))
img_usuario = ImageTk.PhotoImage(img_usuario)
b_usuario = Button(frameEsquerda, command=lambda:control("novo_usuario"), image=img_usuario, compound=LEFT, anchor=NW, text=" Novo Usuário", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_usuario.grid(row=0, column=0, sticky=NSEW, padx=5, pady=6)

# Novo livro
img_nwlivro = Image.open('adicionar.png')
img_nwlivro = img_nwlivro.resize((18,18))
img_nwlivro = ImageTk.PhotoImage(img_nwlivro)
b_nwlivro = Button(frameEsquerda, command=lambda:control("novo_livro"), image=img_nwlivro, compound=LEFT, anchor=NW, text=" Novo Livro", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_nwlivro.grid(row=1, column=0, sticky=NSEW, padx=5, pady=6)

# Exibir livros
img_livro = Image.open('livros.png')
img_livro = img_livro.resize((18,18))
img_livro = ImageTk.PhotoImage(img_livro)
b_livro = Button(frameEsquerda, command=lambda:control("ver_livro"), image=img_livro, compound=LEFT, anchor=NW, text=" Exibir todos os Livros", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_livro.grid(row=2, column=0, sticky=NSEW, padx=5, pady=6)

# Exibir usuarios
img_exibir_usuario = Image.open('pessoa.png')
img_exibir_usuario = img_exibir_usuario.resize((18,18))
img_exibir_usuario = ImageTk.PhotoImage(img_exibir_usuario)
b_exibir_usuario = Button(frameEsquerda,  command=lambda:control("ver_usuarios"), image=img_exibir_usuario, compound=LEFT, anchor=NW, text=" Exibir todos os Usuários", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_exibir_usuario.grid(row=3, column=0, sticky=NSEW, padx=5, pady=6)

# Emprestimo
img_emprestimo = Image.open('adicionar.png')
img_emprestimo = img_emprestimo.resize((18, 18))
img_emprestimo = ImageTk.PhotoImage(img_emprestimo)
b_emprestimo = Button(frameEsquerda, command=lambda:control("emprestar_livro"), image=img_emprestimo, compound=LEFT, anchor=NW, text=" Realizar um Empréstimo", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_emprestimo.grid(row=4, column=0, sticky=NSEW, padx=5, pady=6)

# Devolução
img_devolver = Image.open('devolver.png')
img_devolver = img_devolver.resize((18,18))
img_devolver = ImageTk.PhotoImage(img_devolver)
b_devolver = Button(frameEsquerda, command=lambda:control("devolver_livro"), image=img_devolver, compound=LEFT, anchor=NW, text=" Devolver um livro", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_devolver.grid(row=5, column=0, sticky=NSEW, padx=5, pady=6)

# Exibir Livros emprestados
img_Livro_emprestado = Image.open('emprestado.png')
img_Livro_emprestado = img_Livro_emprestado.resize((18,18))
img_Livro_emprestado = ImageTk.PhotoImage(img_Livro_emprestado)
b_livro_emprestado = Button(frameEsquerda, command=lambda:control("mostrar_livro"), image=img_Livro_emprestado, compound=LEFT, anchor=NW, text=" Exibir livros emprestados", bg=co4, fg=co1, font=("Ivy 11"), overrelief=RIDGE, relief=GROOVE)
b_livro_emprestado.grid(row=6, column=0, sticky=NSEW, padx=5, pady=6)

janela.mainloop()
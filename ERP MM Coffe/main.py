import customtkinter
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Inicializando a aplicação
app = customtkinter.CTk()
app.title('ERP MM Coffee')
app.geometry('900x500')
app.config(bg='#C4F4FF')
app.resizable(False, False)

font1 = ('Times New Roman', 20, 'bold')
font2 = ('Times New Roman', 12, 'bold')
text_color = '#003785'
bg_color = '#C4F4FF'
button_color = '#05A312'
hover_color = '#00850B'

# Conectando ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('ERP_MM_Coffee.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            estoque INTEGER
        )
    ''')

    cursor.execute('''
           CREATE TABLE IF NOT EXISTS Vendas (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               produto TEXT,
               quantidade INTEGER,
               data TEXT
           )
       ''')
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS Despesas (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               valor REAL,
               data TEXT
           )
       ''')

    conn.commit()
    return conn, cursor

# Funções para alternar entre as telas
def show_frame(frame):
    frame.tkraise()

def carregar_resultado_geral():
    mes = mes_combobox.get().zfill(2)
    ano = ano_combobox.get()
    conn, cursor = connect_db()

    # Filtrar as vendas pelo mês e ano
    cursor.execute('''
        SELECT produto, SUM(quantidade) as total_vendido, SUM(valor) as total_valor
        FROM Vendas 
        WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?
        GROUP BY produto
    ''', (mes, ano))
    vendas = cursor.fetchall()

    # Calcular o produto mais vendido e menos vendido
    if vendas:
        produto_mais_vendido = max(vendas, key=lambda x: x[1])
        produto_menos_vendido = min(vendas, key=lambda x: x[1])
    else:
        produto_mais_vendido = None
        produto_menos_vendido = None

    # Calcular o total de vendas
    cursor.execute('''
        SELECT SUM(valor)
        FROM Vendas 
        WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?
    ''', (mes, ano))
    total_vendas = cursor.fetchone()[0] or 0

    # Calcular o total de despesas
    cursor.execute('''
        SELECT SUM(valor)
        FROM Despesas
        WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?
    ''', (mes, ano))
    total_despesas = cursor.fetchone()[0] or 0

    # Calcular o resultado (lucro/prejuízo)
    resultado = total_vendas - total_despesas

    conn.close()

    # Exibir os resultados na interface
    if produto_mais_vendido:
        mais_vendido_label.configure(
            text=f"Produto Mais Vendido: {produto_mais_vendido[0]} - Quantidade: {produto_mais_vendido[1]}")
    else:
        mais_vendido_label.configure(text="Nenhum produto vendido neste período.")

    if produto_menos_vendido:
        menos_vendido_label.configure(
            text=f"Produto Menos Vendido: {produto_menos_vendido[0]} - Quantidade: {produto_menos_vendido[1]}")
    else:
        menos_vendido_label.configure(text="Nenhum produto vendido neste período.")

    resultado_label.configure(text=f"Resultado (Lucro/Prejuízo): R${resultado:.2f}")


def produto_mais_e_menos_vendido():
    conn, cursor = connect_db()
    data_atual = datetime.now().strftime("%d/%m/%Y")
    inicio_mes = '01/' + data_atual.split('/')[1] + '/' + data_atual.split('/')[2]

    cursor.execute('''
        SELECT produto, SUM(quantidade) as total_vendido 
        FROM Vendas 
        WHERE  data BETWEEN ? AND ?
        GROUP BY produto 
        ORDER BY total_vendido DESC
    ''', (inicio_mes, data_atual))

    vendas = cursor.fetchall()

    query = '''
        SELECT
            (SELECT SUM(valor) FROM Vendas) - 
            (SELECT SUM(valor) FROM Despesas) AS Resultado
    '''

    cursor.execute(query)

    resultado = cursor.fetchone()
    conn.close()
    print(vendas, resultado)
    if vendas and resultado:
        mais_vendido = vendas[0]
        menos_vendido = vendas[-1]
        return mais_vendido, menos_vendido, resultado
    else:
        return None, None, None


def atualizar_info_vendas():
    mais_vendido, menos_vendido, resultado = produto_mais_e_menos_vendido()
    if mais_vendido and menos_vendido and resultado:
        if resultado[0] >=0:
            veredito = 'lucro'
        else:
            veredito = 'prejuízo'
        info_label.configure(text=f"Produto mais vendido do mês: {mais_vendido[0]} ({mais_vendido[1]} unidades)\n\n"
                               f"Produto menos vendido do mês: {menos_vendido[0]} ({menos_vendido[1]} unidades)\n\n"
                                f"Resultado Geral: {veredito} de R${resultado[0]}")
    else:
        info_label.configure(text="Nenhum dado de vendas para o mês atual.")
    print(mais_vendido,menos_vendido)
def update_product_list():
    produtos = load_products()
    produto_combobox.configure(values=produtos)
    if produtos:
        produto_combobox.set(produtos[0])  # Opcional: Selecionar o primeiro produto da lista

# Função para cadastrar produtos
def cadastrar_produto():
    descricao = descricao_entry.get()
    valor = valor_entry.get()
    estoque = estoque_entry.get()
    data = datetime.now().strftime("%m/%Y")
    if not descricao or not valor or not estoque:
        messagebox.showerror('Erro', 'Por favor, preencha todos os campos.')
        return

    try:
        valor = float(valor.replace(',', '.'))
        estoque = int(estoque)
    except ValueError:
        messagebox.showerror('Erro', 'Formato Inválido! Por favor, insira valores numéricos válidos.')
        return

    conn, cursor = connect_db()
    # Verificar se o produto já existe
    cursor.execute('SELECT * FROM Produtos WHERE descricao = ?', (descricao,))
    produto_existente = cursor.fetchone()

    if produto_existente:
        messagebox.showerror('Erro', 'Produto já cadastrado!')
        conn.close()
        return
    cursor.execute('SELECT * FROM Despesas WHERE data = ?',
                   (data,))
    data_existente = cursor.fetchone()

    if data_existente:
        despesa = data_existente[1] + valor * estoque
        cursor.execute('UPDATE Despesas SET valor = ? WHERE data = ?',
                       (despesa, data))
    else:
        cursor.execute('INSERT INTO Despesas (valor, data) VALUES (?, ?)',
                   (valor * estoque, data))
    print(data_existente)
    cursor.execute('INSERT INTO Produtos (descricao, valor, estoque) VALUES (?, ?, ?)',
                   (descricao, valor, estoque))
    conn.commit()
    conn.close()

    clear_entries()
    messagebox.showinfo('Sucesso', 'Produto cadastrado com sucesso!')

    # Atualizar a lista de produtos no combobox
    update_product_list()

def atualizar_estoque():
    data = datetime.now().strftime("%m/%Y")
    produto = produto_combobox2.get()
    quantidade = quantidade_entry2.get()

    if not produto:
        messagebox.showerror('Erro', 'Selecione um produto!')
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror('Erro', 'Formato Inválido! Por favor, insira uma quantidade válida.')
        return

    conn = sqlite3.connect('ERP_MM_Coffee.db')
    cursor = conn.cursor()

    # Corrigir a consulta SQL para buscar o preço do produto
    cursor.execute('SELECT * FROM Produtos WHERE descricao = ?', (produto,))
    selecProd = cursor.fetchone()

    if selecProd:
        qtdAdd = max(quantidade - selecProd[3],0) * selecProd[2]

        confirm = messagebox.askyesno('Confirmação', f'Tem certeza que deseja atualizar o estoque do produto?')
        if confirm:
            agora = datetime.now()
            data_atual = agora.strftime("%d/%m/%Y")
            # Inserir a venda no banco de dados
            cursor.execute('UPDATE Produtos SET estoque = ? WHERE descricao = ?',(quantidade, produto))
            cursor.execute('SELECT * FROM Despesas WHERE data = ?',
                           (data,))
            data_existente = cursor.fetchone()

            if data_existente:
                despesa = data_existente[1] + qtdAdd
                cursor.execute('UPDATE Despesas SET valor = ? WHERE data = ?',
                               (despesa, data))
            else:
                cursor.execute('INSERT INTO Despesas (valor, data) VALUES (?, ?)',
                               (qtdAdd, data))
            conn.commit()
            clear_entries()
            messagebox.showinfo('Sucesso', 'Estoque atualizado com sucesso!')
    else:
        messagebox.showerror('Erro', 'Produto não encontrado!')

    conn.close()

def clear_entries():
    descricao_entry.delete(0, 'end')
    valor_entry.delete(0, 'end')
    estoque_entry.delete(0, 'end')


# Função para carregar os produtos no combobox
def load_products():
    conn, cursor = connect_db()
    cursor.execute('SELECT descricao FROM Produtos')
    produtos = cursor.fetchall()
    conn.close()
    return [produto[0] for produto in produtos]


# Função para cadastrar vendas
def setVenda():
    produto = produto_combobox.get()
    quantidade = quantidade_entry.get()

    if not produto:
        messagebox.showerror('Erro', 'Selecione um produto!')
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror('Erro', 'Formato Inválido! Por favor, insira uma quantidade válida.')
        return

    conn = sqlite3.connect('ERP_MM_Coffee.db')
    cursor = conn.cursor()

    # Corrigir a consulta SQL para buscar o preço do produto
    cursor.execute('SELECT valor FROM Produtos WHERE descricao = ?', (produto,))
    selecProd = cursor.fetchone()

    if selecProd:
        preco_produto = selecProd[0]
        venda = preco_produto * quantidade

        confirm = messagebox.askyesno('Confirmação', f'Tem certeza que deseja confirmar esta venda de R${venda:.2f}?')
        if confirm:
            agora = datetime.now()
            data_atual = agora.strftime("%d/%m/%Y")

            cursor.execute('SELECT estoque FROM Produtos WHERE descricao = ?', (produto,))
            selecProd = cursor.fetchone()

            # Inserir a venda no banco de dados
            cursor.execute('INSERT INTO Vendas (valor, data, produto, quantidade) VALUES (?, ?, ?, ?)',
                           (venda, data_atual, produto, quantidade))
            cursor.execute('UPDATE Produtos SET estoque = ? WHERE descricao = ?',(selecProd[0] - quantidade, produto))

            conn.commit()

            clear_entries()
            messagebox.showinfo('Sucesso', 'Venda cadastrada com sucesso!')
    else:
        messagebox.showerror('Erro', 'Produto não encontrado!')

    conn.close()

def setVenda():
    produto = produto_combobox.get()
    quantidade = quantidade_entry.get()

    if not produto:
        messagebox.showerror('Erro', 'Selecione um produto!')
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror('Erro', 'Formato Inválido! Por favor, insira uma quantidade válida.')
        return

    conn = sqlite3.connect('ERP_MM_Coffee.db')
    cursor = conn.cursor()

    # Corrigir a consulta SQL para buscar o preço do produto
    cursor.execute('SELECT valor FROM Produtos WHERE descricao = ?', (produto,))
    selecProd = cursor.fetchone()

    if selecProd:
        preco_produto = selecProd[0]
        venda = preco_produto * quantidade

        confirm = messagebox.askyesno('Confirmação', f'Tem certeza que deseja confirmar esta venda de R${venda:.2f}?')
        if confirm:
            agora = datetime.now()
            data_atual = agora.strftime("%d/%m/%Y")

            cursor.execute('SELECT estoque FROM Produtos WHERE descricao = ?', (produto,))
            selecProd = cursor.fetchone()

            # Inserir a venda no banco de dados
            cursor.execute('INSERT INTO Vendas (valor, data, produto, quantidade) VALUES (?, ?, ?, ?)',
                           (venda, data_atual, produto, quantidade))
            cursor.execute('UPDATE Produtos SET estoque = ? WHERE descricao = ?',(selecProd[0] - quantidade, produto))

            conn.commit()

            clear_entries()
            messagebox.showinfo('Sucesso', 'Venda cadastrada com sucesso!')
    else:
        messagebox.showerror('Erro', 'Produto não encontrado!')

    conn.close()


# Função para exibir todas as vendas
def exibir_vendas():
    for row in vendas_table.get_children():
        vendas_table.delete(row)

    conn, cursor = connect_db()
    cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas')
    vendas = cursor.fetchall()
    conn.close()

    for venda in vendas:
         vendas_table.insert('', 'end', values=venda)

# Função para filtrar vendas por data
def filtrar_vendas():
    # Função para filtrar vendas por data
    conn, cursor = connect_db()
    data_inicial = data_inicial_entry.get()
    data_final = data_final_entry.get()

    for row in vendas_table.get_children():
        vendas_table.delete(row)

    if data_inicial != '' and data_final != '':
        cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE data BETWEEN ? AND ?',
                       (data_inicial, data_final))
    elif data_inicial != '':
        cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE data = ?', (data_inicial,))
    else:
        cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas')
    vendas = cursor.fetchall()

    for venda in vendas:
        vendas_table.insert('', 'end', values=venda)

    conn.close()
    return vendas

# Função para exibir todas as vendas
def exibir_produtos():
    for row in produtos_table.get_children():
        produtos_table.delete(row)

    conn, cursor = connect_db()
    cursor.execute('SELECT descricao, valor, estoque FROM Produtos')
    produtos = cursor.fetchall()
    conn.close()

    for produto in produtos:
         produtos_table.insert('', 'end', values=produto)

# Função para filtrar vendas por data
def filtrar_produtos():
    # Função para filtrar vendas por data
    conn, cursor = connect_db()
    filterKey = filter_entry.get()

    for row in produtos_table.get_children():
        produtos_table.delete(row)

    if filterKey != '':
        cursor.execute('SELECT descricao, valor, estoque FROM Produtos WHERE descricao = ?',
                       (filterKey,))
    else:
        cursor.execute('SELECT descricao, valor, estoque FROM Produtos')
    produtos = cursor.fetchall()

    for produto in produtos:
        produtos_table.insert('', 'end', values=produto)

    conn.close()
    return produtos

# Tela principal
main_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
main_frame.place(relwidth=1, relheight=1)

title_label = customtkinter.CTkLabel(main_frame, text='ERP MM Coffee', font=font1, text_color=text_color)
title_label.pack(pady=10)

cadastro_produto_button = customtkinter.CTkButton(main_frame, text='Cadastrar Produto', font=font2, text_color='#fff',
                                                  fg_color=button_color, hover_color=hover_color,
                                                  command=lambda: show_frame(cadastro_frame))
cadastro_produto_button.pack(pady=5)


venda_button = customtkinter.CTkButton(main_frame, text='Registrar Venda', font=font2, text_color='#fff',
                                       fg_color=button_color, hover_color=hover_color,
                                       command=lambda: show_frame(venda_frame))
venda_button.pack(pady=5)

# Tela de cadastro de produtos
cadastro_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
cadastro_frame.place(relwidth=1, relheight=1)

descricao_label = customtkinter.CTkLabel(cadastro_frame, text='Descrição:', font=font2, text_color=text_color)
descricao_label.place(x=20, y=20)
descricao_entry = customtkinter.CTkEntry(cadastro_frame, width=200)
descricao_entry.place(x=150, y=20)

valor_label = customtkinter.CTkLabel(cadastro_frame, text='Valor:', font=font2, text_color=text_color)
valor_label.place(x=20, y=60)
valor_entry = customtkinter.CTkEntry(cadastro_frame, width=200)
valor_entry.place(x=150, y=60)

estoque_label = customtkinter.CTkLabel(cadastro_frame, text='Estoque:', font=font2, text_color=text_color)
estoque_label.place(x=20, y=100)
estoque_entry = customtkinter.CTkEntry(cadastro_frame, width=200)
estoque_entry.place(x=150, y=100)

cadastrar_button = customtkinter.CTkButton(cadastro_frame, text='Cadastrar', font=font2, text_color='#fff',
                                           fg_color=button_color, hover_color=hover_color, command=cadastrar_produto)
cadastrar_button.place(x=100, y=180)

voltar_button = customtkinter.CTkButton(cadastro_frame, text='Voltar', font=font2, text_color='#fff',
                                        fg_color='#161C25',hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.place(x=250, y=180)

# Tela de registro de vendas
venda_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
venda_frame.place(relwidth=1, relheight=1)

# Combobox para selecionar produto
produto_label = customtkinter.CTkLabel(venda_frame, text='Produto:', font=font2, text_color=text_color)
produto_label.place(x=20, y=60)

produtos = load_products()
produto_combobox = customtkinter.CTkComboBox(venda_frame, values=produtos, width=200)
produto_combobox.place(x=150, y=60)

# Entrada para quantidade
quantidade_label = customtkinter.CTkLabel(venda_frame, text='Quantidade:', font=font2, text_color=text_color)
quantidade_label.place(x=20, y=100)
quantidade_entry = customtkinter.CTkEntry(venda_frame, width=200)
quantidade_entry.place(x=150, y=100)

# Botão para confirmar venda
confirm_button = customtkinter.CTkButton(venda_frame, text='Confirmar Venda', font=font2, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=setVenda)
confirm_button.place(x=100, y=140)

# Botão para voltar à tela principal
voltar_button_venda = customtkinter.CTkButton(venda_frame, text='Voltar', font=font2, text_color='#fff',
                                              fg_color='#161C25', hover_color='#FF7000',
                                              command=lambda: show_frame(main_frame))
voltar_button_venda.place(x=250, y=140)

exibir_vendas_button = customtkinter.CTkButton(main_frame, text='Exibir Vendas', font=font2, text_color='#fff',
                                               fg_color=button_color, hover_color=hover_color,
                                               command=lambda: [exibir_vendas(), show_frame(vendas_frame)])
exibir_vendas_button.pack(pady=5)

exibir_produtos_button = customtkinter.CTkButton(main_frame, text='Exibir Produtos', font=font2, text_color='#fff',
                                               fg_color=button_color, hover_color=hover_color,
                                               command=lambda: [exibir_produtos(), show_frame(produtos_frame)])
exibir_produtos_button.pack(pady=5)

atualizar_estoque_button = customtkinter.CTkButton(main_frame, text='Atualizar Estoque', font=font2, text_color='#fff',
                                               fg_color=button_color, hover_color=hover_color,
                                               command=lambda: show_frame(estoque_frame))
atualizar_estoque_button.pack(pady=5)

estatistica_button = customtkinter.CTkButton(main_frame, text='Estatísticas', font=font2, text_color='#fff',
                                                  fg_color=button_color, hover_color=hover_color,
                                                  command=lambda: show_frame(resultado_frame))
estatistica_button.pack(pady=5)

info_label = customtkinter.CTkLabel(main_frame, text='', font=font2, text_color=text_color)
info_label.pack(pady=5)


# Chamar a função para atualizar a informação na tela principal
atualizar_info_vendas()

# Tela de exibição de vendas
vendas_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
vendas_frame.place(relwidth=1, relheight=1)

#Tela de exibição de produtos
produtos_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
produtos_frame.place(relwidth=1, relheight=1)

#Tela de atualização de estoque
estoque_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
estoque_frame.place(relwidth=1, relheight=1)

produto_label2 = customtkinter.CTkLabel(estoque_frame, text='Produto:', font=font2, text_color=text_color)
produto_label2.place(x=20, y=60)

produtos2 = load_products()
produto_combobox2 = customtkinter.CTkComboBox(estoque_frame, values=produtos, width=200)
produto_combobox2.place(x=150, y=60)

# Entrada para quantidade
quantidade_label2 = customtkinter.CTkLabel(estoque_frame, text='Quantidade:', font=font2, text_color=text_color)
quantidade_label2.place(x=20, y=100)
quantidade_entry2 = customtkinter.CTkEntry(estoque_frame, width=200)
quantidade_entry2.place(x=150, y=100)

# Botão para confirmar atualização de estoque
confirm_button2 = customtkinter.CTkButton(estoque_frame, text='Confirmar Venda', font=font2, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=atualizar_estoque)
confirm_button2.place(x=100, y=140)

# Botão para voltar à tela principal
voltar_button_venda2 = customtkinter.CTkButton(estoque_frame, text='Voltar', font=font2, text_color='#fff',
                                              fg_color='#161C25', hover_color='#FF7000',
                                              command=lambda: show_frame(main_frame))
voltar_button_venda2.place(x=250, y=140)

vendas_label = customtkinter.CTkLabel(vendas_frame, text='Vendas Registradas', font=font1, text_color=text_color)
vendas_label.pack(pady=20)

data_inicial_label = customtkinter.CTkLabel(vendas_frame, text='Data Inicial (dd/mm/yyyy):', font=font2, text_color=text_color)
data_inicial_label.pack(pady=5)
data_inicial_entry = customtkinter.CTkEntry(vendas_frame, width=200)
data_inicial_entry.pack(pady=5)

data_final_label = customtkinter.CTkLabel(vendas_frame, text='Data Final (dd/mm/yyyy):', font=font2, text_color=text_color)
data_final_label.pack(pady=5)
data_final_entry = customtkinter.CTkEntry(vendas_frame, width=200)
data_final_entry.pack(pady=5)
filtrar_button = customtkinter.CTkButton(vendas_frame, text='Filtrar por Data', font=font2, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=filtrar_vendas)
filtrar_button.pack(pady=10)

vendas_table = ttk.Treeview(vendas_frame, columns=('Produto', 'Quantidade', 'Valor', 'Data'), show='headings')
vendas_table.heading('Produto', text='Produto')
vendas_table.heading('Quantidade', text='Quantidade')
vendas_table.heading('Valor', text='Valor')
vendas_table.heading('Data', text='Data')
vendas_table.pack(pady=20, fill='x')

voltar_button = customtkinter.CTkButton(vendas_frame, text='Voltar', font=font2, text_color='#fff',
                                        fg_color='#161C25', hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.place(x=30, y=12)

produtos_label = customtkinter.CTkLabel(produtos_frame, text='Produtos Registradas', font=font1, text_color=text_color)
produtos_label.pack(pady=20)

filter_label = customtkinter.CTkLabel(produtos_frame, text='Nome do produto:', font=font2, text_color='#1465bb')
filter_label.pack(pady=5)
filter_entry = customtkinter.CTkEntry(produtos_frame, width=200)
filter_entry.pack(pady=5)
filtrar_button = customtkinter.CTkButton(produtos_frame, text='Filtrar', font=font2, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=filtrar_produtos)
filtrar_button.pack(pady=10)

produtos_table = ttk.Treeview(produtos_frame, columns=('Descricao', 'Valor', 'Estoque'), show='headings')
produtos_table.heading('Descricao', text='Descrição')
produtos_table.heading('Valor', text='Preço')
produtos_table.heading('Estoque', text='Estoque')
produtos_table.pack(pady=20, fill='x')

voltar_button = customtkinter.CTkButton(produtos_frame, text='Voltar', font=font2, text_color='#fff',
                                        fg_color='#161C25', hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.place(x=30, y=12)

# Tela de resultado geral
resultado_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
resultado_frame.place(relwidth=1, relheight=1)

resultado_label = customtkinter.CTkLabel(resultado_frame, text='Resultado Geral', font=font1, text_color=text_color)
resultado_label.pack(pady=20)

mes_label = customtkinter.CTkLabel(resultado_frame, text='Mês:', font=font2, text_color=text_color)
mes_label.pack(pady=5)
mes_combobox = customtkinter.CTkComboBox(resultado_frame, values=[f'{i:02}' for i in range(1, 13)], width=200)
mes_combobox.pack(pady=5)

ano_label = customtkinter.CTkLabel(resultado_frame, text='Ano:', font=font2, text_color=text_color)
ano_label.pack(pady=5)
ano_combobox = customtkinter.CTkComboBox(resultado_frame, values=[str(i) for i in range(2020, 2031)], width=200)
ano_combobox.pack(pady=5)

filtrar_resultado_button = customtkinter.CTkButton(resultado_frame, text='Filtrar', font=font2, text_color='#fff',
                                                   fg_color=button_color, hover_color=hover_color,
                                                   command=carregar_resultado_geral)
filtrar_resultado_button.pack(pady=10)

mais_vendido_label = customtkinter.CTkLabel(resultado_frame, text='', font=font2, text_color=text_color)
mais_vendido_label.pack(pady=10)

menos_vendido_label = customtkinter.CTkLabel(resultado_frame, text='', font=font2, text_color=text_color)
menos_vendido_label.pack(pady=10)

resultado_label = customtkinter.CTkLabel(resultado_frame, text='', font=font2, text_color=text_color)
resultado_label.pack(pady=10)

voltar_button = customtkinter.CTkButton(resultado_frame, text='Voltar', font=font2, text_color='#fff',
                                        fg_color='#161C25', hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.pack(pady=10)

# Botão na tela principal para exibir a tela de resultado geral
resultado_button = customtkinter.CTkButton(main_frame, text='Resultado Geral', font=font2, text_color='#fff',
                                           fg_color=button_color, hover_color=hover_color,
                                           command=lambda: show_frame(resultado_frame))
resultado_button.pack(pady=10)

# Mostrar a tela principal no início
show_frame(main_frame)

# Iniciar a aplicação
app.mainloop()
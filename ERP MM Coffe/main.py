import customtkinter
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

app = customtkinter.CTk()
app.title('ERP MM Coffee')
app.geometry('900x600')
app.config(bg='#F0F8FF')
app.resizable(False, False)

# Definindo estilos
font_title = ('Arial', 30, 'bold')
font_label = ('Arial', 14)
font_button = ('Arial', 14, 'bold')
text_color = '#000000'
bg_color = '#F0F8FF'
button_color = '#161C25'
hover_color = '#00850B'
entry_bg_color = '#ffffff'
entry_border_color = '#cccccc'

font1 = ('Times New Roman', 28, 'bold')
font2 = ('Times New Roman', 18)
# Conectando ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('ERP_MM_Coffee.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            estoque INTEGER,
            status BOOLEAN
        )
    ''')

    cursor.execute('''
           CREATE TABLE IF NOT EXISTS Vendas (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               valor REAL,
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

    cursor.execute('''
           CREATE TABLE IF NOT EXISTS Resultado(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               resultado REAL,
               data TEXT
           )
       ''')

    conn.commit()
    return conn, cursor

# Funções para alternar entre as telas
def show_frame(frame):
    frame.tkraise()

def carregar_resultado_geral():
    conn, cursor = connect_db()
    # Calcular o total de vendas por mês
    cursor.execute('''
        SELECT substr(data, 4), SUM(valor) 
        FROM Vendas 
        GROUP BY substr(data, 4)
    ''')
    total_vendas = cursor.fetchall()

    # Calcular o total de despesas por mês
    cursor.execute('''
        SELECT (data), SUM(valor)
        FROM Despesas 
        GROUP BY (data)
    ''')
    total_despesas = cursor.fetchall()

    # Criar um dicionário para armazenar os resultados mensais
    resultados = {}

    # Adicionar total de vendas ao dicionário de resultados
    for venda in total_vendas:
        mes = venda[0]
        resultados[mes] = resultados.get(mes, 0) + venda[1]

    # Subtrair despesas do dicionário de resultados
    for despesa in total_despesas:
        mes = despesa[0]
        resultados[mes] = resultados.get(mes, 0) - despesa[1]

    # Inserir os resultados na tabela
    for mes, resultado in resultados.items():

        cursor.execute('''
        SELECT * FROM Resultado WHERE data = ?
    ''', (mes,))
        result = cursor.fetchone()
        if not result:
            cursor.execute('''
            INSERT INTO Resultado (resultado, data)
            VALUES (?,?)
        ''', (resultado,mes))
        else:
            cursor.execute('''
                        UPDATE Resultado SET resultado = ?, data = ?
                    ''', (resultado, mes))
    conn.commit()
    conn.close()
    print(resultados.items())
    exibir_resultados()

def filtrar_resultados():
    mes = resultado_combobox.get()
    conn, cursor = connect_db()
    for row in resultados_table.get_children():
        resultados_table.delete(row)
    cursor.execute('''
        SELECT * FROM Resultado WHERE data = ?
    ''', (mes,))
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()

    for resultado in resultados:
        resultados_table.insert('', 'end', values=resultado)

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
    conn.commit()
    conn.close()
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
        info_label.configure(text=f"\nProduto mais vendido do mês: {mais_vendido[0]} ({mais_vendido[1]} unidades)\n"
                               f"Produto menos vendido do mês: {menos_vendido[0]} ({menos_vendido[1]} unidades)\n"
                                f"Resultado Geral: {veredito} de R${resultado[0]}")
    else:
        info_label.configure(text="\nNenhum dado de vendas para o mês atual.")

def update_product_list():
    produtos = load_products()
    produto_combobox.configure(values=produtos)
    if produtos:
        produto_combobox.set(produtos[0])  # Opcional: Selecionar o primeiro produto da lista

def load_datas():
    conn, cursor = connect_db()
    cursor.execute('SELECT substr(data,4) FROM Vendas group by substr(data,4)')
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    return [resultado[0] for resultado in resultados]

def update_data_list():
    resultados = load_datas()
    resultado_combobox.configure(values=resultados)
    if resultados:
        resultado_combobox.set(resultados[0])  # Opcional: Selecionar o primeiro produto da lista


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
        conn.commit()
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
    cursor.execute('INSERT INTO Produtos (descricao, valor, estoque,status) VALUES (?, ?, ?,?)',
                   (descricao, valor, estoque,True))
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

    cursor.execute('SELECT * FROM Produtos WHERE descricao = ?', (produto,))
    produto_existente = cursor.fetchone()

    if produto_existente:
        # Corrigir a consulta SQL para buscar o preço do produto
        cursor.execute('SELECT * FROM Produtos WHERE descricao = ?', (produto,))
        selecProd = cursor.fetchone()

        if selecProd:
            qtdAdd = max(quantidade - selecProd[3],0) * selecProd[2]

            confirm = messagebox.askyesno('Confirmação', f'Tem certeza que deseja atualizar o estoque do produto para {quantidade} unidades?')
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
    conn.commit()
    conn.close()

def clear_entries():
    descricao_entry.delete(0, 'end')
    valor_entry.delete(0, 'end')
    estoque_entry.delete(0, 'end')

def inativar_produto():
    produto = produto_combobox2.get()
    confirm = messagebox.askyesno('Confirmação', f'Tem certeza que deseja inativar o produto {produto} permanentemente?')
    if confirm:
        conn, cursor = connect_db()
        cursor.execute('UPDATE Produtos SET status = 0 WHERE descricao = ?', (produto,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Produto inativado!')

# Função para carregar os produtos no combobox
def load_products():
    conn, cursor = connect_db()
    cursor.execute('SELECT descricao FROM Produtos')
    produtos = cursor.fetchall()
    conn.commit()
    conn.close()
    return [produto[0] for produto in produtos]


# Função para cadastrar vendas
def setVenda():
    produto = produto_combobox.get()
    quantidade = quantidade_entry.get()
    preco_venda = preco_venda_entry.get()
    if not produto:
        messagebox.showerror('Erro', 'Selecione um produto!')
        return

    try:
        quantidade = int(quantidade)
        preco_venda = float(preco_venda)
    except ValueError:
        messagebox.showerror('Erro', 'Formato Inválido! Por favor, insira uma quantidade e preço válidos.')
        return

    conn = sqlite3.connect('ERP_MM_Coffee.db')
    cursor = conn.cursor()

    # Corrigir a consulta SQL para buscar o preço do produto
    cursor.execute('SELECT valor, status,estoque FROM Produtos WHERE descricao = ?', (produto,))
    selecProd = cursor.fetchone()

    if selecProd:
        status = selecProd[1]
        if status:
            estoque = selecProd[2]
            if estoque < quantidade:
                messagebox.showerror('Erro', 'Estoque insuficiente!')
            else:
                venda = preco_venda * quantidade
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
            messagebox.showerror('Erro', 'Produto inativado!')
    else:
        messagebox.showerror('Erro', 'Produto não encontrado!')

    conn.commit()
    conn.close()

# Função para exibir todas as vendas
def exibir_vendas():
    for row in vendas_table.get_children():
        vendas_table.delete(row)

    conn, cursor = connect_db()
    cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas')
    vendas = cursor.fetchall()
    conn.commit()
    conn.close()

    for venda in vendas:
         vendas_table.insert('', 'end', values=venda)

# Função para filtrar vendas por data
def filtrar_vendas():
    # Função para filtrar vendas por data
    conn, cursor = connect_db()
    data_inicial = data_inicial_entry.get()
    data_final = data_final_entry.get()
    produto = name_entry.get()

    for row in vendas_table.get_children():
        vendas_table.delete(row)

    if data_inicial != '' and data_final != '':
        if produto:
            cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE produto = ? AND data BETWEEN ? AND ?',
                       (produto,data_inicial, data_final))
        else:
            cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE data BETWEEN ? AND ?',
                           (data_inicial, data_final))
    elif data_inicial != '':
        if produto:
            cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE data = ? AND produto = ?', (data_inicial,produto))
        else:
            cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE data = ?', (data_inicial,))
    else:
        if produto:
            cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas WHERE produto = ?',(produto,))
        else:
            cursor.execute('SELECT produto, quantidade, valor, data FROM Vendas')
    vendas = cursor.fetchall()
    print(vendas)

    for venda in vendas:
        vendas_table.insert('', 'end', values=venda)
    conn.commit()
    conn.close()
    return vendas

# Função para exibir todas as vendas
def exibir_produtos():
    for row in produtos_table.get_children():
        produtos_table.delete(row)

    conn, cursor = connect_db()
    cursor.execute('SELECT descricao, valor, estoque FROM Produtos')
    produtos = cursor.fetchall()
    conn.commit()
    conn.close()

    for produto in produtos:
         produtos_table.insert('', 'end', values=produto)

def exibir_resultados():
    update_data_list()
    for row in resultados_table.get_children():
        resultados_table.delete(row)

    conn, cursor = connect_db()
    cursor.execute('SELECT data, resultado FROM Resultado')
    resultados = cursor.fetchall()  # Nome da variável ajustado para 'resultados'
    conn.commit()
    conn.close()

    for resultado in resultados:
        resultados_table.insert('', 'end', values=resultado)

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
    conn.commit()
    conn.close()
    return produtos

# Tela principal
main_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
main_frame.place(relwidth=1, relheight=1)

title_label = customtkinter.CTkLabel(main_frame, text='ERP MM Coffee ®', font=font_title, text_color='#003785', bg_color='#Daa520', width=300, height=70)
title_label.pack(pady=30)

cadastro_produto_button = customtkinter.CTkButton(main_frame, text='Cadastrar Produto', font=font_button, text_color='#fff',
                                                  fg_color=button_color, hover_color=hover_color,
                                                  command=lambda: show_frame(cadastro_frame))
cadastro_produto_button.pack(pady=5)


venda_button = customtkinter.CTkButton(main_frame, text='Registrar Venda', font=font_button, text_color='#fff',
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

valor_label = customtkinter.CTkLabel(cadastro_frame, text='Custo:', font=font2, text_color=text_color)
valor_label.place(x=20, y=60)
valor_entry = customtkinter.CTkEntry(cadastro_frame, width=200)
valor_entry.place(x=150, y=60)

estoque_label = customtkinter.CTkLabel(cadastro_frame, text='Estoque:', font=font2, text_color=text_color)
estoque_label.place(x=20, y=100)
estoque_entry = customtkinter.CTkEntry(cadastro_frame, width=200)
estoque_entry.place(x=150, y=100)

cadastrar_button = customtkinter.CTkButton(cadastro_frame, text='Cadastrar', font=font_button, text_color='#fff',
                                           fg_color=button_color, hover_color=hover_color, command=cadastrar_produto)
cadastrar_button.place(x=100, y=180)

voltar_button = customtkinter.CTkButton(cadastro_frame, text='Voltar', font=font_button, text_color='#fff',
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

# Entrada para quantidade
preco_venda_label = customtkinter.CTkLabel(venda_frame, text='Preço de Venda:', font=font2, text_color=text_color)
preco_venda_label.place(x=20, y=140)
preco_venda_entry = customtkinter.CTkEntry(venda_frame, width=200)
preco_venda_entry.place(x=150, y=140)

# Botão para confirmar venda
confirm_button = customtkinter.CTkButton(venda_frame, text='Confirmar Venda', font=font_button, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=setVenda)
confirm_button.place(x=100, y=200)

# Botão para voltar à tela principal
voltar_button_venda = customtkinter.CTkButton(venda_frame, text='Voltar', font=font_button, text_color='#fff',
                                              fg_color='#161C25', hover_color='#FF7000',
                                              command=lambda: show_frame(main_frame))
voltar_button_venda.place(x=250, y=200)

exibir_vendas_button = customtkinter.CTkButton(main_frame, text='Exibir Vendas', font=font_button, text_color='#fff',
                                               fg_color=button_color, hover_color=hover_color,
                                               command=lambda: [exibir_vendas(), show_frame(vendas_frame)])
exibir_vendas_button.pack(pady=5)

exibir_produtos_button = customtkinter.CTkButton(main_frame, text='Exibir Produtos', font=font_button, text_color='#fff',
                                               fg_color=button_color, hover_color=hover_color,
                                               command=lambda: [exibir_produtos(), show_frame(produtos_frame)])
exibir_produtos_button.pack(pady=5)

atualizar_estoque_button = customtkinter.CTkButton(main_frame, text='Atualizar Estoque', font=font_button, text_color='#fff',
                                               fg_color=button_color, hover_color=hover_color,
                                               command=lambda: show_frame(estoque_frame))
atualizar_estoque_button.pack(pady=5)

estatistica_button = customtkinter.CTkButton(main_frame, text='Estatísticas', font=font_button, text_color='#fff',
                                                  fg_color=button_color, hover_color=hover_color,
                                                  command=lambda: [exibir_resultados(),show_frame(resultado_frame)])
estatistica_button.pack(pady=5)

info_label = customtkinter.CTkLabel(main_frame, text='', font=font2, text_color='#00028B', bg_color='#808080', width=900)
info_label.pack(pady=70)

info_label2 = customtkinter.CTkLabel(main_frame, text='\na\na\na\na\n', font=font2, text_color='#808080', bg_color='#808080', width=900)
info_label2.place(x=0,y=507)

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
confirm_button2 = customtkinter.CTkButton(estoque_frame, text='Atualizar', font=font_button, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=atualizar_estoque)
confirm_button2.place(x=40, y=150)

#para confirmar atualização de estoque
inativar_button = customtkinter.CTkButton(estoque_frame, text='Inativar', font=font_button, text_color='#fff',
                                         fg_color='#E40404', hover_color='#AE0000', command=inativar_produto)
inativar_button.place(x=340, y=150)

# Botão para voltar à tela principal
voltar_button_venda2 = customtkinter.CTkButton(estoque_frame, text='Voltar', font=font_button, text_color='#fff',
                                              fg_color='#161C25', hover_color='#FF7000',
                                              command=lambda: show_frame(main_frame))
voltar_button_venda2.place(x=190, y=150)

vendas_label = customtkinter.CTkLabel(vendas_frame, text='Vendas Registradas', font=font1, text_color=text_color)
vendas_label.pack(pady=20)

data_inicial_label = customtkinter.CTkLabel(vendas_frame, text='Data Inicial (dd/mm/yyyy):', font=font2, text_color='#1465bb')
data_inicial_label.pack(pady=5)
data_inicial_entry = customtkinter.CTkEntry(vendas_frame, width=200)
data_inicial_entry.pack(pady=5)

data_final_label = customtkinter.CTkLabel(vendas_frame, text='Data Final (dd/mm/yyyy):', font=font2, text_color='#1465bb')
data_final_label.pack(pady=5)
data_final_entry = customtkinter.CTkEntry(vendas_frame, width=200)
data_final_entry.pack(pady=5)

name_label = customtkinter.CTkLabel(vendas_frame, text='Produto', font=font2, text_color=text_color)
name_label.pack(pady=3)
name_entry = customtkinter.CTkEntry(vendas_frame, width=200)
name_entry.pack(pady=3)

filtrar_button = customtkinter.CTkButton(vendas_frame, text='Filtrar por Data', font=font_button, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=filtrar_vendas)
filtrar_button.pack(pady=10)

vendas_table = ttk.Treeview(vendas_frame, columns=('Produto', 'Quantidade', 'Valor', 'Data'), show='headings')
vendas_table.heading('Produto', text='Produto')
vendas_table.heading('Quantidade', text='Quantidade')
vendas_table.heading('Valor', text='Valor')
vendas_table.heading('Data', text='Data')
vendas_table.pack(pady=20, fill='x')

voltar_button = customtkinter.CTkButton(vendas_frame, text='Voltar', font=font_button, text_color='#fff',
                                        fg_color='#161C25', hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.place(x=30, y=12)

produtos_label = customtkinter.CTkLabel(produtos_frame, text='Produtos Registradas', font=font1, text_color=text_color)
produtos_label.pack(pady=20)

filter_label = customtkinter.CTkLabel(produtos_frame, text='Nome do produto:', font=font2, text_color='#1465bb')
filter_label.pack(pady=5)
filter_entry = customtkinter.CTkEntry(produtos_frame, width=200)
filter_entry.pack(pady=5)
filtrar_button = customtkinter.CTkButton(produtos_frame, text='Filtrar', font=font_button, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=filtrar_produtos)
filtrar_button.pack(pady=10)

produtos_table = ttk.Treeview(produtos_frame, columns=('Descricao', 'Valor', 'Estoque'), show='headings')
produtos_table.heading('Descricao', text='Descrição')
produtos_table.heading('Valor', text='Preço')
produtos_table.heading('Estoque', text='Estoque')
produtos_table.pack(pady=20, fill='x')

voltar_button = customtkinter.CTkButton(produtos_frame, text='Voltar', font=font_button, text_color='#fff',
                                        fg_color='#161C25', hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.place(x=30, y=12)

# Tela de resultado geral
resultado_frame = customtkinter.CTkFrame(app, bg_color=bg_color)
resultado_frame.place(relwidth=1, relheight=1)

resultado_label = customtkinter.CTkLabel(resultado_frame, text='Resultado Geral', font=font1, text_color=text_color)
resultado_label.pack(pady=40)

resultado_combobox = customtkinter.CTkComboBox(resultado_frame, values=produtos, width=200)
resultado_combobox.place(x=150, y=100)

resultados_table = ttk.Treeview(resultado_frame, columns=('Data', 'Resultado'), show='headings')
resultados_table.heading('Data', text='Data')
resultados_table.heading('Resultado', text='Resultado')
resultados_table.pack(pady=40, fill='x')


filtrar_button = customtkinter.CTkButton(resultado_frame, text='Filtrar', font=font_button, text_color='#fff',
                                         fg_color=button_color, hover_color=hover_color, command=filtrar_resultados)
filtrar_button.place(x=400,y=100)

voltar_button = customtkinter.CTkButton(resultado_frame, text='Voltar', font=font_button, text_color='#fff',
                                        fg_color='#161C25', hover_color='#FF7000',
                                        command=lambda: show_frame(main_frame))
voltar_button.place(x=10,y=24)

carregar_resultado_geral()

# Mostrar a tela principal no início
show_frame(main_frame)

# Iniciar a aplicação
app.mainloop()
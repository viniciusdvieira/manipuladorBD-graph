import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from easygui import enterbox, msgbox,  multenterbox
from func import adicionar_pessoa, remover_pessoa, editar_pessoa
from func import adicionar_conta, remover_conta, atualizar_conta
from func import consultar_pessoas, consultar_contas, obter_colunas_disponiveis, exibir_resultados
import os


class InterfaceGrafica:
    def __init__(self, conn):
        self.window = tk.Tk()
        self.window.title("Manipulador de Banco de Dados")
        
        self.opcao_selecionada = tk.StringVar()
        self.conn = conn
        
        # Elementos da interface gráfica
        self.label_mensagem1 = tk.Label(self.window, text="BEM VINDO", font=("Arial", 16, "bold"))
        self.label_mensagem1.pack(pady=10)
        
        self.label_mensagem2 = tk.Label(self.window, text="Manipulador de banco de dados em Python", font=("Arial", 14))
        self.label_mensagem2.pack(pady=10)
        
        self.botao_avancar = tk.Button(self.window, text="Iniciar \u2192", font=("Arial", 12), command=self.janela_principal)
        self.botao_avancar.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.botao_sair = tk.Button(self.window, text="\u2190 Sair", font=("Arial", 12), command=self.sair)
        self.botao_sair.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Configurações da janela
        self.window.geometry("650x550")  # Define o tamanho da janela
        self.window.resizable(True, True)  # Impede que a janela seja redimensionada
        
        
    def run(self):
        self.window.mainloop()
        
    def avancar(self):
        tabela = self.opcao_var.get()
        if tabela == "pessoas":
            # Lógica para a opção "PESSOAS"
            self.janela_pessoas()
            
        elif tabela == "contas":
            # Lógica para a opção "CONTAS"
            self.janela_contas()
            
        else:
            messagebox.showerror("Opção inválida", "Opção inválida. Digite 1 para PESSOAS, 2 para CONTAS ou 0 para SAIR.")

    def limpar_janela(self):
        # Limpar a janela removendo todos os elementos
        for child in self.window.winfo_children():
            child.destroy()
            
    def sair(self):
            self.window.destroy()

    def janela_principal(self):
        self.limpar_janela()

        self.label_mensagem = tk.Label(self.window, text="Escolha a opção que desejas:", font=("Arial", 14))
        self.label_mensagem.pack(pady=10)

        self.botao_manipular = tk.Button(self.window, text="Manipular o banco de dados", font=("Arial", 12), command=self.janela_manipulador)
        self.botao_manipular.pack(pady=5)

        self.botao_consulta = tk.Button(self.window, text="Consultas no banco de dados", font=("Arial", 12), command=self.janela_consulta)
        self.botao_consulta.pack(pady=5)
        
        self.botao_sair = tk.Button(self.window, text="Sair", font=("Arial", 12), command=self.sair)
        self.botao_sair.pack(pady=5)

    def janela_manipulador(self):
        # Limpar a janela atual
        self.limpar_janela()

        self.label_tabela = tk.Label(self.window, text="Selecione a tabela para consulta:", font=("Arial", 14))
        self.label_tabela.pack(pady=10)

        self.opcao_var = tk.StringVar()
        self.opcao_var.set("pessoas")

        self.radio_pessoas = tk.Radiobutton(self.window, text="Pessoas", variable=self.opcao_var, value="pessoas", font=("Arial", 12))
        self.radio_pessoas.pack()

        self.radio_contas = tk.Radiobutton(self.window, text="Contas", variable=self.opcao_var, value="contas", font=("Arial", 12))
        self.radio_contas.pack()

        self.botao_consultar = tk.Button(self.window, text="Manipular \u2192", font=("Arial", 12), command=self.avancar)
        self.botao_consultar.pack(pady=5)

        self.botao_voltar = tk.Button(self.window, text="\u2190 Voltar", font=("Arial", 12), command=self.janela_principal)
        self.botao_voltar.pack(pady=5)

    def janela_consulta(self):
        self.limpar_janela()

        self.label_tabela = tk.Label(self.window, text="Selecione a tabela para consulta:", font=("Arial", 14))
        self.label_tabela.pack(pady=10)

        self.opcao_var = tk.StringVar()
        self.opcao_var.set("pessoas")

        self.radio_pessoas = tk.Radiobutton(self.window, text="Pessoas", variable=self.opcao_var, value="pessoas", font=("Arial", 12))
        self.radio_pessoas.pack()

        self.radio_contas = tk.Radiobutton(self.window, text="Contas", variable=self.opcao_var, value="contas", font=("Arial", 12))
        self.radio_contas.pack()

        self.botao_consultar = tk.Button(self.window, text="Consultar \u2192", font=("Arial", 12), command=self.abrir_janela_colunas)
        self.botao_consultar.pack(pady=5)
        
        self.botao_exibir_resultados = tk.Button(self.window, text="Exibir Consultas", font=("Arial", 12), command=self.atualizar_janela_consultas)
        self.botao_exibir_resultados.pack(pady=5)

        self.botao_voltar = tk.Button(self.window, text="\u2190 Voltar", font=("Arial", 12), command=self.janela_principal)
        self.botao_voltar.pack(pady=5)

    

    def abrir_janela_colunas(self):
        self.limpar_janela()  # Fechar a janela atual

        self.label_colunas = tk.Label(self.window, text="Selecione as colunas que deseja consultar:", font=("Arial", 14))
        self.label_colunas.pack(pady=10)

        colunas_disponiveis = obter_colunas_disponiveis(self.opcao_var.get())

        self.listbox_colunas = tk.Listbox(self.window, selectmode=tk.MULTIPLE, font=("Arial", 12))
        for coluna in colunas_disponiveis:
            self.listbox_colunas.insert(tk.END, coluna)
        self.listbox_colunas.pack()

        self.botao_consultar_colunas = tk.Button(self.window, text="Consultar \u2192", font=("Arial", 12), command=self.realizar_consulta_colunas)
        self.botao_consultar_colunas.pack(pady=5)

        self.botao_voltar = tk.Button(self.window, text="\u2190 Voltar", font=("Arial", 12), command=self.janela_consulta)
        self.botao_voltar.pack(pady=5)


    def atualizar_janela_consultas(self):
        self.limpar_janela()

        opcoes_menu = [d for d in os.listdir('consultas') if os.path.isdir(os.path.join('consultas', d))]
        if len(opcoes_menu) == 0:
            self.label_resultados = tk.Label(self.window, text="Não há resultados de consulta para exibir.", font=("Arial", 14))
            self.label_resultados.pack(pady=10)
        else:
            self.label_selecione = tk.Label(self.window, text="Selecione o tipo de consulta para exibir os resultados:", font=("Arial", 14))
            self.label_selecione.pack(pady=10)

            for i, opcao_menu in enumerate(opcoes_menu):
                botao_opcao = tk.Button(self.window, text=opcao_menu, font=("Arial", 12), command=lambda opc=opcao_menu: self.exibir_resultados_consulta(opc))
                botao_opcao.pack(pady=5)

        self.botao_voltar = tk.Button(self.window, text="\u2190 Voltar", font=("Arial", 12), command=self.janela_principal)
        self.botao_voltar.pack(pady=5)

    def exibir_resultados_consulta(self, tipo_consulta):
        resultados = exibir_resultados(tipo_consulta)
        if not resultados:
            messagebox.showinfo("Aviso", "Não há resultados para esta consulta.")
        else:
            self.limpar_janela()
            self.label_resultados = tk.Label(self.window, text="Resultados da consulta:")
            self.label_resultados.pack()

            text_box = tk.Text(self.window)
            text_box.pack()
            for resultado in resultados:
                text_box.insert(tk.END, resultado.strip() + "\n")

            self.botao_voltar = tk.Button(self.window, text="Voltar", command=self.atualizar_janela_consultas)
            self.botao_voltar.pack()


    def realizar_consulta_colunas(self):
        tabela = self.opcao_var.get()
        colunas = [self.listbox_colunas.get(idx) for idx in self.listbox_colunas.curselection()]

        if tabela == "pessoas":
            consultar_pessoas(colunas)
        elif tabela == "contas":
            consultar_contas(colunas)

    def janela_pessoas(self):
        # Limpar a janela atual
        self.limpar_janela()

        # Elementos da janela para a opção "PESSOAS"
        self.label_mensagem = tk.Label(self.window, text="Escolha uma opção:")
        self.label_mensagem.pack(pady=10)

        self.botao_adicionar_pessoa = tk.Button(self.window, text="Adicionar pessoa", font=("Arial", 12), command=self.adicionar_pessoa)
        self.botao_adicionar_pessoa.pack(pady=5)

        self.botao_remover_pessoa = tk.Button(self.window, text="Remover pessoa", font=("Arial", 12), command=self.remover_pessoa)
        self.botao_remover_pessoa.pack(pady=5)

        self.botao_editar_pessoa = tk.Button(self.window, text="Editar pessoa", font=("Arial", 12), command=self.editar_pessoa)
        self.botao_editar_pessoa.pack(pady=5)

        self.botao_mostrar_pessoas = tk.Button(self.window, text="Mostrar pessoas", font=("Arial", 12), command=self.mostrar_pessoas)
        self.botao_mostrar_pessoas.pack(pady=5)

        self.botao_voltar = tk.Button(self.window, text="\u2190 Voltar", font=("Arial", 12), command=self.janela_manipulador)
        self.botao_voltar.pack(pady=5)

    def mostrar_pessoas(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pessoas")
        pessoas = cursor.fetchall()

        # Definir o número de registros por página
        registros_por_pagina = 20

        # Calcular o número total de páginas
        num_paginas = (len(pessoas) + registros_por_pagina - 1) // registros_por_pagina

        # Variável para controlar a página atual
        pagina_atual = 1

        def exibir_pagina(pagina):
            nonlocal pagina_atual

            # Atualizar a página atual
            pagina_atual = pagina

            # Limpar a janela atual
            for widget in frame_tabela_info.winfo_children():
                widget.destroy()

            # Exibir as informações da página atual
            inicio = (pagina - 1) * registros_por_pagina
            fim = min(inicio + registros_por_pagina, len(pessoas))

            # Cabeçalho das colunas
            for j, coluna in enumerate(cursor.description):
                label_cabecalho = tk.Label(frame_tabela_info, text=coluna[0], width=15, anchor=tk.W, relief=tk.GROOVE,
                                        font=('Arial', 10, 'bold'))
                label_cabecalho.grid(row=0, column=j, sticky=tk.W, padx=5, pady=5)

            # Linhas de dados
            for i, pessoa in enumerate(pessoas[inicio:fim]):
                for j, valor in enumerate(pessoa):
                    label_valor = tk.Label(frame_tabela_info, text=valor, width=15, anchor=tk.W, relief=tk.GROOVE,
                                        font=('Arial', 10))
                    label_valor.grid(row=i + 1, column=j, sticky=tk.W, padx=5, pady=2)

        # Criar uma nova janela para exibir as informações
        janela_mostrar = tk.Toplevel(self.window)
        janela_mostrar.title("Pessoas")

        # Criar um frame para conter a tabela e a barra de rolagem
        frame_tabela = tk.Frame(janela_mostrar)
        frame_tabela.pack(fill=tk.BOTH, expand=True)

        # Criar uma barra de rolagem vertical
        scrollbar = tk.Scrollbar(frame_tabela)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Criar um canvas para conter a tabela e a barra de rolagem
        canvas = tk.Canvas(frame_tabela, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar a barra de rolagem para controlar o canvas
        scrollbar.config(command=canvas.yview)

        # Criar um frame para conter as informações da tabela
        frame_tabela_info = tk.Frame(canvas)
        frame_tabela_info.pack()

        # Exibir a primeira página
        exibir_pagina(1)

        def pagina_anterior():
            if pagina_atual > 1:
                exibir_pagina(pagina_atual - 1)

        def proxima_pagina():
            if pagina_atual < num_paginas:
                exibir_pagina(pagina_atual + 1)

        def ir_para_pagina(pagina):
            if 1 <= pagina <= num_paginas:
                exibir_pagina(pagina)

        # Criar campo de entrada e botão para seleção de página
        frame_selecao_pagina = tk.Frame(janela_mostrar)
        frame_selecao_pagina.pack(pady=10)


        # Criar cascata para seleção de página
        menu_paginas = tk.Menu(janela_mostrar)
        janela_mostrar.config(menu=menu_paginas)

        menu_paginas.add_command(label="Anterior", command=pagina_anterior)
        menu_paginas.add_command(label="Próxima", command=proxima_pagina)

        submenu_paginas = tk.Menu(menu_paginas, tearoff=0)
        menu_paginas.add_cascade(label="Ir para página", menu=submenu_paginas)

        for pagina in range(1, num_paginas + 1):
            submenu_paginas.add_command(label=f"Página {pagina}", command=lambda p=pagina: ir_para_pagina(p))

        # Permitir rolagem com a roda do mouse
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    
    def adicionar_pessoa(self):
        cpf = self.input_dialog("Insira o CPF")
        primeiro_nome = self.input_dialog("Insira o primeiro nome")
        nome_meio = self.input_dialog("Insira o nome do meio")
        sobrenome = self.input_dialog("Insira o sobrenome")
        idade = self.input_dialog("Insira a idade")
        conta = self.input_dialog("Insira o número da conta")

        conn = self.conn
        adicionar_pessoa(conn, cpf, primeiro_nome, nome_meio, sobrenome, idade, conta)
        
    def remover_pessoa(self):
        # Lógica para remover pessoa
        cpf = self.input_dialog("Insira o CPF da pessoa que deseja remover")
        conn = self.conn
        remover_pessoa(conn, cpf)
        # Chame sua função remover_pessoa(conn) aqui
        
    def editar_pessoa(self):
        # Lógica para editar pessoa
        cpf = self.input_dialog("Insira o CPF da pessoa que deseja editar")
        campos_disponiveis = "primeiro_nome, nome_meio, sobrenome, idade"
        msg = "Os campos disponíveis para edição são:\n" + campos_disponiveis
        fields = ["Digite o Campo desejado: "]
        field_values = multenterbox(msg, "Editar Pessoa", fields)
        
        if field_values:
            campo = field_values[0]
            novo_valor = self.input_dialog("Insira o novo valor")
            
            conn = self.conn
            editar_pessoa(conn, cpf, campo, novo_valor)
    
    

    def janela_contas(self):
        # Limpar a janela atual
        self.limpar_janela()

        # Elementos da janela para a opção "CONTAS"
        self.label_mensagem = tk.Label(self.window, text="Escolha uma opção:")
        self.label_mensagem.pack(pady=10)

        self.botao_adicionar_conta = tk.Button(self.window, text="Adicionar conta", font=("Arial", 12), command=self.adicionar_conta)
        self.botao_adicionar_conta.pack(pady=5)

        self.botao_remover_conta = tk.Button(self.window, text="Remover conta", font=("Arial", 12), command=self.remover_conta)
        self.botao_remover_conta.pack(pady=5)

        self.botao_editar_conta = tk.Button(self.window, text="Editar conta", font=("Arial", 12), command=self.editar_conta)
        self.botao_editar_conta.pack(pady=5)

        self.botao_mostrar_contas = tk.Button(self.window, text="Mostrar contas", font=("Arial", 12), command=self.mostrar_contas)
        self.botao_mostrar_contas.pack(pady=5)

        self.botao_voltar = tk.Button(self.window, text="\u2190 Voltar", font=("Arial", 12), command=self.janela_manipulador)
        self.botao_voltar.pack(pady=5)

    def mostrar_contas(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas")
        pessoas = cursor.fetchall()

        # Definir o número de registros por página
        registros_por_pagina = 30

        # Calcular o número total de páginas
        num_paginas = (len(pessoas) + registros_por_pagina - 1) // registros_por_pagina

        # Variável para controlar a página atual
        pagina_atual = 1

        def exibir_pagina(pagina):
            nonlocal pagina_atual

            # Atualizar a página atual
            pagina_atual = pagina

            # Limpar a janela atual
            for widget in frame_tabela_info.winfo_children():
                widget.destroy()

            # Exibir as informações da página atual
            inicio = (pagina - 1) * registros_por_pagina
            fim = min(inicio + registros_por_pagina, len(pessoas))

            # Cabeçalho das colunas
            for j, coluna in enumerate(cursor.description):
                label_cabecalho = tk.Label(frame_tabela_info, text=coluna[0], width=15, anchor=tk.W, relief=tk.GROOVE,
                                        font=('Arial', 10, 'bold'))
                label_cabecalho.grid(row=0, column=j, sticky=tk.W, padx=5, pady=5)

            # Linhas de dados
            for i, pessoa in enumerate(pessoas[inicio:fim]):
                for j, valor in enumerate(pessoa):
                    label_valor = tk.Label(frame_tabela_info, text=valor, width=15, anchor=tk.W, relief=tk.GROOVE,
                                        font=('Arial', 10))
                    label_valor.grid(row=i + 1, column=j, sticky=tk.W, padx=5, pady=2)

        # Criar uma nova janela para exibir as informações
        janela_mostrar = tk.Toplevel(self.window)
        janela_mostrar.title("Pessoas")

        # Criar um frame para conter a tabela e a barra de rolagem
        frame_tabela = tk.Frame(janela_mostrar)
        frame_tabela.pack(fill=tk.BOTH, expand=True)

        # Criar uma barra de rolagem vertical
        scrollbar = tk.Scrollbar(frame_tabela)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Criar um canvas para conter a tabela e a barra de rolagem
        canvas = tk.Canvas(frame_tabela, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar a barra de rolagem para controlar o canvas
        scrollbar.config(command=canvas.yview)

        # Criar um frame para conter as informações da tabela
        frame_tabela_info = tk.Frame(canvas)
        frame_tabela_info.pack()

        # Exibir a primeira página
        exibir_pagina(1)

        def pagina_anterior():
            if pagina_atual > 1:
                exibir_pagina(pagina_atual - 1)

        def proxima_pagina():
            if pagina_atual < num_paginas:
                exibir_pagina(pagina_atual + 1)

        def ir_para_pagina(pagina):
            if 1 <= pagina <= num_paginas:
                exibir_pagina(pagina)

        # Criar campo de entrada e botão para seleção de página
        frame_selecao_pagina = tk.Frame(janela_mostrar)
        frame_selecao_pagina.pack(pady=10)


        # Criar cascata para seleção de página
        menu_paginas = tk.Menu(janela_mostrar)
        janela_mostrar.config(menu=menu_paginas)

        menu_paginas.add_command(label="Anterior", command=pagina_anterior)
        menu_paginas.add_command(label="Próxima", command=proxima_pagina)

        submenu_paginas = tk.Menu(menu_paginas, tearoff=0)
        menu_paginas.add_cascade(label="Ir para página", menu=submenu_paginas)

        for pagina in range(1, num_paginas + 1):
            submenu_paginas.add_command(label=f"Página {pagina}", command=lambda p=pagina: ir_para_pagina(p))

        # Permitir rolagem com a roda do mouse
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def adicionar_conta(self):

        agencia = self.input_dialog("Insira a agencia")
        numero = self.input_dialog("Insira o numero da conta")
        saldo = self.input_dialog("Insira o saldo")
        gerente = self.input_dialog("Insira o id do gerente")
        titular = self.input_dialog("Insira o id do titular")
        conta = self.input_dialog("Insira o ID da Conta que deseja adicionar")

        conn = self.conn
        adicionar_conta(conn, agencia, numero, saldo, gerente, titular, conta)

    def remover_conta(self):
        conta = self.input_dialog("Insira o ID da Conta que deseja remover")

        conn = self.conn
        remover_conta(conn, conta)
        # Chame sua função remover_conta(conn) aqui

    def editar_conta(self):
        conta = self.input_dialog("Insira o ID da Conta que deseja editar")
        campos_disponiveis = "agencia, numero, saldo, gerente, titular"
        msg = "Os campos disponíveis para edição são:\n" + campos_disponiveis
        fields = ["Digite o Campo desejado: "]
        field_values = multenterbox(msg, "Editar Conta", fields)

        if field_values:
            campos_conta = field_values[0]
            novo_valor_conta = self.input_dialog("Insira o novo valor")
            
            conn = self.conn
            atualizar_conta(conn, conta, campos_conta, novo_valor_conta)
        # Chame sua função editar_conta(conn) aqui

    

    def input_dialog(self, label):
        result = enterbox(label)
        return result if result else ""
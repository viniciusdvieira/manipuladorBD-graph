import sqlite3
import os

def adicionar_pessoa(conn, cpf, primeiro_nome, nome_meio, sobrenome, idade, conta):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO pessoas(cpf, primeiro_nome, nome_meio, sobrenome, idade, conta) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (cpf, primeiro_nome, nome_meio, sobrenome, idade, conta))
        conn.commit()
        print('Pessoa adicionada com sucesso')
    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)
 

def remover_pessoa(conn,cpf):
    try:
        cursor = conn.cursor()
        query = "DELETE FROM pessoas WHERE cpf = ?"
        cursor.execute(query, (cpf,))
        conn.commit()
        print('Pessoa removida com sucesso')
    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)


def editar_pessoa(conn, cpf, campo, novo_valor):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM pessoas WHERE cpf = ?"
        cursor.execute(query, (cpf,))
        pessoa = cursor.fetchone()

        if pessoa is None:
            print("Pessoa não encontrada")
            return

        query = f"UPDATE pessoas SET {campo} = ? WHERE cpf = ?"
        cursor.execute(query, (novo_valor, cpf))
        conn.commit()
        print("Pessoa editada com sucesso")
    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)



def adicionar_conta(conn, agencia, numero, saldo, gerente, titular, conta):   
    try:
        cursor = conn.cursor()
        query = "INSERT INTO contas (agencia, numero, saldo, gerente, titular, conta) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (agencia, numero, saldo, gerente, titular, conta))
        conn.commit()
        print("Conta adicionada com sucesso!")
    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)

def remover_conta(conn,conta):
    try:
        cursor = conn.cursor()
        query = "DELETE FROM contas WHERE conta = ?"
        cursor.execute(query, (conta,))
        conn.commit()
        print("Conta removida com sucesso!")
    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)

def atualizar_conta(conn, conta,  campos_conta, novo_valor_conta):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM contas WHERE conta = ?"
        cursor.execute(query, (conta,))
        conto= cursor.fetchone()

        if conto is None:
            print("Conta não encontrada")
            return

        query = f"UPDATE contas SET {campos_conta} = ? WHERE conta = ?"
        cursor.execute(query, (novo_valor_conta, conta))
        conn.commit()
        print("Conta editada com sucesso!")
    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)



def salvar_resultados(resultados, tipo_consulta):
    pasta = f'consultas/{tipo_consulta}'
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    with open(f'{pasta}/resultados.txt', 'w') as arquivo:
        for resultado in resultados:
            arquivo.write(str(resultado) + '\n')



def exibir_resultados(tipo_consulta):
    pasta = f'consultas/{tipo_consulta}'
    resultados = []
    if not os.path.exists(pasta):
        return resultados
    with open(f'{pasta}/resultados.txt', 'r') as arquivo:
        resultados = arquivo.readlines()
    return resultados

def consultar_pessoas(colunas):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    colunas_disponiveis = obter_colunas_disponiveis('pessoas')
    colunas_validas = [coluna for coluna in colunas if coluna in colunas_disponiveis]
    colunas_selecionadas = ', '.join(colunas_validas) if colunas_validas else '*'

    consulta_sql = f"SELECT {colunas_selecionadas} FROM pessoas"
    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    tipo_consulta = f'consulta_por_{", ".join(colunas_validas)}' if colunas_validas else 'consulta_todas_colunas'
    salvar_resultados(resultados, tipo_consulta)
    print("Consulta bem sucedida")

def consultar_contas(colunas):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    colunas_disponiveis = obter_colunas_disponiveis('contas')
    colunas_validas = [coluna for coluna in colunas if coluna in colunas_disponiveis]
    colunas_selecionadas = ', '.join(colunas_validas) if colunas_validas else '*'

    consulta_sql = f"SELECT {colunas_selecionadas} FROM contas"
    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    tipo_consulta = f'consulta_por_{", ".join(colunas_validas)}' if colunas_validas else 'consulta_todas_colunas'
    salvar_resultados(resultados, tipo_consulta)
    print("Consulta bem sucedida")

def obter_colunas_disponiveis(tabela):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabela}")
    colunas = [coluna[0] for coluna in cursor.description]
    cursor.close()
    conn.close()
    return colunas
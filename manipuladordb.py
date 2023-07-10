import sqlite3
import os
from graph import InterfaceGrafica

def main():
    
    try:
        #botar a , no arquivo txt
        with open('nomes.txt','r') as f:
            lines = f.readlines()
            new_lines = []
            for line in lines:
                new_line = ','.join(line.strip().split())
                new_lines.append(new_line + '\n') 
            f.close()
        with open('nomes.txt','w') as f:
            f.writelines(new_lines)
            f.close()

        with open('contas.txt','r') as d:
            lines2 = d.readlines()
            new_lines = []
            for line in lines2:
                new_line = ','.join(line.strip().split())
                new_lines.append(new_line + '\n') 
            d.close()

        with open('contas.txt','w') as d:
            d.writelines(new_lines)
            d.close()

        #conectando o banco de daos e criando a tabela     
        conn = sqlite3.connect('database.db')
        print('Conexao com o BD bem sucedida')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas(
            cpf TEXT,
            primeiro_nome TEXT,
            nome_meio TEXT,
            sobrenome TEXT,
            idade INTEGER,
            conta INTEGER PRIMARY KEY
        ); 
        """)
        print("tabela pessoas criada")
        with open('nomes.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                values = line.strip().split(',')
                cpf, primeiro_nome, nome_meio, sobrenome, idade, conta = values
                query = "INSERT OR IGNORE INTO pessoas (cpf, primeiro_nome, nome_meio, sobrenome, idade, conta) VALUES (?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (cpf, primeiro_nome, nome_meio, sobrenome, idade, conta))

            f.close()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas(
            agencia TEXT,
            numero TEXT,
            saldo TEXT,
            gerente INTEGER,
            titular INTEGER,
            conta INTEGER,
            FOREIGN KEY(conta) REFERENCES pessoas(conta)
        );
        """)
        print("tabela contas criada")


        with open('contas.txt','r') as d:
            lines2 = d.readlines()
            for line in lines2:
                values = line.strip().split(',')
                agencia, numero, saldo, gerente, titular = values
                cursor.execute("SELECT conta FROM pessoas WHERE conta=?", (titular,))
                conta = cursor.fetchone()[0]
                query = "INSERT OR IGNORE INTO contas (agencia, numero, saldo, gerente, titular, conta) VALUES (?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (agencia, numero, saldo, gerente, titular, conta))
        d.close()

        

        conn.commit()
        cursor.close()
        
        interface = InterfaceGrafica(conn)
        interface.run()
    

    except sqlite3.Error as erro:
        print('Ocorreu um erro: ', erro)
    finally:
        if conn:
            conn.close()
            print('Conexão encerrada')
    
if __name__ == '__main__':
    main()



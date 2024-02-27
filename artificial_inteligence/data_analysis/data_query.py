import psycopg2
import pandas as pd

conexao_parametros = "dbname='postgres' user='postgres' password='$Pebav1la+' host='25.73.143.27'"

def bring_description(input_coluna, input_tabela):
    try:
        # Conecta ao banco de dados
        conexao = psycopg2.connect(conexao_parametros)

        cursor = conexao.cursor()
        
        consulta_sql = f"SELECT {input_coluna} FROM {input_tabela};"
        
        cursor.execute(consulta_sql)
        
        resultados = cursor.fetchall()
        
        #print(resultados)
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao acessar o banco de dados: {error}")
    finally:

        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
    return resultados

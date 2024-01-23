import yfinance as yf
import time
import datetime

def obter_dados_acoes_bovespa(intervalo_horas_coleta=0.03, simbolos_acoes=["PETR4.SA"]):  #Adicionar o resto das acoes como parametro base depois
    """
    Função para obter dados em tempo real das ações da Bovespa.
    Devolve dados das acoes e recomeca contagem depois que e excutada logica do programa.
    """
    # Lista dos símbolos das ações na Bovespa. 
    '''
    Adicionar lista com todas acoes da bovespa.
    '''

    dados_acoes = {}

    for simbolo in simbolos_acoes:
        acao = yf.Ticker(simbolo)
        dados_acoes[simbolo] = acao.history()


    print(f"{dados_acoes}--> Consulta e coleta realizadas com sucesso")

    return dados_acoes, main(intervalo_horas_coleta, dados_acoes)

def main(intervalo_horas_coleta = 0, dados_acoes={}):
    
# falta salvar esses dados em algum arquivo por enquanto so esta criando um dicionario q eh resetado a cada excecucao,
# logica pode ser essa mas add no bd





    """
    Timer para acompanhar o tempo de execucao do codigo.
    """
    # Tempo inicial para a contagem regressiva
    end_time = datetime.datetime.now() + datetime.timedelta(hours=intervalo_horas_coleta)

    # Ajuste de tempo de execucao para coleta de dados
    intervalo_horas_coleta = 0.03

    while True:

        # Calcula o tempo restante
        remaining_time = end_time - datetime.datetime.now()

        # Verifica se o tempo acabou
        if remaining_time.total_seconds() <= 0:
            print("00:00:00")
            break

        # Formata a saída para mostrar horas, minutos e segundos
        remaining_time_str = str(remaining_time).split('.')[0]  # Remove a parte de microsegundos
        print(remaining_time_str, end="\r")  # Usa '\r' para sobrescrever a linha atual no terminal
        time.sleep(1)  # Aguarda um segundo

    return obter_dados_acoes_bovespa(intervalo_horas_coleta)



# Exemplo de uso: Contagem regressiva de 0 segundo para iniciar o programa (default = 0 para comecar o programa coletando instantaneamente)
main()


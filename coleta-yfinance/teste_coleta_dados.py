import yfinance as yf
import time
import datetime

def obter_dados_acoes_bovespa(intervalo_horas_coleta=0.03, simbolos_acoes= ["PETR4.SA", 'SANB11.SA']):
    '''[ "ABEV3.SA",  # Ambev S.A.
    "AZUL4.SA",  # Azul S.A.
    "B3SA3.SA",  # B3 S.A. - Brasil, Bolsa, Balcão
    "BBAS3.SA",  # Banco do Brasil S.A.
    "BBDC3.SA",  # Banco Bradesco S.A.
    "BBDC4.SA",  # Banco Bradesco S.A.
    "BBSE3.SA",  # BB Seguridade Participações S.A.
    "BEEF3.SA",  # Minerva S.A.
    "BPAC11.SA", # Banco BTG Pactual S.A.
    "BRAP4.SA",  # Bradespar S.A.
    "BRDT3.SA",  # Petrobras Distribuidora S.A.
    "BRFS3.SA",  # BRF S.A.
    "BRKM5.SA",  # Braskem S.A.
    "BRML3.SA",  # BR Malls Participações S.A.
    "BTOW3.SA",  # B2W - Companhia Digital
    "CCRO3.SA",  # CCR S.A.
    "CIEL3.SA",  # Cielo S.A.
    "CMIG4.SA",  # CEMIG
    "COGN3.SA",  # Cogna Educação S.A.
    "CPFE3.SA",  # CPFL Energia S.A.
    "CRFB3.SA",  # Carrefour Brasil
    "CSAN3.SA",  # Cosan S.A.
    "CSNA3.SA",  # Companhia Siderúrgica Nacional
    "CVCB3.SA",  # CVC Brasil Operadora e Agência de Viagens S.A.
    "CYRE3.SA",  # Cyrela Brazil Realty S.A. Empreendimentos e Participações
    "ECOR3.SA",  # EcoRodovias Infraestrutura e Logística S.A.
    "EGIE3.SA",  # Engie Brasil Energia S.A.
    "ELET3.SA",  # Centrais Elétricas Brasileiras S.A. - Eletrobrás
    "ELET6.SA",  # Centrais Elétricas Brasileiras S.A. - Eletrobrás
    "EMBR3.SA",  # Embraer S.A.
    "ENBR3.SA",  # EDP Energias do Brasil S.A.
    "ENGI11.SA", # Energisa S.A.
    "EQTL3.SA",  # Equatorial Energia S.A.
    "FLRY3.SA",  # Fleury S.A.
    "GGBR4.SA",  # Gerdau S.A.
    "GNDI3.SA",  # Grupo Notre Dame Intermédica
    "GOAU4.SA",  # Metalúrgica Gerdau S.A.
    "GOLL4.SA",  # Gol Linhas Aéreas Inteligentes S.A.
    "HAPV3.SA",  # Hapvida Participações e Investimentos S.A.
    "HGTX3.SA",  # Cia. Hering
    "HYPE3.SA",  # Hypera Pharma
    "IGTA3.SA",  # Iguatemi Empresa de Shopping Centers S.A.
    "IRBR3.SA",  # IRB-Brasil Resseguros S.A.
    "ITSA4.SA",  # Itaúsa - Investimentos Itaú S.A.
    "ITUB4.SA",  # Itaú Unibanco Holding S.A.
    "JBSS3.SA",  # JBS S.A.
    "KLBN11.SA", # Klabin S.A.
    "LAME4.SA",  # Lojas Americanas S.A.
    "LREN3.SA",  # Lojas Renner S.A.
    "MGLU3.SA",  # Magazine Luiza S.A.
    "MRFG3.SA",  # Marfrig Global Foods S.A.
    "MRVE3.SA",  # MRV Engenharia e Participações S
    ]):'''  #Adicionar o resto das acoes como parametro base depois
    
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
        dados_acoes[simbolo+'_0'] = acao.history(period="2h", interval="1m")
        dados_acoes[simbolo+'_1'] = acao.actions
        dados_acoes[simbolo+'_3'] = acao.balance_sheet
        dados_acoes[simbolo+'_4'] = acao.basic_info
        dados_acoes[simbolo+'_5'] = acao.calendar
        dados_acoes[simbolo+'_6'] = acao.capital_gains
        dados_acoes[simbolo+'_7'] = acao.cash_flow
        dados_acoes[simbolo+'_8'] = acao.dividends
        dados_acoes[simbolo+'_10'] = acao.earnings_dates
        dados_acoes[simbolo+'_13'] = acao.fast_info
        dados_acoes[simbolo+'_14'] = acao.financials

        # Linhas de baixo ainda nao implementada na biblioteca
        ''' 
        dados_acoes[simbolo+'_2'] = acao.analyst_price_target
        #dados_acoes[simbolo+'_9'] = acao.earnings
        #dados_acoes[simbolo+'_11'] = acao.earnings_forecasts
        #dados_acoes[simbolo+'_12'] = acao.earnings_trend
        '''

    print(f"{dados_acoes}--> Consulta e coleta realizadas com sucesso")

    return dados_acoes

def main(intervalo_horas_coleta = 0, dados_acoes={}):
    
# falta salvar esses dados em algum arquivo por enquanto so esta criando um dicionario q eh resetado a cada excecucao,
# logica pode ser essa mas add no bd
    """
    Timer para acompanhar o tempo de execucao do codigo.
    """
    # Tempo inicial para a contagem regressiva
    end_time = datetime.datetime.now() + datetime.timedelta(hours=intervalo_horas_coleta)

    # Ajuste de tempo de execucao para coleta de dados
    intervalo_horas_coleta = 0.01

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


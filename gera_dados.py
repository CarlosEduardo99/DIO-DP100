import pandas as pd
import numpy as np

def gerar_dados_sorveteria(num_linhas=365):
    """Gera dados sintéticos para vendas de sorveteria."""

    datas = pd.date_range(start='2023-01-01', periods=num_linhas).tolist()
    temperaturas = np.random.uniform(25, 38, num_linhas).round(1)
    dias_semana = [data.strftime('%A') for data in datas]
    feriados = np.random.choice([True, False], num_linhas, p=[0.1, 0.9])
    eventos_especiais = np.random.choice([True, False], num_linhas, p=[0.05, 0.95])
    
    # Distribuição de vendas por sabor (varia com temperatura e eventos)
    vendas_morango = (50 + temperaturas * 2 + eventos_especiais * 30 + np.random.normal(0, 10, num_linhas)).round().astype(int)
    vendas_chocolate = (60 + temperaturas * 2.5 + eventos_especiais * 40 + np.random.normal(0, 12, num_linhas)).round().astype(int)
    vendas_limao = (20 + temperaturas * 1 + eventos_especiais * 15 + np.random.normal(0, 8, num_linhas)).round().astype(int)
    vendas_pistache = (15 + temperaturas * 0.8 + eventos_especiais * 10 + np.random.normal(0, 6, num_linhas)).round().astype(int)
    vendas_maracuja = (18 + temperaturas * 0.9 + eventos_especiais * 12 + np.random.normal(0, 7, num_linhas)).round().astype(int)
    vendas_total = vendas_morango + vendas_chocolate + vendas_limao + vendas_pistache + vendas_maracuja

    dados = {
        'date': datas,
        'temp': temperaturas,
        'week_day': dias_semana,
        'holiday': feriados,
        'event': eventos_especiais,
        'strawberry': vendas_morango,
        'chocolate': vendas_chocolate,
        'lemon': vendas_limao,
        'grape': vendas_pistache,
        'mango': vendas_maracuja,
        'total': vendas_total
    }

    df = pd.DataFrame(dados)
    return df

# Gere e salve a tabela em formato CSV
tabela_sorveteria = gerar_dados_sorveteria()
tabela_sorveteria.to_csv("vendas_sorveteria.csv", index=False) #salva o arquivo no mesmo diretório em que o script está localizado

print("Tabela salva em vendas_sorveteria.csv")
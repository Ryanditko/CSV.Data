import pandas as pd
import os
import logging

logging.basicConfig(filename='verificação.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def detectar_separador(caminho):
    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
        linha = f.readline()
        for sep in [',', ';', '\t']:
            if sep in linha:
                return sep
    return ','

def limpar_colunas(df):
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df

def tratar_dados(df):
    # Limpa caracteres não padrão
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].map(lambda x: ''.join([c for c in str(x) if ord(c) < 128 or (0x00C0 <= ord(c) <= 0x00FF)]) if isinstance(x, str) else x)
    df = df.dropna(how='all', axis=1)  # Remove colunas totalmente vazias
    df = df.drop_duplicates()
    return df

def processar_csv(arquivo):
    try:
        sep = detectar_separador(arquivo)
        try:
            df = pd.read_csv(arquivo, encoding='utf-8', sep=sep)
        except UnicodeDecodeError:
            df = pd.read_csv(arquivo, encoding='latin-1', sep=sep)
    except Exception as e:
        logging.error(f'Erro ao ler {arquivo}: {e}')
        return False

    df = limpar_colunas(df)
    df = tratar_dados(df)

    try:
        df.to_csv(arquivo, index=False, encoding='utf-8-sig', sep=',')
        logging.info(f'Arquivo processado com sucesso: {arquivo}')
        return True
    except Exception as e:
        logging.error(f'Erro ao salvar {arquivo}: {e}')
        return False

def main():
    for arquivo in os.listdir('.'):
        if arquivo.lower().endswith('.csv'):
            processar_csv(arquivo)

if __name__ == "__main__":
    main() 
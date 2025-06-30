import pandas as pd
import os

def ler_csv_com_fallback(caminho):
    # Tenta ler em UTF-8, se falhar tenta Latin-1
    try:
        return pd.read_csv(caminho, encoding='utf-8', sep=None, engine='python')
    except UnicodeDecodeError:
        try:
            return pd.read_csv(caminho, encoding='latin-1', sep=None, engine='python')
        except Exception as e:
            print(f'Erro ao ler {caminho}: {e}')
            return None

# Lista todos os arquivos do diretório atual
for arquivo in os.listdir('.'):
    if arquivo.lower().endswith('.csv'):
        nome_base = os.path.splitext(arquivo)[0]
        caminho_csv = arquivo
        caminho_excel = f'{nome_base}.xlsx'
        caminho_csv_utf8 = f'{nome_base}_utf8.csv'
        df = ler_csv_com_fallback(caminho_csv)
        if df is not None:
            # Limpa caracteres não padrão
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].map(lambda x: ''.join([c for c in str(x) if ord(c) < 128 or (0x00C0 <= ord(c) <= 0x00FF)]) if isinstance(x, str) else x)
            # Salva como Excel
            try:
                df.to_excel(caminho_excel, index=False, engine='openpyxl')
                print(f'Arquivo convertido com sucesso: {caminho_excel}')
            except Exception as e:
                print(f'Erro ao converter {arquivo} para Excel: {e}')
            # Salva como CSV UTF-8 com BOM e separador vírgula
            try:
                df.to_csv(caminho_csv_utf8, index=False, encoding='utf-8-sig', sep=',')
                print(f'Arquivo salvo como CSV UTF-8: {caminho_csv_utf8}')
            except Exception as e2:
                print(f'Erro ao salvar {arquivo} como CSV UTF-8: {e2}')
        else:
            print(f'Falha ao processar {arquivo}')
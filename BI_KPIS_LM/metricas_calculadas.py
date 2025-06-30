import pandas as pd
import os
import logging
from datetime import datetime, timedelta
import numpy as np

logging.basicConfig(filename='metricas.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def converter_tempo_para_segundos(tempo_str):
    """Converte string de tempo (HH:MM:SS) para segundos"""
    try:
        if pd.isna(tempo_str) or tempo_str == '':
            return None
        
        # Se já é um número, assume que é segundos
        if isinstance(tempo_str, (int, float)):
            return float(tempo_str)
        
        # Se é string, tenta converter
        if isinstance(tempo_str, str):
            # Remove espaços e caracteres especiais
            tempo_str = tempo_str.strip()
            
            # Se contém apenas números, assume segundos
            if tempo_str.replace('.', '').replace(',', '').isdigit():
                return float(tempo_str.replace(',', '.'))
            
            # Tenta formatos de tempo
            if ':' in tempo_str:
                partes = tempo_str.split(':')
                if len(partes) == 3:  # HH:MM:SS
                    horas, minutos, segundos = map(float, partes)
                    return horas * 3600 + minutos * 60 + segundos
                elif len(partes) == 2:  # MM:SS
                    minutos, segundos = map(float, partes)
                    return minutos * 60 + segundos
        
        return None
    except:
        return None

def calcular_tme_tmt(df, coluna_tempo):
    """Calcula TME/TMT baseado na fórmula DAX fornecida"""
    if coluna_tempo not in df.columns:
        logging.warning(f'Coluna {coluna_tempo} não encontrada')
        return df
    
    # Converte para segundos
    df[f'{coluna_tempo}_segundos'] = df[coluna_tempo].apply(converter_tempo_para_segundos)
    
    # Filtra valores válidos (> 5 segundos)
    df_filtrado = df[df[f'{coluna_tempo}_segundos'] > 5].copy()
    
    if len(df_filtrado) > 0:
        # Calcula média ponderada
        media_segundos = df_filtrado[f'{coluna_tempo}_segundos'].mean()
        
        # Converte para formato HH:MM:SS
        horas = int(media_segundos // 3600)
        minutos = int((media_segundos % 3600) // 60)
        segundos = int(media_segundos % 60)
        
        tme_formatado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        
        # Adiciona coluna calculada
        df[f'{coluna_tempo}_tme_tmt'] = tme_formatado
        df[f'{coluna_tempo}_media_segundos'] = media_segundos
    else:
        df[f'{coluna_tempo}_tme_tmt'] = "00:00:00"
        df[f'{coluna_tempo}_media_segundos'] = 0
    
    return df

def calcular_rechamadas(df, coluna_identificador):
    """Calcula quantidade de rechamadas baseado na fórmula DAX"""
    if coluna_identificador not in df.columns:
        logging.warning(f'Coluna {coluna_identificador} não encontrada')
        return df
    
    # Conta ocorrências por identificador
    contagem = df[coluna_identificador].value_counts()
    
    # Identifica rechamadas (> 1 ocorrência)
    rechamadas = contagem[contagem > 1]
    
    # Adiciona coluna indicando se é rechamada
    df[f'{coluna_identificador}_qtd_ocorrencias'] = df[coluna_identificador].map(contagem)
    df[f'{coluna_identificador}_eh_rechamada'] = df[f'{coluna_identificador}_qtd_ocorrencias'] > 1
    
    # Calcula métricas agregadas
    qtd_rechamadas = len(rechamadas)
    qtd_clientes_unicos = len(contagem[contagem == 1])
    
    # Adiciona colunas de métricas
    df[f'{coluna_identificador}_qtd_rechamadas_total'] = qtd_rechamadas
    df[f'{coluna_identificador}_qtd_clientes_unicos'] = qtd_clientes_unicos
    
    return df

def processar_metricas_especificas(df, nome_arquivo):
    """Aplica métricas específicas baseadas no tipo de arquivo"""
    
    # Para arquivos de voz (TME/TMT)
    if 'voz' in nome_arquivo.lower():
        # Procura por colunas de tempo
        colunas_tempo = [col for col in df.columns if any(palavra in col.lower() for palavra in ['tempo', 'duracao', 'tme', 'tmt', 'time'])]
        
        for col in colunas_tempo:
            df = calcular_tme_tmt(df, col)
    
    # Para arquivos de interações (rechamadas e clientes únicos)
    if 'intera' in nome_arquivo.lower() or 'todas as filas' in nome_arquivo.lower():
        # Procura por colunas de identificação
        colunas_id = [col for col in df.columns if any(palavra in col.lower() for palavra in ['ani', 'marca', 'identificador', 'cliente'])]
        
        for col in colunas_id:
            df = calcular_rechamadas(df, col)
    
    return df

def processar_csv_com_metricas(arquivo):
    """Processa um arquivo CSV aplicando as métricas calculadas"""
    try:
        # Lê o arquivo
        df = pd.read_csv(arquivo, encoding='utf-8-sig')
        
        # Aplica métricas específicas
        df = processar_metricas_especificas(df, arquivo)
        
        # Salva o arquivo com as métricas
        df.to_csv(arquivo, index=False, encoding='utf-8-sig', sep=',')
        logging.info(f'Métricas aplicadas com sucesso: {arquivo}')
        return True
        
    except Exception as e:
        logging.error(f'Erro ao processar métricas em {arquivo}: {e}')
        return False

def main():
    """Processa todos os arquivos CSV aplicando as métricas"""
    for arquivo in os.listdir('.'):
        if arquivo.lower().endswith('.csv'):
            processar_csv_com_metricas(arquivo)

if __name__ == "__main__":
    main() 
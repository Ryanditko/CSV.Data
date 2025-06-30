# BI For LOOKER STUDIO / DATA STUDIO

Projeto de tratamento e preparação de bases de dados para análise em BI (Looker Studio e Power BI).

## Objetivo

Automatizar a limpeza, padronização e cálculo de métricas em arquivos CSV para facilitar a análise de dados em ferramentas de BI, especialmente Looker Studio (Google Data Studio) e Power BI.

## Estrutura do Projeto

- `main.py`: Script para limpeza e padronização dos arquivos CSV.
- `metricas_calculadas.py`: Script para cálculo de métricas específicas (TME, TMT, Rechamadas, Clientes Únicos) e geração de colunas prontas para uso no Looker Studio.
- Arquivos CSV: Bases de dados a serem tratadas.

## Como Usar

1. **Instale as dependências:**

```bash
pip install pandas numpy
```

2. **Coloque os arquivos CSV na mesma pasta dos scripts.**

3. **Execute a limpeza básica:**

```bash
python main.py
```

4. **Execute o cálculo das métricas:**

```bash
python metricas_calculadas.py
```

5. **Importe os arquivos CSV tratados no Looker Studio ou Power BI.**

## O que cada script faz

### main.py
- Detecta automaticamente o separador dos arquivos CSV.
- Remove colunas totalmente vazias e linhas duplicadas.
- Limpa caracteres especiais e padroniza nomes das colunas.
- Salva os arquivos limpos em UTF-8.

### metricas_calculadas.py
- Calcula métricas como TME, TMT, Rechamadas e Clientes Únicos.
- Cria colunas prontas para uso direto em dashboards do Looker Studio.
- Gera logs de processamento para acompanhamento.

## Dicas para o Looker Studio
- Após rodar os scripts, basta importar os arquivos CSV no Looker Studio.
- As colunas calculadas já estarão disponíveis para uso em gráficos e tabelas.
- Não é necessário criar fórmulas complexas no Looker Studio, pois o tratamento já foi feito no Python.


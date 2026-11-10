import logging
import time
import requests
import json
from pathlib import Path
from datetime import date, timedelta

URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_page(params):
    for tentativa in range(3):
        try:
            
            r = requests.get(URL, params=params, timeout=30)
            r.raise_for_status()
            if r.status_code == 204:
                logger.info("A pesquisa está vazia")
                return {"data": [], "totalRegistros": 0, "totalPaginas": 0}

            return r.json()
        except(requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning("Tentativa %s falhou (rede ou timeout)", tentativa + 1)
            if tentativa < 2:
                time.sleep(2**tentativa)
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 429:
                espera = int(e.response.headers.get("Retry-After", 10 * (tentativa + 1)))
                logger.warning("429: aguardando %ss (tentativa %s)", espera, tentativa + 1)
                time.sleep(espera)
                continue
            elif 400 <= status < 500:
                logger.warning("Status %s: pedido inválido, não adianta tentar de novo", status) 
                raise
            elif status >= 500:
                logger.warning("Status %s: erro no servidor (tentativa %s)", status, tentativa + 1)
                if tentativa < 2:
                    time.sleep(2**tentativa)
    logger.error("Desisti depois de 3 tentativas")
    raise RuntimeError("Desisti depois de 3 tentativas")

def fetch_all_pages(params):
    primeira = fetch_page(params)
    total_paginas = primeira["totalPaginas"]
    logger.info("total de páginas: %s", total_paginas)
    logger.info("totalRegistros da API: %s", primeira["totalRegistros"])

    todos = []
    todos.extend(primeira["data"])

    for pagina in range(2, total_paginas + 1):
        copia = params.copy()
        copia["pagina"] = pagina      
        time.sleep(1)
        nova_pagina = fetch_page(copia)
        todos.extend(nova_pagina["data"])

    return todos

def gerar_janelas(inicio,fim):
    janelas = []
    data_atual = inicio

    while data_atual <= fim:
        data_final = data_atual + timedelta(days=6)
        data_final = min(data_final, fim)

        janelas.append((data_atual, data_final))

        data_atual = data_final + timedelta(days=1)

    return janelas

if __name__ == "__main__":

    pasta_raw = Path("data/raw")
    pasta_raw.mkdir(parents=True, exist_ok=True)

    hoje = date.today()
    inicio = hoje - timedelta(days=89)

    modalidades = [6, 8]
    janelas = gerar_janelas(inicio, hoje)

    for data_inicial, data_final in janelas:
        for modalidade in modalidades:

            nome_arquivo = f"licitacoes_{modalidade}_{data_inicial.strftime('%Y%m%d')}_{data_final.strftime('%Y%m%d')}.json"
            arquivo = pasta_raw / nome_arquivo

            if arquivo.exists():
                logger.info("Já existe, pulando: %s", arquivo.name)
                continue

            params = {
                "dataInicial": data_inicial.strftime("%Y%m%d"),
                "dataFinal": data_final.strftime("%Y%m%d"),
                "codigoModalidadeContratacao": modalidade,
                "codigoMunicipioIbge": "2507507",
                "pagina": 1,
                "tamanhoPagina": 50,
            }

            dados = fetch_all_pages(params)
            logger.info("Total coletado: %s", len(dados))

            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)

            time.sleep(1)
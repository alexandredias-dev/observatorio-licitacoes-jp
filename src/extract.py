import logging
import time
import requests
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
            if 400 <= status < 500:
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
        params["pagina"] = pagina      
        time.sleep(1)
        nova_pagina = fetch_page(params)
        todos.extend(nova_pagina["data"])

    return todos


if __name__ == "__main__":

    hoje = date.today()
    inicio = hoje - timedelta(days=30)

    params = { 
        "dataInicial" : inicio.strftime("%Y%m%d"),
        "dataFinal" : hoje.strftime("%Y%m%d"),
        "codigoModalidadeContratacao" : 6,
        "codigoMunicipioIbge": "2507507",
        "pagina" : 1,
        "tamanhoPagina" : 50,
    }

    dados = fetch_all_pages(params)
    logger.info("Total coletado: %s", len(dados))
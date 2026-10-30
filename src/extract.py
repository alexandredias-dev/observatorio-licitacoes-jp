import logging
import time
import requests
from datetime import date, timedelta

#URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
URL = "https://httpbin.org/status/204"


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


if __name__ == "__main__":

    hoje = date.today()
    inicio = hoje - timedelta(days=7)

    params = { 
        "dataInicial" : inicio.strftime("%Y%m%d"),
        "dataFinal" : hoje.strftime("%Y%m%d"),
        "codigoModalidadeContratacao" : 6,
        "codigoMunicipioIbge": "2507507",
        "pagina" : 1,
        "tamanhoPagina" : 50,
    }

    dados = fetch_page(params)
    logger.info("Total de Registros %s", dados["totalRegistros"])
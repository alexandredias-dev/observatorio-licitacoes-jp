import logging
import time
import requests
from datetime import date, timedelta

URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_page(params):
    r = requests.get(URL, params=params, timeout=30)
    r.raise_for_status()

    return r.json()


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
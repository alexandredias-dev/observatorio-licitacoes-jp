import requests
import pandas as pd
from datetime import date, timedelta

URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"

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

r = requests.get(URL, params=params)
print("Status:", r.status_code)

r.raise_for_status()

dados = r.json()
print(type(dados))
print(dados.keys())

print("total de registros:", dados["totalRegistros"])
print("registros nesta pagina:", len(dados["data"]))

df = pd.json_normalize(dados["data"])

print(df.shape)
print(df.columns.tolist())

print(df.isna().sum().sort_values(ascending=False).head(5))

print(df.value_counts("orgaoEntidade.razaoSocial").head(5))

print(df["orgaoEntidade.esferaId"].value_counts().head(5))

esfera_n = df["orgaoEntidade.esferaId"] == "N"
caras = df[esfera_n]
orgaos_n = caras["orgaoEntidade.razaoSocial"]
print(orgaos_n.value_counts())

data = pd.to_datetime(df["dataInclusao"])
print(data.min())
print(data.max())

print(df["valorTotalEstimado"].dtype)
print(df["valorTotalEstimado"].head())

agrupado = df.groupby("orgaoEntidade.razaoSocial")["valorTotalEstimado"]
print(agrupado.sum().sort_values(ascending=False).head(5))



print(df.shape)
print(df.columns)
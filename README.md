# observatorio-licitacoes-jp

## Colunas escolhidas

De 45 colunas retornadas pela API, 15 foram mantidas.

| Nome na API | Nome novo | Por que escolhi |
|---|---|---|
| numeroControlePNCP | numero_controle_pncp | Chave única de cada compra; usada para deduplicar no upsert |
| objetoCompra | objeto_compra | Descreve o que foi comprado; útil para mostrar ao cidadão no painel |
| dataPublicacaoPncp | data_publicacao_pncp | Define o mês de publicação (pergunta 1) |
| dataInclusao | data_inclusao | Data de entrada no sistema; comparar com a publicação |    
| dataAtualizacao | data_atualizacao | Critério para manter o registro mais recente no upsert |
| dataAberturaProposta | data_abertura_proposta | Mostra quando a disputa abre; contexto da compra |
| orgaoEntidade.cnpj | orgao_cnpj | Identificador estável do órgão, mais confiável que o nome; usado na extração de contratos |
| orgaoEntidade.razaoSocial | orgao_razao_social | Nome legível do órgão para o ranking (pergunta 2) |
| orgaoEntidade.esferaId | orgao_esfera_id | Filtro de escopo (M, E, F, N) |
| unidadeOrgao.nomeUnidade | unidade_nome | Mostra qual unidade dentro do órgão comprou |
| valorTotalEstimado | valor_total_estimado | Valor das compras por mês e por órgão (perguntas 1 e 2) |
| valorTotalHomologado | valor_total_homologado | Permite comparar estimado vs homologado; nulo se não homologada |
| modalidadeId | modalidade_id | Código estável para classificar dispensa vs pregão no SQL (pergunta 3) |
| modalidadeNome | modalidade_nome | Texto legível para os rótulos do painel |
| situacaoCompraNome | situacao_compra_nome | Mostra se a compra foi homologada, revogada etc. |
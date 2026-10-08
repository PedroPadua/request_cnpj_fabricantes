
# Classificador de Empresas Industriais

Automação em Python que consulta dados de CNPJ na [cnpj.ws](https://cnpj.ws)
e classifica empresas como industriais a partir das descrições de suas
atividades econômicas (CNAE principal e secundárias).

## O que faz

- Consulta cada CNPJ na API pública da cnpj.ws (com tratamento de 404 e rate limit)
- Verifica se a atividade principal e as secundárias contêm termos industriais
  (Fabricação, Montagem, Processamento, Beneficiamento...)
- Consolida o resultado em uma linha por empresa, no formato wide:
  cada tipo de tarefa/licença vira uma coluna com seu vencimento

## Stack

- `requests` — consumo da API
- `pandas` — normalização, deduplicação e pivot dos dados
- Saída em `.xlsx`

## Estrutura

- `utils/exceptions.py` — exceções próprias (`CNPJNaoEncontrado`, `RateLimitError`)
- `Fabricantes` — classe com requisição e análise de atividades

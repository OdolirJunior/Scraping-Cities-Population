# Neoway
Projeto Datapirates

## Executando o Projeto

Você pode executar o projeto usando o comando: 
    `py imdb_scraping.py` 
Desde que esteja acessando a raiz do projeto. 

## Dependências para a execução: 
  
Para executar o projeto é necesário que as seguintes bibliotecas estejam instaladas previamente:
    `from warnings import warn`
    `from requests import get`
    `from bs4 import BeautifulSoup`
    `import json`

## Requisitos do projeto:

Dentre todos os requisitos solicitados, somente a exportação para arquivos JSONL não foi atendida. Pois a arquitetura inicial foi pensada utilizando BeautifulSoup que posteriormente identifiquei que não possuia compatibilidade com JSONL.  
No entanto esta sendo gerado exportação para arquivos JSON. 

## Aprendizado: 

Buscar pensar na aplicação de forma geral, antes de executar a  codificação, pois assim percebi que poderia ter utilizado a biblioteca Scrapy, que possui compatibilidade com JSONL. 
Porem, devido ao prazo de entrega, essa alteração não foi possivel. 

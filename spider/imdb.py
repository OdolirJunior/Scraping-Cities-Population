from warnings import warn
from requests import get
from bs4 import BeautifulSoup
import json


def format_to_use_json(filme):
    filme_formated = []
    imdb = {'imdb': float(filme[0])}
    name = {'name': filme[1]}
    genre = {'genre': filme[2]}
    filme_formated.append([imdb, name, genre])
    return filme_formated


class ImdbSpider(object):

    def scraping(self):
        filmes = []
        requests = 0
        pages = [str(i) for i in range(1, 11)]
        headers = {"Accept-Language": "en-US,en;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"}
        for page in pages:
                response = get('http://www.imdb.com/search/title?&sort=num_votes,desc&page=' + page, headers = headers)
                if response.status_code != 200:
                    warn('Request: {}; Status code: {}'.format(requests, response.status_code))
                page_html = BeautifulSoup(response.text, 'html.parser')
                mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
                for container in mv_containers:
                    requests += 1
                    imdb = float(container.strong.text)
                    name = container.h3.a.text
                    genre = container.find('span', class_='genre').text
                    genre = ''.join(genre.split())
                    genre = genre.split(',')
                    filmes.append([imdb, name, genre])
                print('Quantidade de titulos obtidos ate o momento: %s'% (requests))
        ordenado = sorted(filmes, key=lambda row: row[0])
        return ordenado

    def separa_genero(self):
        filmes_por_genero = {}
        format=[]
        for filme in self:
            generos = filme[2]
            for genero in generos:
                if genero in filmes_por_genero:
                    format = format_to_use_json(filme)
                    filmes_por_genero[genero].append(format)
                else:
                    format = format_to_use_json(filme)
                    filmes_por_genero[genero] = [format]
        return filmes_por_genero


    def salva_json(filmes_por_genero):
        dict_key = filmes_por_genero.keys()
        for filmes in filmes_por_genero:
            if dict_key.__contains__(filmes):
                with open('JSONs/%s.json'% (filmes), 'w') as fp:
                    json.dump(filmes_por_genero[filmes], fp)

        print('Arquivos JSONs gerados')





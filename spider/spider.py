import time
import unicodedata

import requests
from lxml import html
from requests import get
import json

from cities_state import cities



def format_to_use_json(filme):
    json_create ={filme[0]+'-'+filme[1]:
        {
        'UF': filme[0],
        'city': filme[1],
        'quantidade': filme[2],
        'Data_ultimo_censo': filme[3],
        'Pop_estimada_2018': filme[4]}
    }
    return json_create

def remover_acentos(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    text = text.replace(' ', '-').lower()
    text = text.replace('\'', '')
    return text



class Spider(object):
    def scraping(self):
        global pop_ultimo_censo, dt_ultimo_censo_norm, pop_estimada_norm
        i = 0
        result = []
        final = {}
        cities_dict = cities()
        pop_ultimo_censo = None
        dt_ultimo_censo_norm = None
        pop_estimada_norm = None

        for uf in cities_dict['estados']:
            uf_normalize = remover_acentos(uf['sigla'])
            print('Estado: '+ str(uf['nome']))
            for city in uf['cidades']:
                city_normalize = remover_acentos(city)
                url = 'https://cidades.ibge.gov.br/brasil/'+uf_normalize+'/'+city_normalize+'/panorama'
                print(url)
                time.sleep(3)
                try:
                    response = get(url,timeout=10)
                except:
                    while response.status_code != 200:
                        print('repetindo...')
                        response = get(url)
                tree = html.fromstring(response.content)
                buyers = tree.xpath('//*[@id="dados"]/panorama-resumo/table/tr[4]/td[3]/text()')
                if buyers:
                    pop_ultimo_censo = buyers[0].replace(' ','').replace('\n','')
                dt_ultimo_censo = tree.xpath('//*[@id="dados"]/panorama-resumo/table/tr[4]/td[2]/small/text()')
                if dt_ultimo_censo:
                    dt_ultimo_censo_norm = dt_ultimo_censo[0].replace(' ', '').replace('\n', '')
                pop_estimada = tree.xpath('//*[@id="dados"]/panorama-resumo/table/tr[2]/td[3]/text()')
                if pop_estimada:
                    pop_estimada_norm = pop_estimada[0].replace(' ','').replace('\n','')

                result.append(uf_normalize)
                result.append(city_normalize)
                result.append(pop_ultimo_censo)
                result.append(dt_ultimo_censo_norm)
                result.append(pop_estimada_norm)
                print('salvando... ' + str(i))
                i+=1
                formatted = format_to_use_json(result)
                result=[]
                final.update(formatted)
        with open('cities.json', 'w') as fp:
            json.dump(final, fp)
        print('Arquivos JSONs gerados')





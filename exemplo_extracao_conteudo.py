import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
pag = http.request('GET', 'https://pt.wikipedia.org/wiki/M%C3%A1rcio_Fran%C3%A7a')

sopa = BeautifulSoup(pag.data, 'lxml')

for tags in sopa(['script', 'style']): #comandos js/tags do css
    tags.decompose() #remover todo o conteúdo da tag
    
conteudo = ' '.join(sopa.stripped_strings) #O método do sopa pega todas as strings do documento e remove os espaços em branco
#O espaço em branco antes do join ordena que para cada palavra adicionada, se adicione um espaço entre elas (para não ficar tudo grudado)
    
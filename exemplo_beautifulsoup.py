from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Desabilitar avisos (especificamente por causa do erro de certificações)
http = urllib3.PoolManager()
pag = http.request('GET', 'https://g1.globo.com')
pag.status

sopa = BeautifulSoup(pag.data, 'lxml') #Pegando conteúdo da página
#lxml = Parser do html para o retorno da função (fazer análise do documento, separar tags, etc)

sopa # = pag.data, porém sem formatação

sopa.title.string #Retorna o título da página, sem as tags

links = sopa.find_all('a') #pega todos os links da página

for link in links: #retornando todos os links encontrados na página / nome
    print(link.get('href'), link.contents)

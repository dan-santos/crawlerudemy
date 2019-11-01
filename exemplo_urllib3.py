import urllib3

http = urllib3.PoolManager() #PoolManager = fazer requisição http/Pegar conteúdo da página

pag = http.request('GET', 'https://g1.globo.com')

pag.status #Se ao rodar, o console der o código 2oo, é porque a conexão foi bem sucedida e conteúdo da pag foi pego

pag.data #retorna todo o código html da página
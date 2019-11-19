import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin #para colocar o https no início de todo 'href' das tags 'a' da página
import re
import nltk
import pymysql
#Aqui, e necessario conectar a aplicacao ao banco de dados. Para isso, devemos abrir o anaconda prompt
#e digitar o seguinte comando: conda install pymysql. Eh uma biblioteca do python responsavel pela conexao
def paginaIndexada(url):
    retorno = -1 #-1 = nao existe a pagina
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='indice')
    #maquina, user, senha, banco
    cursorUrl = conexao.cursor()
    #cursor = objeto para realizar consultas sql
    cursorUrl.execute('select idurl from urls where url = %s', url)
    if cursorUrl.rowcount > 0: #se retornou mais de 0 linhas, eh pq existe registro
        #print('url cadastrada')
        idUrl = cursorUrl.fetchone()[0] #pegando id do primeiro valor
        cursorPalavra = conexao.cursor()
        cursorPalavra.execute('select idurl from palavra_localizacao where idurl = %s', idUrl)
        if cursorPalavra.rowcount > 0:
            #print('url com palavras')
            retorno = -2 #-2 = existe pag com palavras cadastradas
        else:
            #print('url sem palavras')
            retorno = idUrl #existe a pag sem palavras
        cursorPalavra.close()
    #else:
        #print('url nao cadastrada')
    cursorUrl.close()
    conexao.close()
    return retorno
    
paginaIndexada('teste')
    
#Separa palavras, remove stopwords e considera apenas os radicais da palavra
def separaPalavras(texto):
    stopW = nltk.corpus.stopwords.words('portuguese')
    stemmer = nltk.stem.RSLPStemmer()
    splitter = re.compile('\\W+')
    
    listaPalavras = []
    lista = [p for p in splitter.split(texto) if p != '']

    for p in lista:
        if p.lower() not in stopW: 
            if len(p) > 1:   
                listaPalavras.append(stemmer.stem(p).lower())
    return listaPalavras
    
#Tira as tags html/css/js
def getTexto(sopa): 
    for tags in sopa(['script', 'style']): #comandos js/tags do css
        tags.decompose() #remover todo o conteúdo da tag
    
    return ' '.join(sopa.stripped_strings)

#TRATAMENTO DE LINKS
def crawler(pags, profundidade):
    #Profundidade = 1: Só executa a página passada como parâmetro
    #Profundidade = 2: Exceuta todas as páginas com links válidos
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    for i in range(profundidade):
        
        novasPaginas = set()
        for pag in pags: #Vai rodar por todas as páginas encontradas
            http = urllib3.PoolManager()
            try:
                dados_pag = http.request('GET', pag)
            except:
                print("Erro ao abrir a página " + pag)
                continue
                
            sopa = BeautifulSoup(dados_pag.data, 'lxml')
            links = sopa.find_all('a')
            #contador = 0 #links no total
            #contadorLink = 0 #links com o href
            #contadorRel = 0 #Links com href relativo (sem o início do link)
            for link in links :
                #print(str(link.contents) + ' - ' + str(link.get('href')))
                #link.contents = Nome do link
                #Notamos que nem todos os links possuem o atributo 'href', logo, nem sempre saberemos para onde o link aponta
                print(link.attrs)#todos os atributos da variável link
                print('\n')
                
                if('href' in link.attrs):
                    url = urljoin(pag, str(link.get('href')))
                    #basicamente o que a linha superir faz é concatenar uma url base com uma url relativa
                    #por exemplo, 'https://www.wikipedia.com/ é a url base, tudo que vem depois do / ao final do link
                    #principal é considerado url relativa. O urljoin verifica se o atributo href do link precisa ou não
                    #do começo do link, visto que nem todos os href vêm completos, um prérequisito para que tudo funcione direito
                    if(url.find("'") != -1):# Se encontrou url com apóstrofo (') é pq ela é invalida e não deve ser contada
                        #O continue barra a excecução daquele índice em específico e pula para o próximo
                        continue
                    #print(url)
                    url = url.split('#')[0] #Todos os links com '#' são links internos para a própria página, logo, não devevmos os 
                                    #levar em consideração. Para isso, chamamos o método split que quebra a string e pegamos apenas a 
                                    #primeira parte da mesma, que é a que não corresponde ao link interno.
                    #print(url)
                    #print('\n')
                    #if url != link.get('href'):
                        #print(url) #link corrigido
                        #print(link.get('href')) #link original
                        #contadorRel += 1
                    #contadorLink += 1
                #contador += 1
                    if url[0:4] == 'http':
                        novasPaginas.add(url)
                        
            pags = novasPaginas
            #print(contador)#printar quantos links tem no total
            #print(contadorLink)#printar quantos links tem o atributo href
            #print(contadorRel)#printar quantos links incompletos haviam
    

teste = set()
teste.add('a')
teste.add('b')
teste.add('a') #Apesar de rodar com sucesso, a lista não permite a adicção de valores repetidos

listaPaginas = ['https://pt.wikipedia.org/wiki/Jo%C3%A3o_Doria'] #Onde iremos armazenar as páginas que passarão pelo método  
crawler(listaPaginas, 2) #função que pegará todos os links da página passada como parâmetro

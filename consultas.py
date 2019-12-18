import pymysql
import nltk

def pesquisa(consulta):
    linhas, palavrasID = buscaMaisPalavras(consulta)
    scores = dict([linha[0], 0] for linha in linhas) #dict = dicionário. dict(chave, valor)
    #A linha acima retorna a quantidade de urls que se enquadram na busca por duas (ou mais) palavras
    #for url, score in scores.items():
    #   print(str(url) + ' - ' + str(score))
    
    #Nos comandos abaixo, nos ordenamos os scores e printamos o score e a idurl
    scoresOrdenado = sorted([(score, url) for (url, score) in scores.items()]) #sorted = ordenando
    for(score, idurl) in scoresOrdenado[0:10]: #retorna as 10 primeiras pags
        print('%f\t%s' % (score, getUrl(idurl)))
        
def getUrl(idurl):
    retorno = ''
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='indice')
    cursor = conexao.cursor()
    cursor.execute('select url from urls where idurl = %s', idurl)
    if cursor.rowcount > 0:
        retorno  = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return retorno

pesquisa('governo eleição')

def buscaMaisPalavras(consulta):
    listaCampos = 'p1.idurl'
    listaTabelas = ''
    listaClausulas = ''
    palavrasId = []
    
    palavras = consulta.split(' ') #quebrando palavras recebidas no parametro
    numeroTabela = 1
    for palavra in palavras:
        idpalavra = getIDPalavra(palavra)
        if idpalavra > 0:
            palavrasId.append(idpalavra)
            if numeroTabela > 1:
                listaTabelas += ', '
                listaClausulas += ' and '
                listaClausulas += 'p%d.idurl = p%d.idurl and ' % (numeroTabela-1, numeroTabela)
            listaCampos += ', p%d.localizacao' % numeroTabela
            listaTabelas += ' palavra_localizacao p%d' % numeroTabela
            listaClausulas += 'p%d.idpalavra = %d' % (numeroTabela, idpalavra)
            numeroTabela += 1
    consultaCompleta = 'select %s from %s where %s' % (listaCampos, listaTabelas, listaClausulas)
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='indice')
    cursor = conexao.cursor()
    cursor.execute(consultaCompleta)
    linhas = [linha for linha in cursor]
    cursor.close()
    conexao.close()
    return linhas, palavrasId


def getIDPalavra(palavra):
    returno = -1;
    stemmer = nltk.stem.RSLPStemmer()
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='indice')
    cursor = conexao.cursor()
    cursor.execute('select idpalavra from palavras where palavra = %s', stemmer.stem(palavra))
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return retorno

getIDPalavra('governo') 

def buscaUmaPalavra(palavra): #a palavra passada como prametro já será só o radical
    idPalavra = getIDPalavra(palavra)
    conexao = pymysql.connect(host='localhost', user='root', passwd='fsociety', db='indice')
    cursor = conexao.cursor()
    cursor.execute('select urls.url from palavra_localizacao plc inner join urls on plc.idurl = urls.idurl where plc.idpalavra = %s', idPalavra)
    paginas= set() #armazenar pags encontradas e impedir duplicação
    for url in cursor:
        paginas.add(url[0])
        
    print('Páginas encontradas: ' + str(len(paginas)))
    
    for url in paginas:
        print(url)
    cursor.close()
    conexao.close()
    
buscaUmaPalavra('governo')
import re #re = regular expression.Filtros em docs de string
import nltk #natural language toolkit. Usado para definir algumas stopwords, ao invÃ©s de adicionarmos todas manualmente
#nltk.download() #Ã© necessÃ¡rio fazer o download dos pacotes do nltk
stop1 = ['é'] #stopwords = palavras que nÃ£o tem sentido sozinhas
#stopwords devem ser removidas dos textos
stop2 = nltk.corpus.stopwords.words('portuguese')
stop2.append('é')
#se precisar de mais stopwords, apenas inserimos com o .append() na variável stop2
splitter = re.compile('\\W+')#splitter = separaÃ§Ã£o das palavras
#W = buscar qlqr caractere que nÃ£o seja uma palavra. + significa que pode ter qualquer coisa a frente
stemmer = nltk.stem.RSLPStemmer() #usado para remover os componentes nao-radicais das palavras
listaPalavras = [] #colocar todas as palvras que o re conseguiu identificar

lista = [p for p in splitter.split('Este lugar é apavorante a b c c++') if p != '']
#for para percorrer tds as palavras existentes no texto

for p in lista:
    if p.lower() not in stop2: #é case sensitive, llogo, colocamnos tudo em minusculo
        #Nao e necessario stemmer na linha anterior pois radicais de stopwords podem ser adicionado na lista por engando.
        #Por exemplo, sendo 'este' uma stopword, seu radical 'est' nao seria considerado uma stopword e seria adicionado.
        if len(p) > 1: #excluindo inclusão de letras     
            listaPalavras.append(stemmer.stem(p).lower())
    
stemmer.stem('nova') #retorna nov, que é o radical
stemmer.stem('novamente') #retorna nov, que é o radical
 
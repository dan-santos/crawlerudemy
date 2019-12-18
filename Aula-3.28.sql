select idurl, idpalavra, localizacao
from palavra_localizacao
where idpalavra = 1142;

select p1.idurl, p1.localizacao, p2.localizacao
from palavra_localizacao p1, palavra_localizacao p2
where p1.idpalavra = 1142 and p1.idurl = p2.idurl
and p2.idpalavra = 1143;

select * from palavra_localizacao
select * from palavras where palavra = 'govern';

select urls.idurl, urls.url, plc.localizacao from palavra_localizacao plc
inner join urls on plc.idurl = urls.idurl where plc.idpalavra = 1142;
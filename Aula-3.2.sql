select plc.idurl, urls.url, plc.idpalavra, plv.palavra, plc.localizacao from palavra_localizacao plc
inner join urls on plc.idurl = urls.idurl 
inner join palavras plv on plc.idpalavra = plv.idpalavra
order by urls.idurl;

select urls.url, count(plc.idurl) from palavra_localizacao plc
inner join urls on plc.idurl = urls.idurl
group by plc.idurl order by 2;
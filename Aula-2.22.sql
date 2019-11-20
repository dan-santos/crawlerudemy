delete from palavra_localizacao;
delete from palavras;
delete from urls;

alter table urls auto_increment = 1; /*Resetar a contagem dos registros da tabela*/
alter table palavra_localizacao auto_increment = 1;
alter table palavras auto_increment = 1;

select * from palavras;
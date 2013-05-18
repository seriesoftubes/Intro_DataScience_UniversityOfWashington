-- select.txt

select count(*)
from frequency
where docid = '10398_txt_earn';


-- select_project.txt

select term
from frequency
where docid = '10398_txt_earn' and count = 1;


-- union.txt

select term
from frequency
where docid = '10398_txt_earn' and count = 1
union
select term
from frequency
where docid = '925_txt_trade' and count = 1;


-- count.txt

select count(distinct docid)
from frequency
where term = 'parliament' and count > 0;


-- big_documents.txt

select docid
from frequency
group by docid
having sum(count) > 300


-- two_words.txt

select count(*)
from
(
	select docid
	from frequency
	where term = 'transactions' and count > 0 
	intersect 
	select docid
	from frequency
	where term = 'world' and count > 0
);


-- multiply.txt

select A.row_num, B.col_num, sum(A.value * B.value) as value
from A inner join B on A.col_num=B.row_num
group by A.row_num, B.col_num
order by 1, 2;


-- similarity_matrix.txt

select sum(doc1.matching_term_count * doc2.matching_term_count)
from 
(
	select term, count as matching_term_count
	from frequency 
	where docid = '10080_txt_crude'
) doc1 inner join 
(
	select term, count as matching_term_count
	from frequency 
	where docid = '17035_txt_earn'
) doc2 on doc1.term=doc2.term;


-- keyword_search.txt

select docid, 
	sum(
		case 
		when term in ('washington', 'taxes', 'treasury') then count
		else 0
		end
	) as similarity_score
from frequency
group by docid
order by 2 desc
limit 5;
# Tatoeba

I have tries working with data from tatoeba 


## import process lesson learned
1. it is much easier to insert to a new table updates are very slow 
2. so it would be better to create a new table for each step and move the data into this table.
3. it would not be a bad idea to have all the calculation in memory and not in the  data base - 
    for example select options was much faster when uploaded all the sentences into memory selection options and inserting it back into database (to a new table)
4. when uploading from file we should already to some cleanups - like removing sentences that are too long

##
performance differences 


this takes 4 sec
```sql
select l.*, s.*, s2.*
from tatoeba.links4 l 
join tatoeba.parts s
on s.part_id = l.id
join tatoeba.parts s2
on l.to_id = s2.part_id
where l.lang = 'ara'
and l.to_lang = 'eng'
and l.id in (608065, 332182 ,332187,332222,332222)
```

this takes 0.004 sec
```sql
select l.*, s.*, s2.*
from tatoeba.links4 l 
join tatoeba.parts s
on s.part_id = l.id
and s.lang = 'ara'
join tatoeba.parts s2
on l.to_id = s2.part_id
and s2.lang = 'eng'
where l.lang = 'ara'
and l.to_lang = 'eng'
and l.id in (608065, 332182 ,332187,332222,332222)
```


The link table has keys:
lang:
to lang
id
to_id

The parts table has the keys
lang
id 

So when we search using all the primary key values for each table we get a good performance 
And it is important that this is part of the join statement 

## differences between tatoeba and the older corpus

1. Lang is 3 chars 
2. We have a link table (that can have multiple 1 to many)
    - We should consider multiple choice quiz 
    - alternatively we have to verify that similar links are not in options  
3. We do not have dialogues 
4. We do not have dialogues lines 
5. Optimizes step id to be int4
6. We do not know on which lang->to_lang we would have links in the link table 
    - maybe it is a good idea to create steps for each lang_to_lang combination
7. steps include a single word
8. steps ranking is only by how common is this word in the corpus 


### 6 - lang to lang step links 

We already have a link table that include both languages 
link4 
We can loop over steps select the ids
select only ids that ids that have values in tha lang to lang option
and create a step lang to lang with this ids 
Probably will take a long time to run



### 2 duplicate translations 

All we need to do is search on link4 and count to_id
```sql 
select lang,to_lang,id,count(to_id) as count_to_ids
where lang = 
and to_lang = 
group by lang,to_lang,id
having count_to_ids >1
```

## TODO
- [] add recording - use google recording 
-     [] try japanese, hebrew, arabic 





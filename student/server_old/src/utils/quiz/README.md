# quiz 
This module contains the logic for generating a quiz per user.

User can have the following stages:
evaluate - we do not know user level
novice - user is new to the language
beginner - user is beginner
intermediate - user is intermediate
advanced - user is advanced
expert - user is expert

Optional - replace this levels with something numerical
We can base the levels on how common the words are in the language.


200-250
...
750-800
this gives us 10 levels

Other options that customizes the quiz for a user
1. Max length of sentences 
2. Choose similar options (from the top of the list) - or less similar
3. When getting by words - how many words to include - 1-4
 



## type of quizzes
1. by words - select 1-5{opt} words and search sentences that contain them
2. step/step - get current step/step
3. practice - select last used parts
4. refresh - select old practice parts - that need refreshing - older than a week/month
5. dialogue - ordered 
6. lines - like parts but sentences can be longer 

## params
1. max length of the sentences
2. min mark - if a user is not able to learn a sentences - live it for now 
3. max mark - if a user has a mark higher then x - do not show this part in practice. 
4. in practice by words - number of words to include in the search
5. refresh - how many hours to go back for refreshing memory

## jumping up and down in levels

we should take latest 20 records in journal and put them on a scale 
We should only take into account 30% - 100% and disregard the low 30% as they are likely to be the statistical mistake. 

0 -10 - down 2 steps - or evaluation mode
20-40 - down 1 step
40-80 - stay until complete
80-92 - up 1 steps 
92-100 - up 2 steps - or evaluation mode  

We will jump down only when we can
- We did do these steps already
- We are not at the lowest step
- Maybe the jumps down should be valid only in evaluation mode
- Jump up can be valid all the time. 
- Or jumps up and down the evaluation mode are multiplied by factor of  10 



## Practice mode

In the past I have used different practice modes for each level. 
Does that make sense now or should we have it simple 

Dialogues:
- should it be available for a complete beginner? 
- maybe there is simply no dialogue in the lowest levels 




### in a story mode

- a user join 
    - we are in select level mode - we choose something in the middle 
    - she can choose a level
- We get quiz on the current level
    - before each quiz we evaluate and select level
    - after let's say 10 quizzes in evaluation mode 
        - we exit evaluation mode
        - we jump up and down slowly
    - we go back to evaluation when we are over 92% or less than 10%
 
## issues 
- practice and refresh do not include lines and dialogues currently 
solutions 
- add a line practice mode 
- add all dialogue lines to parts? - now we have only sorts once there

## number of queries

### get quiz 

how can we save 
1. get_user_vocab - save by passing it to and from the client
2. should step up or down - we can calculate it only after 3 quizzes 
3. get words, get dialogue id  
4. get data - 3 joins
The queries can not be performed at the same time, because they are dependant on each other 


it is not much different from mongo 
the only difference 
1. in the old day we have added words to the user vocab so we may save a single query

### save results 
probably the same as in mongo 3 queries 
1. journal 
2. practice_type - step, dialogue 
3. part_id, line_id


if performance is the most important here we could do
1. use a key value database - at least for the user data
2. try and avoid preparation queries - like get the words for the step
    - we can save it in the step table - though it will not save a lot
    it is still a query - returning


Another options for saving time 
After saving results we can decide if we need to step up, and report it back to the client and then the client will as for it. 

Performance 
let's say that each query is around 50 ms 
so 4 queries is 200 ms - this should not be a problem 



## TASKS

- [] 


## after some manual experiments 

1. we should have a step table that should contain 
    a. words - use for get by words 
    b. structures + ids - use for structure - if not exists - skip structure 
    c. ids - use by random step element
2. we should have tags table, it should contain
    a. words used in all dialogues - see bellow tags level setting 
3. advanced mode - this should be complex sentences - TODO:
4. align dialogues to step
5. align tags to steps 


Consider - adding lines to parts with only adding dialogue id and line number 

Tags level settings 
We should collect all the words in the dialogues (lets say above 400)
We should get the avg rank of words. and median of words rank  
The median will set the level
now we collect all words that have rank value of X (say 150 ) bellow median and all the words above 
Now we will collect words and ids (5 ids per word, short sentences) to be included in the TAG

### relations between step and tags
Once we have set the level og the tags - when we reach this level we can add dialogues to steps

### user results structure 


would be best if we could in a single query get all the results of a user
We could use join to do this get or have all the data in a single table 


#### single table option

- lang, user_id, first_time, last_time, time_count, step, subject*, part_id, dialogue, dialogue_line, structure**, mark


* we can make subject as a step
** we do not have the specific structure - we can only remember that the quiz was using structure 
*** mark - add value 

- how to get user status
select sum(mark) - 
where user
order by time DESC
limit X

#### multiple 


- journal 

lang, user_id, time(minute), times, mark
optional do not merge - just 
perfect of statistics

- parts 

to be used for 
1. get by step
2. refresh

- steps 
1. move next steps

- dialogues & lines 
1. dialogue 
2. lines 

- combine parts + dialogues + lines 
1. refresh 
2. get by step
3. dialogue 
4. lines 

- steps + tags 
1. move next steps
2. tag status



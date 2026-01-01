

# questions 
Are there more sub branches for the current main branch?
A. we know it whent we do the actual search 

How to get the next branch?
We can order branches by level so we are sure that we are getting the lower branch first 



Here is a simplified version of the algorithm

1. select a branch 
2. if the branch avg_mark is greater than X 
    a. go to the next branch order by level an the same main branch
    b. if times is over max time go to the next branch and keep this branch as something to return to 
3. if not more sum branches on main branch - move to a new main branch

Limit user's level
When users vocabulary is small - or 



Let's describe the full process 

1. Select a main branch 
2. Set users limit on level (number of words in branch) word cout sentences, we start with a set of defualts 
3. Get the the list of ids from the branch and save them in the user's data 
4. Create a quize using this ids as params
5. For each next create quiz we will choose parts from the branch. When we have not more part ids we move to the next branch 
6. We also have refresh and repeat modes 
7. Refresh is looking for parts that havn't been for a week
8. repeat is latly viewed sentences that need to be repeated 
9. currently we do not have dialogue yet. 
10. do we have the only words practice? maybe we should



the queries 

For quiz 
- get use data from aerospike - AS 
- if needed - get next steps from PG
- PG get quiz 
- update user data on AS 

Save resutl
- Create a journal record (AS or AS)?
- Update user data on AS


We can simplify the Journal record by saving only the following data
- user
- lang
- part_id
- answer time in sec
- tries 
- play times 
- words 
- mode 


### modes 
- new branch part
- repeat 
- refresh
- repeat last quiz

Should we diffrenciate between repeat in the branch and repeat of any part?
Or maybe 
reapet - current branch
repeat - current main branch and all sub branches 
repaet - any


We can define practice of current sub branch as 
- Branch practice
While repeat would take any elements from current main branch
Refresh would take part form all the lsit of elements in UserData 

So now it is well defined:

- branch curent branch practice - under a certain level 
- repaet - current main branch
- referesh - any parts 

# Modes v2
- brnch 
- referesh - (2,7,14 ... days)
- return to older main branches, when we the level is raised
- repeat last quiz   


## Finding user's level

What would be the best way to find users level for new users.
1. let users chose (branch) words to start with 
2. let users choose limits , level, sentences length
This should be good for testing the system - later we can find ways to automate it. 





## UserData functinality

get_branch_parts
get_referesh_part
get_repeat_parts

Desicion making 
get_branch_avg_mark
get_branch_times


## deceision making 

there should be a list element for a user to make a decision
We can use function on different values to change this data  
1. part completed mark - say 6.5 
2. branch mark - if you have this mark in a branch we move on
 - we could devide this mark by the number of parts with max = 20 
3. branch times - max times to spend in a branch event if we did not reach the mark
4. Max words in sentence - we start with 4 and climbe up 
5. can we have a trial mode - say that user is quite good with branches of up to 4 words, when we decide to move to 6 words we see a steep decline in performace. - We need to have a way to go back to 4 words limit 

Can we do all the login in an agant - When we feed the agaent all user's data?

Let's try and write it as a story 


## Test Mode:
- show a combination of diferent level 
- calculate results for each level
- level should be well defined in this case - should include w_count, words rank etc.
- after say 10 quizes we can calculate the top level where user was doing well. if none - he is a complete beginner. 

## Normal Mode
- We are always in a main branch/branch level
- We save results without evaluation - as is 
- We evaluate only when getting the next quiz
- When we do the next quiz - we check if we should move to a new main branch. or continue to a new branch
- we combine branch practice with refresh practice
- modes are number 0 is branch practice, then number of days back 2, 7, 14 etc 
- We can do in place calcualtion for times/score for any mode
- I have looked at differnt ccalculations - like zigmoid,exponential etc. ask Claude  
- We may want to say that 0.4 is the statistic error. so 0.4 = 0
- We make our decisions and show the user the quiz.  


## what do we change when we we evaluate results

1. Should we switch branch
2. Should we switch main branch
3. Should we rais the wcount 
4. should we rais level 
5. save history score

## what do we change everytime we do evaluate score 
1. should we change paramaters - like max score, max times 


### Save history score
- We save history score every 10 quiz 

### Should we change banch? 
- no more available part to practice
- acieved high score on branch
- spend too much time on branch - even if we didn't learn it properly we may want to move on

### Should we switch main branch
- no more avaialble sub branched - with level limit 
- achieved high score on branch - 
- spend too much times on this main branch - this is problematic as some branches have many sub branches and some on a few - maybe avoif this options 

### should rais level
- Words vocabulary in greater than 150
### should rais w_count 
- Words vocabulary in greater than 200
- Score greater than 0.75 for 3 history  



Ok here is the simple story
- ever new quiz we evaluate results 
- when eveluating result - we check if we have reached the 10 quizes - if we did we add history
- we make decision for the next quiz 
- when we have a history milestone - we change parameter
- we should also have a way to scale down the user 
- reduce word count 
- reduce level

## App Parameters that can be used for a/b testing and fine tunning
- history milestone. 10, 12, 8
- next level milestone. 0.65, 0.7 0.75 
- refresh days - list  
- refresh raise score limit for days 0.1 0.3 0.5 
- reduce level score threashold 
- reduce word count threashold 

Do we need functinality like exponential, sigmoid?
We will see. 



-> app aprams -> evaluate -> set user params -> move branches -> move tree -> create quiz


in test mode?
- We could do evalute more often
- We could mix long and short sentences in a single quiz 

Test mode could simply be a mode like once in a while we can show all users test mode. 
Could be part of the evaluation.
In test mode we can change branches every quiz and help assess user's level


-> a/b testing -> appParams -> userParams 
-> evaluate -> compare 4/6 

For refresh mode - we can have a seprate evaluation. 
So 











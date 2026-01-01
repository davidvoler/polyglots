# Models for the user data algorithms

We at looking for simplicity and externtiability
We assume that data is in branches - currently branches are only based on common words 
Later we can use sentences structure , or other elements asbranches 


Here are the login behind this plan
1. We have app parameters that can influence user algorithms - this parameters can change
2. We assume that we store that user data in a cache db - Aerospike seems the correct DB - it has documents and is fast
3. We save user's results using insert, into the cache db - we evaluate results when compsing the quiz 
4. We save results with 2 api calls - read - modify, save 
5. Refresh is simplified - we search for part in user data that needs to be refreshed. 
6. We have only 3 modes now - branch (new) and refresh and mixed
7. Mixed is when there is not enough elments in the other mode and we got both new and refereshed. 



## Questions 
- We have an issue with branches that are too small - less than say 10 parts 
I can some solution for that 
1. Keep onnly main branch in user data, when we add new elements - we get more than one sub branch at a time
2. Verify that branches are bigger - have at least 10 parts each.  

## option 1 - main branch only
- UserData has a list of new parts 
- We evaluate 
- Keep only main branch statistics in user data 
- Add multiple sub branch's parts to user data
- When we run out of new elements we ad more sub branches or switch branch  
- We switch main branch 
    - No more sub branches 
    - Score
    - times
- We switch branch
    - new items smaller than 10 


Cons. 
- Missing data on sub branch level
Pros. 
- Simple logic on adding new branches/parts
- No need to limit merge branches 
    

## option 2 - bigger branches 
- option - in this case when we get branch data - we do not check for score on parts 
- we are here to teach a word or combination of words - or say later a sentence structure
- we swith branch
    - No more new items 
    - Score
    - times 


- We switch main branch
    - no more sub branches 
    - score
    - times 



Cons. 
- More complext logic when to switch branch
- We need to merge brnches and verify that a branche has 10 or more questions  
Pros. 
- We concentrate on a branch until we get it correct 



in both option we can solve smaller branches by simple add refresh elements. 

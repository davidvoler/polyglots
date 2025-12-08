# User Data algo and cache

I have spent some time looking at the making user algorithm using cache 


1. The idea is to break the logic into a few parts, keep some of it in cache. 
2. Be dynamic in the way user is learning 
3. Use cache for user data 
4. Avoid updates - will not work well with postgres
5. Keep the ability for fine tunning parameters without the need to change code 
6. Save results one multiple results
7. Cache user next quiz 
a. return user's cache quiz - and async do the following actions 
b. save results
c. calc next quiz - save it in cache 
8. save user's data in balk not action by action



I was doing this project at the same time as grouping by words similarity and using ArangoDB
For calculating the groups and sub groups 
The idea was that a group has a root word and sub groups all have the root words and additional words 

The code is in user_data

## Tasks 
- [v] understand what we have and how it can be added 
- [] there is already an experiment called use data - see what can be taken from there 
- [] Add a general user_data into  





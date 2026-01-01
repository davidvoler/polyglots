# the new server

## changes 
1. using postgres as database - not using mongo anymore
2. cleanup - not used code is removed 
3. unit tests in folder tests


##  scenarios

#### sign up  

- get user email from social login
- generate a user id from the email (hash)
- open the configuration page so user selects languages

#### User data 
user data is saved in 2 tables 

- users 
    - user_id
    - customer 
    - email?
    - lang
    - to lang
- user_vocab
    - lang
    - user_id
    - practice_type
    - practice_id 
    - configuration .... any configuration is specific to a language 
    - internal statistics


There will be a model that combines user preferences and user data 

Once in a while - we need to decide what even triggers this - we will update the stats data of user vocab.
This data will always be sent to the server so it does not need to read it from the database
However once in a while we will save it to the database and read it from there . 
It makes sense as sometime users' will be use the app on different devices. 

We will calculate user data/statistics when:
- when ever we complete a quiz  
- every new login - or load of the site from cookie.

We will get statistics statistics 
We will update user_vocab - statistical data - on the client
We will update the collected statistics back to database 


#### Login 

if you have a cookie 
- use cookie to load user data 
If not 
- use social login and get user's email
- get user data based on user's email

#### save preferences

When saving preferences, we may save the following elements  
- change languages (users)
- change config (vocab)
- change active learning tag/step (vocab)


#### quiz request 
I can see 2 options 
- pass entire data from client side - or at least what we have
    - last quiz data
        - last_mode
        - configuration - if changed or not 
        - mark or accuracy
    - when we do not have the data like in the following cases:
        - we have changed into a new language
        - this is the first login
        - we have opened the size just now 
    - we load this data from the database
- on the server side 
    - always update user vocab - when getting a new quiz request




#### completed a quiz 
When we get to the last part of the quiz - we save the last question 
- get statistics 
- get data for the next quiz - options - this would make running the next quiz faster

#### loading full statistics 
- we can do it as part of loading a quiz 
- we could do it every X (say 20) save results

#### goals and achievements 
- can be calculated as part of the results. 


### API changes 

#### stats 
Added stats granularity

#### quiz 
We have a single API for quiz
Quiz will return different types of quizzes (like a round robin) - not all quiz types available for each quiz

A user is always at some step - the step is set by the server but user can also change it manually
This are the types of quiz in step:
Each step has a few words - the low step have 4 while the high step have 30 words 
All types of practices have one or more step words 

Step: practices
- parts: sentences, phrases,  words  
- dialogue: a dialogue in order 
- lines: lines from different dialogues - not in order.
- structure - sentences with similar structure - usually all contain the same root words 
- refresh - repeat sentences and words - belonging to the step

#### Tag

When use select learning by tag he will have similar 
- parts: sentences, phrases,  words  
- dialogue: a dialogue in order 
- lines: lines from different dialogues - not in order.
- refresh - repeat sentences and words - belonging to the tag


#### repeat last quiz 

this does not require using the server api
- we just cleanup the answered values on the client
- navigate to the first question 
- and run the same quiz again



#### user preferences 

All preferences are save in UserVocab
Preferences are unique per languages 
so if you are learning multiple languages you have your preferences saved once per each language 


#### multi tenant 
This version is ready for multi tenant 

To start using it we need:
- create a new customer 
- create customer schemas 
- let the customer create content, preview, approve 
- let the customer add users 



#### Trophies and achievements

What can be count as an achievement:
- time spent learning per day/week/month
- streak - I am not sure I like this isea - it is good to take breaks of learning
- accuracy improvement
- number of questions per day/week/month
- new words/sentences/dialogues 
- practiced word/sentences/dialogues 
- master word/sentences/dialogues 

We could define a goals for a user. 
Or she could define the goals for herself

- get x new words in the next week/month/year
- master x new word in the next week/month/year
- spend that much time learning

Q: Do we need a new table to save those Trophies or they can be calculated?
A: All the above can be calculated from journal and or user content. 


We do need a table for goals - if we want the user to set up gaols 

lets calculate minute learning per day/week/month
```sql
SELECT toStartOfMinute(ts), sum(mark), sum(times) from journal
WHERE  ts > toStartOfDay(now())
```

accuracy improvement
```sql
SELECT toStartOfDay(ts), sum(mark), sum(times) from journal
WHERE  ts > toStartOfMonth(now())
```

Number of words/sentences per day/week/time 
This measurement should be saved - as we only have last date in the terms
We can however get the number of new once 
New words/sentences 
```sql
SELECT count(*)
WHERE first_time > now - 7 days
```

As for last_seen - this is a bit volatile - as the number of time a user should review a term depends on the current accuracy.


We can redefine the achievement as counting the practiced/refreshed terms  
Than we are correct

```sql
SELECT count(*) 
FROM users.content
WHERE last_time > now - 7 days
```


#### simple achievements

- 50 question per day 
- 20 new parts per day 
- 20 completed parts per day

you can have multiple such achievements 


We can save this data daily in a goals database we can query this data 






### caching 
I was considering using aerospike for user;s data instead of prostgres 
Why?
1. Because I ahve a lot of updates and postgres is not the best for updates 
2. When it is the right tool for the task

Some of the data can be exported to Postgress alter in large Chunks - for ML research  
I could write the extract code later 






# moving to sql based database - an experiments

## how to server multi tenant 
1. field 
2. schema 
3. database 

for now schema loos like the bests solution

it is easy to move from schema to database 
we can use shared table like user's data, 
Let's start with a schema and see if something need to change

## generating content 

we could have the following database schemas 

1. content generation 
    - prompts 
    - sentences 
    - dialogues
    - options generations - ? here or in the unique table 
2. unique sentences words - shared for all tenants - we do not want to repeat ourselves 
    - sentences
    - words 
    - dialogues 
    - dialogue lines 
    - translations 
    - recording
    - options generations  
3. quiz 
    - parts 
        - sentences
        - words 
        - phrases 
        - dialogues lines 
    - dialogues
    - dialogue lines
    - link tables 
        - steps
        - dialogues
        - levels
        - structure 
4. user data 
    - journal 
    - parts 
    - level ....


## the generation process 

1. Prompt (do we manipulate the prompt)
    - length limit
    - simplicity level
2. review - results
3. generate more data with the same prompts
4. review - 
    - add manual sentences 
    - remove sentences 
5. generate options  
    - manually add remove options 
6. translate
7. record 
8. preview quizzes

## accepts process 
let other people review content


### acl

We can define the following role 
- generate content
- review content 
- accept content
- admin users 




## provisioning 

We could offer our customers

generate a token for login
add a list of 
send invites 


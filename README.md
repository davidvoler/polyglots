# Polyglots 

Polyglots is a system for authoring, and managing language learning data using ai

The has 3 main models 

1. Content manager - for creating, loading and generating content
2. Editor - for creating courses and lessons from existing content
3. Student - for learning   

### TASKS

## Step 1 
started - 2025-12-07

### content_server
- [v] api code routes and models  

### content ui 
- [v] start adding functionality

### Content
- [v] import options 
- [v] start planning course - router/api
- [v] implement batch processing - so it can be used to run/preview/accept or delete - with the ability to iterate 
- [v] implement analyzer - use current analyze code - with or without Spacy

### Content Raw - Existing data transfer
- [v] implement break into elements for Spacy 
- [v] implement break into elements without Spacy

### Editor
- [v] create course/lesson Tables
- [v] create course/lesson UI

### Step Summary

- It looks like the data is in the new database
- I have the server and some functionality in the client in the raw data 
- The next stage will require to play with creating course and lessons - this will require some more work on the data/server and client 
- This is what should be done in the next stage 

## Step 2 - analyzer  

started - 2025-12-11

### Analyzer 

Raw Content playground
- [v] Make a list of elements that are needed to start generating and editing courses 
- [v] implement analyze sentences as a batch process 
- [v] test analyze sentences from api 
- [v]? Issue - to run analyze in docker is complicated -  shall I dod that or run with a local python?
Running locally for now - no docker 
When needed we will solve this issue

### improve analyzer 

- [v] add verb lemma and verb form
- [v] add words maybe also as word1 word2 etc - maybe up to 4 words - chose les frequent. 
- [v] have all the data of a sentences ready to use by the auto course generation.
- [v] root word
- [v] japanese - consider saving verbs with the auxiliary as a single element?
- [v] japanese root - maybe also use spacy
- [v] add options to the final table 
-

### data 
- [v] upload English
- [v] upload japanese 

Completed - 2025-12-13
Data collection will take a few more days 

## Step 2.1 
Started - 2025-12-13

### Content Raw 





### Content UI


### Step 2.3
started 2025/12/13


### Editor UI
- [v] design the ui for course/lesson generation - not UI now only the forms and processes
- [v] start planning auto generated course - (with AI?) Maybe the AI style will come later 
- [v] When we refer to leaning of a language one size does NOT fit all

### The editor UI - course/lesson generator 

We have to ask the course creator 
How important for her is that the students improve in
We can ha a slider  for the following - what is more important
We should ask for the reason of the course 
- exam - school/university/
- day to day language use . 

Is this a course that planned for multiple levels, and that should include 
- level test 
- reading
- writing 
- understanding 
- speaking

We have also to ask for target like:
- Vocabulary
- Correct sentence composition
- Learn by example  
- Grammar and syntax - explicit 
- Grammar and syntax - By example
- Learning the alphabet
- Is the alphabet completely new to the students?
- Learning how to read

We should also allow for free text 
Important elements should be working 
Elements that are less useful for now - show text requires more permissions 

### generated course - How will it work

1. Use AI to generate the all the titles and explanation 
2. Us AI to select verbs and elements from the list we give it for each lesson or step
3. If learning alphabet is selected - Create lessons or the alphabet - but it should include letters 
4. Select sentences containing the words /verbs/noun/adjectives in selected by AI
5. Go into the Editing mode 

a. Change order 
b. Add lessons - manual or generated  
c. Edit texts 
d. Add exercise type 

### Content - Courses and lessons 

### Editor UI
- [v] Create the generate lesson page
- [v]  Implement the backend - maybe with Olama
Tested olama directly it is not doing the job properly 
We will need a better guidance from our side 
I took a decision to do some work before 

Completed - 15-December 2025
As the generation I was planning did not match what is needed - we have to follow the data. 
I have moved the work on the ui to the next step

### Step 2.4
Started 16-December-2025

This step is a planning stem with little implementation

Now I understand what I want from ai generation
1. First select elements from the data - root, verb, words
2. Create some structure 
3. Let the user add remove modules lessons 
4. Add placeholders - for the ai to create. 
5. ask ai to create specific explanation etc.  
The example course was created in the last step
Let's see if we can do the generation using a blend of AI and logic on the existing data


What is needed to complete the process?


1. make list of verbs, nouns adjectives, etc 
2. collect them, let the user re-order them
3. add placeholders for explanations
4. early modules will have smaller number of sentences but as we go forward we will have more sentences per module/lesson
a. sentences structure
b. cultural issues
c. The alphabet 
4. create templates for lessons names
a. example sentences 
b. verb %s %s (見る, to go )
```python
class WordsGen:
    word:str
    type:str #verb, adjective, noun, propn, etc
    is_lemma:bool
    is_root:bool

def get_full_course_words():
    """Collects words for a complete course  
    """
    return [WordsGen(**w) for w in data]
```

Other option 

1. Prepare by words and how common they are - and also how many sentences for each length are there 1-4 5-6 7-9 10-16
2. in this list we can add word lemma, word type (verb, aux etc)
3. add word frequency 
4. use this list to generate lessons 
5. Add words to course by some order
6. Select words per module. start with 2 words per module and than 4,8,10 etc
7. Select max words in sentence per module
8. start maybe with words you already know. 

#### Generated course 

1. Welcome to English ,4
a. words you probably know - thanks, Thank you, please,...
b. words you probably know - Good morning, Good evening, Good afternoon 
2. Verbs to eat, to drink, to see, to go ,4
3. verbs,[] 5
4. I, you - using the verbs we have learned and cordial words 
5. he, she, they - the same
...
12 verbs [], 

#### Data
- [v] Group together words with lemma and word type
- [v] Play with the data - what should be the most common words to choose by  

#### Editor UI
- [] find the right tool for editing - editable - recommended by Jemini and claude 
- [] find the right tool for drag and drop - there are many options - I should let the code generator to decide 

### Step 2.5

### Data 
- [] test hebrew 
- [] upload hebrew for experiment 
- [] make a words collections 
1. Used zipf ranking 
2. Using how common it is in out corpus 




### step 2.6
### Analyzer UI
- [] create a ui for this process
- [] data - prepare the data needed
- [] use batch process to prepare the data - like analyze sentences
- [] api we need on on content side 

### step 2.7
### backup data 
- [] reorder sound files 
- [] backup data to desktop


## Step 3 
Make a decision on functionality - in content and course
What features should be included in alpha 
Does editor need a separate server/ separate client 


## Step 4

Complete features for Alpha - Content and Editor


## Step 5 

Start working on student app
### Student 

#### Desgin 
New ui design as we have now implemented course and lessons 
#### Data 
What should the data look like - Are we going for the idea of a single record well defined data

## Step 6
This is a decision making stage 
User data 
Algorithms 
Cache 
Algorithm tunning  

## Step 7 

Implementing the decisions of step 6 
Now we have the data structure set - the server should be simple with minimal 



### Backend 
- [] plan the api model/routes 

### Big Data - collecting user activity 

### Cache implementation 


## Step 8 
Student implementation
User interaction - statistics 

## Step 9 
Prepare for Alpha

## Step 10 
Alpha


## Steps 11 - 20
Product
Sales 
Searching for users 



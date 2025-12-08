# Unified table structure

## mongo

- a single part collection
- 


## polyglots

- is = english sentence.lower()
- no joins 
- use inner join to get data from one language to another language 
- all languages were translated from English - there should be multiple mistakes there. 

## totoeba

- we do not have all sentences translated to all languages 
- we have a link table 
- we do joins based on link table 



Should like tatoeba is more likely to be correct - 
We should translate more sentences automatically and maybe humans should review them


We have the following issues with tatoeba
Because of the join we get multiplication of sentences repeating themselves with different translation 



### authoring 

I thought as having the the key as a lang + hash on the sentence
We should have a problem if we allow authoring and changing sentences. 
Of course if we only correct the sentence we have a new id, however what if we only want to change the options 


We have to decide on the best structure taking into account 
1. id structure
2. link structure
3. multiple sentence -> translation link
4. option



### full quiz options 

In this structure we would have a single record for a quiz - in which we have the data formatted 
What dod we do when we want an upside down quiz from student language the learned language to practice reading? 
In this case we should maybe switch back to mongo, even if postgres is not so bad in complex json like documentation 
This options will not save data as we have many duplicates 
On the other hand the formatting is almost done automatically  - we only need to randomly reorder the answers 

- A Quiz is a full document 
- What would be the key?
- The data size may be big 
- when you find an error in one quiz question in one language - you will not reuse this finding for other languages


### sentence -> translation link 

In this case we may want to 


Explanation about the diffrents structures
1. tatoeba - sentences table and a link table connecting a sentence to a sentence 
2. polyglots - id is the sentence in english and we assume that all language match the translation - usualy works for sentences but not for ward and is never exact
3. content document - a single document that contains everything - lang, to lang, option, correct, option in learned language - 
4. content/translation - this is similar to the above option but with reuse - we create 2 records for each learning type - one is the learned language record and the other is the explanation - option correct in the student language.
This enable us to reuse content for student speaking other languages





Feature                 | tatoeba | content document| ployglots  | Content/Translation  
--------------------------------------------------------------------------------------   
Save space              | V       | X               | V          | X 
Correct data            | V       | V               | X  *       | V    
Reuse correction        | V       | X               | V          | V ****
Simple format           | X       | V               | X          | V 
Duplicate issue         | X       | V               | V          | V 
Unique explain          | v **    | V               | X          | V 
Editing simplicity      |         |                 |            | V 
Simple ID               |V        | V ***               | V      | V 
join during load        |2        |0                | 1          | 1


* assuming lang <=> lang which is mostly not the case - was based on translation from English
** we can add unique explanation to the link table
*** it is a challenge to find a simple if for this solution - but it is doable 
**** we reuse correction in the learned language - not in the explanation



## Summary 
- polyglots option is simply incorrect - it should be taken out as an option
- totoeba is good for reuse and saving space and clear id - however it requires formatting and joining 
- question document is:
    - Simple 
    - Easily adding fields when needed somewhere in the document
    - can have indexes and fields that will help with the search for the right questions 
    - will require probably more space on disk - however this is not that expensive anymore  
    - requires more work while authoring - however much less work when getting the data. 
    - id = compound key, lang,hash(sentences),owner 
        - owner can be null when it is   

- Content/translation seem now like a good option for reuse - however it requires always a clear cut between the learned language part and the student language part - is the cut always that clear?
The reuse option is it really important?
We could reuse simple by copying the document without the specific fields.



####
data structure differences 


##### content document 
```sql 
create table sentence(
    lang char(3),
    to_lang char(3),
    id int8, -- cityhash of the text in sentence - easier to work with than string 
    text varchar(255),
    elements json, -- transliteration, translation and maybe coloring based on element type
    options []
    options_lang []
    correct str
    primary key (lang, to_lang, id)
)
```

##### content/translation document 
main content - sentence in this example 
```sql 
create table sentence(
    lang char(3),
    id int8, -- cityhash of the text in sentence - easier to work with than string 
    text varchar(255),
    options []
    elements json, -- transliteration, translation and maybe coloring based on element type
    primary key (lang, id)
)
```
The translated part 
```sql 
create table sentence_translation(
    lang char(3),
    to_lang char(3),
    translation_id int8, -- the id we translate
    text varchar(255),
    options []
    elements json, -- transliteration, translation and maybe coloring based on element type
    primary key (lang, to_lang, id)
)
```




## lessons and steps 

We have to define the structure of lessons and steps withing a lesson 
We can have a list of of keys as well - like search sentences that have words, verbs, length etc. 


### Databases:
When we are in significant scale we could have the following structure

clickhouse/postgres for user results - save them raw and use for to manage a model
mongo/postgres for language data 
aeorospike for cached user data - maybe also as a cache layer over mongo
 

### authoring and version

We need to solve the as a separate issue - it should not affect the data structure 
How do we handle private data 
The simplest way would be to add a key 'school' to the table with default public 

# Grouping and steps


I had the following experiments with sentences grouping 
1. by words zipf rating 
2. by words combinations  and how common they are in text (user_Data) 
3. by dialogues and subject
4. by verbs, adjective and other part of speech
5. In japanese by auxilary_verb  - as it has a special meaning (I want to V , I did V, I will not do V and many others)
6. manual - this could really help with the initial steps - and good for using with teachers. 




Can we create a unified type of grouping and use it for all above groups?

Requires more thought and data design




### Structure with link language to language


This structure is a combination 


### Lessons/chapters 


currently I have used 2 levels 
- lesson
- step

maybe naming is not the best consult AI


Course → Lesson → Step

Common alternatives:

Course → Unit → Lesson → Exercise
Course → Module → Lesson → Activity
Course → Chapter → Lesson → Step
Course → Section → Topic → Exercise

For language learning specifically, you might also consider:

Course → Skill → Lesson → Exercise (Duolingo-style)
Course → Grammar Topic → Lesson → Drill
Course → Level (A1/A2/B1) → Lesson → Activity

For Japanese context, you could layer by script/level:

Course → Hiragana/Katakana/Kanji/Grammar → Lesson → Step

My suggestion: Stick with your Course → Lesson → Step, but add one more level if you're organizing around topics:

Course (e.g., "Japanese Fundamentals")
Unit/Module (e.g., "Greetings", "Verb Conjugation")
Lesson (specific lesson within unit)
Step/Exercise (individual activity)



## ownership

Are we going to be multi tenant?
The simplest way to put is is to say no - each tenant data is completely separated
We could say that the raw data can be shared by tenants - however the final data is unique
We could serve multi tenant in the same database but this would require to add tenant/school in every data.  

Requires further thinking 

## version

Do we manage version 
And if so how do we do it?
I would recommend starting without it.


### Stages of data

When working with data I have a lot of stages to prepare it to be in the correct format
I can think of the following 
- raw
- cleanup
- tools like Spacy and similar - get sentence structure 
- break into word 
- remove/ use proper names
- identify root word. (is it applicable to all languages?) 
- select words per sentence 
- transliteration
- dialogues and parts 
- create automatic options 
- steps and grouping
  - by common words
  - by common verb, adjective etc
  - by time 
  - other 


So far all these steps were automatic 
We have to think of the manual - human involved stage 

What of the stages do we need and 


I can think of the following stages 

- Automated
    - raw (+ cleanup)
    - analyze sentences  
    - translation
    - transliteration
    - select option
    - group similar sentences
- Manual review - learned language only
    - sentence 
    - option 
- Manual review language to language
    - review translation
    - review options (too close, to easy, etc)
    - create course/lesson/step


#### Technology - postgres vs mongodb 

I have discuss this issue with Claude.ai - the summary of the response is quite firm 
Use postgres 
Yet another thought 
As process are automatic or at list most of them - we should consider saving the data of each stage. 
So a postgres wel defined tables might be the best choice - this way we can repeat a stage that failed. or we did got it all wrong  


### ownership 

pre-processing database  
- no ownership

final data - ownership is part of the key

an alternative - public vs private data 
when you own a school - all the data there is owned by you - it is up to us to decide if it is in a different schema or a different database 
When it is in the public space we do have an author id - but it is not part of the key

Should we discuss it with ai?


### Initial Implementation

databases 

- Raw content 
    - sentence, dialogue - and source 
- Pre Processing 
    - pre processing - spacy, transliteration more 
    - translation -> translation link 
    - generate options
    - group sentences by different elements - common words - common 
- Review database - do we need it or shall we have a field that indicates if reviewed or not and review comments 
   -  Select course/lessons/step from group of words 
   -  Order the courses/lessons 
   -  review elements for each stage 
   -  Create other explanations for lessons course 
   -  Review  
- Final content 
  - Single document per language to langue element
  - Ordered courses and lessons 

Suggestion - skip review table - this can all happen in pre-processing database 

  



RAW CONTENT
├─ sentences (sentence, dialogue, source, language_pair, created_at)

PRE-PROCESSING (append-only, mostly)
├─ sentences_processed
│  ├─ sentence_id (FK)
│  ├─ spacy_analysis JSONB (pos, deps, entities, chunks)
│  ├─ transliteration JSONB (pinyin, romaji, etc)
│  ├─ translations JSONB (array of {text, language})
│  ├─ options JSONB (array of multiple choice options)
│  ├─ element_tags JSONB (["common_verb:want", "grammar:imperative", ...])
│  └─ version (if you reprocess)

GROUPING/ELEMENTS (reference data)
├─ elements
│  ├─ id, language, element_type (common_verb, grammar_structure, etc)
│  ├─ element_name ("imperative_mood", "verb:want")
│  └─ description

REVIEW & CURATION (this is where decisions happen)
├─ courses (id, language_pair, title, description, created_at, reviewed)
├─ lessons (id, course_id, title, order, created_at, reviewed)
├─ steps (id, lesson_id, title, order, created_at, reviewed)
├─ step_sentences (step_id, sentence_id, order, review_status, review_notes, reviewed_at)
│  └─ This is where you track: approved/pending/rejected, any notes

FINAL CONTENT (read-only, published)
├─ published_courses (snapshot of above when reviewed=true)




### process - manual and automatic  

#### upload raw data - in bulk 
- load lots of sentences or dialogue 
    - from file
    - from existing database 
- load translation links if available 
- remove spaces 
- remove emoticons ? 


#### processing dialogues 

- break into lines 

#### pre process - sentences 
- Spacy - or alternative 
- transliterate 
- create elements

#### preprocessing - translate 
- verify that a translation does not already exists 
- create a new translation - sentence in raw into the new language 
- sometime the create fails - as the translation sentence already exists 
- create a translation link 


#### review in bulk
- review sentence 
- review correct translation 
- review options 

#### review after preprocessing  
- show in quiz format - but show all option not only a selection
- show words in sentence and their translation
- show elements + transliteration if available 
There should be the following option to mark:
- sentence in correct or makes little sense
- translation - incorrect  
- words in sentence - might not be correct - ability to correct in place 
- options too close - or irrelevant 
Edit option 
- change translation
- change word translation 
- remove options 
- add options 
- select a different word for root 

## select and review course and lessons 
- create course 
- select lesson
- select by 
  - group of words 
  - limit word_count
  - structure 
  - verbs 
   









#### create new manually 
- create sentence and translation? or only sentences 
- check if it exists in raw data 
- if not create and run the preprocessing








### Tasks 

- [v] compare the different concepts we had so far 
- [v] try and decide of the best concept
- [V] understand the stages of data -
- [V] select a database technology   
- [v] ownership  
- [v] versions - start without it  
- [v] structure for each stage/database  
- [] create table for each stage 
- [] start loading existing data 
- [] start with initial implementations  





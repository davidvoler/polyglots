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

## Step 2 - Improve analyzer  

started - 2025-12-11

### Analyzer 

Raw Content playground
- [v] Make a list of elements that are needed to start generating and editing courses 
- [v] implement analyze sentences as a batch process 
- [v] test analyze sentences from api 
- []? Issue - to run analyze in docker is complicated - it may require a lot of work - shall I dod that or run with a local python?
- improve analyzer 
- [] add verb lemma and verb form
- [] add words maybe also as word1 word2 etc - maybe up to 4 words - chose les frequent. 
- [] have all the data of a sentences ready to use by the auto course generation.





## Step 2.1 


### Analyzer UI
- [] create a ui for this process
- [] data - prepare the data needed
- [] use batch process to prepare the data - like analyze sentences
- [] api we need on on content side 

### backup data 
- [] reorder sound files 
- [] backup data to desktop
### Content UI

### Editor UI
- [] design the ui for course/lesson generation - not UI now only the forms and processes
- [] start planning auto generated course - (with AI?) Maybe the AI style will come later 


Important elements should be working 
Elements that are less useful for now - show text requires more permissions 

### Content - Courses and lessons 


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



## Roadmap - Planning - Times - MVP

There are a lot tasks
When diving in - I tent to find more sub tasks
Should we think of an MVP and take it from there.

What would I need for myself?


What are the list of all possible features 
1. Japanese 
  a. Sentence structure - with highlighting elements
  b. Transliteration
  c. Reading - Katakana, Kanji, and maybe some Hiragana
  d. play a single word

2. Arabic
  a. Transliteration
  b. Reading

In all languages 
1. writing - how to do that? 
2. composition - composing a correct sentences 
3. hyperlinks - from a word in a sentence to other sentences 
4. description - what is a certain particle - when it is used
5. video - spot words

UI
Course lesson view 
Skip to the lesson you are 



What should the next steps?
- If I invest in the teachers part - create a lesson with a few clicks - edit and configure it as you like. 
I would invest a few month in the composer part 
- For myself - Improving my ability to learn languages
if so I would concentrate on the student side. 


For both cases we need to have more than a single option in the learning - identify words
We need 
- Explanations 
- Transliteration
- Single word play
- reading exercise
- Annotated sentences  
- writing ? 


### Features that require cracking - or research

### Spacy like  functionality for hebrew
Claud
https://github.com/amir-zeldes/HebPipe
pip failed - maybe not compatible with mac 
has not api only a cli 

https://github.com/NNLP-IL/Hebrew-Resources/blob/master/models_tools_services.rst

Invested over 2 hours in all option and did not find a good solution

https://huggingface.co/dicta-il/dictabert-morph
maybe this will work
Well no - it has only a lot of guesses - but there eis no way to say which is correct

https://nakdan.dicta.org.il/ 
this look like the best option - I wrote them an email.
https://huggingface.co/dicta-il/collections


### Spacy like  functionality for Arabic 
have tested the following tools 
CAMeL Tools - installs successful - but complicated API
Farasa - installed - yet not clear how to use 
https://farasa.qcri.org/ - not yet tested - but looks interesting
pyarabic installed
trying nltk 
claud.ai wrote code for me. 
it has a limited number of verbs - however maybe it is a starting point


### Progress indicator
- progress and statistics - 
I thought and experimented on that subject quite a lot 
- graph time based, words, sentences, accuracy 
- tree - invested some time 

I would go for a simple solution - lesson progress, word and sentences. 
As we have moved to the Course/module/lesson format Let's go for the simple solution

- Course Relates
Lessons done
Modules done 
- App lelve
words
sentences 
- Progress 
Show a simple graph of this week this month
Example 

words
------******====
*  this month
= this week
We can play with the details bu it is a simple and visible progress indicator

We can add set goals - and it is yet another point on this line 

------******====  Goal1    Goal2  Goal3

Add test to match your module stage.
So when I am taking a course I can start from the beginning or the test can skip modules I may know already.
We can simply test sentences from those lessons  
The skipped modules will be marked as skipped 

### Annotated Sentence 

Already experimented - and found a reasonable solution

### Teach alphabet 
- Use only letter from words already learned 
- Use only complete words - not invented words
- Try generating such a quiz  




### Sentence structure 
- Show it - let the users notice it and go into details when it is relevant  
invested time - and found a solution more or less. 



### Transliteration 
- Hebrew - invested some time but a solution was not found 
Invested a few hours - did not find a good solution
https://huggingface.co/spaces/malper/taatiknet
this works well - find how to download and use
- Arabic - not researched

### Video 
- Read the subtitles 
- Generate a quiz from subtitles 
- Show quiz when subtitles is ready

### In google sheet
https://docs.google.com/spreadsheets/d/1S5GkRuU7FoiSmkOAE0tr2lNWM_Ut7Rei9BADSu_hGoA/edit?gid=1004725881#gid=1004725881
This doc show what should be done and what can be skipped 


## What would help us to make money fro this project?
- I need a partner with AI startup experience
- Student side 
- Code generation 



### Iterative process 

The idea of iterative process is to complete some level over the entire process. 
- content
- course generator
- student

Let's say that we have completed the process in content, we have some of the course but it is not complete yet. 
Let's try and get it working - in a way that a single course will be created. 
Than we move to the student part and we show the courses created there. 
We need of course to complete a minimal functionality for that to work. 

Then we add feature by feature - in all 3 elements. 



#### Iteration 1 - Japanese Hebrew
1. Create a course for japanese English (Or Hebrew better)
2. Add some explanation - lets say 10 of them generated with AI - can be done manually - not as part of the course generation
3. Kanji - 
    a. sound or transliteration
    b. full words - not a single char
    c. Prefer words with a single Kanji 
4. Katakana 
    a. prefer short words 
    b. repeat 
5. Hiragana
    a. like above - start with small words or particles very common
6. Add course/lesson view 
7. Progress - Simple - optional


##### Raw Data 
We probably need to do the following 
- Recreate raw data this time in a way that matches the English structure
- Currently I have only collected some elements, many verb, noun and compound
- Add also particles - maybe in a separate fields - this will be used to use the for 
    - learning particles - explanation
    - learning hiragana 
    - annotations

##### Course Generation 
- Do it half planned half manual as long as it is working 


#### Iteration 2 - Hebrew English - optional
- given that I find some some solution for transliteration - nikud and maybe context

#### Iteration 3 - English for my kids - optional

- Say in a year from now - I could think of an app that will help with vocabulary 
- reading and sound 

#### Iteration 4 - Arabic for myself - optional 
- Assuming I have solved the transliteration issue for arabic and found a model like Spacy with morphological analyzer.
- Even only transliteration would be good 
- If not consider doing a simple course with a simpler learning process   

#### Iteration 4 - Course Editor - Make it Production ready


#### Iteration 5 - Student side - Make it Production ready



### Games and exercise type 


#### - alphabet related 
all games should be about fun - not too difficult

Find words in an array
like find car in this array

a b c 
c a a
d b r


Or find as many words you already know - etc

find a letter in text - it can be preset more than once. 

Later on this can be complicated where you do not show the words in the learned language - but in student language
User will have to translate and find the words 

All these games can lead to writing exercises 

##### - writing exercises
Type words 
show a word  - for 5 second
hide the word 
show the letters and write the word or short sentence
Show limited letters - not the entire alphabet
pres ready when you are done 
--- time based with progress bar ---

#### quiz with hidden original text

hidden quiz 
- show text
- hide it - wait 5 seconds 
- show selection of choices

#### Video related
- build quiz from video


#### user interaction progress indicator

- try to get it really simple 
- any answer give you a point 
- answering faster - or getting correct give you a bonus 
- later we can add bonuses - say for learning new words etc. 
--- show a simple daily progress in the home page ---
# Implement the full course process using iteration



## Iteration 1 - Japanese Hebrew/English

 - [done] create alphabet tables - letters and words 
 - [done] - populate letters and words into databases 
 - [ ] - create a course that teaches kanji - as part of the course 
    - [ ] - Select kanjis from words learned so far
    - [ ] - Once selected a a word - take its kanji and practice it with other words - with single kanji, 2 words per reading or kanji letter  
    - [ ] - after 2 kanji lessons - add lessons combining last 2 lessons 4 kanjis 
    - [ ] - and then add lessons for all kanji learned so far 
    - [ ] - maybe we can skip the -  all kanji learned so far  - as we have the refresh mechanism 
    - [ ] - do we want to do refresh mechanism specific for letters? or it is just part of the learning system and it is simple?

Example 
lesson 1 出,上
lesson 2 合,見
lesson 3 comb 出,上,合,見
lesson 4 so far - 出,上,合,見
lesson 5 取,込
lesson 6 立,手
lesson 7 comb 取,込,立,手
lesson 8 so far - 出,上,合,見,取,込,立,手
...

The full course generation so far:
[] = machine 
-|- = manual
[] select words by - order by how common they are in short sentences 
-|- select from this words - and reorder them
[] generate lessons from this words - export to a file 
-|- review the file - iterate until happy
[] generate letters learning for words so far - include all 3 katakana, hiragana and kanji - save as file, add sentences and translation
-|- review file. add remove sentences 
-|- add some explanations - japanese alphabet, particle system, auxiliary verb, etc
[] load from file - save to db 
-|- final review and generate 

### Student side 

- [ ] Design with course 
- [ ] Using cache - how does it work now that we have lesson 
    - [ ] - now that we have lessons it should be rather simple - we only need to save current lesson and users data
    - [ ] - we can say that we truncate user's sentences

With course and lesson we are always in the context of a module and a lesson
- We have practice module 
- practice all - so far
- we can go back to order module and choose practice specific module 
- we can choose to review explanations
Do we still need to work with cache?
Lets describe the process from the point of view of a user

1. select module - probably the first one 
2. start start learning - lesson 1 
3. load all the sentences in the lesson. 
    a. quiz 
    b. explanation
    c. learn a new alphabet letter 
    d. learn how write a word 
    e. he->ja 
    f. hearing and writing 
4. lesson is made of all possible question types - the order could change - especially if we repeat the lesson
5. when lesson is mastered - say 80% correct move to next lesson
6. when last lesson is completed - do a module review 
7. practice so far - this can be a lesson type - maybe we need both type practice module and practice so far
    a. we can have practice module in different location in the module 
    b. we can have practice so far as a lesson in different location of the module
    c. user can on his own - choose practice so far
    d. he system could know how many elements we need to practice so far and how often to offer it  




## Iteration 2 - Hebrew English - optional
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

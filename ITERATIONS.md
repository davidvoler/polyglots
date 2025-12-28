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
8. we add practice words by words - but we do not show all words in the sentences - only the important once 
9. repeat lessons - could have value for how many time to repeat, and of course we stop when all old data has a value greater than say 80% correct 
10. we can also ask the user if he want to repeat or to go to next lesson 
11. we can add recommendations 

Now we should ask the question again - do we need the cache 
Maybe only for performance reasons 
Lesson is made of say 10 sentences + explanations 
In a lesson we choose to change direction he->ja 
It is about doing a select by id - should be fast 
for practicing words,letters and sentences so far cache would make it faster - but we could start simple - without it.
- we wanted to avoid update to postgres - that was one of the reasons for cache
it is a good reason for scale - not sure it is needed for - not sure it is the best for simplicity

get data 
- select all lesson sentences 
- select explanations 
- Format - or Mode  
    - based on lesson definition sometime we format he->ja
    - sometime we hide text - only listening 
    - sometimes we skip explanations 
    - sometime we show annotated text sometimes we sip it 
- Alphabet lesson 
    - it is like any other lesson - only the header and icon is changing 

- repeat logic 
    - repeat module - get exercises for all module elements so far
    - repeat general - get everything that needs practice so far
        - choose random 
        - prefer later 
        - prefer earlier 
    - consider the logic in done in the cache module
 
Questions 
- We have the following elements so far 
    - words 
    - sentences 
    - hearing - text is hidden

Q. Should we let the user choose practicing of only one of these types?
A. It is more complicated from UI point of view 
    a. maybe let the backend decide - show an icon of what we are practicing 
    b. always mix - practice elements  
    c. let the course author decide what type of practice we are doing 

Q. When do we insert En -> JA  - in the question mode
A. When we have leaned some reading 
A. Always - Use sound with text or without it 




### implementation of the above 

- [done] Export words to files - Japanese
- [done] Reorder words 
- [done] Generate sentences from selected words - Ja - En
- [done] Generate sentences from selected words - Ja - HE
- [done] Generate greetings - JA 
- [done] Prepare placeholders for explanation 
- [done] Prepare placeholders for grammar (particles) 
- [done] Prepare placeholders for alphabets 

- [done] MARK Duplicate sentences. with the same meaning - remove - manually select the simplest  
- [done] Add alphabet teaching as part of the question - but only when we have encountered enough words that can be practiced (make use of words so far)
- [ ] Insert the placeholder 
- [ ] Add missing words  
- [ ] Group question into lessons 
- [ ] Group lessons into modules
- [ ] Load from files to database 





## Iteration 2 - Hebrew English - optional
- given that I find some some solution for transliteration - nikud and maybe context

## Iteration 3 - English for my kids - optional

- Say in a year from now - I could think of an app that will help with vocabulary 
- reading and sound 

## Iteration 4 - Arabic for myself - optional 
- Assuming I have solved the transliteration issue for arabic and found a model like Spacy with morphological analyzer.
- Even only transliteration would be good 
- If not consider doing a simple course with a simpler learning process   

## Iteration 4 - Course Editor - Make it Production ready


## Iteration 5 - Student side - Make it Production ready

# Question types 

## Sentences 
Until now we had only one type of question 
listen and identify/guess the meaning of the sentences 

An alternative version of it was - reverse mode - when we show the sentence in student language and let the user choose 

What else is there?
Identify words in speech - a short or a long sentences 
Annotated sentences
Annotation links 
- link to sentences with similar words 
- link to explanation about parts of speech  
Build a sentence from 2/3 parts. - very similar to Duolingo


Seems that I have now around 7 different question types

1. explanation
2. single choice - all - can be used for grammar too 
3. multiple choice - all - can be used for grammar too 
4. identify words - listening
5. words in array - reading
6. memory game - reading/alphabet - can be used for letters but also for words
7. type text - writing/alphabet 


general purpose | listening | reading     | writing | grammar
------------------------------------------------------------- 
1,2,3           | 2,3,4     | all         | 7       | all 


### Break down by functionality 

2. or 3. 
a. play audio, selection
b. play audio, show text, show selection
c. play audio, options are hidden, show option one by one
d. Play audio, show option in learned languages


We have the same data as above sentence but we act differently in the ui
We can do it randomly in the ui - it does not have to be part of the data. with some limitations 
- play audio -> read sentences - makes sense only if student has learned to read enough of the letters in the sentences - or we add transliteration 
- show the options one by one require testing - especially how does it feel.


### Future questions 
- video with quiz - can be all the above question types 
8. select words or phrases  when you hear them - extension of identify words 


### Sentence annotation
Play word sound
Show word meaning and structure
Link to other sentences with this word
Link to explanation - particles, auxiliary

## Reading 


## Alphabet

### Kanji


For Kanji (Multiple Readings & Large Set)
1. Reading Roulette / Guess the Reading

Show a Kanji character with context (in a sentence)
User selects the correct reading (hiragana options) based on context
Teaches that context determines pronunciation
Example: 生 in different contexts (生まれる / 生活 / 先生)

2. Kanji Building Blocks

Show a Kanji broken into its radicals/components
User learns the structure and meaning of each part
Drag radicals together to "build" the Kanji
Reinforces memory through visual decomposition

3. Kanji Family Tree

Show a base radical and all Kanji that contain it
User connects them and learns the semantic relationships
Example: All 水-related Kanji (水, 河, 海, 湿, etc.)

4. Kanji Stroke Order Animation + Quiz

Animate the correct stroke order
User then draws or taps strokes in correct order
Critical for proper Kanji writing

5. Kanji "Spot & Match" Game

Show a paragraph of text with one target Kanji highlighted multiple times
User identifies all instances and their different readings
Teaches pattern recognition and reading variation

6. Reading Context Game

Show same Kanji in different sentences
User matches each sentence to the correct reading
Forces active engagement with context-dependent meanings

### Arabic 

For Arabic (Letter Form Changes)
1. Letter Transformation Journey

Show an Arabic letter in all 4 forms: isolated, initial, medial, final
Animate the transformation as the letter "moves" through a word
User learns each form through visual progression
Interactive: Click each position to see the letter morph

2. Word Building with Form Changes

User drags letters to build a word, seeing them transform as they're placed
Letters automatically change shape based on position
Real-time visual feedback on correct letter forms
Example: Building ك + ت + ا → كتا (letters change shape as placed)

3. Form Matching Pairs

Show 4 cards with the same letter in different forms
User must match them to prove they recognize the same letter
Gamify with speed/scoring

4. "Spot the Letter" Game

Show a paragraph in Arabic script
Highlight one letter in a specific form (e.g., ب in final position)
User finds all instances of that letter in that same position
Teaches form-specific recognition

5. Connect the Letter Forms

Show 4 forms of a letter scattered on screen
User draws lines connecting them in order: isolated → initial → medial → final
Visual reinforcement of the transformation sequence

6. Puzzle Assembly

Show a complete word broken into letter forms
Each letter shown in its correct form for that position
User arranges them to spell the word, understanding form changes

Cross-Alphabet Gamification Concepts
7. Progressive Difficulty System

Level 1: Single letters in isolation
Level 2: Letters with one form variation
Level 3: Multiple forms mixed
Level 4: In real words and sentences
Level 5: Speed challenges

8. Alphabet Bingo

Create a 3x3 or 4x4 grid of letters in different forms
Call out letters (show in one form, user marks all forms on their card)
Traditional game with alphabet twist

9. Memory Card Game

Pairs: Same letter in different forms (Kanji readings, Arabic letter forms)
User flips cards to find matching pairs
Builds recognition muscle memory

10. Timed Relay / Speed Challenge

Flash a letter/form for 2 seconds
User must identify it or select its pair
Tracks speed progression over time
Satisfying for competitive learners

11. Story Mode

Create a visual narrative where user "unlocks" new letters as they progress
Each letter introduced with its variations
Provides context and motivation
Can tie to cultural elements

12. AR Mirror / Writing Practice

User writes the letter on screen
System shows the correct form overlaid
User traces to correct their form
Real-time feedback on stroke order and shape

Implementation Priority
I'd suggest starting with:

Reading Context Game (for Kanji) - teaches the core challenge of context-dependent readings
Letter Transformation Journey (for Arabic) - visually shows the shape-changing concept
Memory Card Pairs - reliable gamification that works for both
Stroke Order Animation (for Kanji) - critical skill for writing

### memory cards 
Key improvements:

Identical Letter Matching - Each pair contains two cards with the same letter (火-火, 木-木, ب-ب, etc.)
Better Visual Feedback

Cards show a question mark when face-down
Cards flip with smooth animations to reveal the letter
Matched pairs turn green and stay revealed
Unmatched cards flip back after 1 second


Improved Stats Display

Shows pairs found, remaining pairs, and move count
Color-coded stat box for better visibility


Better UX

Prevents clicking more than 2 cards at a time
Prevents clicking already matched cards
Cards have shadows and better styling
Instructions included in the game
"New Game" button to restart
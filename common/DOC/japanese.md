# tasks for learning japanese

After trying without much success to learn japanese I cane to the following conclusions 

1. it is better to learn with context 
2. it is important to have transliteration 
3. it is important to know words meaning 
4. it is important to see transliteration.






### better grouping of words in sentence

The problem with Japanese and tools like Spacy is that maybe of the sentence parts categorized as particles. 
However sometime a few particles together have a meaning as a word. 
So I have replaced spacy with code I have written that breaks sentences and searches for 'Words" or a sent of particles that form meaning. 


### Learning the alphabets 

1. complexity 
a. 3 different alphabet 
b. hiragana 64 + combinations - used for japanese 
c. katakana 64 + combination - used for foreign words 
d. kanji - is quite complex to remember has multiple reading in different words       


## other complexities 

- order of the sentence 
- no form for single and multiple
- lots of - particles
- lots of different auxiliary verbs changing the meaning of the sentence    



## tasks 

### annotated sentences 
- [v] transliteration tool - research
- [v] annotated text to be able to add translation and sound per word
- [v] combine the two features - annotation + transliteration
- [v] support RTL languages 

The solution was to use ruby text and extend it 
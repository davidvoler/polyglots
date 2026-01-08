import re
from collections import defaultdict

class SimpleArabicPOS:
    def __init__(self):
        # Basic MSA vocabulary for the four POS categories
        # These are common words - expand as needed
        self.verbs = {
            'كان', 'ذهب', 'جاء', 'أخذ', 'أعطى', 'قال', 'سمع', 'رأى',
            'عمل', 'حدث', 'وضع', 'مد', 'أراد', 'يريد', 'يذهب', 'تذهب',
            'يقول', 'تقول', 'يسمع', 'تسمع', 'يرى', 'ترى', 'يعمل', 'تعمل',
            'فعل', 'فعلت', 'فعلوا', 'فعلن', 'كانت', 'كانوا', 'كن'
        }
        
        self.nouns = {
            'رجل', 'امرأة', 'بيت', 'كتاب', 'قلم', 'طاولة', 'سيارة', 'شارع',
            'مدينة', 'بلد', 'عالم', 'يوم', 'شهر', 'سنة', 'وقت', 'مكان',
            'شمس', 'قمر', 'نجم', 'ماء', 'نار', 'هواء', 'أرض', 'سماء',
            'أب', 'أم', 'أخ', 'أخت', 'ابن', 'ابنة', 'صديق', 'معلم'
        }
        
        self.adjectives = {
            'كبير', 'صغير', 'أحمر', 'أزرق', 'أخضر', 'أسود', 'أبيض', 'جميل',
            'قبيح', 'طويل', 'قصير', 'سمين', 'نحيف', 'قوي', 'ضعيف', 'سريع',
            'بطيء', 'حار', 'بارد', 'جديد', 'قديم', 'جيد', 'سيء', 'عالي',
            'منخفض', 'مرتفع', 'منخفض', 'ذكي', 'غبي'
        }
        
        self.pronouns = {
            'أنا', 'أنت', 'أنتِ', 'أنتم', 'أنتن', 'هو', 'هي', 'هم', 'هن',
            'ي', 'ك', 'ه', 'نا', 'كم', 'كن', 'هم', 'نحن', 'كنا', 'تهم',
            'تها', 'تنا', 'تي', 'تك', 'ني', 'نني', 'هما', 'هاتا',
            'ما', 'من', 'ذا', 'تلك', 'هذا', 'هذه'
        }
    
    def tokenize(self, text):
        """Simple tokenization - split on whitespace and punctuation"""
        # Keep Arabic text, split on spaces and common punctuation
        tokens = re.findall(r'\S+', text)
        return tokens
    
    def tag(self, tokens):
        """Tag tokens with POS"""
        tagged = []
        for token in tokens:
            # Remove diacritics for matching (optional but helps)
            clean_token = self._remove_diacritics(token)
            
            if clean_token in self.verbs:
                pos = 'VERB'
            elif clean_token in self.nouns:
                pos = 'NOUN'
            elif clean_token in self.adjectives:
                pos = 'ADJ'
            elif clean_token in self.pronouns:
                pos = 'PRON'
            else:
                pos = 'X'  # Unknown
            
            tagged.append((token, pos))
        
        return tagged
    
    def process(self, text):
        """Tokenize and tag in one step"""
        tokens = self.tokenize(text)
        return self.tag(tokens)
    
    def _remove_diacritics(self, text):
        """Remove Arabic diacritical marks"""
        diacritics = re.compile(r'[\u064B-\u065F]')
        return diacritics.sub('', text)
    
    def add_words(self, words, pos_type):
        """Add words to a POS category"""
        pos_dict = {
            'VERB': self.verbs,
            'NOUN': self.nouns,
            'ADJ': self.adjectives,
            'PRON': self.pronouns
        }
        if pos_type in pos_dict:
            pos_dict[pos_type].update(words)


# Usage example
if __name__ == "__main__":
    tagger = SimpleArabicPOS()
    
    text = "قال الرجل الكبير أنا أحب الكتاب الجميل"
    result = tagger.process(text)
    
    print("Text:", text)
    print("\nTokens and POS:")
    for token, pos in result:
        print(f"  {token:15} -> {pos}")
    
    # Add custom words
    print("\n--- Adding custom words ---")
    tagger.add_words(['محمد', 'علي', 'فاطمة'], 'NOUN')
    tagger.add_words(['يدرس', 'تدرس'], 'VERB')
    
    text2 = "محمد يدرس الكتاب"
    result2 = tagger.process(text2)
    
    print("Text:", text2)
    print("\nTokens and POS:")
    for token, pos in result2:
        print(f"  {token:15} -> {pos}")
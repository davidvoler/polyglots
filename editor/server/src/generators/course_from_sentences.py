from utils.db import get_query_results


def _load_elements(folder, fname):
    results = []
    with open(f"{folder}/{fname}.csv") as f:
        lines =  f.readlines()
        for l in lines:
            results.append(l.strip().split("\t"))
    return results


def _load_alphabet(ab:list):
    res = {}
    last_w = ''
    for a in ab:
        if len(a) == 1:
            last_w = a[0]
        else:
            res[last_w] = a
    return res
def _load_alphabet_all(ab:list):
    res = [] 
    last_w = ''
    for a in ab:
        res.append(
            {"ab_type":a[0],"letter":a[1], "words":a[2:]}
        )
    return res



def sentences_from_folder(folder:str, target:str):
    alphabet =   _load_alphabet(_load_elements(folder, "alphabet"))
    alphabet_all =   _load_alphabet_all(_load_elements(folder, "alphabet_all"))
    greeting =   _load_elements(folder, "greeting_with_ids")
    sentences =   _load_elements(folder, "sentences")

    for k, v in alphabet.items():
        print(k)
        print(v)


    lessons = []
    greeting_word = greeting[0][0]
    sentences_so_far = []
    for g in greeting:
        if g[0] != greeting_word:
            lessons.append(
                ('greeting',greeting_word,sentences_so_far)
            )
            sentences_so_far = []
            greeting_word =g[0]
            sentences_so_far.append(g)
        else:
            sentences_so_far.append(g)
    lessons.append(
        ('greeting',greeting[-1][0],sentences_so_far)
    )
    sentences_so_far = []
    sentences_word = sentences[0][0] 
    for s in sentences:
        if s[0] != sentences_word:
            lessons.append(
                ('by_words',sentences_word,sentences_so_far)
            )
            sentences_so_far = []
            if sentences_word in alphabet:
                lessons.append(
                    ('alphabet',f'{alphabet[sentences_word][0]} {alphabet[sentences_word][1]}'  , [alphabet[sentences_word]])
                )
            sentences_word = s[0]
        else:
            sentences_so_far.append(s)
    lessons.append(
        ('by_words',sentences[-1][0],sentences_so_far)
    )

    print(len(lessons))
    # for l in lessons[:5]:
    #     print(f'L\t{l[0]}\t{l[1]}\n')
    #     for s in l[2]:
    #             print("\t".join(s))
    with open(target, 'w') as f:
        for l in lessons:
            f.write(f'L\t{l[0]}\t{l[1]}\n')
            for s in l[2]:
                f.write(f'S\t{"\t".join(s)}\n')



def create_modules(lessons_path):
    lessons = _load_elements(lessons_path,'course')
    module_idx = 0 
    lessons_per_module = 5
    lessons_so_far = 0
    lessons_to_write = [] 
    modules = []
    lesson_types = set()
    lesson_words = {}
    module_idx = 0
    for l in lessons:
        if l[0] == "L":
            lesson_types.add(l[1])
            if l[1] not in lesson_words:
                lesson_words[l[1]] = set()
            lesson_words[l[1]].add(",".join(l[2:]))
            lessons_so_far+=1
        lessons_to_write.append(l)    
        if lessons_so_far > lessons_per_module:
            module = []
            for l in lesson_types:
                module.append((l,list(lesson_words[l])))
            modules.append(module)
            lesson_types = set()
            lesson_words = {}
            lessons_so_far=1
            with open(f'{lessons_path}/modules.csv', 'a+') as f:
                module_idx+=1
                n = f'M\t{module_idx}\t'
                for s in module:
                    n+= f'{s[0]}:{'\t'.join(s[1])} |'
                f.write(n+"\n")
                for l in lessons_to_write[:-1]:
                    f.write("\t".join(l) +"\n")
                lessons_to_write = [lessons_to_write[-1]]



async def correct_greeting(lessons_path):
    greeting_with_ids = []
    
    sql = """ 
    SELECT l.id as id, l.lang as lang,t.id as to_id
        from content_raw.sentence_elements l 
        join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
        join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
        where tl.lang = %s and tl.to_lang = %s and l.id = %s and t.text = %s
    """

    greeting = _load_elements(lessons_path, "greeting")
    for g in greeting:
        word = g[0]
        s_id = g[1]
        lang = g[2]
        to_lang = g[3]
        text = g[4]
        to_text = g[5]
        res = await get_query_results(sql,
        (lang,to_lang,s_id,to_text))
        if len(res)>0:
            greeting_with_ids.append((word,s_id, lang,to_lang,str(res[0].get('to_id'))))
    with open(f"{lessons_path}/greeting_with_ids.csv", 'w') as f:
        for gi in greeting_with_ids:
            f.write("\t".join(gi) +"\n")

    

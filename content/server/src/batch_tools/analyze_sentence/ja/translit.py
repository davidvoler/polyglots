from pykakasi import kakasi
import json
kks = kakasi()

def translit(text:str) -> str:
    translit = kks.convert(text)
    results = []
    len_so_far = 0
    for item in translit:
        ln = len(item['orig'])
        position = len_so_far
        len_so_far += ln
        hira = item['hira'] if item['hira']!=item['orig'] else ''
        kana = item['kana'] if item['kana']!=item['orig'] else ''
        roma = item['hepburn'] if item['hepburn']!=item['orig'] else ''
        results.append({
            "orig": item['orig'],
            "hira": hira,
            "kana": kana,
            "roma": roma,
            "position": position,
            "length": ln
        })
    return results

def translit_single(text:str) -> str:
    words = translit(text)
    hira = "".join([w['hira'] for w in words])
    kana = "".join([w['kana'] for w in words])
    roma = "".join([w['roma'] for w in words])
    return {
        "hira": hira,
        "kana": kana,
        "roma": roma
    }
    


# if __name__ == "__main__":
#     sentences = [
#     "こんにちは世界",
#     "私の名前は田中です",
#     "東京駅に行きます",
#     "美味しい寿司を食べました",
#     "今すぐ読みたいんだ"
#     ]
#     for idx, s in enumerate(sentences):
#             results = translit(s)
#             print(json.dumps(results, indent=2, ensure_ascii=False))



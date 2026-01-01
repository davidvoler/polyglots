from sentence_transformers import SentenceTransformer, util
from collections import OrderedDict
import random

# Load a sentence transformer model optimized for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

# Original sentence

def get_similarity_score_simple(sentence, options, max_similarity=0.8):
    
    # Encode the original sentence and options
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    option_embeddings = model.encode(options, convert_to_tensor=True)

    # Compute cosine similarity
    try:
        cosine_scores = util.cos_sim(sentence_embedding, option_embeddings)
    except Exception as e:
        return options
    # Print results
    results = []
    for i, option in enumerate(options):
        results.append((option, cosine_scores[0][i].item()))
    return results

def get_similarity_score(sentence, options, max_similarity=0.8):
    options = list(set(options))
    
    # Encode the original sentence and options
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    option_embeddings = model.encode(options, convert_to_tensor=True)

    # Compute cosine similarity
    try:
        cosine_scores = util.cos_sim(sentence_embedding, option_embeddings)
    except Exception as e:
        return options
    # Print results
    results = []
    for i, option in enumerate(options):
        results.append((option, cosine_scores[0][i].item()))
    sorted_data = sorted(results, key=lambda x: x[1], reverse=False)
    
    ordered_dict = OrderedDict(sorted_data)
    ordered_list = []
    for k, v in ordered_dict.items():
        if v >= max_similarity:
            print(sentence, '<->',  k, v)
        else:
            ordered_list.append((k, v))
    # return ordered_dict
    return ordered_list
    # return results


def get_similarity_grouping(sentence, options, min_similarity=0.4 ,max_similarity=0.8):
    options = list(set(options))

    # Encode the original sentence and options
    sentence_embedding = model.encode(sentence, convert_to_tensor=True)
    option_embeddings = model.encode(options, convert_to_tensor=True)

    # Compute cosine similarity
    cosine_scores = util.cos_sim(sentence_embedding, option_embeddings)

    # Print results
    results = []
    for i, option in enumerate(options):
        results.append((option, cosine_scores[0][i].item()))
    sorted_data = sorted(results, key=lambda x: x[1], reverse=True)
    
    ordered_dict = OrderedDict(sorted_data)
    ordered_list = []
    too_low = []
    too_high = []
    for k, v in ordered_dict.items():
        if v < min_similarity:
            # print("too low", sentence, k, v)
            too_low.append(k)
        elif v >= max_similarity:
            # print("too high", sentence, k, v)
            too_high.append(k)
        else:
            ordered_list.append(k)
    # return ordered_dict
    return ordered_list, too_low, too_high
    # return results


def test_fixed():
    sentence = "I have a headache"

    # Option sentences
    options = [
        "My head hurts",        # Expected: High similarity
        "I am not feeling well", # Expected: Moderate similarity
        "My uncle got married",  # Expected: Low similarity
        "I have a headache",     # Expected: Very high similarity
        "I have a headache!",     # Expected: Very high similarity
        "i have a headache",     # Expected: Very high similarity
        "I have a headache...",     # Expected: Very high similarity
        "I have a bellyache",     # Expected: Very high similarity
    ]
    res = get_similarity_score(sentence, options)
    print(res)

if __name__ == "__main__":
    test_fixed()

   
    



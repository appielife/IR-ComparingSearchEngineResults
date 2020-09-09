import json
import numpy as np
import pandas as pd

def query_diff(google_res, sengine_res):
    diff = []
    for idx,query in enumerate(sengine_res):
        query = query.lower()
        query = query.replace("https","")
        query = query.replace("http","")
        query = query.replace("www.","")
        if(query[-1] =='/'):
            query =  query[:-1]
        sengine_res[idx] = query

    for idx,query in enumerate(google_res):
        query = query.lower()
        query = query.replace("https","")
        query = query.replace("http","")
        query = query.replace("www.","")
        if(query[-1] =='/'):
            query =  query[:-1]
        google_res[idx] = query

    for idx_google, result in enumerate(google_res):
        if result in sengine_res:
            sengine_idx = sengine_res.index(result)
            diff.append(idx_google - sengine_idx)
    n = len(diff)
    difference = np.array(diff)
    return difference, n

def spearman_val(diff, n):
    if n == 0:
        return 0
    elif n == 1:
        if sum(diff) == 0:
            return 1
        else:
            return 0
    spearman_coef = 1 - ((6 * np.sum(diff ** 2)) / (n * (n ** 2 - 1)))
    return spearman_coef

def generate_rank(google_pairs, sengine_pairs, output_file='hw1.csv'):
    rank = pd.DataFrame(columns=["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficient"])
    for query in google_pairs.keys():
        google_res, sengine_res = google_pairs[query], sengine_pairs[query]
        diff, n = query_diff(google_res, sengine_res)
        spearman_coef = spearman_val(diff, n)
        rank = rank.append(
            pd.Series(
                [query, n, (n / 10.0) * 100, spearman_coef],
                index=["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficient"]
            ),
            ignore_index=True
        )
    rank = rank.set_index('Queries')
    rank = rank.append(rank.mean(axis=0).rename('Averages'))
    rank.to_csv(output_file)
    return rank

if __name__ == '__main__':
    s_engine = 'hw1.json'
    google_file = 'Google_Result3.json'
    google_pairs = json.loads(open(google_file).read())
    ask_pairs = json.loads(open(s_engine).read())
    generate_rank(google_pairs, ask_pairs)


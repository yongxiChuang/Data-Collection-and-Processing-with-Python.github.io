# JSON Format and the JSON Module
import json
a_string = '\n\n\n{\n "resultCount":25,\n "results": [\n{"wrapperType":"track", "kind":"podcast", "collectionId":10892}]}'
print(a_string)
d = json.loads(a_string) # json.loads()可以把string轉成dictionary
print('---------')
print(type(d))  # class <dict>
print(d.keys())  # dict_keys(['resultCount', 'results'])
print(d['resultCount'])  # 25

p = json.dumps(d)  # json.dumps()可以把dictionary轉成string
# p = json.dumps(d, indent = 2)
print('---------')
print(p)

# --------------------------------------------------------------------------------
# Shallow Copies
original = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'e']]
copied = original[:]  # copy form [0:-1]，其中list皆為指標，所以一但更改其中一個，另一個也會跟著變動
print(copied is original)  # false
print(copied == original)  # true
copied[1].append('z')
print(copied)  # [['a', 'b', 'c'], ['d', 'e', 'f', 'z'], ['g', 'e']]
print(original)  # [['a', 'b', 'c'], ['d', 'e', 'f', 'z'], ['g', 'e']]

# --------------------------------------------------------------------------------
# Deep Copies
import copy
original = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'e']]
shallow_copy = original[:]
deep_copy = copy.deepcopy(original)
original.append('Original')
shallow_copy[0].append('shallow')
print(original)
print("------------------")
print(shallow_copy)
print("------------------")
print(deep_copy)

# --------------------------------------------------------------------------------
# Map
import copy
original = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'e']]
shallow_copy = original[:]
deep_copy = copy.deepcopy(original)
original.append('Original')
shallow_copy[0].append('shallow')
print(original)
print("------------------")
print(shallow_copy)
print("------------------")
print(deep_copy)

# --------------------------------------------------------------------------------
# Filter
lst = ['apple', 'ball', 'cat', 'dog']
filter_lst = list(filter(lambda word: 'a' in word, lst))
# filter 和 map 用法相似
print(filter_lst)  # ['apple', 'ball', 'cat']

# question 6
l1 = ['left', 'up', 'front']
l2 = ['right', 'down', 'back']
l3 = list(zip(l1, l2))
opposites = list(filter(lambda s: len(s[0])>3 and len(s[1])>3, l3))
print(opposites)

# **List comprehensions**
# [<transformer_expr> for <variable> in <sequence> if <filtration_expr>]

# --------------------------------------------------------------------------------
# Zip
L1 = [3, 4, 5]
L2 = [1, 2, 3]
L4 = list(zip(L1, L2))  # zip 可以將兩個list同樣位子的元素組成tuple放入新的list中
print(L4)  # [(3, 1), (4, 2), (5, 3)]
L3 = [(x1 + x2) for(x1, x2) in L4]
print(L3)  # [4, 6, 8]

# --------------------------------------------------------------------------------
# Fetching a Page
import requests
import json

page = requests.get("https://api.datamuse.com/words?rel_rhy=apple")
print(type(page))   # <class 'requests.models.Response'>
print(page.text[:150])   # [{"word":"grapple","score":1309,"numSyllables":2},{"word":"pineapple","score":858,"numSyllables":3},{"word":"chapel","score":760,"numSyllables":2},{"w
print(page.url)   # https://api.datamuse.com/words?rel_rhy=apple
print("------------")
txt = page.json()   # <class 'list'>
print(type(txt))
print("---first item in the list---")
print(txt[0])   # {'word': 'grapple', 'score': 1309, 'numSyllables': 2}
print("---the whole list, pretty printed---")
print(json.dumps(txt, indent=2))
'''   {
    "word": "grapple",
    "score": 1309,
    "numSyllables": 2
  },
  {
    "word": "pineapple",
    "score": 858,
    "numSyllables": 3
  },
  {
    "word": "chapel",'''

# Figuring Out How to Use a REST API
# import statements for necessary Python modules
import requests

def get_rhymes(word):
    baseurl = "https://api.datamuse.com/words"
    params_diction = {} # Set up an empty dictionary for query parameters
    params_diction["rel_rhy"] = word
    params_diction["max"] = "3" # get at most 3 results
    resp = requests.get(baseurl, params=params_diction)
    # return the top three words
    word_ds = resp.json()
    return [d['word'] for d in word_ds]  # 若沒有這行的話，會輸出整個dictionary
    return resp.json() # Return a python object (a list of dictionaries in this case)，但其實可省略
		# 這個function有兩個return!

print(get_rhymes("funny"))

# --------------------------------------------------------------------------------
# Project: OMDB and TasteDive Mashup
#1
import requests_with_caching
import json
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages

def get_movies_from_tastedive(movie):
    parameters = {}
    parameters["q"] = "Bridesmaids"
    parameters["type"] = "movies"
    parameters["limit"] = 5
    res = requests_with_caching.get("https://tastedive.com/api/similar", parameters)
    print("->" + res.url)
    return res.json()

result1 = get_movies_from_tastedive("Bridesmaids")
print(result1['Results'])
# get_movies_from_tastedive("Black Panther")

#2
import requests_with_caching
import json

def get_movies_from_tastedive(movie):
    parameters = {}
    parameters["q"] = "Tony Bennett"
    parameters["type"] = "movies"
    parameters["limit"] = 5
    res = requests_with_caching.get("https://tastedive.com/api/similar", parameters)
    return res.json()

def extract_movie_titles(res):
    print(json.dumps(res, indent=2)[:150])
    Results = res["Similar"]["Results"]
    return [d["Name"] for d in Results]
    return res.json()
    
    
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
print(extract_movie_titles(get_movies_from_tastedive("Tony Bennett")))
# extract_movie_titles(get_movies_from_tastedive("Black Panther"))

#3
import requests_with_caching
import json

def get_movies_from_tastedive(movie):
    parameters = {}
    parameters["q"] = movie
    parameters["type"] = "movies"
    parameters["limit"] = 5
    res = requests_with_caching.get("https://tastedive.com/api/similar", parameters)
    return res.json()

def extract_movie_titles(res):
    print(json.dumps(res, indent=2)[:150])
    Results = res["Similar"]["Results"]
    return [d["Name"] for d in Results]
    return res.json()

def get_related_titles(lst):
    movie_lst = []
    for movie in lst:
        for name in extract_movie_titles(get_movies_from_tastedive(movie)):
            if name not in movie_lst:
                movie_lst.append(name)
    return movie_lst
        

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])

#4
import requests_with_caching
import json

def get_movie_data(movie):
    parameter = {}
    parameter["t"] = movie
    parameter["r"] = "json"
    res = requests_with_caching.get("http://www.omdbapi.com/", parameter)
    print(res.url)
    return res.json()
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_movie_data("Venom")
get_movie_data("Baby Mama")

#5
import requests_with_caching
import json


def get_movie_data(movie):
    parameter = {}
    parameter["t"] = movie
    parameter["r"] = "json"
    res = requests_with_caching.get("http://www.omdbapi.com/", parameter)
    print(res.url)
    return res.json()

def get_movie_rating(res):
    for i in res['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':
            rating = int(i['Value'][:-1])
            break
        else:
            rating = 0
    return rating
    return res.json()
    
print(get_movie_rating(get_movie_data("Deadpool 2")))

#6
# https://gist.github.com/cibofdevs/4ca80f401792e7728e71565b4b3a4fdf
import requests_with_caching
import json

def get_movies_from_tastedive(title):
    endpoint = 'https://tastedive.com/api/similar'
    param = {}
    param['q'] = title
    param['limit'] = 5
    param['type'] = 'movies'
    this_page_cache = requests_with_caching.get(endpoint, params=param)
    return json.loads(this_page_cache.text)

def extract_movie_titles(dic):
    list = []
    for i in dic['Similar']['Results']:
        list.append(i['Name'])
    return(list)

def get_related_titles(titles_list):
    list = []
    for i in titles_list:
        new_list = extract_movie_titles(get_movies_from_tastedive(i))
        for i in new_list:
            if i not in list:
                list.append(i)
    print(list)
    return list

def get_movie_data(title):
    endpoint = 'http://www.omdbapi.com/'
    param = {}
    param['t'] = title
    param['r'] = 'json'
    this_page_cache = requests_with_caching.get(endpoint, params=param)
    return json.loads(this_page_cache.text)

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_movie_rating(get_movie_data("Deadpool 2"))

def get_movie_rating(data):
    rating = 0
    for i in data['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':
            rating = int(i['Value'][:-1])
            #print(rating)
    return rating 

def get_sorted_recommendations(list):
    new_list = get_related_titles(list)
    new_dict = {}
    for i in new_list:
        rating = get_movie_rating(get_movie_data(i))
        new_dict[i] = rating
    print(new_dict)
    #print(sorted(new_dict, reverse=True))
    return [i[0] for i in sorted(new_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
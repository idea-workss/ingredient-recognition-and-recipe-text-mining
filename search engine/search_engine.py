import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.stem import PorterStemmer
import re
import string
import text_result

def preprocessing_query(query) :
    #preprocessing
    #make all word to lowercase
    query = query.lower()
    #remove number
    rm_number = str.maketrans('', '', string.digits)
    query = query.translate(rm_number)
    #remove punctuations
    rm_punctuations = str.maketrans('', '', string.punctuation)
    query = query.translate(rm_punctuations)
    #remove UNICODE characters
    query = query.encode("ascii", "ignore")
    query = query.decode()
    #remove whitespaces
    query = query.strip()

    #Tokenize Query
    query_tokenize = word_tokenize(query)

    #Filtering
    query_filtered = []
    stopword = stopwords.words('english')
    new_stopword = ["tbsp", "lb", "tsp", "oz", "g", "inch", "inches", "tablespoons", "cup", "teaspoon"]
    stopword.extend(new_stopword)

    for t in query_tokenize :
        if t not in stopword :
            query_filtered.append(t)

    #Stemming
    stemmer = PorterStemmer()
    querylist = []

    for query_t in query_filtered:
        querylist.append(stemmer.stem(query_t))

    return querylist

def search_engine(querylist) :
    data = pd.read_csv("Food Ingredients and Recipe Dataset with Image Name Mapping.csv")
    data = data[data['Ingredients'].str.len() > 2]
    score = text_result.score
       
    #search Engine
    rankdocs = []
    index = []
    idx = 0
    for score in scores :
        val = 0
        idx = idx + 1;
        for word, frequency in score :
            for query in querylist :
                if word == query :
                    val = val + frequency

        if(val != 0) :
            index.append(idx)
            rankdocs.append(val)

    temp_index = [x for _,x in sorted(zip(rankdocs, index), reverse=True)]
    temp_rankdocs = np.sort(rankdocs)[::-1]
    result = []
    
    for i in range(len(index)) :
        result.append(data.iloc[temp_index[i]-1])
        #print(str(temp_index[i]-1) + ":" + str(data.iloc[temp_index[i]-1]["Title"]) + ":" + str(temp_rankdocs[i]))
       
    return result
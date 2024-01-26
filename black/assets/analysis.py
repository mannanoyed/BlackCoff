import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
import nltk.data
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
#  nltk.download('stopwords')

from nltk.stem import WordNetLemmatizer
import re

import curses
from curses.ascii import isdigit
from nltk.corpus import cmudict


### MASTER DICTIONARY ###
positive_data = open("MasterDictionary/positive-words.txt", "r")
positive_wds = positive_data.read() 
negative_data = open("MasterDictionary/negative-words.txt", "r")
negative_wds = negative_data.read()


### SENTIMENTAL STOPWORDS LIST ###


file = open("StopWords/StopWords_auditor.txt","r")
s = file.read()
stopwords_sentiment = list(re.split(r'\n| ', s))

file = open("StopWords/StopWords_Currencies.txt","r")
s = file.read()
s = s.replace('\n', '')
s = s.replace('|', '')
stop = list(re.split(r'\n| ', s))
stopwords_sentiment.extend(stop)


file = open("StopWords/StopWords_DatesandNumbers.txt","r")
s = file.read()
stop = list(re.split(r'\n| ', s))
stopwords_sentiment.extend(stop)


file = open("StopWords/StopWords_Generic.txt","r")
s = file.read()
stop = list(re.split(r'\n| ', s))
stopwords_sentiment.extend(stop)


file = open("StopWords/StopWords_Geographic.txt","r")
s = file.read()
s = s.replace('|', '')
stop = list(re.split(r'\n| ', s))
stopwords_sentiment.extend(stop)


file = open("StopWords/StopWords_GenericLong.txt","r")
s = file.read()
stop = list(re.split(r'\n| ', s))
stopwords_sentiment.extend(stop)


file = open("StopWords/StopWords_Names.txt","r")
s = file.read()
stop = list(re.split(r'\n| ', s))
stopwords_sentiment.extend(stop)

### DICTIONARY FOR SYLLABEL ###
d = cmudict.dict()










path = './text' 
if not os.path.exists(path):
    os.makedirs(path)
df = pd.read_excel("input.xlsx")


### DATA ABSTRACTION WITH BEAUTIFULSOUP ###
ind=0
for ind in df.index:
    x = df["URL"].loc[ind]
    file_name = ind
    
    req = requests.get(x)
    soup = BeautifulSoup(req.content,"html.parser")
    title = soup.title.string
    result = soup.find("div", {"class":"td-post-content tagdiv-type"})
    if result is None:
        r = str("")
    else:
        r =result.text
    with open('text/{}.txt'.format(file_name), mode='wt', encoding='utf-8') as file:
        file.write(title)
        file.write(r)




df["POSITIVE SCORE"] = ''
df["NEGATIVE SCORE"] = ''
df["POLARITY SCORE"] = ''
df["SUBJECTIVITY SCORE"] = ''
df["AVG SENTENCE LENGTH"] = ''
df["PERCENTAGE OF COMPLEX WORDS"] = ''
df["FOG INDEX"] = ''
df["AVG NUMBER OF WORDS PER SENTENCE"] = ''
df["COMPLEX WORD COUNT"] = ''
df["WORD COUNT"] = ''
df["SYLLABLE PER WORD"] = ''
df["PERSONAL PRONOUNS"] = ''
df["AVG WORD LENGTH"] = ''

### VARIABLE DECLARATION ###

number_of_sentences = 0
number_of_words = 0
avg_syllabel = 0


## VARIABLES FOR DERIVATION ##
pos_score = 0
neg_score = 0
polarity = 0
subjectivity = 0

avg_sent_length =0
percentage_of_complex_words=0
fog_index=0
complex_words= 0

word_count = 0
syllabel_per_word=0
personal_pronoun_count = 0
avg_word_len = 0
    









i=0
for i in df.index:

    filename = f"{i}"
    f = open('text/{}.txt'.format(filename),"r",encoding='utf-8')
    
    r = f.read()

    def remove_punctuation(text):
        # Define the regex pattern for punctuation
        punctuation_pattern = re.compile(r'[^\w\s]')

        # Use the pattern to substitute punctuation with an empty string
        text_without_punctuation = punctuation_pattern.sub('', text)

        return text_without_punctuation

    raw = remove_punctuation(r)


    tokenized_sentences=nltk.sent_tokenize(r)
    tokenized_words=nltk.word_tokenize(raw)




    ### NUMBER OF SENTENCE, WORDS AND AVERAGE SENTENCE LENGTH ###


    for each_sentence in tokenized_sentences:
        words=nltk.tokenize.word_tokenize(each_sentence)
        number_of_sentences += 1



    for each_word in tokenized_words:
        words=nltk.tokenize.word_tokenize(each_word)
        number_of_words += 1

    avg_sent_length =   number_of_words/number_of_sentences



    ### Extracting Derived variables ###

    filtered_tokens = [item for item in tokenized_words if not item in stopwords_sentiment]


    for tokens in filtered_tokens:
        if tokens in positive_wds:
             pos_score += 1
        if tokens in negative_wds:
             neg_score -= 1

    neg_score = neg_score * (-1)


    polarity = (pos_score-neg_score)/((pos_score+neg_score)+0.000001)

    subjectivity = (pos_score + neg_score)/((len(filtered_tokens))+0.000001)



    ### AVG WORD LENGTH ###

    avg_word_len = sum(len(tokenized_words) for word in tokenized_words) / number_of_words



    ### PERSONAL_PRONOUN ###

    pattern = re.compile(r'\b(?:I|we|my|our|(?-i:us))\b', flags=re.IGNORECASE)
    matches = pattern.findall(raw)
    personal_pronoun_count = len(matches)



    ### NUMBER of syllaber per word (avg)  ###

    if raw.lower() in d:
        syllabel_count = max([len(list(y for y in x if y[-1].isdigit())) for x in d[raw.lower()]])
        
                       
    else:
        # If the word is not found in the dictionary, use a simple count of vowels as a fallback
        vowels = "aeiouAEIOU"
        syllabel_count = sum(1 for char in raw if char in vowels)

    for word in tokenized_words:
         if word.endswith("es") or word.endswith("ed"):
              syllabel_count -=1
    


    avg_syllabel = syllabel_count/number_of_words




    ### COMPLEX WORD ###
 
    vowels = "aeiouAEIOU"
    for words in tokenized_words:
        syllabel_per_word = 0
        for char in words:
              if char in vowels:
                   syllabel_per_word += 1
        if syllabel_per_word>2:
              complex_words += 1
     


    ### PERCENTAGE OF COMPLEX WORDS ###

    percentage_of_complex_words = complex_words/number_of_words



    ### FOG INDEX ###

    fog_index = 0.4*( avg_sent_length + percentage_of_complex_words)



    ### WORD COUNT ###


    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in tokenized_words if not w.lower() in stop_words]
    filtered_sentence = []
    for w in tokenized_words:
        if w not in stop_words:
            filtered_sentence.append(w)

    word_count = len(filtered_sentence)



    
    ### DF ENTRY

    df["POSITIVE SCORE"].loc[i] = pos_score
    df["NEGATIVE SCORE"].iloc[i] = neg_score
    df["POLARITY SCORE"].loc[i] = polarity
    df["SUBJECTIVITY SCORE"].loc[i] = subjectivity
    df["AVG SENTENCE LENGTH"].loc[i] = avg_sent_length
    df["PERCENTAGE OF COMPLEX WORDS"].loc[i] = percentage_of_complex_words
    df["FOG INDEX"].loc[i] = fog_index
    df["AVG NUMBER OF WORDS PER SENTENCE"].loc[i] = avg_sent_length
    df["COMPLEX WORD COUNT"].loc[i] = complex_words
    df["WORD COUNT"].loc[i] = word_count
    df["SYLLABLE PER WORD"].loc[i] = syllabel_per_word
    df["PERSONAL PRONOUNS"].loc[i] = personal_pronoun_count
    df["AVG WORD LENGTH"].loc[i] = avg_word_len




with pd.ExcelWriter('output.xlsx') as excel_writer:
    df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
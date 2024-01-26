#####    Sentimental Analysis for Blackcloffer ####

REQUIREMENT:
--import requests
--bs4 --> BeautifulSoup
--pandas 
--os
--nltk
--nltk.data
--nltk.tokenize 
--from nltk.corpus --> stopwords
--nltk.download('stopwords')
--nltk.stem --> WordNetLemmatizer
--re
--curses
--curses.ascii --> isdigit
--nltk.corpus --> cmudict 


INSTRUCTIONS :

__file directory__

|-blackcloffer
	|--MasterDictionary
	|	|--negative-words.txt
	|	|--positive-words.txt
	|--StopWords
	|	|--StopWords_Auditor
	|	|--StopWords_Currencies
	|	|--StopWords_DatesandNumbers
	|	|--StopWords_Generic
	|	|--StopWords_GenericLong
	|	|--StopWords_Geographic
	|	|--StopWords_Names
	|--analysis.py
	|--Input.xlsx

after assembling the resources run python analysis.py to generate:
	-text folder with abstracted data using beautiful soup named according to the index(can not save url as filename)
	-output.xlsx to for all the genrated results 


Explanation:
	- use pandas to input the file as dataframe
	- loop though the dataframe and pass url in variable to soup requests 
	- after use beautiful soup to abstract title and div "class":"td-post-content tagdiv-type" for text from article.
	- Aplly Exception handling if data is not fetched in automation
	- Save all files abstracted as indexed name
	- after the text folder saved with txt file with index name we can start performing our sentimental analysis
	- import all the needed libraries from pandas, nltk and regex
	- tokenize words and tokenize sentences
	- make custom directory list for both positive and negative words
	- count positive score by comaparing words in positive words list and henceforth for negative and adding counter +1 and -1 respectively
	- negative score = negative score * -1
	- calculate polarity = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
	- calculate subjectivity = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
	- the number of words can be calclulated by len[tokenised_words]
	- the number of words can be calclulated by len[tokenised_sentences]
	- Average Sentence Length = the number of words / the number of sentences
	- to calculate syllabel of word the given logic is based on number of vovels in each word hence create a string of vowels uppercase and lower case vowels=[aeiouAEIOU]
	- for complex word count then add a counter to check each character of word if they are greater than 2 to find out number of complex words
	- with the same technique we can calculate the total number of syllabales 
	- add else conditon to scan through words if they end with 'et', 'ed' ,'er' and do counter-- 
	- after acquiring these above varibales apply in the formula
	- Percentage of Complex words = the number of complex words / the number of words
	- Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
	- to remove stopwords we can create a filtered list which scans compares both stopword and tokenised_words and enter into the list by using ``if not in``
	- to remove punctuation use regex pattern for punctuation and Use the pattern to substitute punctuation with an empty string
	- for personal pronouns use regex to find words in raw file where it is I, we, us, our, my with IGNORECASE to subsitute the case where us and US are considered different we are appying condition in regex to only consider smallcase (us and not US)
	- to calculate average wordlenth we loop through tokenizised_words using sum and len function ``sum(len(tokenised_words)`` 
	- after getting all the derived variables we save it back in out input dataframe and export it to excel


As it is an auotmated process for data abstraction some pages may not allow for text abstraction all the time for which we have added an if conditon working as an exception.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@ MANN VISHNOI
email: mannvishnoi100@gmail.com			
ph : 08375044287
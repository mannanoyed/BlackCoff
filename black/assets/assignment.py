import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

path = './text' 
if not os.path.exists(path):
    os.makedirs(path)
df = pd.read_excel("input.xlsx")



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




import pandas as pd
import json
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
from nltk.stem import LancasterStemmer
lancaster=LancasterStemmer()
from nltk.tokenize import word_tokenize

# Import NERFunctions.py
# NERFunctions contains the preprocessing and searching functions 

import NERFunctions 

question=''
sentence=NERFunctions.preprocess(question)

# READ CSV FILE
df = pd.read_csv("./EntityLables.csv")
# Or Read Pickel FIle
#df = pd.read_pickle("./EntityLables.pkl") 
Search_list=[]
NERFunctions.SearchEntity(Search_list,df,sentence,pd,word_tokenize)

print(Search_list)

Entity=[]
Label=[]
if len(Search_list)>=1:
        entity=NERFunctions.findLable(Search_list,sentence)
        Label=entity[0]
        Entity=entity[1]
        print(Entity ,Label)
else:
    print('Entity Not found ,make sure the spelling is correct and entity is present in the excel file database.')

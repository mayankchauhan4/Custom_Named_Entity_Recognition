# -*- coding: utf-8 -*-
"""
Created on Mon May 24 20:15:08 2021

@author: MayankChauhan
"""


def preprocess(question):
    sentence=question.lower()
    sentence=sentence.replace('ampersand','&')
    replacevalues=["'",'"','?',',','what is','(',')']
    for i in replacevalues:
        sentence=sentence.replace(i,' ')
    return sentence

def findLable(Search_list,sentence):
        import pandas as pd
        from functools import reduce
        Search_list2=reduce(lambda x,y: x+y,Search_list)
        
        result=pd.DataFrame(Search_list2, columns= ['ACTUAL_ENTITIES','ALIAS','LABLE','SIMILARITY_VALUE','SEARCHED_GRAM','Entitylen','CONDITIONAL_ALIAS'])
        ranked = result[(result['SEARCHED_GRAM'] == result['Entitylen'])] 
        ranked.drop_duplicates(subset ="ACTUAL_ENTITIES", keep = 'last', inplace = True)
        #######if CONDITIONAL_ALIAS is yes remove it from the table because it will not be found in sentence
        colname=[]
        entityname=[]
        Aliasyes=ranked[ranked['CONDITIONAL_ALIAS']=='Yes']
        Aliasno=ranked[ranked['CONDITIONAL_ALIAS']=='No']
        
        if Aliasno.empty==False:
            List_of_similar = list(Aliasno[Aliasno.columns[0]])
            Label_for_similar = list(Aliasno[Aliasno.columns[2]])
            sent_to_word = sentence.split()
            
            sent_to_word=[x.lower() for x in sent_to_word]
            Nested_List_of_similar = []
            ###########################
            
            for it in List_of_similar:
                if str(it).count(' ')>0:        
                    nl = it.split()
                    Nested_List_of_similar.append(nl)
                else:
                    Nested_List_of_similar.append([it])
            status=[]
            fnd = []
            finallist=[]
            for i in Nested_List_of_similar:
                for j in range(len(i)):
                    if i[j].lower() in sent_to_word:
                        fnd.append(i[j])
                        status.append(0)
                    else:
                        status.append(1)
                if 1 in status:
                    pass
                else:
                    if len(fnd)>=1:
                        finallist.append(fnd)
                status=[]
                fnd=[]
            #print(finallist)
            
            for i in finallist:
                entity=' '.join(i)
                entityname.append(entity)
                if entity in List_of_similar:
                    index=List_of_similar.index(entity)
                    colname.append(Label_for_similar[index])
          
        if Aliasyes.empty==False:
            List_of_similar = list(Aliasyes[Aliasyes.columns[0]])
            Label_for_similar = list(Aliasyes[Aliasyes.columns[2]])
            for i in range(len(List_of_similar)):
                entityname.append(List_of_similar[i])
                colname.append(Label_for_similar[i])
        Entity=[colname,entityname]
        return Entity


def SearchEntity(Search_list,df,sentence,pd,word_tokenize):
    import threading
    
    from nltk.util import ngrams
    from sklearn.feature_extraction.text import TfidfVectorizer
    from functools import reduce
    from sklearn.metrics.pairwise import cosine_similarity
    global_lock = threading.Lock()
    Entity_Alias = list(df['ENTITY_ALIAS'])
    Actual = list(df['ENTITY'])
    Label = list(df['LABEL'])
    Conditional_Alias = list(df['CONDITIONAL_ALIAS'])
    ln_of_sent_by_words=len(sentence.split())
    if ln_of_sent_by_words >10:
        ln_of_sent_by_words = 10
    def for_ngram_list(sentence):
        ngrams_list = []
    
        def ngramsTokenizer(sentence, n):
            n_grams = ngrams(word_tokenize(sentence), n)
            return [ ' '.join(grams) for grams in n_grams]
               
        for rn in range(ln_of_sent_by_words):       
            ngrams_list.append(ngramsTokenizer(sentence, rn+1))
            
        return ngrams_list
    #new_sents='saga'
    
    def ngram_similar(new_sents):   
            #inserting sentence on top
    #        global Entity_Alias
            gramlen = len(new_sents.split())
            gramlist=[]
            entitylenlist=[]
            Entity_Alias.insert(0,new_sents)
            
    #            from sklearn.feature_extraction.text import TfidfVectorizer
            TfidfVectorizer_model = TfidfVectorizer()
            
            Tfidf_matrix = TfidfVectorizer_model.fit_transform(Entity_Alias)
    
            val = cosine_similarity(Tfidf_matrix[0:1],Tfidf_matrix)
            val_list =val.tolist()
            
            Entity_Alias.remove(new_sents)
            val_list[0].pop(0)
    
            for i in range(len(Entity_Alias)):
                entitylen=len(str(Entity_Alias[i]).split())
                gramlist.append(gramlen)
                entitylenlist.append(entitylen)
            Similarity = pd.DataFrame(list(zip(Actual,Entity_Alias,Label,val_list[0],gramlist,entitylenlist,Conditional_Alias)),columns=['ACTUAL_ENTITIES','ALIAS','LABLE','SIMILARITY_VALUE','SearchGram','EntityLen','CONDITIONAL_ALIAS'])
            subst = Similarity[Similarity['SIMILARITY_VALUE']>=0.99]
    
            result_list = subst.values.tolist()
            if len(result_list)!=0:
                global_lock.acquire()
                Search_list.append(result_list)
                global_lock.release()
    
    ngrams_list=for_ngram_list(sentence)
    
    ngrams_list2=reduce(lambda x,y: x+y,ngrams_list)
    
    threads = []
    
    for i in range(len(ngrams_list2)-1):
    
        t = threading.Thread(target = ngram_similar, args = (ngrams_list2[i],))
        threads.append(t)
        t.start()
        t.join()
    return Search_list 
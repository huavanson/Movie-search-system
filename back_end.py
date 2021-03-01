import datetime
import os
import time
import math
import numpy as np
import re 

import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.neighbors import NearestNeighbors

from pyvi import ViTokenizer, ViPosTagger

def load_data(path) :
  df = pd.read_csv(path)
  df = df.drop('Unnamed: 0',1)
  return df

def remove_stopword(query):
  stop_word = ['bị', 'bởi', 'cả', 'các', 'cái', 'cần', 'càng', 'chỉ',
               'chiếc', 'cho', 'chứ', 'chưa', 'chuyện', 'có', 'có_thể', 'cứ', 'của', 'cùng', 'cũng', 'đã', 
               'đang', 'đây', 'để', 'đến_nỗi', 'đều', 'điều', 'do', 'đó', 'được', 'dưới', 'gì', 'khi', 'không', 'là',
               'lại', 'lên', 'lúc', 'mà', 'mỗi', 'một_cách', 'này', 'nên', 'nếu', 'ngay', 'nhiều', 'như', 'nhưng', 'những',
               'nơi', 'nữa', 'phải', 'qua', 'ra', 'rằng', 'rằng', 'rất', 'rất', 'rồi', 'sau', 'sẽ', 'so', 'sự', 'tại', 'theo',
               'thì', 'trên', 'trước', 'từ', 'từng', 'và', 'vẫn', 'vào', 'vậy', 'vì', 'việc', 'với', 'vừa']
  result = []             
  for word in query.split():
    if word not in stop_word :
      result.append(word)
  return ' '.join(result)

def pos (query):
  query = re.sub(r'[?|$|.|!|<|=|,|\-|\'|\“|\”]',r'', query )
  b = ViPosTagger.postagging(ViTokenizer.tokenize(query))
  important = ['N', 'Nc', 'Ny', 'Np', 'Nu', 'A', 'V']
  result = []
  for i in range (len(b[1])):
    if (b[1][i]  in important):
      result.append(b[0][i])
  return ' '.join(result)

def input_query(a):
  return pos(a)

def preprocess(new_df):
  for index in range (len(new_df['Content'])):
    temp = pos(str(new_df['Content'][index]))
    temp = remove_stopword(temp)
    new_df['Content'][index] = temp
  return new_df


def append_new_query_to_tail(in_put):
  global main_df1
  new_df = main_df1.append({'Content': input_query(in_put)}, ignore_index= True)
  return new_df

def remove_tail():
  global main_df1
  main_df1 = main_df1.drop([main_df1.tail(1).index[0]],axis=0)

def search_engine(new_df,k) :  
  count_vect = CountVectorizer()
  
  X_train_counts = count_vect.fit_transform(new_df['Content'].apply(lambda X_train_counts: np.str_(X_train_counts)))

  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
  tfidf_matrix = X_train_tfidf.toarray()

  neigh = NearestNeighbors(n_neighbors=k, metric='cosine')
  neigh.fit(X_train_tfidf)

  (distance, found_index) = neigh.kneighbors([tfidf_matrix[-1]])
  result = new_df.iloc[found_index.tolist()[0]]
  return result

########################################## begin - part 2 #####################################
def append_new_query_to_tail_df2(df, in_put):
  new_df = df.append({'Content': input_query(in_put)}, ignore_index= True)
  return new_df

def remove_tail_df2():
  global main_df2
  main_df2 = main_df2.drop([main_df2.tail(1).index[0]],axis=0)

def group_by_category(df):
  df2 = df.groupby(['URL','Viet-name','Content','rank'])['Category'].apply(','.join).reset_index()
  return df2

def cate_query(list_cate) :
  global main_df2
  list_df = []
  for i in range(len(list_cate)):
    cate_df = main_df2[main_df2['Category']==list_cate[i]]
    list_df.append(cate_df)
  new_df = pd.concat(list_df).reset_index()
  new_df = new_df.drop('index' ,1)
  
  return new_df
def get_rank (dataframe):
    # tạo list gồm tên phim trong r
    name = list(dataframe['Viet-name'])
    count = 0
    rank = []
    for i in range (1, len(name)):
        # những phim nào trùng tên thì cho cùng 1 mức rank 
        if (name[i]!= name[i-1]):
            count+=1
        rank.append(count)
    # bỏ row đầu chứa cái query
    final = dataframe.iloc[1:]
    final.insert(0, 'rank', rank, True)
    group_cate = group_by_category(final)
    # sort dataframe theo rank 
    group_cate.sort_values(by= ['rank'], inplace= True)
    return group_cate
########################################## end - part 2 #####################################

main_df1 = pd.read_csv('data_posed_2.csv')
main_df2 = pd.read_csv('data_posed_3.csv')


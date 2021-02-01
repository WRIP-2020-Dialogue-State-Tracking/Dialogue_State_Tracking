# -*- coding: utf-8 -*-
"""WRIP_TASK_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OfgawP_XWK_4mCOT9CG9UN4dxuE13wsz
"""

import json
import os

import numpy as np
import pandas as pd

path = input('Enter the dataset path : ')

domains = ['attraction','hospital','hotel','police','restaurant','taxi','train'] # List of all domains
selected_domains = ['attraction','restaurant','taxi'] # Select the required domains

left_domains = [domain for domain in domains if domain not in selected_domains] # Get the domains to be ignored 

import itertools

dataset = {'__invalid':None}
for r in range(1,len(selected_domains)+1):
  dataset.update({'_' + '_'.join(comb):None for comb in (itertools.combinations(selected_domains, r))}) # Generate all possible comb

mapper = {list(dataset.keys())[i]:i for i in range(0,len(dataset))} # Map every combination to an integer for ease

df = pd.read_json(path).T

def checkValid(goal,left_domains) -> bool: # Checks whether the goal has a domain in left_domains
  return (True if "".join([domain for domain in left_domains if goal[domain]]) == "" else False)

def getDomain(goal,selected_domains,left_domains) -> str: # Gets the domain of goal
  return ("__invalid" if checkValid(goal,left_domains) == False else '_'+'_'.join([domain for domain in selected_domains if goal[domain]]))

df['domain'] = [getDomain(x,selected_domains,left_domains) for x in df['goal']]
df['domain_key'] = [mapper[x] for x in df['domain']]

stats = df['domain'].value_counts().reset_index().values 

for index,key in enumerate(dataset):
  if not key == '__invalid':
    tempDf = df[df['domain_key']==index].copy(deep=True)
    if tempDf.empty == False:
      os.makedirs('dataset/{}'.format(key), exist_ok=True)
      os.makedirs('dataset/dataset_txt/{}'.format(key),exist_ok=True)
      with open('dataset/{}/list.json'.format(key),'w') as f:
        json.dump(list(tempDf.index),f)
      for index,i in enumerate(tempDf.index):
        tempDf.iloc[[index]][['goal','log']].T.to_json("dataset/{}/{}".format(key,tempDf.index[index]))
      tempDf['log'] =  [[{'text':item['text']} for item in x] for x in tempDf['log']]
      for index,i in enumerate(tempDf.index):
        tempDf.iloc[[index]][['goal','log']].T.to_json("dataset/dataset_txt/{}/{}_txt.json".format(key,str(tempDf.index[index]).split('.')[0]))
    else:
      stats = np.vstack((stats,np.array([key,0])))

pd.DataFrame(stats,columns=['Domain','Count']).to_excel('stats.xlsx') # Dump as xlsx
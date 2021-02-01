import constants
from typing import List
import typings

import numpy as np
import pandas as pd
import itertools

def splitIntoDomains(dataset_path:str,domains:List[str],selected_domains:List[str]) -> typings.dataset:
  """Splits the dataset into all possible combinations of domains.

  To be used in conjunction with `getDatasetofDomain()`

  Args:

      datasetpath : Path of data.json file
      domains : Array of string containing all possible domains
      selecteddomains : Array of string containing all selected domains domains

  Returns:
      dataset: A dictionary containing Dataframes for all possible domains and a stats Dataframe for stats.
  """  
  left_domains = [domain for domain in domains if domain not in selected_domains] # Get the domains to be ignored 
  dataset = {'__invalid':None}
  for r in range(1,len(selected_domains)+1):
    dataset.update({'_' + '_'.join(comb):None for comb in (itertools.combinations(selected_domains, r))}) # Generate all possible comb

  mapper = {list(dataset.keys())[i]:i for i in range(0,len(dataset))} # Map every combination to an integer for ease

  df = pd.read_json(dataset_path).T

  def checkValid(goal,left_domains) -> bool: # Checks whether the goal has a domain in left_domains
    return (True if "".join([domain for domain in left_domains if goal[domain]]) == "" else False)

  def getDomain(goal,selected_domains,left_domains) -> str: # Gets the domain of goal
    return ("__invalid" if checkValid(goal,left_domains) == False else '_'+'_'.join([domain for domain in selected_domains if goal[domain]]))

  df['domain'] = [getDomain(x,selected_domains,left_domains) for x in df['goal']]
  df['domain_key'] = [mapper[x] for x in df['domain']]

  stats = df['domain'].value_counts().reset_index().values 

  for index,key in enumerate(dataset):
    if not key == '__invalid':
      tempDf = df[df['domain_key']==index].copy(deep=False)
      dataset[key] = tempDf[['goal','log']].T
      if tempDf.empty == False:
         stats = np.vstack((stats,np.array([key,0])))
       
  dataset['__status'] = pd.DataFrame(stats,columns=['Domain','Count'])
  return dataset

def getDatasetOfDomain(domains:List[str],dataset:typings.dataset) -> typings.dataframe:
  """ Returns the dataframe of requested domain

  Arguments:

      domains list : Array of string containing name of required domains
      dataset dict : DataFrame dictionary generated from splitIntoDomains

  Returns:

      pd.DataFrame : DataFrame of requested domain
  """  
  domains.sort()
  domain_string = '_'+'_'.join(list(domains))
  return dataset[domain_string]

if __name__ == "__main__":
    splitDataset = splitIntoDomains('a',constants.domains,constants.selected_domains)
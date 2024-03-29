import json
import os
import typings

def writeSplitDatasetToJson(dataset:typings.dataset,split:bool):
  """
  Write the dataset generate by `segregate.py` into separate json files and dumps the stats as stats.xlsx

  Args:
  
      dataset : dataset generated by segregate
      split : Whether to also write split dataset consisting of only conversations.
  """  
  for index,key in enumerate(dataset):
    os.makedirs('dataset',exist_ok=True)
    if (key != "__status" and key!='__invalid'):
      os.makedirs('dataset/{}'.format(key), exist_ok=True)
      os.makedirs('dataset/dataset_txt/{}'.format(key),exist_ok=True)
      tempDf = dataset[key].T
      with open('dataset/{}/list.json'.format(key),'w') as f:
        json.dump(list(tempDf.index),f)
      for index in range(0,len(tempDf.index)):
        with open("dataset/{}/{}".format(key,tempDf.index[index]), 'w', encoding='utf-8') as file:
          json.dump(json.loads(str(tempDf.iloc[[index]][['goal','log']].T.to_json(force_ascii=False)).replace("null","")),file,ensure_ascii=False,indent=4)
      print("{} files written!".format(len(tempDf.index)))
      if split == True:
        tempDf['log'] =  [[{'text':item['text']} for item in x] for x in tempDf['log']]
        for index in range(0,len(tempDf.index)):
          with open("dataset/dataset_txt/{}/{}_txt.json".format(key,str(tempDf.index[index]).split('.')[0]), 'w', encoding='utf-8') as file:
            json.dump(json.loads(str(tempDf.iloc[[index]][['goal','log']].T.to_json(force_ascii=False)).replace("null","")),file,ensure_ascii=False,indent=4)
        print("Splitting files! {} files written!".format(len(tempDf.index)))
  dataset['__status'].to_excel('dataset/stats.xlsx')
  print("Stats.xlsx written!")

if __name__ == "__main__":
  pass
     
    

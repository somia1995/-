import json
import pandas as pd

def analysis(file,user_id):
      
   # filepath = '/home/shiyanlou/Code/user_study.json' 
    try:
      df=pd.read_json(file) 
   # minutes = df[df['user_id']==userid]['minutes'].sum()
   # t = df[df['user_id'] == user_id] 
   # times = t['user_id'].value_counts().sum()
    except:
     return 0,0  

    df = df[df['user_id'] == user_id].minutes
   
    return df.count(),df.sum()
   

print(analysis('user_study.json',199071))

    

        
 


import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

def getPosition(position):
    print(f'scraping position: {position}')
    url=f'https://rivals.rivals.com/position_rankings/Football/2023/{position}'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'lxml')
    dirty_string=soup.find('rv-state-ranking')['prospects']
    json_string=dirty_string.replace('"{','{').replace('}"','}').replace('\\','')
    return pd.DataFrame(json.loads(json_string))

def getRating(prospect_url):
    prospect_page=requests.get(prospect_url)
    soup=BeautifulSoup(prospect_page.text,'lxml')
    return soup.find('div',{'data-philter':'prospect-profile-rating-rank-number'}).text
    
def getPlayers(file):
    positions = ['APB','ATH','C','CB','DT','DUAL','ILB','OG','OLB','OT','PRO','RB','S','SDE','TE','WDE','WR']
    df_list=[getPosition(pos) for pos in positions]
    df=pd.concat(df_list)
    df.to_csv(file,index=False)

def getPlayerRatings(input_file,start_index,output_file):
    df=pd.read_csv(input_file).sort_values(by='id').reset_index(drop=True)
    rows=[]
    for index,row in df.iloc[start_index:].iterrows():
        print(f'requesting index: {index}')
        rating=None
        try:
            rating=getRating(row.prospect_url)
        except:
            break
        rows.append({'id':row.id, 'rating':rating})
    df=pd.DataFrame(rows)
    df.to_csv(output_file,index=False)
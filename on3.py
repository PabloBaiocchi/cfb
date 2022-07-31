import requests
import numpy as np
import pandas as pd

playersDf=None
ratingsDf=None

def getPage(page,year):
    print(f'requestiong.. year: {year}   page: {page}')
    base_url='https://api.on3.com/public/rdb/v1/players/industry-comparision'
    params={
        'sportKey':1,
        'year':year,
        'page':page,
        'sortByIndustry':'On3Consensus'
    }
    res=requests.get(base_url,params=params)
    if res.status_code!=200:
        return None
    return res.json()

def processPlayers(playerList):
    global playersDf
    global ratingsDf
    players=[]
    ratings=[]
    for item in playerList:
        players.append(item['person'])
        for rating in item['ratings']:
            rating['key']=item['person']['key']
        ratings=ratings+item['ratings']
    pDf=pd.DataFrame(players)
    rDf=pd.DataFrame(ratings)
    if playersDf is None:
        playersDf=pDf
        ratingsDf=rDf
    else:
        playersDf=pd.concat([playersDf,pDf])
        ratingsDf=pd.concat([ratingsDf,rDf])

def scrape(year,startPage=1):
    firstPage=getPage(1,year)
    page_count=firstPage['pagination']['pageCount']
    if startPage==1:
        processPlayers(firstPage['list'])
    for page in np.arange(2 if startPage==1 else startPage,page_count+1):
        response=getPage(page,year)
        processPlayers(response['list'])

def run(playerFile,ratingFile,startYear,endYear,startPage):
    global playersDf
    global ratingsDf
    for year in np.arange(startYear,endYear+1):
        firstPage=startPage if year==startYear else 1
        try:
            scrape(year,firstPage)
        except Exception as e:
            print('ERROR!!')
            print(e)
    playersDf.to_csv(playerFile,index=False)
    ratingsDf.to_csv(ratingFile,index=False)

    
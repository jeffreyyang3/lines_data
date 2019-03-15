import pandas as pd
import json
import sys


def initialRead(fileName):

    df = pd.read_csv(fileName)
    for thing in df:
        print(thing)
    return df


def getMetadata(df, startIndex):
    allMeta = df.iloc[startIndex]['player.allMetadata']
    return allMeta


def getSessionLevel(playerAllMeta):
    sessionLevel = {}
    for key in playerAllMeta:
        sessionLevel['numPlayers'] = len(playerAllMeta[key]['queue'])
        date = str(pd.to_datetime(key, unit='ms'))
        date = date.split()[0]
        sessionLevel['sessionDate'] = date
        return sessionLevel


print(initialRead("linez.csv"))
allMetadata = json.loads(getMetadata(initialRead("linez.csv"), 0))


print(getSessionLevel(json.loads(allMetadata['1'])))


'''
structure: 

{
  date
  numSubjects
  period: {
    master: all swaps (metadata)
    players: list -> {
      cost: 
      value:
      endowment:
      finalEarning:
      history: {
        player.metadata
      }
    }
  }




}

metadata should contain: IDs, timestamp, action, message

'''

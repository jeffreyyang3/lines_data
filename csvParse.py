import pandas as pd
import json
import sys
df = pd.read_csv(sys.argv[1])

for thing in df:
    print(thing)


for i in range(len(df)):
    print(df.iloc[i]['player.metadata'])


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

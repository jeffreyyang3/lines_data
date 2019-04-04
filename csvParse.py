import pandas as pd
import json
import sys


def getMetadata(df, startIndex):
    allMeta = df.iloc[startIndex]['player.allMetadata']
    return allMeta

# session data (date, number of subjects, exchange type) can all be taken from part of swap metadata
# need:


def getSessionLevel(playerAllMeta):
    for key in playerAllMeta:
        date = str(pd.to_datetime(key, unit='ms'))
        date = date.split()[0]
        return {
            'numPlayers': len(playerAllMeta[key]['queue']),
            'sessionDate': date
        }


def getPeriods(base, numPlayers):
    periods = []
    for i in range(0, len(base) - 3, 4):
        periods.append(base[i:i+4])
    print(len(base))
    print(len(periods))

    return periods


def periodLevel(df):  # need swap method, communication, numplayers, totaltime,
    examplePlayer = df.iloc[0]
    allSwaps = json.loads(examplePlayer['player.allMetadata'])

    return {
        'swapMethod': examplePlayer['player.swap_method'],
        'payMethod': examplePlayer['player.pay_method'],
        'messageEnabled': bool(examplePlayer['player.messaging'] == 1),
        'discrete': bool(examplePlayer['player.discrete'] == 1),
        'allSwaps': json.loads(df.iloc[0]['player.allMetadata']),
        'players': [{
            'playerNumber': int(df.iloc[i]['player.id_in_group']),
            'cost': float(df.iloc[i]['player.cost']),
            'endowment': float(df.iloc[i]['player.endowment']),
            'payRate': float(df.iloc[i]['player.pay_rate']),
            'payoff': float(df.iloc[i]['player.round_payoff']),
            'history': json.loads(df.iloc[i]['player.metadata']),
        }
            for i in range(df.shape[0])],
    }
# check if metadata includes: player ids, timestamp, action
# individual-session: need rounds chosen for payment, show fee,


topLevel = {}
inFile = pd.read_csv(sys.argv[1])
allMetadata = json.loads(getMetadata(inFile, 0))
sessionLevel = getSessionLevel(json.loads(allMetadata['1']))
sessionLevel['periods'] = [periodLevel(period)
                           for period in getPeriods(inFile, 4)]
# 4 players hardcoded at the moment

"""for key in sessionLevel['periods'][0]:
    print(key)
    print(type(sessionLevel['periods'][0][key])) """
with open('out.json', 'w') as outfile:
    json.dump(sessionLevel, outfile)

# for thing in inFile:
#    print(thing)
'''

for example:
  import json

  js = json.loads(open('out.json').read())
  js['sessionDate']
  js['periods'][0]['swapMethod']
  js['periods'][0]['payMethod']
  js['periods'][0]['players'][1]['endowment']
  js['periods'][0]['players'][1]['payoff']
  js['periods'][0]['players'][1]['payoff']

  p1Players = js['periods'][0]['players']
  for i in range(len(p1Players)):
    print(p1Players[i]['cost'])




structure:

{
  date
  numSubjects
  period: {
    allSwaps: all swaps (metadata)
    swap method
    pay method

    players: list -> {
      cost:
      value:
      endowment:
      finalEarning:
      history: {
        contains all transactions involving this player
      }
    }
  }




}

metadata should contain: IDs, timestamp, action, message

'''

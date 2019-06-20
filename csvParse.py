import pandas as pd
import json
import sys
import operator
from dateutil import parser
from datetime import timedelta


def getMetadata(df, startIndex):
    allMeta = df.iloc[startIndex]["player.allMetadata"]
    return allMeta


# session data (date, number of subjects, exchange type) can all be taken from part of swap metadata
# need: group size, total period time, player swap time ompared to start


def getSessionLevel(playerAllMeta):
    for key in playerAllMeta:
        date = str(pd.to_datetime(key, unit="ms"))
        date = date.split()[0]
        return {"groupSize": len(playerAllMeta[key]["queue"]), "sessionDate": date}


def getPeriods(base, numPlayers):
    periods = []
    for i in range(0, len(base) - numPlayers - 1, numPlayers):
        periods.append(base[i: i + numPlayers])

    return periods


def allMetaCheck(meta):
    print("yo yo yo ")
    print(meta)
    print(type(meta))


def createTs(timestring):
    if isinstance(timestring, str):
        entryTime = parser.parse(timestring)
        +timedelta(hours=9)
        entryTime = entryTime.timestamp()
        return entryTime
    else:
        print(timestring)
        print("problem")


def getPlayerHistory(history, num, entry):
    playerTransactions = []
    one = json.loads(history["1"])

    for key in one:
        conv = int(key) / 1000
        if one[key]["requester"] == num or one[key]["requestee"] == num:
            one[key]["originalTS"] = key
            one[key]["timeSinceStart"] = conv - entry
            playerTransactions.append(one[key])
    return playerTransactions


def periodLevel(df):  # need swap method, communication, numplayers, totaltime,
    examplePlayer = df.iloc[0]
    ts = examplePlayer["player.time_Service"]
    entryTime = "na"
    if isinstance(ts, str):
        entryTime = parser.parse(examplePlayer["player.time_Queue"])
        +timedelta(hours=9)
        entryTime = entryTime.timestamp()

    allMeta = json.loads(df.iloc[0]["player.allMetadata"])
    playerHist = json.loads(df.iloc[0]["player.allMetadata"])
    return {
        "entryTime": entryTime,
        "swapMethod": examplePlayer["player.swap_method"],
        "payMethod": examplePlayer["player.pay_method"],
        "messageEnabled": bool(examplePlayer["player.messaging"] == 1),
        "discrete": bool(examplePlayer["player.discrete"] == 1),
        "allSwaps": allMeta,
        # 'allSwaps': allMetaCheck(df.iloc[0]['player.allMetadata']),
        "players": [
            {
                #    "playerEntry": int(df.iloc[i]["player.time_Service"]),
                "playerNumber": int(df.iloc[i]["player.id_in_group"]),
                "playerEntry": createTs(df.iloc[i]["player.time_Queue"]),
                "cost": float(df.iloc[i]["player.cost"]),
                "endowment": float(df.iloc[i]["player.endowment"]),
                "payRate": float(df.iloc[i]["player.pay_rate"]),
                "payoff": float(df.iloc[i]["player.round_payoff"]),
                "history": getPlayerHistory(
                    playerHist,
                    int(df.iloc[i]["player.id_in_group"]),
                    createTs(df.iloc[i]["player.time_Queue"]),
                ),
                # for some reason, empty metadata gets read as NaN, which is a float
                "start_pos": int(df.iloc[i]["player.start_pos"]),
                "end_pos": int(df.iloc[i]["player.end_pos"]),
            }
            for i in range(df.shape[0])
        ],
    }


# check if metadata includes: player ids, timestamp, action
# individual-session: need rounds chosen for payment, show fee,


topLevel = {}
inFile = pd.read_csv(sys.argv[1])
allMetadata = json.loads(getMetadata(inFile, 0))
sessionLevel = getSessionLevel(json.loads(allMetadata["1"]))
sessionLevel["periods"] = [periodLevel(period)
                           for period in getPeriods(inFile, 8)]
"""for key in sessionLevel['periods'][0]:
    print(key)
    print(type(sessionLevel['periods'][0][key])) """

allTransactions = {}


for period in sessionLevel['periods']:
    for player in period['players']:
        for transaction in player['history']:
            if transaction['originalTS'] not in allTransactions:
                allTransactions[transaction['originalTS']] = transaction

allTransactionsList = [allTransactions[key] for key in allTransactions]
allTransactionsList.sort(key=lambda x: int(x['originalTS']))

allTransactionsDictDf = pd.DataFrame.from_dict(allTransactions)
allTransactionsListDf = pd.DataFrame(allTransactionsList)
otherDataDf = pd.DataFrame.from_dict(sessionLevel)

allTransactionsDictDf.to_csv('allTransactionsDictDf.csv')
allTransactionsListDf.to_csv('allTransactionsListDf.csv')
otherDataDf.to_csv('otherDataDf.csv')
with open("out.json", "w") as outfile:
    json.dump(sessionLevel, outfile)

"""

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

"""

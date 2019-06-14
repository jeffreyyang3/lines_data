import json
import sys
import pandas as pd

js = json.loads(open(sys.argv[1]).read())


def printTransactions(tDict, startTime):
    asdf = 0
    if startTime != 'na':
        asdf = int(startTime)
        print("XX")
        print(asdf)
        print("xx")

    for key in tDict:

        ts = json.loads(tDict[key])

        if ts:
            for key in ts:
                print("bing")
                print(int(asdf))
                print(int(key))
                print('bong')
                print(str(asdf - int(key)))

                print(
                    "Player {} to Player {}, for ${}, {}".format(
                        ts[key]["requester"],
                        ts[key]["requestee"],
                        ts[key].get("bid"),
                        ts[key]["status"],
                    )
                )
            return


def printPeriodLevel(period):
    print("Period Swap Method: {}".format(period["swapMethod"]))
    for player in period["players"]:
        printPlayerLevel(player)
    #print("all transactions:")
    # printTransactions(period["allSwaps"])
    # print("YO")
    # print(period['entryTime'])


def printPlayerLevel(player):
    print(
        "Player {}: Cost: {} Payoff: {} Start Position: {} End Position: {}".format(
            player["playerNumber"],
            player["cost"],
            player["payoff"],
            player["start_pos"],
            player["end_pos"],
        )
    )


for period in js["periods"]:
    printPeriodLevel(period)


p1Players = js["periods"][0]["players"]


# print("period transactions")
# printTransactions(p1Players[0]["history"])

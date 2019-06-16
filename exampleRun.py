import json
import sys
import pandas as pd

js = json.loads(open(sys.argv[1]).read())


def printTransactions(tList):

    for trans in tList:
        print(
            "Player {} to Player {}, for {}, {}, at {} seconds: message {}".format(
                trans["requester"],
                trans["requestee"],
                trans.get("bid"),
                trans["status"],
                int(trans["timeSinceStart"]),
                trans.get("message"),
            )
        )
    return


def printPeriodLevel(period):
    print("Period Swap Method: {}".format(period["swapMethod"]))
    for player in period["players"]:
        printPlayerLevel(player)
        printTransactions(player["history"])
    print("\n\n\n\n\n")
    # print("all transactions:")
    # printTransactions(period["allSwaps"])
    # print("YO")
    # print(period['entryTime'])


def printPlayerLevel(player):
    print("=====================================================")
    print(
        "Player {}: Cost: {} Payoff: {} Start Position: {} End Position: {}".format(
            player["playerNumber"],
            player["cost"],
            player["payoff"],
            player["start_pos"],
            player["end_pos"],
        )
    )


def printSessionLevel(session):
    for period in session["periods"]:
        printPeriodLevel(period)


printSessionLevel(js)
p1Players = js["periods"][0]["players"]


# print("period transactions")
# printTransactions(p1Players[0]["history"])

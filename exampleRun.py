import json
import sys

js = json.loads(open(sys.argv[1]).read())


def printTransactions(tDict):

    for key in tDict:
        ts = json.loads(tDict[key])
        if ts:
            for key in ts:
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
    print("all transactions:")
    printTransactions(period["allSwaps"])


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

import json

js = json.loads(open('out.json').read())


print("Session Date: {} \nPeriod Swap Method: {}".format(
    js['sessionDate'], js['periods'][0]['swapMethod']))

p1Players = js['periods'][0]['players']


def printTransactions(tDict):
    for key in tDict:
        print("Player {} to Player {}, for ${}, {}".format(
            tDict[key]['requester'], tDict[key]['requestee'], tDict[key].get('bid'), tDict[key]['status']))


for i in range(len(p1Players)):
    print("Player {}: Cost: {} Payoff: {}".format(
        p1Players[i]['playerNumber'], p1Players[i]['cost'], p1Players[i]['payoff'])
    )

print("period transactions")
printTransactions(p1Players[0]['history'])

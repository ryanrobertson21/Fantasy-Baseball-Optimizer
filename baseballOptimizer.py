import csv, itertools
from poolReducer import poolReducer

lineupSpreadsheet = open('/Users/RyanRobertson21/Desktop/baseballData.csv')
lineupReader = csv.reader(lineupSpreadsheet)
playerDict = {}

for row in lineupReader:
    playerList = []
    if lineupReader.line_num == 1:
        continue
    playerList.append(row[1])
    playerList.append(row[3])
    playerList.append(float(row[5]))
    playerList.append(int(row[7]))
    try:
        playerList.append(row[13])
    except IndexError:
        pass
    playerDict[row[0]] = playerList

lineupSpreadsheet.close()

outfielders = {}
for ids in playerDict:
    if playerDict[ids][0] == 'OF':
        outfielders[ids] = playerDict[ids]

pitchers = {}
for ids in playerDict:
    if playerDict[ids][0] == 'P':
        try:
            if playerDict[ids][4] == 'Yes':
                pitchers[ids] = playerDict[ids]
        except IndexError:
            pass

catchers = {}
for ids in playerDict:
    if playerDict[ids][0] == 'C':
        catchers[ids] = playerDict[ids]

firstBase = {}
for ids in playerDict:
    if playerDict[ids][0] == '1B':
        firstBase[ids] = playerDict[ids]

secondBase = {}
for ids in playerDict:
    if playerDict[ids][0] == '2B':
        secondBase[ids] = playerDict[ids]

shortStop = {}
for ids in playerDict:
    if playerDict[ids][0] == 'SS':
        shortStop[ids] = playerDict[ids]

thirdBase = {}
for ids in playerDict:
    if playerDict[ids][0] == '3B':
        thirdBase[ids] = playerDict[ids]


def positionFilter(positionDict):
    filteredDict = {}
    for player in positionDict:
        if positionDict[player][3] not in filteredDict:
            filteredDict[positionDict[player][3]] = positionDict[player]
        else:
            if positionDict[player][2] > filteredDict[positionDict[player][3]][2]:
                filteredDict[positionDict[player][3]] = positionDict[player]
    return filteredDict


print(len(positionFilter(firstBase)))
print(len(positionFilter(secondBase)))
print(len(positionFilter(thirdBase)))
print(len(positionFilter(shortStop)))
print(len(positionFilter(pitchers)))
print(len(positionFilter(catchers)))


outfielderGroups = list(itertools.combinations(outfielders, 3))

allLineups = list(itertools.product(outfielderGroups, pitchers, catchers, firstBase, secondBase, shortStop, thirdBase))

underCap = {}
for lineup in allLineups:
    salary = 0
    projectedPoints = 0
    for item in lineup:
        if type(item) == tuple:
            for of in item:
                salary += playerDict[of][3]
                projectedPoints += playerDict[of][2]
        else:
            salary += playerDict[item][3]
            projectedPoints += playerDict[item][2]
    if salary <= 35000:
        underCap[projectedPoints] = lineup


pp = max(underCap)
optimalLineup = underCap[pp]
capUsed = 0
for item in optimalLineup:
    if type(item) == tuple:
        for of in item:
            capUsed += playerDict[of][3]
            print(playerDict[of][0] + ": " + playerDict[of][1])
    else:
        capUsed += playerDict[item][3]
        print(playerDict[item][0] + ": " + playerDict[item][1])
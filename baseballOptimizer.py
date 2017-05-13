import csv, itertools, copy
from collections import Counter
from poolReducer import poolReducer

lineupSpreadsheet = open('/Users/RyanRobertson21/Desktop/newTest.csv')
lineupReader = csv.reader(lineupSpreadsheet)

print('Reading in Data...')
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

print('Filling in Position Dictionaries...')
pitchers = {}
catchers = {}
firstBase = {}
secondBase = {}
thirdBase = {}
shortStop = {}
outfielders = {}

for ids in playerDict:

    if playerDict[ids][0] == 'P':
        try:
            if playerDict[ids][4] == 'Yes':
                pitchers[ids] = playerDict[ids]
        except IndexError:
            pass

    elif playerDict[ids][0] == 'C':
        catchers[ids] = playerDict[ids]

    elif playerDict[ids][0] == '1B':
        firstBase[ids] = playerDict[ids]

    elif playerDict[ids][0] == '2B':
        secondBase[ids] = playerDict[ids]

    elif playerDict[ids][0] == '3B':
        thirdBase[ids] = playerDict[ids]

    elif playerDict[ids][0] == 'SS':
        shortStop[ids] = playerDict[ids]

    elif playerDict[ids][0] == 'OF':
        outfielders[ids] = playerDict[ids]


print('AFTER LOADING IN THE DATA...')
print('Pitchers: ' + str(len(pitchers)))
print('Catchers: ' + str(len(catchers)))
print('FirstBase: ' + str(len(firstBase)))
print('SecondBase: ' + str(len(secondBase)))
print('ThirdBase: ' + str(len(thirdBase)))
print('ShortStop: ' + str(len(shortStop)))
print('Outfielders: ' + str(len(outfielders)))



def positionFilter(positionDict):
    filteredDict = {}
    for player in positionDict:
        if positionDict[player][3] not in filteredDict:
            filteredDict[positionDict[player][3]] = positionDict[player]
            filteredDict[positionDict[player][3]].append(player)
        else:
            if positionDict[player][2] > filteredDict[positionDict[player][3]][2]:
                filteredDict[positionDict[player][3]] = positionDict[player]
                filteredDict[positionDict[player][3]].append(player)
    return filteredDict



def ofPositionFilter(positionDict):
    outfielderSalaries = []
    for of in positionDict:
        outfielderSalaries.append(positionDict[of][3])

    ofSalaryCounts = Counter(outfielderSalaries)

    outfielderSalariesToFilter = {k: v for k, v in ofSalaryCounts.items() if v > 3}

    for salary in outfielderSalariesToFilter:
        playersWithSameSalary = []
        for of in positionDict:
            if positionDict[of][3] == salary:
                playersWithSameSalary.append(positionDict[of][2])

        ofCopy = copy.deepcopy(positionDict)
        for num in range(outfielderSalariesToFilter[salary] - 3):
            lowestPP = min(playersWithSameSalary)
            for of in ofCopy:
                if ofCopy[of][2] == lowestPP and ofCopy[of][3] == salary:
                    del positionDict[of]
                    playersWithSameSalary.remove(lowestPP)

    return positionDict


def filterMoreExpensiveLessPP(positionDict):
    salariesToDelete = set()

    for salary in positionDict:
        for otherSalaries in positionDict:
            if salary < otherSalaries and positionDict[salary][2] >= positionDict[otherSalaries][2]:
                salariesToDelete.add(otherSalaries)

    for item in salariesToDelete:
        del positionDict[item]

    filteredDict = {}
    for key in positionDict:
        filteredDict[positionDict[key][-1]] = positionDict[key]
    return filteredDict


def ofFilterMoreExpensiveLessPP(positionDict):
    outfielderList = []
    for key in positionDict:
        playerEntry = []
        playerEntry.append(key)
        for info in positionDict[key]:
            playerEntry.append(info)
        outfielderList.append(playerEntry)

    outfielderListSalaryOrder = sorted(outfielderList, key=lambda x: (x[4], x[3] * -1))

    lowestSalaryOutfielders = outfielderListSalaryOrder[0:3]
    count = 1
    while 2 + count < len(outfielderListSalaryOrder) - 1:

        minProjectedPoints = min(lowestSalaryOutfielders, key=lambda x: x[3])

        outfieldersToDelete = []
        for of in outfielderListSalaryOrder[2 + count:]:
            if of[3] < minProjectedPoints[3] and of[4] > minProjectedPoints[4]:
                outfieldersToDelete.append(of)

        outfielderListSalaryOrder = [x for x in outfielderListSalaryOrder if x not in outfieldersToDelete]

        lowestSalaryOutfielders.remove(minProjectedPoints)

        try:
            lowestSalaryOutfielders.append(outfielderListSalaryOrder[2 + count])
        except IndexError:
            break

        count += 1

    return outfielderListSalaryOrder


print('AFTER FIRST FILTER!')
print(len(positionFilter(pitchers)))
print(len(positionFilter(catchers)))
print(len(positionFilter(firstBase)))
print(len(positionFilter(secondBase)))
print(len(positionFilter(thirdBase)))
print(len(positionFilter(shortStop)))
print(len(ofPositionFilter(outfielders)))

pitchers = filterMoreExpensiveLessPP(positionFilter(pitchers))
catchers = filterMoreExpensiveLessPP(positionFilter(catchers))
firstBase = filterMoreExpensiveLessPP(positionFilter(firstBase))
secondBase = filterMoreExpensiveLessPP(positionFilter(secondBase))
thirdBase = filterMoreExpensiveLessPP(positionFilter(thirdBase))
shortStop = filterMoreExpensiveLessPP(positionFilter(shortStop))
outfielders = ofFilterMoreExpensiveLessPP(ofPositionFilter(outfielders))


print('AFTER BOTH FILTERS...')
print('Pitchers: ' + str(len(pitchers)))
print('Catchers: ' + str(len(catchers)))
print('FirstBase: ' + str(len(firstBase)))
print('SecondBase: ' + str(len(secondBase)))
print('ThirdBase: ' + str(len(thirdBase)))
print('ShortStop: ' + str(len(shortStop)))
print('Outfielders: ' + str(len(outfielders)))


outfielderGroups = list(itertools.combinations(outfielders, 3))
print(len(outfielderGroups))

allLineups = list(itertools.product(pitchers, catchers, firstBase, secondBase, thirdBase, shortStop, outfielderGroups))
print(len(allLineups))

underCap = {}
count = 1
for lineup in allLineups:
    salary = 0
    for item in lineup:
        if type(item) == tuple:
            for of in item:
                salary += of[4]
        else:
            salary += playerDict[item][3]
    if salary <= 35000:
        underCap[count] = lineup
        count += 1

print(len(underCap))

underCapPP = {}
for key in underCap:
    projectedPoints = 0
    for item in underCap[key]:
        if type(item) == tuple:
            for of in item:
                projectedPoints += of[3]
        else:
            projectedPoints += playerDict[item][2]
    underCapPP[projectedPoints] = underCap[key]

pp = max(underCapPP)
optimalLineup = underCapPP[pp]
print(pp)
print(optimalLineup)

capUsed = 0
for item in optimalLineup:
    if type(item) == tuple:
        for of in item:
            capUsed += of[4]
            print(of[1] + ": " + of[2] + ' PP: ' + str(round(of[3], 2)) + ' Cost: ' + str(of[4]))
    else:
        capUsed += playerDict[item][3]
        print(playerDict[item][0] + ": " + playerDict[item][1] + ' PP: ' + str(round(playerDict[item][2], 2)) + ' Cost: ' + str(playerDict[item][3]))

print("Cap Used: $" + str(capUsed))
print("Projected Points: " + str(round(pp, 2)))

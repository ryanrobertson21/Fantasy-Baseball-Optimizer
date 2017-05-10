import csv, itertools

lineupSpreadsheet = open('/Users/RyanRobertson21/Desktop/simpleball.csv')
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
    playerDict[row[0]] = playerList

lineupSpreadsheet.close()

outfielders = {}
for ids in playerDict:
    if playerDict[ids][0] == 'OF':
        outfielders[ids] = playerDict[ids]

pitchers = {}
for ids in playerDict:
    if playerDict[ids][0] == 'P':
        pitchers[ids] = playerDict[ids]

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

outfielderGroups = list(itertools.combinations(outfielders, 3))

allLineups = list(itertools.product(outfielderGroups, pitchers, catchers, firstBase, secondBase, shortStop, thirdBase))

print(len(allLineups))
print(thirdBase)
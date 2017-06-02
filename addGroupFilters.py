import csv, itertools, copy, time, os, re, shutil
from collections import Counter
from selenium import webdriver
from poolReducer import poolReducer
import pandas as pd

teamNames = {
'LAA' : 'Angels',
'HOU' : 'Astros',
'OAK' : 'Athletics',
'TOR' : 'Blue Jays',
'ATL' : 'Braves',
'MIL' : 'Brewers',
'STL' : 'Cardinals',
'CHC' : 'Cubs',
'ARI' : 'Diamondbacks',
'LOS' : 'Dodgers',
'SFG' : 'Giants',
'CLE' : 'Indians',
'SEA' : 'Mariners',
'MIA' : 'Marlins',
'NYM' : 'Mets',
'WAS' : 'Nationals',
'BAL' : 'Orioles',
'SDP' : 'Padres',
'PHI' : 'Phillies',
'PIT' : 'Pirates',
'TEX' : 'Rangers',
'TAM' : 'Rays',
'BOS' : 'Red Sox',
'CIN' : 'Reds',
'COL' : 'Rockies',
'KAN' : 'Royals',
'DET' : 'Tigers',
'MIN' : 'Twins',
'CWS' : 'White Sox',
'NYY' : 'Yankees'
}

# urlBat = 'http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim&team=0&lg=all&players=0'
# urlPit = 'http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim&team=0&lg=all&players=0'
# urlFanDuel = 'https://www.fanduel.com/games/19553/contests/19553-209736007/enter'
# # urlFanDuel should be user input on website
#
# batFolderPath = '/Users/RyanRobertson21/Desktop/battersPP-'
# pitFolderPath = '/Users/RyanRobertson21/Desktop/pitchersPP-'
# fanDuelFolderPath = '/Users/RyanRobertson21/Desktop/fanDuel-'
#
# def downloadData(folderPath, url, linkTextString):
#     name = str(time.asctime(time.localtime(time.time()))).replace(':', '_')
#     folderPath = folderPath + name
#     os.makedirs(folderPath)
#
#     profile = webdriver.FirefoxProfile()
#     profile.set_preference('browser.download.folderList', 2)
#     profile.set_preference('browser.download.manager.showWhenStarting', False)
#     profile.set_preference('browser.download.dir', folderPath)
#     profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
#
#     browser = webdriver.Firefox(profile)
#     browser.get(url)
#     linkElem = browser.find_element_by_link_text(linkTextString)
#     linkElem.click()
#     time.sleep(5)
#     for file in os.listdir(folderPath):
#         filePath = folderPath + '/' + file
#     with open(filePath) as spreadSheetFile:
#         dataList = list(csv.reader(spreadSheetFile))[1:]
#     browser.quit()
#     # KEEP FOR NOW TO CHECK DATA shutil.rmtree(folderPath)
#     return dataList
# s1= time.time()
# print('Downloading batters data from FanGraphs...')
# battersPP = downloadData(batFolderPath, urlBat, 'Export Data')
# e1 = time.time()
# print(e1-s1)
# time.sleep(3)
# s2 = time.time()
# print('\nDownloading pitchers data from FanGraphs...')
# pitchersPP = downloadData(pitFolderPath, urlPit, 'Export Data')
# e2 = time.time()
# print(e2-s2)
# time.sleep(3)
# s3 = time.time()
# print('\nDownloading contest data from FanDuel...')
# contestLineup = downloadData(fanDuelFolderPath, urlFanDuel, 'Download players list')
# e3 = time.time()
# print(e3-s3)
start = time.time()
# to test when PP is not updated yet
contestLineup = list(csv.reader(open('/Users/RyanRobertson21/Desktop/fanDuel-Sat May 20 15_35_56 2017/FanDuel-MLB-2017-05-20-19376-players-list.csv')))[1:]
battersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/battersPP-Sat May 20 16_29_31 2017/FanGraphs Leaderboard.csv')))[1:]
pitchersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/pitchersPP-Sat May 20 16_29_48 2017/FanGraphs Leaderboard.csv')))[1:]

def editPlayerName(elementName, rowIndex):
    fullName = elementName[rowIndex].lower().replace(".", "").replace(" jr", "").split(' ', 1)
    firstName = fullName[0]
    if len(firstName) > 2:
        firstName = firstName[:3]
    lastName = fullName[1]
    name = firstName + " " + lastName
    removeInitial = re.compile(r' \w ').search(name)
    if removeInitial:
        name = name.replace(removeInitial.group(), ' ')
    return name

playerNamesToCheck = []
playerDict = {}



for row in contestLineup:
    for ppRow in battersPP:
        fdName = editPlayerName(row, 3)
        ppName = editPlayerName(ppRow, 0)

        if fdName == ppName and row[1] != 'P' and (teamNames[row[9]] == ppRow[1] or ppRow[1] == ''):
            playerList = []
            playerList.append(row[1])
            playerList.append(row[3])
            playerList.append(float(ppRow[-3]))
            playerList.append(int(row[7]))
            playerDict[row[0]] = playerList
            playerNamesToCheck.append(fdName)


for row in contestLineup:
    for ppRow in pitchersPP:
        fdName = editPlayerName(row, 3)
        ppName = editPlayerName(ppRow, 0)

        if fdName == ppName and row[1] == 'P' and (teamNames[row[9]] == ppRow[1] or ppRow[1] == ''):
            playerList = []
            playerList.append(row[1])
            playerList.append(row[3])
            playerList.append(float(ppRow[-3]))
            playerList.append(int(row[7]))
            playerDict[row[0]] = playerList
            playerNamesToCheck.append(fdName)

# Used to test to make sure players are being read in from Fangraphs pitchers and Fangraphs batters spreadsheets, as well
# as FanDuels total lineup spreadsheet. Works best when no games have started yet, otherwise players in games that have started
# are no longer eligibile to be selected for the contest in Fanduel. So while they will appear in the projected poitns spreadsheet
# they wont, and shouldn't appear on fanduel, and thus wont be read in.

print('\nBatters missing from PP\n')
for ppRow in battersPP:
    ppName = editPlayerName(ppRow, 0)

    if ppName not in playerNamesToCheck:
        print(ppName)

print('\nPitchers missing from PP\n')
for ppRow in pitchersPP:
    ppName = editPlayerName(ppRow, 0)

    if ppName not in playerNamesToCheck:
        print(ppName)

# print('\nPlayer missing from FanDuel\n')
# for row in contestLineup:
#     fdName = editPlayerName(row, 3)
#
#     if fdName not in playerNamesToCheck:
#         print(fdName, row[1])

print('\nPlayer Dict Info')
print(len(playerDict))




print('\nFilling in Position Dictionaries...')
pitchers = {}
catchers = {}
firstBase = {}
secondBase = {}
thirdBase = {}
shortStop = {}
outfielders = {}

for ids in playerDict:

    if playerDict[ids][0] == 'P':
        pitchers[ids] = playerDict[ids]

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

print('\nAFTER LOADING IN THE DATA...')
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
    outfielders = [item[0] for item in outfielderListSalaryOrder]
    return outfielders


print('\nAFTER FIRST FILTER!')
pitchers = positionFilter(pitchers)
catchers = positionFilter(catchers)
firstBase = positionFilter(firstBase)
secondBase = positionFilter(secondBase)
thirdBase = positionFilter(thirdBase)
shortStop = positionFilter(shortStop)
outfielders = ofPositionFilter(outfielders)

print('Pitchers: ' + str(len(pitchers)))
print('Catchers: ' + str(len(catchers)))
print('FirstBase: ' + str(len(firstBase)))
print('SecondBase: ' + str(len(secondBase)))
print('ThirdBase: ' + str(len(thirdBase)))
print('ShortStop: ' + str(len(shortStop)))
print('Outfielders: ' + str(len(outfielders)))


print('\nAFTER BOTH FILTERS...')
pitchers = filterMoreExpensiveLessPP(pitchers)
catchers = filterMoreExpensiveLessPP(catchers)
firstBase = filterMoreExpensiveLessPP(firstBase)
secondBase = filterMoreExpensiveLessPP(secondBase)
thirdBase = filterMoreExpensiveLessPP(thirdBase)
shortStop = filterMoreExpensiveLessPP(shortStop)
outfielders = ofFilterMoreExpensiveLessPP(outfielders)


print('Pitchers: ' + str(len(pitchers)))
print('Catchers: ' + str(len(catchers)))
print('FirstBase: ' + str(len(firstBase)))
print('SecondBase: ' + str(len(secondBase)))
print('ThirdBase: ' + str(len(thirdBase)))
print('ShortStop: ' + str(len(shortStop)))
print('Outfielders: ' + str(len(outfielders)))


pitchersCatchers = set(itertools.product(pitchers, catchers))
firstSecond = set(itertools.product(firstBase, secondBase))
thirdShort = set(itertools.product(thirdBase, shortStop))



def groupFilter(group):
    toDelete = set()
    print(len(group))
    for x, y in group:
        for x2, y2 in group:
            if playerDict[x][3] + playerDict[y][3] > playerDict[x2][3] + playerDict[y2][3] and playerDict[x][2] + playerDict[y][2] <= playerDict[x2][2] + playerDict[y2][2]:
                pair = (str(x), str(y))
                toDelete.add(pair)
    group = group.difference(toDelete)
    print(len(group))

    toDelete = set()
    for x, y in group:
        for x2, y2 in group:
            if playerDict[x][3] + playerDict[y][3] == playerDict[x2][3] + playerDict[y2][3] and playerDict[x][2] + playerDict[y][2] < playerDict[x2][2] + playerDict[y2][2]:
                pair = (str(x), str(y))
                toDelete.add(pair)
    group = group.difference(toDelete)
    print(len(group))
    return group

pitchersCatchers = groupFilter(pitchersCatchers)
firstSecond = groupFilter(firstSecond)
thirdShort = groupFilter(thirdShort)

c = set(itertools.product(firstSecond, thirdShort))



print(c)
print(len(c))

toDelete = set()
for x, y in c:
    for x2, y2 in c:
        if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] > playerDict[x2[0]][3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] \
            and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] <= playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2]:
            quad = ((str(x[0]), str(x[1])), (str(y[0]), str(y[1])))
            toDelete.add(quad)
c = c.difference(toDelete)
print(len(c))

toDelete = set()
for x, y in c:
    for x2, y2 in c:
        if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] == playerDict[x2[0]] \
            [3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] \
                and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] < \
                playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2]:
            quad = ((str(x[0]), str(x[1])), (str(y[0]), str(y[1])))
            #is str() necessary here?
            toDelete.add(quad)
firstSecondThirdShort = c.difference(toDelete)
print(len(firstSecondThirdShort))

print(firstSecondThirdShort)
firstSecondThirdShortss = set()
for group in firstSecondThirdShort:
    squad = []
    for pair in group:
        for player in pair:
            squad.append(player)
    squad = tuple(squad)
    firstSecondThirdShortss.add(squad)
print(len(firstSecondThirdShortss))
print(firstSecondThirdShortss)

infielders = set(itertools.product(pitchersCatchers, firstSecondThirdShortss))
print(len(infielders))


toDelete = set()
for x, y in infielders:
    for x2, y2 in infielders:
        if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] + playerDict[y[2]][3] + playerDict[y[3]][3] \
        > playerDict[x2[0]][3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] + playerDict[y2[2]][3] + playerDict[y2[3]][3] \
        and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] + playerDict[y[2]][2] + playerDict[y[3]][2] \
        <= playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2] + playerDict[y2[2]][2] + playerDict[y2[3]][2]:
            squad = (x, y)
            toDelete.add(squad)

print(len(toDelete))
infielders = infielders.difference(toDelete)
print(len(infielders))

toDelete = set()
for x, y in infielders:
    for x2, y2 in infielders:
        if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] + playerDict[y[2]][3] + playerDict[y[3]][3] \
        == playerDict[x2[0]][3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] + playerDict[y2[2]][3] + playerDict[y2[3]][3] \
        and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] + playerDict[y[2]][2] + playerDict[y[3]][2] \
        < playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2] + playerDict[y2[2]][2] + playerDict[y2[3]][2]:
            squad = (x, y)
            toDelete.add(squad)

print(len(toDelete))
infielders = infielders.difference(toDelete)
print(len(infielders))

print(infielders)

infielders2 = set()
for group in infielders:
    squad = []
    for pair in group:
        for player in pair:
            squad.append(player)
    squad = tuple(squad)
    infielders2.add(squad)
print(infielders2)



outfielderGroups = list(itertools.combinations(outfielders, 3))
print("\nNumber of oufielder combinations: {:,d}".format(len(outfielderGroups)))

allLineups = list(itertools.product(infielders2, outfielderGroups))
print("\nNumber of possibly optimal lineups: {:,d}".format(len(allLineups)))
#print(allLineups[2])
# toDelete = set()
# for infield, outfield in allLineups:
#     for infield2, outfield2 in allLineups:
#         if playerDict[infield[0]][3] + playerDict[infield[1]][3] + playerDict[infield[2]][3] + playerDict[infield[3]][3] + playerDict[infield[4]][3] + \
#         playerDict[infield[5]][3] + playerDict[outfield[0]][3] + playerDict[outfield[1]][3] + playerDict[outfield[2]][3] > playerDict[infield2[0]][3] + \
#         playerDict[infield2[1]][3] + playerDict[infield2[2]][3] + playerDict[infield2[3]][3] + playerDict[infield2[4]][3] + playerDict[infield2[5]][3] + \
#         playerDict[outfield2[0]][3] + playerDict[outfield2[1]][3] + playerDict[outfield2[2]][3] and playerDict[infield[0]][2] + playerDict[infield[1]][2] + \
#         playerDict[infield[2]][2] + playerDict[infield[3]][2] + playerDict[infield[4]][2] + playerDict[infield[5]][2] + playerDict[outfield[0]][2] + \
#         playerDict[outfield[1]][2] + playerDict[outfield[2]][2] <= playerDict[infield2[0]][2] + playerDict[infield2[1]][2] + playerDict[infield2[2]][2] +\
#         playerDict[infield2[3]][2] + playerDict[infield2[4]][2] + playerDict[infield2[5]][2] + playerDict[outfield2[0]][2] + playerDict[outfield2[1]][2] + \
#         playerDict[outfield2[2]][2]:
#             squad = (infield, outfield)
#             toDelete.add(squad)
# allLineups = allLineups.difference(toDelete)
# print(len(allLineups))

underCap = []
for infield, outfield in allLineups:
    salary = 0
    salary += playerDict[infield[0]][3] + playerDict[infield[1]][3] + playerDict[infield[2]][3] + playerDict[infield[3]][3] + playerDict[infield[4]][3] + \
              playerDict[infield[5]][3] + playerDict[outfield[0]][3] + playerDict[outfield[1]][3] + playerDict[outfield[2]][3]
    if salary <= 35000:
        team = (infield, outfield)
        underCap.append(team)


print("\nNumber of possibly optimal lineups under the cap: {:,d}\n".format(len(underCap)))


print(underCap[1])
underCapPP = {}
#count = 0
for infield, outfield in underCap:
    projectedPoints = 0
    projectedPoints += playerDict[infield[0]][2] + playerDict[infield[1]][2] + playerDict[infield[2]][2] + playerDict[infield[3]][2] + \
                       playerDict[infield[4]][2] + playerDict[infield[5]][2] + playerDict[outfield[0]][2] + playerDict[outfield[1]][2] + playerDict[outfield[2]][2]

    #if projectedPoints in underCapPP:
        #count += 1
    team = (infield, outfield)
    underCapPP[projectedPoints] = team

#print(len(underCapPP))
#print(count)


pp = max(underCapPP)
optimalLineup = underCapPP[pp]
### CHECK TO SEE HOW MANY TRULEY OPTIMAL LINEUPS EXIST
# count = 0
# for infield, outfield in underCap:
#     projectedPoints = 0
#     projectedPoints += playerDict[infield[0]][2] + playerDict[infield[1]][2] + playerDict[infield[2]][2] + playerDict[infield[3]][2] + \
#                        playerDict[infield[4]][2] + playerDict[infield[5]][2] + playerDict[outfield[0]][2] + playerDict[outfield[1]][2] + playerDict[outfield[2]][2]
#
#     if projectedPoints == pp:
#         count += 1
# print('number of optimal lineups that exist')
# print(count)


capUsed = 0
for group in optimalLineup:
    for player in group:
        capUsed += playerDict[player][3]

    if len(group) == 3:
        outfield = sorted(group, key=lambda x: (playerDict[x][3] * -1, x[2] * -1))
        for of in outfield:
            print(playerDict[of][0] + ": " + playerDict[of][1] + ' PP: ' + str(round(playerDict[of][2], 2)) + ' Cost: ${:,d}'.format(playerDict[of][3]))
    else:
        for player in group:
            print(playerDict[player][0] + ": " + playerDict[player][1] + ' PP: ' + str(round(playerDict[player][2], 2)) + ' Cost: ${:,d}'.format(playerDict[player][3]))

print("\nCap Used: ${:,d}".format(capUsed))
print("Projected Points: " + str(round(pp, 2)))

end = time.time()
print("\nRuntime from outfielderGroups calculation til end of program: " + str(end-start) + " seconds.")



### TEST BOTH WITH AND WITHOUT CHANGING OUTFIELDER GROUP FROM LIST TO SET OR WHATEVER I DID
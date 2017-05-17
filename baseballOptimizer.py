import csv, itertools, copy, time, os, re, shutil
from collections import Counter
from selenium import webdriver
from poolReducer import poolReducer

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

urlBat = 'http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim&team=0&lg=all&players=0'
urlPit = 'http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim&team=0&lg=all&players=0'
urlFanDuel = 'https://www.fanduel.com/games/19327/contests/19327-209469721/enter'
# urlFanDuel should be user input on website

batFolderPath = '/Users/RyanRobertson21/Desktop/battersPP-'
pitFolderPath = '/Users/RyanRobertson21/Desktop/pitchersPP-'
fanDuelFolderPath = '/Users/RyanRobertson21/Desktop/fanDuel-'

def downloadData(folderPath, url, linkTextString):
    name = str(time.asctime(time.localtime(time.time()))).replace(':', '_')
    folderPath = folderPath + name
    os.makedirs(folderPath)

    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', folderPath)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    browser = webdriver.Firefox(profile)
    browser.get(url)
    linkElem = browser.find_element_by_link_text(linkTextString)
    linkElem.click()
    time.sleep(5)
    for file in os.listdir(folderPath):
        filePath = folderPath + '/' + file
    with open(filePath) as spreadSheetFile:
        dataList = list(csv.reader(spreadSheetFile))[1:]
    browser.quit()
    shutil.rmtree(folderPath)
    return dataList

battersPP = downloadData(batFolderPath, urlBat, 'Export Data')
time.sleep(3)
pitchersPP = downloadData(pitFolderPath, urlPit, 'Export Data')
time.sleep(3)
contestLineup = downloadData(fanDuelFolderPath, urlFanDuel, 'Download players list')

# to test when PP is not updated yet
# contestLineup = list(csv.reader(open('/Users/RyanRobertson21/Desktop/FD_5-16.csv')))[1:]
# battersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/battersPP-Tue May 16 18_17_23 2017/FanGraphs Leaderboard.csv')))[1:]
# pitchersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/pitchersPP-Tue May 16 18_17_56 2017/FanGraphs Leaderboard.csv')))[1:]

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
# print('\nBatters missing from PP\n')
# for ppRow in battersPP:
#     ppName = editPlayerName(ppRow, 0)
#
#     if ppName not in playerNamesToCheck:
#         print(ppName)
#
# print('\nPitchers missing from PP\n')
# for ppRow in pitchersPP:
#     ppName = editPlayerName(ppRow, 0)
#
#     if ppName not in playerNamesToCheck:
#         print(ppName)
# print('\nPlayer missing from FanDuel\n')
# for row in contestLineup:
#     fdName = editPlayerName(row, 3)
#
#     if fdName not in playerNamesToCheck:
#         print(fdName, row[1])

print('Player Dict Info')
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

    return outfielderListSalaryOrder


print('\nAFTER FIRST FILTER!')
print('Pitchers: ' + str(len(positionFilter(pitchers))))
print('Catchers: ' + str(len(positionFilter(catchers))))
print('FirstBase: ' + str(len(positionFilter(firstBase))))
print('SecondBase: ' + str(len(positionFilter(secondBase))))
print('ThirdBase: ' + str(len(positionFilter(thirdBase))))
print('ShortStop: ' + str(len(positionFilter(shortStop))))
print('Outfielders: ' + str(len(ofPositionFilter(outfielders))))

pitchers = filterMoreExpensiveLessPP(positionFilter(pitchers))
catchers = filterMoreExpensiveLessPP(positionFilter(catchers))
firstBase = filterMoreExpensiveLessPP(positionFilter(firstBase))
secondBase = filterMoreExpensiveLessPP(positionFilter(secondBase))
thirdBase = filterMoreExpensiveLessPP(positionFilter(thirdBase))
shortStop = filterMoreExpensiveLessPP(positionFilter(shortStop))
outfielders = ofFilterMoreExpensiveLessPP(ofPositionFilter(outfielders))


print('\nAFTER BOTH FILTERS...')
print('Pitchers: ' + str(len(pitchers)))
print('Catchers: ' + str(len(catchers)))
print('FirstBase: ' + str(len(firstBase)))
print('SecondBase: ' + str(len(secondBase)))
print('ThirdBase: ' + str(len(thirdBase)))
print('ShortStop: ' + str(len(shortStop)))
print('Outfielders: ' + str(len(outfielders)))

start = time.time()
outfielderGroups = list(itertools.combinations(outfielders, 3))
print("\nNumber of oufielder combinations: " + str(len(outfielderGroups)))

allLineups = list(itertools.product(pitchers, catchers, firstBase, secondBase, thirdBase, shortStop, outfielderGroups))
print("\nNumber of possibly optimal lineups: " + str(len(allLineups)))
print(allLineups[2])
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

print("\nNumber of possibly optimal lineups under the cap: " + str(len(underCap))+"\n")

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


capUsed = 0
for item in optimalLineup:
    if type(item) == tuple:
        for of in item:
            capUsed += of[4]
            print(of[1] + ": " + of[2] + ' PP: ' + str(round(of[3], 2)) + ' Cost: ' + str(of[4]))
    else:
        capUsed += playerDict[item][3]
        print(playerDict[item][0] + ": " + playerDict[item][1] + ' PP: ' + str(round(playerDict[item][2], 2)) + ' Cost: ' + str(playerDict[item][3]))

print("\nCap Used: $" + str(capUsed))
print("Projected Points: " + str(round(pp, 2)))

end = time.time()
print("\nRuntime from outfielderGroups calculation til end of program: " + str(end-start) + " seconds.")
import csv, itertools, copy, time, os, re, math, shutil, sys
from collections import Counter
from selenium import webdriver
import pandas as pd
start = time.time()

# teamNames = {
# 'LAA' : 'Angels',
# 'HOU' : 'Astros',
# 'OAK' : 'Athletics',
# 'TOR' : 'Blue Jays',
# 'ATL' : 'Braves',
# 'MIL' : 'Brewers',
# 'STL' : 'Cardinals',
# 'CHC' : 'Cubs',
# 'ARI' : 'Diamondbacks',
# 'LOS' : 'Dodgers',
# 'SFG' : 'Giants',
# 'CLE' : 'Indians',
# 'SEA' : 'Mariners',
# 'MIA' : 'Marlins',
# 'NYM' : 'Mets',
# 'WAS' : 'Nationals',
# 'BAL' : 'Orioles',
# 'SDP' : 'Padres',
# 'PHI' : 'Phillies',
# 'PIT' : 'Pirates',
# 'TEX' : 'Rangers',
# 'TAM' : 'Rays',
# 'BOS' : 'Red Sox',
# 'CIN' : 'Reds',
# 'COL' : 'Rockies',
# 'KAN' : 'Royals',
# 'DET' : 'Tigers',
# 'MIN' : 'Twins',
# 'CWS' : 'White Sox',
# 'NYY' : 'Yankees'
# }

teamNames2 = {
'LAA' : 'ana',
'HOU' : 'hou',
'OAK' : 'oak',
'TOR' : 'tor',
'ATL' : 'atl',
'MIL' : 'mil',
'STL' : 'sln',
'CHC' : 'chn',
'ARI' : 'ari',
'LOS' : 'lan',
'SFG' : 'sfn',
'CLE' : 'cle',
'SEA' : 'sea',
'MIA' : 'mia',
'NYM' : 'nyn',
'WAS' : 'was',
'BAL' : 'bal',
'SDP' : 'sdn',
'PHI' : 'phi',
'PIT' : 'pit',
'TEX' : 'tex',
'TAM' : 'tba',
'BOS' : 'bos',
'CIN' : 'cin',
'COL' : 'col',
'KAN' : 'kca',
'DET' : 'det',
'MIN' : 'min',
'CWS' : 'cha',
'NYY' : 'nya'
}

# def downloadData(folderPath, url, linkTextString):
#     name = str(time.asctime(time.localtime(time.time()))).replace(':', '_')
#     folderPath += name
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
#
#     for file in os.listdir(folderPath):
#         filePath = folderPath + '/' + file
#         with open(filePath) as spreadSheetFile:
#             dataList = list(csv.reader(spreadSheetFile))[1:]
#             #shutil.rmtree(folderPath)
#             browser.quit()
#             return dataList

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

def combinationsCalculator(n):
    groupings = 3
    combos = int(math.factorial(n)/(math.factorial(groupings)*math.factorial(n-groupings)))
    return combos





# urlBat = 'http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim&team=0&lg=all&players=0'
# urlPit = 'http://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim&team=0&lg=all&players=0'
# urlFanDuel = 'https://www.fanduel.com/games/19571/contests/19571-209763228/enter'
# # urlFanDuel should be user input on website
#
# batFolderPath = '/Users/RyanRobertson21/Desktop/battersPP-'
# pitFolderPath = '/Users/RyanRobertson21/Desktop/pitchersPP-'
# fanDuelFolderPath = '/Users/RyanRobertson21/Desktop/fanDuel-'
#
#
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

# to test when PP is not updated yet
contestLineup = list(csv.reader(open('/Users/RyanRobertson21/Desktop/FanDuel-MLB-2017-06-06-19609-players-list.csv')))[1:]
#battersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/battersPP-Fri Jun  2 13_32_18 2017/FanGraphs Leaderboard.csv')))[1:]
#pitchersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/pitchersPP-Fri Jun  2 13_33_08 2017/FanGraphs Leaderboard.csv')))[1:]
saberSim = list(csv.reader(open('/Users/RyanRobertson21/Desktop/sabersim_players_2017-06-06 23_05_00_15_mlb.csv')))[1:]



playerNamesToCheck = []
playerDict = {}

"""Saber Sim Test"""
for row in contestLineup:
    for ppRow in saberSim:
        fdName = editPlayerName(row, 3)
        ssName = editPlayerName(ppRow, 0)
        if fdName == ssName and (teamNames2[row[9]] == ppRow[1] or ppRow[1] == ''):
            playerList = [row[1], row[3], float(ppRow[15]), int(row[7]), row[9]]
            playerDict[row[0]] = playerList
            playerNamesToCheck.append(fdName)

# for row in contestLineup:
#     for ppRow in battersPP:
#         fdName = editPlayerName(row, 3)
#         ppName = editPlayerName(ppRow, 0)
#
#         if fdName == ppName and row[1] != 'P' and (teamNames[row[9]] == ppRow[1] or ppRow[1] == ''):
#             playerList = [row[1], row[3], float(ppRow[-3]), int(row[7]), row[9]]
#             playerDict[row[0]] = playerList
#             playerNamesToCheck.append(fdName)
#
# for row in contestLineup:
#     for ppRow in pitchersPP:
#         fdName = editPlayerName(row, 3)
#         ppName = editPlayerName(ppRow, 0)
#
#         if fdName == ppName and row[1] == 'P' and (teamNames[row[9]] == ppRow[1] or ppRow[1] == ''):
#             playerList = [row[1], row[3], float(ppRow[-3]), int(row[7]), row[9]]
#             playerDict[row[0]] = playerList
#             playerNamesToCheck.append(fdName)

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

print('\nPlayers missing from saber sim\n')
for ppRow in saberSim:
    ssName = editPlayerName(ppRow, 0)

    if ssName not in playerNamesToCheck:
        print(ssName)

# print('\nPlayer missing from FanDuel\n')
# for row in contestLineup:
#     fdName = editPlayerName(row, 3)
#
#     if fdName not in playerNamesToCheck:
#         print(fdName, row[1])


print('\nPlayer Dictionary Length: ' + str(len(playerDict)))

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

numLineups = len(pitchers) * len(catchers) * len(firstBase) * len(secondBase) * len(thirdBase) * len(shortStop) * combinationsCalculator(len(outfielders))
print("\nNumber of Possibly Optimal Lineups: {:,d}".format(numLineups))
#
#
#
# print('\nAFTER FIRST FILTER!')
# pitchers = positionFilter(pitchers)
# catchers = positionFilter(catchers)
# firstBase = positionFilter(firstBase)
# secondBase = positionFilter(secondBase)
# thirdBase = positionFilter(thirdBase)
# shortStop = positionFilter(shortStop)
# outfielders = ofPositionFilter(outfielders)
#
# print('Pitchers: ' + str(len(pitchers)))
# print('Catchers: ' + str(len(catchers)))
# print('FirstBase: ' + str(len(firstBase)))
# print('SecondBase: ' + str(len(secondBase)))
# print('ThirdBase: ' + str(len(thirdBase)))
# print('ShortStop: ' + str(len(shortStop)))
# print('Outfielders: ' + str(len(outfielders)))
#
# numLineups = len(pitchers) * len(catchers) * len(firstBase) * len(secondBase) * len(thirdBase) * len(shortStop) * combinationsCalculator(len(outfielders))
# print("\nNumber of Possibly Optimal Lineups: {:,d}".format(numLineups))
#
# print('\nAFTER BOTH FILTERS...')
# pitchers = filterMoreExpensiveLessPP(pitchers)
# catchers = filterMoreExpensiveLessPP(catchers)
# firstBase = filterMoreExpensiveLessPP(firstBase)
# secondBase = filterMoreExpensiveLessPP(secondBase)
# thirdBase = filterMoreExpensiveLessPP(thirdBase)
# shortStop = filterMoreExpensiveLessPP(shortStop)
# outfielders = ofFilterMoreExpensiveLessPP(outfielders)
#
#
# print('Pitchers: ' + str(len(pitchers)))
# print('Catchers: ' + str(len(catchers)))
# print('FirstBase: ' + str(len(firstBase)))
# print('SecondBase: ' + str(len(secondBase)))
# print('ThirdBase: ' + str(len(thirdBase)))
# print('ShortStop: ' + str(len(shortStop)))
# print('Outfielders: ' + str(len(outfielders)))
#
# numLineups = len(pitchers) * len(catchers) * len(firstBase) * len(secondBase) * len(thirdBase) * len(shortStop) * combinationsCalculator(len(outfielders))
# print("\nNumber of Possibly Optimal Lineups: {:,d}".format(numLineups))
#
# pitchersCatchers = set(itertools.product(pitchers, catchers))
# firstSecond = set(itertools.product(firstBase, secondBase))
# thirdShort = set(itertools.product(thirdBase, shortStop))
# outfielderGroups = set(itertools.combinations(outfielders, 3))
#
# print("\nNumber of oufielder combinations: {:,d}".format(len(outfielderGroups)))
# outfielderGroups = oufielderGroupFilter(outfielderGroups)
# print("\nNumber of oufielder combinations: {:,d}".format(len(outfielderGroups)))
#
#
#
# allLineups = list(itertools.product(pitchersCatchers, firstSecond, thirdShort, outfielderGroups))
#
# print(len(allLineups))
# print(allLineups[0])

# underCap = []
# for pc, fs, ts, of in allLineups:
#      salary = 0
#      salary += playerDict[pc[0]][3] + playerDict[pc[1]][3] + playerDict[fs[0]][3] + playerDict[fs[1]][3] + playerDict[ts[0]][3] + playerDict[ts[1]][3] + \
#          playerDict[of[0]][3] + playerDict[of[1]][3] + playerDict[of[2]][3]
#      if salary <= 35000:
#          team = (pc, fs, ts, of)
#          underCap.append(team)
#
#
# print("\nNumber of possibly optimal lineups under the cap: {:,d}\n".format(len(underCap)))
#
# underCapPP = {}
# for pc, fs, ts, of in underCap:
#     projectedPoints = 0
#     projectedPoints += playerDict[pc[0]][2] + playerDict[pc[1]][2] + playerDict[fs[0]][2] + playerDict[fs[1]][2] + playerDict[ts[0]][2] + \
#                        playerDict[ts[1]][2] + playerDict[of[0]][2] + playerDict[of[1]][2] + playerDict[of[2]][2]
#
#     team = (pc, fs, ts, of)
#     underCapPP[projectedPoints] = team
#
#
# sys.setrecursionlimit(len(underCapPP))


######################

def findMaxPP(pitchers, catchers, firstBase, secondBase, thirdBase, shortStop, outfielders, teams=set(), lineupsViolateConstraint=set(), maxPlayer = 4):

    def positionFilter(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        for player in positionDict:
            for player2 in positionDict:
                if positionDict[player][3] == positionDict[player2][3] and positionDict[player][2] < \
                        positionDict[player2][2] and positionDict[player2][-1] not in teams:
                    if player in positionDictCopy:
                        del positionDictCopy[player]
        return positionDictCopy

    def filterMoreExpensiveLessPP(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        for player in positionDict:
            for player2 in positionDict:
                if positionDict[player][3] > positionDict[player2][3] and positionDict[player][2] <= \
                        positionDict[player2][2] and positionDict[player2][-1] not in teams:
                    if player in positionDictCopy:
                        del positionDictCopy[player]
        return positionDictCopy

    def ofPositionFilter(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        outfielderSalaries = []
        for of in positionDict:
            outfielderSalaries.append(positionDict[of][3])

        ofSalaryCounts = Counter(outfielderSalaries)

        outfielderSalariesToFilter = {k: v for k, v in ofSalaryCounts.items() if v > 3}

        onTeams = 0
        for salary in outfielderSalariesToFilter:
            playersWithSameSalary = []
            for of in positionDict:
                if positionDict[of][3] == salary:
                    playersWithSameSalary.append(positionDict[of][2])
                    if positionDict[of][-1] in teams:
                        onTeams += 1

            for num in range(outfielderSalariesToFilter[
                                 salary] - 3 - onTeams):  # so won't eliminate someone on team if it should??
                lowestPP = min(playersWithSameSalary)
                for of in positionDict:
                    if positionDict[of][2] == lowestPP and positionDict[of][3] == salary:
                        del positionDictCopy[of]
                        playersWithSameSalary.remove(lowestPP)

        return positionDictCopy

    def ofFilterMoreExpensiveLessPP(positionDict):
        outfielderList = []
        for key in positionDict:
            playerEntry = [key]
            for info in positionDict[key]:  # can do this better?
                playerEntry.append(info)
            outfielderList.append(playerEntry)

        outfielderListSalaryOrder = sorted(outfielderList, key=lambda x: (x[4], x[3] * -1))
        count = 0
        i = 0
        lowestSalaryOutfielders = []
        while count < 3:
            if outfielderListSalaryOrder[i][-1] not in teams:
                lowestSalaryOutfielders.append(outfielderListSalaryOrder[i])
                i += 1
                count += 1
            else:
                i += 1

        count2 = 1
        while count2 + 1 < len(outfielderListSalaryOrder):

            minPPOFer = min(lowestSalaryOutfielders, key=lambda x: x[3])

            outfieldersToDelete = []
            for of in outfielderListSalaryOrder[2 + count2:]:
                if of[3] < minPPOFer[3] and of[4] >= minPPOFer[4]:
                    outfieldersToDelete.append(of)

            outfielderListSalaryOrder = [x for x in outfielderListSalaryOrder if x not in outfieldersToDelete]

            try:
                if outfielderListSalaryOrder[2 + count2][-1] not in teams:
                    lowestSalaryOutfielders.remove(minPPOFer)
                    lowestSalaryOutfielders.append(outfielderListSalaryOrder[2 + count2])
                else:
                    pass
            except IndexError:
                break

            count2 += 1
        outfielders = [item[0] for item in outfielderListSalaryOrder]
        return outfielders

    def groupFilter(group):
        toDelete = set()
        for x, y in group:
            for x2, y2 in group:
                if playerDict[x][3] + playerDict[y][3] > playerDict[x2][3] + playerDict[y2][3] and playerDict[x][2] + \
                        playerDict[y][2] <= playerDict[x2][2] + \
                        playerDict[y2][2] and playerDict[x2][-1] not in teams and playerDict[y2][-1] not in teams:
                    pair = (x, y)
                    toDelete.add(pair)

        group = group.difference(toDelete)

        toDelete = set()
        for a, b in group:
            for a2, b2 in group:
                if playerDict[a][3] + playerDict[b][3] == playerDict[a2][3] + playerDict[b2][3] and playerDict[a][2] + \
                        playerDict[b][2] < playerDict[a2][2] + \
                        playerDict[b2][2] and playerDict[a2][-1] not in teams and playerDict[b2][-1] not in teams:
                    pair = (a, b)
                    toDelete.add(pair)

        group = group.difference(toDelete)
        return group

    def oufielderGroupFilter(group):
        toDelete = set()
        for x, y, z in group:
            for x2, y2, z2 in group:
                if playerDict[x][3] + playerDict[y][3] + playerDict[z][3] > playerDict[x2][3] + playerDict[y2][3] + playerDict[z2][3] and \
                    playerDict[x][2] + playerDict[y][2] + playerDict[z][2] <= playerDict[x2][2] + playerDict[y2][2] + playerDict[z2][2] and \
                    playerDict[x2][-1] not in teams and playerDict[y2][-1] not in teams and playerDict[z2][-1] not in teams:

                    team = (x, y, z)
                    toDelete.add(team)
        group = group.difference(toDelete)

        toDelete = set()
        for x, y, z in group:
            for x2, y2, z2 in group:
                if playerDict[x][3] + playerDict[y][3] + playerDict[z][3] == playerDict[x2][3] + playerDict[y2][3] + playerDict[z2][3] and \
                    playerDict[x][2] + playerDict[y][2] + playerDict[z][2] < playerDict[x2][2] + playerDict[y2][2] + playerDict[z2][2] and \
                    playerDict[x2][-1] not in teams and playerDict[y2][-1] not in teams and playerDict[z2][-1] not in teams:

                    team = (x, y, z)
                    toDelete.add(team)
        outfielderGroups = group.difference(toDelete)
        return outfielderGroups
    s1 = time.time()
    pitchers2 = positionFilter(pitchers)
    catchers2 = positionFilter(catchers)
    firstBase2 = positionFilter(firstBase)
    secondBase2 = positionFilter(secondBase)
    thirdBase2 = positionFilter(thirdBase)
    shortStop2 = positionFilter(shortStop)
    outfielders2 = ofPositionFilter(outfielders)
    pitchers2 = filterMoreExpensiveLessPP(pitchers2)
    catchers2 = filterMoreExpensiveLessPP(catchers2)
    firstBase2 = filterMoreExpensiveLessPP(firstBase2)
    secondBase2 = filterMoreExpensiveLessPP(secondBase2)
    thirdBase2 = filterMoreExpensiveLessPP(thirdBase2)
    shortStop2 = filterMoreExpensiveLessPP(shortStop2)
    outfielders2 = ofFilterMoreExpensiveLessPP(outfielders2)
    pitchersCatchers = set(itertools.product(pitchers2, catchers2))
    firstSecond = set(itertools.product(firstBase2, secondBase2))
    thirdShort = set(itertools.product(thirdBase2, shortStop2))
    outfielderGroups = set(itertools.combinations(outfielders2, 3))
    outfielderGroups = oufielderGroupFilter(outfielderGroups)
    allLineups = list(itertools.product(pitchersCatchers, firstSecond, thirdShort, outfielderGroups))
    print('num lineups BEFORE underCap')
    print(len(allLineups))
    underCap = set()
    e1 = time.time()
    print('TIME FOR ALL INITIAL FUNCTIONS')
    print(e1-s1)
    s2 = time.time()
    for pc, fs, ts, of in allLineups:
        salary = 0
        salary += playerDict[pc[0]][3] + playerDict[pc[1]][3] + playerDict[fs[0]][3] + playerDict[fs[1]][3] + \
                  playerDict[ts[0]][3] + playerDict[ts[1]][3] + \
                  playerDict[of[0]][3] + playerDict[of[1]][3] + playerDict[of[2]][3]

        squad = (pc, fs, ts, of)
        if salary <= 35000:
            underCap.add(squad)
    underCap = underCap.difference(lineupsViolateConstraint)
    print('num limeups after underCap')
    print(len(underCap))
    e2 = time.time()
    print('underCap Time')
    print(e2-s2)
    s3 = time.time()
    underCapPP = {}
    #figureo ut why pycharm added the below and learn it and shoould i use it
    if __name__ == '__main__':
        for pc, fs, ts, of in underCap:
            projectedPoints = 0
            projectedPoints += playerDict[pc[0]][2] + playerDict[pc[1]][2] + playerDict[fs[0]][2] + playerDict[fs[1]][2] + \
                               playerDict[ts[0]][2] + \
                               playerDict[ts[1]][2] + playerDict[of[0]][2] + playerDict[of[1]][2] + playerDict[of[2]][2]

            team = (pc, fs, ts, of)
            underCapPP[projectedPoints] = team
    print('underCapPP Time')
    e3 = time.time()
    print(e3-s3)
    #sys.setrecursionlimit(len(underCapPP))
    print(lineupsViolateConstraint)
    print(teams)
    print(lineupsViolateConstraint)
    print('len lineups violate constraint')
    print(len(lineupsViolateConstraint))
    pp = max(underCapPP)
    count = 0
    while True:
        if count > 0:
            lineupToDelete = underCapPP[pp]
            lineupsViolateConstraint.add(lineupToDelete)
            del underCapPP[pp]
            pp = max(underCapPP)
        teamsCounter = []
        optimalLineup = underCapPP[pp]
        for group in optimalLineup:
            for player in group:
                teamsCounter.append(playerDict[player][-1])
        teamsCounter = Counter(teamsCounter)
        print(teamsCounter)
        print(pp)
        print(optimalLineup)
        maxTeamFreq = max(teamsCounter.values())
        teamPlayersCantElim = []
        # make into list comprehension
        for teamName in teamsCounter:
            if teamsCounter[teamName] == maxTeamFreq:
                if teamName not in teamPlayersCantElim: teamPlayersCantElim.append(teamName)
        if maxTeamFreq > maxPlayer and all(x in teams for x in teamPlayersCantElim):
            count += 1
            continue
        elif max(teamsCounter.values()) > maxPlayer:
            print('called outer one')
            print(teams, teamPlayersCantElim)
            [teams.add(x) for x in teamPlayersCantElim]
            lineupToDelete = underCapPP[pp]
            lineupsViolateConstraint.add(lineupToDelete)
            return findMaxPP(pitchers, catchers, firstBase, secondBase, thirdBase, shortStop, outfielders, teams, lineupsViolateConstraint)
        else:
            return underCapPP[pp], pp

optimalLineup, pp = findMaxPP(pitchers,catchers,firstBase,secondBase,thirdBase,shortStop,outfielders)
print(optimalLineup)

capUsed = 0
for group in optimalLineup:
    for player in group:
        capUsed += playerDict[player][3]

    if len(group) == 3:
        outfield = sorted(group, key=lambda x: (playerDict[x][3] * -1, x[2] * -1))
        for of in outfield:
            print(playerDict[of][0] + ": " + playerDict[of][1] + ' PP: ' + str(round(playerDict[of][2], 2)) + ' Cost: ${:,d}'.format(playerDict[of][3]) + \
                " Team: " + str(playerDict[of][-1]))
    else:
        for player in group:
            print(playerDict[player][0] + ": " + playerDict[player][1] + ' PP: ' + str(round(playerDict[player][2], 2)) + ' Cost: ${:,d}'.format(playerDict[player][3]) + \
            " Team: " + str(playerDict[player][-1]))

print("\nCap Used: ${:,d}".format(capUsed))
print("Projected Points: " + str(round(pp, 2)))

end = time.time()
print("\nRuntime of program: " + str(end-start) + " seconds.")


# """CHECK TO SEE HOW MANY TRULEY OPTIMAL LINEUPS EXIST"""
# # count = 0
# # for infield, outfield in underCap:
# #     projectedPoints = 0
# #     projectedPoints += playerDict[infield[0]][2] + playerDict[infield[1]][2] + playerDict[infield[2]][2] + playerDict[infield[3]][2] + \
# #                        playerDict[infield[4]][2] + playerDict[infield[5]][2] + playerDict[outfield[0]][2] + playerDict[outfield[1]][2] + playerDict[outfield[2]][2]
# #
# #     if projectedPoints == pp:
# #         count += 1
# # print('number of optimal lineups that exist')
# # print(count)
#

### TEST BOTH WITH AND WITHOUT CHANGING OUTFIELDER GROUP FROM LIST TO SET OR WHATEVER I DID








# firstSecondThirdShort = set(itertools.product(firstSecond, thirdShort))
#
#
# toDelete = set()
# for x, y in firstSecondThirdShort:
#     for x2, y2 in firstSecondThirdShort:
#         if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] > playerDict[x2[0]][3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] \
#             and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] <= playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2]:
#             quad = ((str(x[0]), str(x[1])), (str(y[0]), str(y[1])))
#             toDelete.add(quad)
# firstSecondThirdShort = firstSecondThirdShort.difference(toDelete)
#
#
# toDelete = set()
# for x, y in firstSecondThirdShort:
#     for x2, y2 in firstSecondThirdShort:
#         if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] == playerDict[x2[0]] \
#             [3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] \
#                 and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] < \
#                 playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2]:
#             quad = ((x[0], x[1]), (y[0], y[1]))
#             toDelete.add(quad)
# firstSecondThirdShort = firstSecondThirdShort.difference(toDelete)
#
# firstSecondThirdShortNew = set()
# for group in firstSecondThirdShort:
#     squad = []
#     for pair in group:
#         for player in pair:
#             squad.append(player)
#     squad = tuple(squad)
#     firstSecondThirdShortNew.add(squad)
#
#
# infielders = set(itertools.product(pitchersCatchers, firstSecondThirdShortNew))

#
###### maybe run the below if size of all lineups is above a certain threshold?
#
# toDelete = set()
# for x, y in infielders:
#     for x2, y2 in infielders:
#         if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] + playerDict[y[2]][3] + playerDict[y[3]][3] \
#         > playerDict[x2[0]][3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] + playerDict[y2[2]][3] + playerDict[y2[3]][3] \
#         and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] + playerDict[y[2]][2] + playerDict[y[3]][2] \
#         <= playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2] + playerDict[y2[2]][2] + playerDict[y2[3]][2]:
#             squad = (x, y)
#             toDelete.add(squad)
#
# infielders = infielders.difference(toDelete)
#
# toDelete = set()
# for x, y in infielders:
#     for x2, y2 in infielders:
#         if playerDict[x[0]][3] + playerDict[x[1]][3] + playerDict[y[0]][3] + playerDict[y[1]][3] + playerDict[y[2]][3] + playerDict[y[3]][3] \
#         == playerDict[x2[0]][3] + playerDict[x2[1]][3] + playerDict[y2[0]][3] + playerDict[y2[1]][3] + playerDict[y2[2]][3] + playerDict[y2[3]][3] \
#         and playerDict[x[0]][2] + playerDict[x[1]][2] + playerDict[y[0]][2] + playerDict[y[1]][2] + playerDict[y[2]][2] + playerDict[y[3]][2] \
#         < playerDict[x2[0]][2] + playerDict[x2[1]][2] + playerDict[y2[0]][2] + playerDict[y2[1]][2] + playerDict[y2[2]][2] + playerDict[y2[3]][2]:
#             squad = (x, y)
#             toDelete.add(squad)
#
# infielders = infielders.difference(toDelete)
#
#
# infieldersNew = set()
# for group in infielders:
#     squad = []
#     for pair in group:
#         for player in pair:
#             squad.append(player)
#     squad = tuple(squad)
#     infieldersNew.add(squad)
#
#
# allLineups = list(itertools.product(infieldersNew, outfielderGroups))
# print("\nNumber of possibly optimal lineups: {:,d}".format(len(allLineups)))
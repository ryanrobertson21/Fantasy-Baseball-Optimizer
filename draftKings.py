import csv, itertools, copy, time, re, math, shutil
from collections import Counter

"""
Constraints:
1) 2 Pitchers, 1 Catcher, 1 FirstBaseman, 1 Secondbaseman, 1 Thirdbaseman, 1 Shortstop, 3 Outfielders
2) Total lineup salary cannot exceed $50,000
3) Can not have more than 5 batters from the same MLB team in lineup
4) Must have players from at least 3 different teams in lineup
5) A player can not be in lineup more than once (DraftKings lists some players at multiple positions)
"""

s1=time.time()

teamDict = {
'LAA' : 'Angels',
'HOU' : 'Astros',
'OAK' : 'Athletics',
'TOR' : 'Blue Jays',
'ATL' : 'Braves',
'MIL' : 'Brewers',
'STL' : 'Cardinals',
'CHC' : 'Cubs',
'ARI' : 'Diamondbacks',
'LAD' : 'Dodgers',
'SF'  : 'Giants',
'CLE' : 'Indians',
'SEA' : 'Mariners',
'MIA' : 'Marlins',
'NYM' : 'Mets',
'WAS' : 'Nationals',
'BAL' : 'Orioles',
'SD'  : 'Padres',
'PHI' : 'Phillies',
'PIT' : 'Pirates',
'TEX' : 'Rangers',
'TB'  : 'Rays',
'BOS' : 'Red Sox',
'CIN' : 'Reds',
'COL' : 'Rockies',
'KC'  : 'Royals',
'DET' : 'Tigers',
'MIN' : 'Twins',
'CWS' : 'White Sox',
'NYY' : 'Yankees'
}

# # Sabersim team names
# teamDict2 = {
# 'LAA' : 'ana',
# 'HOU' : 'hou',
# 'OAK' : 'oak',
# 'TOR' : 'tor',
# 'ATL' : 'atl',
# 'MIL' : 'mil',
# 'STL' : 'sln',
# 'CHC' : 'chn',
# 'ARI' : 'ari',
# 'LAD' : 'lan',
# 'SF'  : 'sfn',
# 'CLE' : 'cle',
# 'SEA' : 'sea',
# 'MIA' : 'mia',
# 'NYM' : 'nyn',
# 'WAS' : 'was',
# 'BAL' : 'bal',
# 'SD'  : 'sdn',
# 'PHI' : 'phi',
# 'PIT' : 'pit',
# 'TEX' : 'tex',
# 'TB'  : 'tba',
# 'BOS' : 'bos',
# 'CIN' : 'cin',
# 'COL' : 'col',
# 'KC'  : 'kca',
# 'DET' : 'det',
# 'MIN' : 'min',
# 'CWS' : 'cha',
# 'NYY' : 'nya'
# }

# Calculates how many different ways you can choose g items from n item set (used to figure out how many combinations of outfielders and pitchers are possible)
def combinationsCalculator(n, g):
    combos = int(math.factorial(n)/(math.factorial(g)*math.factorial(n-g)))
    return combos

# Removes inconsistencies between players names in draftkings and fangraphs
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

contestLineup = list(csv.reader(open('/Users/RyanRobertson21/Downloads/DKSalaries-3.csv')))[1:]
battersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/bbat.csv')))[1:]
pitchersPP = list(csv.reader(open('/Users/RyanRobertson21/Desktop/ppit.csv')))[1:]
saberSim = list(csv.reader(open('/Users/RyanRobertson21/Downloads/sabersim_players_2017-06-24 23_15_00_7_mlb.csv')))[1:]

playerNamesToCheck = []
playerDict = {}


for row in contestLineup:
    for ppRow in battersPP:
        contestName = editPlayerName(row, 1)
        ppName = editPlayerName(ppRow, 0)

        if contestName == ppName and 'P' not in row[0] and (teamDict[row[-1]] == ppRow[1] or ppRow[1] == ''):
            playerList = [row[0], row[1], float(ppRow[-2]), int(row[2]), row[-1]]
            playerDict[ppRow[-1]] = playerList
            playerNamesToCheck.append(contestName)


for row in contestLineup:
    for ppRow in pitchersPP:
        contestName = editPlayerName(row, 1)
        ppName = editPlayerName(ppRow, 0)

        if contestName == ppName and 'P' in row[0] and (teamDict[row[-1]] == ppRow[1] or ppRow[1] == ''):
            playerList = [row[0], row[1], float(ppRow[-2]), int(row[2]), row[-1]]
            playerDict[ppRow[-1]] = playerList
            playerNamesToCheck.append(contestName)


# #For testing with Sabersim, matches up the players from fanduel with their projected points from Sabersim
# for row in contestLineup:
#     for ppRow in saberSim:
#         fdName = editPlayerName(row, 1)
#         ssName = editPlayerName(ppRow, 1)
#         if fdName == ssName and (teamDict2[row[-1]] == ppRow[2] or ppRow[2] == ''):
#             playerList = [row[0], row[1], float(ppRow[9]), int(row[2]), row[-1]]
#             playerDict[ppRow[0]] = playerList
#             playerNamesToCheck.append(fdName)

# Print the total number of players read in
print('\nPlayer Dictionary Length: ' + str(len(playerDict)))

# Assign the players to dictionaries by position
print('\nFilling in Position Dictionaries...')
pitchers = {}
catchers = {}
firstBase = {}
secondBase = {}
thirdBase = {}
shortStop = {}
outfielders = {}
playersCantElim = {}

for ids in playerDict:

    if 'P' in playerDict[ids][0] :
        pitchers[ids] = playerDict[ids]

    if 'C' in playerDict[ids][0]:
        catchers[ids] = playerDict[ids]

    if '1B' in playerDict[ids][0]:
        firstBase[ids] = playerDict[ids]

    if '2B' in playerDict[ids][0]:
        secondBase[ids] = playerDict[ids]

    if '3B' in  playerDict[ids][0]:
        thirdBase[ids] = playerDict[ids]

    if 'SS' in playerDict[ids][0]:
        shortStop[ids] = playerDict[ids]

    if 'OF' in playerDict[ids][0]:
        outfielders[ids] = playerDict[ids]

    if '/' in playerDict[ids][0]:
        playersCantElim[ids] = playerDict[ids]


# Print the number of players at each position
print('\nAFTER LOADING IN THE DATA...')
print('Pitchers: ' + str(len(pitchers)))
print('Catchers: ' + str(len(catchers)))
print('FirstBase: ' + str(len(firstBase)))
print('SecondBase: ' + str(len(secondBase)))
print('ThirdBase: ' + str(len(thirdBase)))
print('ShortStop: ' + str(len(shortStop)))
print('Outfielders: ' + str(len(outfielders)))

# Print the number of possible lineups
numLineups = combinationsCalculator(len(pitchers), 2) * len(catchers) * len(firstBase) * len(secondBase) * len(thirdBase) * len(shortStop) * combinationsCalculator(len(outfielders), 3)
print("\nNumber of Possibly Optimal Lineups: {:,d}\n".format(numLineups))


"""
   Function to find the optimal lineup. Finds the lineup with the highest projected points total that satisfies
   the constraints. Function is recursive so that if the optimal lineup violates the max players from the same team
   constraint, or the players from at least 3 different teams constraint, it runs again without using players from whichever
   team(s) caused it to violate that constraint as the basis to eliminate other players from consideration.
"""
def findMaxPPDraftKings(playerDict, pitchers, catchers, firstBase, secondBase, thirdBase, shortStop, outfielders,
                        playersCantElim, teams=set(), lineupsViolateConstraint=set(), maxBatter=5):

    # Eliminate all but the player with the highest projected points value for each salary, by position
    def positionFilter(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        for player in positionDict:
            for player2 in positionDict:
                if positionDict[player][3] == positionDict[player2][3] and positionDict[player][2] < \
                   positionDict[player2][2] and positionDict[player2][-1] not in teams and player2 not in playersCantElim and player in positionDictCopy:
                    del positionDictCopy[player]
        return positionDictCopy

    # Eliminate all players who have a higher salary and a lesser or equal projected points value of another player, by position
    def filterMoreExpensiveLessPP(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        for player in positionDict:
            for player2 in positionDict:
                if positionDict[player][3] > positionDict[player2][3] and positionDict[player][2] <= \
                   positionDict[player2][2] and positionDict[player2][-1] not in teams and player2 not in playersCantElim and player in positionDictCopy:
                    del positionDictCopy[player]
        return positionDictCopy

    # If more than two pitchers share the same salary, eliminate all but the two with the highest projected points value
    def pitcherPositionFilter(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        pitcherSalaries = [positionDict[pit][3] for pit in positionDict]

        ofSalaryCounts = Counter(pitcherSalaries)

        pitcherSalariesToFilter = {k: v for k, v in ofSalaryCounts.items() if v > 2}

        for salary in pitcherSalariesToFilter:
            onTeams = 0
            pitchersWithSameSalary = []
            for pit in positionDict:
                if positionDict[pit][3] == salary:
                    pitchersWithSameSalary.append(positionDict[pit][2])
                    if positionDict[pit][-1] in teams:
                        onTeams += 1

            for num in range(pitcherSalariesToFilter[salary] - 2 - onTeams):
                lowestPP = min(pitchersWithSameSalary)
                for pit in positionDict:
                    if positionDict[pit][2] == lowestPP and positionDict[pit][3] == salary and pit in positionDictCopy:
                        del positionDictCopy[pit]
                        pitchersWithSameSalary.remove(lowestPP)
                        break
        return positionDictCopy

    # If there are at least two pitchers who have a salary equal to or lower than another pitcher, and a higher projected
    # points value, eliminate that pitcher
    def pitcherFilterMoreExpensiveLessPP(positionDict):
        pitcherList = []
        for key in positionDict:
            playerEntry = [key]
            [playerEntry.append(info) for info in positionDict[key]]
            pitcherList.append(playerEntry)

        pitcherListSalaryOrder = sorted(pitcherList, key=lambda x: (x[4], x[3] * -1))

        count = 0
        index = 0
        lowestSalaryPitchers = []
        while count < 2:
            if pitcherListSalaryOrder[index][-1] not in teams:
                lowestSalaryPitchers.append(pitcherListSalaryOrder[index])
                count += 1
            index += 1

        count = 0
        while count + 1 < len(pitcherListSalaryOrder):
            minPitcher = min(lowestSalaryPitchers, key=lambda x: x[3])

            pitchersToDelete = []
            for of in pitcherListSalaryOrder[2 + count:]:
                if of[3] < minPitcher[3] and of[4] >= minPitcher[4]:
                    pitchersToDelete.append(of)
            pitcherListSalaryOrder = [x for x in pitcherListSalaryOrder if x not in pitchersToDelete]

            try:
                if pitcherListSalaryOrder[2 + count][-1] not in teams:
                    lowestSalaryPitchers.remove(minPitcher)
                    lowestSalaryPitchers.append(pitcherListSalaryOrder[2 + count])
                else:
                    pass
            except IndexError:
                break

            count += 1
        pitchers = [item[0] for item in pitcherListSalaryOrder]
        return pitchers

    # If more than three outfielders share the same salary, eliminate all but the three with the highest projected points value
    def ofPositionFilter(positionDict):
        positionDictCopy = copy.deepcopy(positionDict)
        outfielderSalaries = [positionDict[of][3] for of in positionDict]

        ofSalaryCounts = Counter(outfielderSalaries)

        outfielderSalariesToFilter = {k: v for k, v in ofSalaryCounts.items() if v > 3}

        for salary in outfielderSalariesToFilter:
            cantElim = 0
            playersWithSameSalary = []
            for of in positionDict:
                if positionDict[of][3] == salary:
                    playersWithSameSalary.append(positionDict[of][2])
                    if positionDict[of][-1] in teams or of in playersCantElim:
                        cantElim += 1

            for num in range(outfielderSalariesToFilter[salary] - 3 - cantElim):
                lowestPP = min(playersWithSameSalary)
                for of in positionDict:
                    if positionDict[of][2] == lowestPP and positionDict[of][3] == salary:
                        if of in positionDictCopy:
                            del positionDictCopy[of]
                            playersWithSameSalary.remove(lowestPP)
                            break
        return positionDictCopy

    # If there are at least three outfielders who have a salary equal to or lower than another outfielder, and a higher projected
    # points value, eliminate that outfielder
    def ofFilterMoreExpensiveLessPP(positionDict):
        outfielderList = []
        for key in positionDict:
            playerEntry = [key]
            for info in positionDict[key]:
                playerEntry.append(info)
            outfielderList.append(playerEntry)

        outfielderListSalaryOrder = sorted(outfielderList, key=lambda x: (x[4], x[3] * -1))

        count = 0
        index = 0
        lowestSalaryOutfielders = []
        while count < 3:
            if outfielderListSalaryOrder[index][-1] not in teams and outfielderListSalaryOrder[index][0] not in playersCantElim:
                lowestSalaryOutfielders.append(outfielderListSalaryOrder[index])
                count += 1
            index += 1

        count = 1
        while count + 1 < len(outfielderListSalaryOrder):

            minPPOFer = min(lowestSalaryOutfielders, key=lambda x: x[3])

            outfieldersToDelete = []
            for of in outfielderListSalaryOrder[2 + count:]:
                if of[3] < minPPOFer[3] and of[4] >= minPPOFer[4]:
                    outfieldersToDelete.append(of)

            outfielderListSalaryOrder = [x for x in outfielderListSalaryOrder if x not in outfieldersToDelete]

            try:
                if outfielderListSalaryOrder[2 + count][-1] not in teams and outfielderListSalaryOrder[2 + count][0] not in playersCantElim:
                    lowestSalaryOutfielders.remove(minPPOFer)
                    lowestSalaryOutfielders.append(outfielderListSalaryOrder[2 + count])
                else:
                    pass
            except IndexError:
                break

            count += 1
        outfielders = [item[0] for item in outfielderListSalaryOrder]
        return outfielders

    # Eliminate pairs of players in the same way as before
    def groupFilterTwo(group):

        # If one pair has a higher combined salary and a lower or equal combined projected points value than another pair, eliminate that pair
        toDelete = set()
        for x, y in group:
            for x2, y2 in group:
                if playerDict[x][3] + playerDict[y][3] > playerDict[x2][3] + playerDict[y2][3] and playerDict[x][2] + \
                        playerDict[y][2] <= playerDict[x2][2] + playerDict[y2][2] and playerDict[x2][-1] not in teams and \
                        playerDict[y2][-1] not in teams and x2 not in playersCantElim and y2 not in playersCantElim:
                    toDelete.add((x, y))

        group.difference_update(toDelete)

        # If one pair has the same combined salary as another pair but a lower combined projected points value, eliminate that pair
        toDelete = set()
        for a, b in group:
            for a2, b2 in group:
                if playerDict[a][3] + playerDict[b][3] == playerDict[a2][3] + playerDict[b2][3] and playerDict[a][2] + \
                        playerDict[b][2] < playerDict[a2][2] + playerDict[b2][2] and playerDict[a2][-1] not in teams and \
                        playerDict[b2][-1] not in teams and a2 not in playersCantElim and b2 not in playersCantElim:
                    toDelete.add((a, b))

        group.difference_update(toDelete)
        return group

    # Eliminate groups of players in the same way as before
    def groupFilterThree(group):

        # Find the total salary and total projected points for each group of players
        newGroup = set()
        for x, y, z in group:
            salaryOF = playerDict[x][3] + playerDict[y][3] + playerDict[z][3]
            projectedPointsOF = playerDict[x][2] + playerDict[y][2] + playerDict[z][2]
            newGroup.add((x, y, z, projectedPointsOF, salaryOF))

        # If a group of players has a higher total salary and a lower or equal total projected points value than another group, eliminate that group
        toDelete = set()
        for x, y, z, pp, sal in newGroup:
            for x2, y2, z2, pp2, sal2 in newGroup:
                if sal > sal2 and pp <= pp2 and playerDict[x2][-1] not in teams and playerDict[y2][-1] not in teams and \
                                playerDict[z2][-1] not in teams and x2 not in playersCantElim and y2 not in playersCantElim and z2 not in playersCantElim:
                    toDelete.add((x, y, z))
        group.difference_update(toDelete)

        # If a group of players has the same total salary as another group but a lower total projected points value, eliminate that group
        toDelete = set()
        for x, y, z, pp, sal in newGroup:
            for x2, y2, z2, pp2, sal2, in newGroup:
                if sal == sal2 and pp < pp2 and playerDict[x2][-1] not in teams and playerDict[y2][-1] not in teams and \
                                playerDict[z2][-1] not in teams and x2 not in playersCantElim and y2 not in playersCantElim and z2 not in playersCantElim:
                    toDelete.add((x, y, z))
        group.difference_update(toDelete)

        return group

    # Filter out players that would never be selected for the optimal lineup
    pitchers2 = pitcherFilterMoreExpensiveLessPP(pitcherPositionFilter(pitchers))
    catchers2 = filterMoreExpensiveLessPP(positionFilter(catchers))
    firstBase2 = filterMoreExpensiveLessPP(positionFilter(firstBase))
    secondBase2 = filterMoreExpensiveLessPP(positionFilter(secondBase))
    thirdBase2 = filterMoreExpensiveLessPP(positionFilter(thirdBase))
    shortStop2 = filterMoreExpensiveLessPP(positionFilter(shortStop))
    outfielders2 = ofFilterMoreExpensiveLessPP(ofPositionFilter(outfielders))

    # Filter out groups of players that would never be selected for the optimal lineup
    pitcherGroups = groupFilterTwo(set(itertools.combinations(pitchers2, 2)))
    catchersFirstSecond = groupFilterThree(set(itertools.product(catchers2, firstBase2, secondBase2)))
    thirdShort = groupFilterTwo(set(itertools.product(thirdBase2, shortStop2)))
    outfielderGroups = groupFilterThree(set(itertools.combinations(outfielders2, 3)))

    # Create every possible lineup from the remaining players
    allLineups = list(itertools.product(pitcherGroups, catchersFirstSecond, thirdShort, outfielderGroups))

    # Eliminate all lineups which violate the max salary cap constraint
    underCap = set([(p, cfs, ts, of) for p, cfs, ts, of in allLineups if playerDict[p[0]][3] + playerDict[p[1]][3] + playerDict[cfs[0]][3] + playerDict[cfs[1]][3] +
                    playerDict[cfs[2]][3] + playerDict[ts[0]][3] + playerDict[ts[1]][3] + \
                    playerDict[of[0]][3] + playerDict[of[1]][3] + playerDict[of[2]][3] <= 50000])

    # If any lineups have previously violated the max batters from the same team constraint or the players from at least 3 different teams constraint, eliminate them
    underCap.difference_update(lineupsViolateConstraint)

    # Calculate the projected points for all remaining lineups
    underCapPP = {playerDict[p[0]][2] + playerDict[p[1]][2] + playerDict[cfs[0]][2] + playerDict[cfs[1]][2] + playerDict[cfs[2]][2] +
                    playerDict[ts[0]][2] + playerDict[ts[1]][2] + playerDict[of[0]][2] + playerDict[of[1]][2] + \
                    playerDict[of[2]][2]: (p, cfs, ts, of) for p, cfs, ts, of in underCap}

    # Find the lineup with the highest projected points total
    pp = max(underCapPP)

    count = 0
    while True:
        # If this loop has run without being reset then delete the previous optimal lineup for violating the max batters
        # from the same team constraint or the players from at least 3 different teams constraint, and find the lineup
        # with the next highest projected points total, since the team(s) responsible for this lineup violating the max
        # player constraint had already been added to the set not to use to eliminate
        if count > 0:
            lineupToDelete = underCapPP[pp]
            lineupsViolateConstraint.add(lineupToDelete)
            del underCapPP[pp]
            pp = max(underCapPP)

        optimalLineup = underCapPP[pp]
        flattenedOptimalLineup = [player for lineup in optimalLineup for player in lineup]
        teamsCounterForBatters = []
        teamsCounter = []

        # Find out the number of players and batters each team has in the optimal lineup
        for player in range(len(flattenedOptimalLineup)):
            # Add the teams for all players
            teamsCounter.append(playerDict[flattenedOptimalLineup[player]][-1])
            # Add the teams for batters only
            if player > 1:
                teamsCounterForBatters.append(playerDict[flattenedOptimalLineup[player]][-1])

        teamsCounterForBatters = Counter(teamsCounterForBatters)
        uniqueTeams = Counter(teamsCounter)
        maxTeamFreq = max(teamsCounterForBatters.values())

        # If the optimal lineup violates the max batters from the same team constraint, or the players from at least 3 different teams constraint,
        # add team(s) to a list to reference
        teamPlayersCantElim = []

        if len(uniqueTeams) < 3:
            [teamPlayersCantElim.append(teamNames) for teamNames in uniqueTeams]

        if maxTeamFreq > maxBatter:
            for teamName in teamsCounterForBatters:
                if teamsCounterForBatters[teamName] == maxTeamFreq and teamName not in teamPlayersCantElim:
                    teamPlayersCantElim.append(teamName)

        # If the optimal lineup violates the max batters from the same team constraint or the players from at least 3 different teams constraint but team(s)
        # had already been added to the set of teams not to eliminate from, revert to the top of this loop. Or if the same player appears twice in Optimal Lineup
        if len(set(flattenedOptimalLineup)) != len(flattenedOptimalLineup) or maxTeamFreq > maxBatter and all(x in teams for x in teamPlayersCantElim) \
                or len(uniqueTeams) < 3 and all(x in teams for x in teamPlayersCantElim):
            count += 1
            continue

        # If the optimal lineup had more than 5 batters from the same team(s) or had less than 3 different teams, and team(s) weren't already added to
        # the set of teams not to eliminate from, rerun this function without using any players from the team(s) as a basis to eliminate another player
        elif maxTeamFreq > maxBatter or len(uniqueTeams) < 3:
            [teams.add(x) for x in teamPlayersCantElim]
            lineupToDelete = underCapPP[pp]
            lineupsViolateConstraint.add(lineupToDelete)
            return findMaxPPDraftKings(playerDict, pitchers, catchers, firstBase, secondBase, thirdBase, shortStop,outfielders,
                                       teams, lineupsViolateConstraint)

        # All constraints have been satisfied, return the optimal lineup and its projected points total
        else:
            optimalLineup = tuple(sorted(optimalLineup[0], key=lambda x: (playerDict[x][3] * -1, x[2] * -1))) + \
                            optimalLineup[1] + optimalLineup[2] + tuple(sorted(optimalLineup[3], key=lambda x: (playerDict[x][3] * -1, x[2] * -1)))
            return optimalLineup, pp


optimalLineup, pp = findMaxPPDraftKings(playerDict,pitchers,catchers,firstBase,secondBase,thirdBase,shortStop,outfielders, playersCantElim)

# Format and print out optimal lineup information
capUsed = 0
for player in optimalLineup:
    capUsed += playerDict[player][3]
    playerEntry = [playerDict[player][0], playerDict[player][1], str(round(playerDict[player][2], 2)), '${:,d}'.format(playerDict[player][3]), playerDict[player][-1]]
    print(playerEntry)
print("\nCap Used: ${:,d}".format(capUsed))
print("Projected Points: " + str(round(pp, 2)))

e1 = time.time()
print("\nRuntime of program: " + str(e1-s1) + " seconds.")




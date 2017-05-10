import csv, itertools

lineupSpreadsheet = open('/Users/RyanRobertson21/Desktop/simpleball.csv')
lineupReader = csv.reader(lineupSpreadsheet)
lineupList = []
for row in lineupReader:
    playerList = []
    if lineupReader.line_num == 1:
        continue
    playerList.append(row[0])
    playerList.append(row[1])
    playerList.append(row[3])
    playerList.append(row[5])
    playerList.append(row[7])
    lineupList.append(playerList)

 ### change the above to take the full name cell instead of the first and last name cells, will use id number to identify
lineupSpreadsheet.close()

outfielders = []
for entry in lineupList:
    if entry[1] == 'OF':
        outfielders.append(entry[2])

print(len(list(itertools.combinations(outfielders, 3))))
print(lineupList)
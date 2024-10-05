def updateMockPara():
	"""Update the mock draft parameters when called."""
	### Getting saved mock parameters
	from data_open import saved_mock_data
	saved_mock = saved_mock_data()

	### Points information
	passYards = saved_mock[0][2]/25    		### 1 point per 25 yards
	passTDs = saved_mock[0][3] 	 		### 4 points per passing touchdown
	picks = saved_mock[0][4]			### -2 points for each picked pass
	fumble = saved_mock[0][5]				### -2 points for fumble lost
	recYards = saved_mock[0][6]/10   			### 1 point per 10 yards
	recTDs = saved_mock[0][7]  			### 6 points per receiving TDs
	rec = saved_mock[0][8]			### 1 point per reception
	rushYards = saved_mock[0][9]/10			### 1 point per 10 yards
	rushTDs = saved_mock[0][10]	 		### 6 points per rushing TDs

	### Team information
	numberTeams = saved_mock[0][0]
	teamName = saved_mock[0][1]

	mockParas = [passYards, passTDs, picks, fumble, recYards, recTDs, rec, rushYards, rushTDs, numberTeams, teamName]
	return mockParas

#####################################################################################################################################
def mockDataqb(players_stats, CurrentRos, mockPara):
	"""Gettig QB's stats for the mock draft table"""

	### points based off of saved parameters
	passYards = mockPara[0]
	passTDs = mockPara[1]
	picks = mockPara[2]
	fumble = mockPara[3]
	rushYards = mockPara[7]
	rushTDs = mockPara[8]

###			(l_name, f_name, year_born, year, age, team, games_played, games_started, \
###			passing_attempts,passing_comps,passing_yards, passing_touchdowns, picks, \
###			rushing_attempts,rushing_yards,rushing_touchdowns,fumbles))

	ListTotal = []
	for items in players_stats["QB"]:
		for item in CurrentRos["QB"]:		### lname, fname, birth year check for current roster
			if item[1][0] == items[0] and item[1][1] == items[1] and item[1][3] == items[2]: 
				try:					## Last and first name  and birth yearCheck if already in list then delete it.
					if ListTotal[-1][2] == items[0] and ListTotal[-1][1] == items[1] and ListTotal[-1][3] == items[2]:  
						fanPoints = round(passYards*items[10] + passTDs*items[11] + picks*items[12] +\
										  rushYards*items[-3] + rushTDs*items[-2] + fumble*items[-1], 2)
						lastFanPoints = ListTotal[-1][-2]
						del ListTotal[-1]

						### Calculating the percent difference 
						try: twoYears = round(((fanPoints - lastFanPoints)/lastFanPoints)*100, 2)
						except ZeroDivisionError: twoYears = "N/A"

					else:
						twoYears = "N/A"		
						fanPoints = round(passYards*items[10] + passTDs*items[11] + picks*items[12] +\
										  rushYards*items[-3] + rushTDs*items[-2] + fumble*items[-1], 2)

				except IndexError:
					twoYears = "N/A"		
					fanPoints = round(passYards*items[10] + passTDs*items[11] + picks*items[12] +\
									  rushYards*items[-3] + rushTDs*items[-2] + fumble*items[-1], 2)
	
				### Team, First Name, Last Name, Birth Year, position, pass yards, pass touchdowns, picks, rushing yards, rushing touchdowns, fumbles, year, fantasy points, two years trend
				ListTotal.append((item[0], items[1], items[0], items[2], "QB",items[10], items[11], items[12], items[-3], items[-2], items[-1], items[3], fanPoints, twoYears))

	### Sorting by Fantasy Stats
	ListTotal.sort(key=lambda ListTotal: ListTotal[-2], reverse=True)
	dicTotal = {"QB" : ListTotal}
	return dicTotal

#####################################################################################################################################
def mockDatarb(players_stats, CurrentRos, mockPara):
	"""Gettig RB's stats for the mock draft table"""

	### points based off of saved parameters
	rushYards = mockPara[7]
	rushTDs = mockPara[8]
	fumble = mockPara[3]
	recYards = mockPara[4]
	recTDs = mockPara[5]
	rec = mockPara[6]

	ListTotal = []
	for items in players_stats["RB"]:
		for item in CurrentRos["RB"]:		### lname, fname, birth year check for current roster
			if item[1][0] == items[0] and item[1][1] == items[1] and item[1][3] == items[2]: 
				try:					## Last and first name  and birth yearCheck if already in list then delete it.
					if ListTotal[-1][2] == items[0] and ListTotal[-1][1] == items[1] and ListTotal[-1][3] == items[2]:
						fanPoints = round(rushYards*items[9] + rushTDs*items[10] + fumble*items[11] +\
										  rec*items[13] + recYards*items[14] + recTDs*items[15], 2)
						lastFanPoints = ListTotal[-1][-2]
						del ListTotal[-1]

						### Calculating the percent difference 
						try: twoYears = round(((fanPoints - lastFanPoints)/lastFanPoints)*100, 2)
						except ZeroDivisionError: twoYears = "N/A"

					else:
						twoYears = "N/A"		
						fanPoints = round(rushYards*items[9] + rushTDs*items[10] + fumble*items[11] +\
										  rec*items[13] + recYards*items[14] + recTDs*items[15], 2)
				except IndexError:
					twoYears = "N/A"		
					fanPoints = round(rushYards*items[9] + rushTDs*items[10] + fumble*items[11] +\
									  rec*items[13] + recYards*items[14] + recTDs*items[15], 2)

				### Team, First Name, Last Name, Birth Year, position, rush yards, rush touchdowns, fumbles,  targets, receptions, rec yards, rec touchdowns, year, fantasy points, two years trend
				ListTotal.append((item[0], items[1], items[0], items[2], "RB", items[9], items[10], items[11], items[13], items[14], items[15], items[3], fanPoints, twoYears))

	### because one player is named 0 0 with a birthyear of 0....
	ListTotal = [items for items in ListTotal if items[1] !=0 and items[2] != 0]
	ListTotal.sort(key=lambda ListTotal: ListTotal[-2], reverse=True) ### Sorting by fantasy Stats
	dicTotal = {"RB" : ListTotal}		
	return dicTotal

#####################################################################################################################################
def mockDataWRTE(players_stats, CurrentRos, mockPara):
	"""Gettig WR's and TE's stats for the mock draft table"""

	### points based off of saved parameters
	recYards = mockPara[4]
	recTDs = mockPara[5]
	rec = mockPara[6]

	dicTotal = {}
	positions = ["WR", "TE"]
	for pos in positions:
		ListTotal = []
		for items in players_stats[pos]:
			for item in CurrentRos[pos]:		### lname, fname, birth year check for current roster
				if item[1][0] == items[0] and item[1][1] == items[1] and item[1][3] == items[2]:  
					try:					## Last and first name  and birth yearCheck if already in list then delete it.
						if ListTotal[-1][2] == items[0] and ListTotal[-1][1] == items[1] and ListTotal[-1][3] == items[2]:  
							fanPoints = round(rec*items[9] + recYards*items[10] + recTDs*items[11], 2)
							lastFanPoints = ListTotal[-1][-2]
							del ListTotal[-1]

							### Calculating the percent difference 
							try: twoYears = round(((fanPoints - lastFanPoints)/lastFanPoints)*100, 2)
							except ZeroDivisionError: twoYears = "N/A"

						else:
							twoYears = "N/A"		
							fanPoints = round(rec*items[9] + recYards*items[10] + recTDs*items[11], 2)

					except IndexError:
						twoYears = "N/A"		
						fanPoints = round(rec*items[9] + recYards*items[10] + recTDs*items[11], 2)				

					### Team, First Name, Last Name, Birth Year, position, targets, receptions, rec yards, rec touchdowns, year, fantasy points, two years trend
					ListTotal.append((item[0], items[1], items[0], items[2], pos, items[8], items[9], items[10], items[11], items[3], fanPoints, twoYears))

		ListTotal.sort(key=lambda ListTotal: ListTotal[-2], reverse=True)
		tempDic = {pos : ListTotal}
		dicTotal.update(tempDic)
	return dicTotal

#####################################################################################################################################
def mockData(players_stats, currentRos, returnAll = False):
	"""Gettig all stats for the mock draft table"""
	mockPara = updateMockPara()
	dicQB = mockDataqb(players_stats, currentRos, mockPara)
	dicRB = mockDatarb(players_stats, currentRos, mockPara)
	dicWRTE = mockDataWRTE(players_stats, currentRos, mockPara)


	dicTotal = {}
	dicTotal.update(dicQB)
	dicTotal.update(dicRB)
	dicTotal.update(dicWRTE)
	if returnAll == False:
		return dicTotal

	elif returnAll == True:
		tempList  = [items for KEYS in dicTotal.keys() for items in dicTotal[KEYS]]
		tempList.sort(key=lambda tempList: tempList[-2], reverse=True)
		dicTotal["allPlayers"] = tempList
		return dicTotal

#####################################################################################################################################

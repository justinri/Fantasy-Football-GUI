from help_options import pop_up_msg
from fun_file import mock_pop_up

### Creating default fonts
lFont = ("Helvetica", 10, "bold")
norm_font = ("Times", 10)

### Sitting up starter numders for each position
qbNum = 1
rbNum = 2
wrNum = 3
teNum = 1
flexNum = 1
#kNum = 1
#defNum = 1
kNum = 0
defNum = 0
benchNum = 7
posNums = [qbNum, rbNum, wrNum, teNum, flexNum, kNum, defNum, benchNum]
numStarters = sum(posNums) - benchNum

def team_organizer(team):
	"""Organizes teams to display in order... IE QB, RB, WR, TE, Flex, K, Def, Bench"""

	### Putting in order by fantasy points:
	team = [item for items in team for item in items]
	team.sort(key=lambda team: int(round(team[-1])), reverse=True)

	### Put the starters in order to display in the teams' players listbox 
	qbCount = 0;  qbTmp = []
	rbCount = 0;  rbTmp = []
	wrCount = 0;  wrTmp = []
	teCount = 0;  teTmp = []
	flexCount=0;  flexTmp = []
	kCount = 0;   kTmp = []
	defCount = 0; defTmp = []
	leftTmp = []
	for num, items in enumerate(team):
		tmpPos = items[0]
		if tmpPos == "QB" and qbCount < qbNum:
			qbTmp.append(items)
			qbCount += 1

		elif tmpPos == "RB" and rbCount < rbNum:
			rbTmp.append(items)
			rbCount += 1

		elif tmpPos == "WR" and wrCount < wrNum:
			wrTmp.append(items)
			wrCount += 1

		elif tmpPos == "TE" and teCount < teNum:
			teTmp.append(items)
			teCount += 1
	
		elif tmpPos in ["RB", "WR", "TE"] and flexCount < flexNum:
			flexTmp.append(items)
			flexCount=+ 1

		elif tmpPos == "K" and kCount < kNum:
			kTmp.append(items)
			kCount += 1

		elif tmpPos == "DEF" and defCount < defNum:
			defTmp.append(items)
			defCount += 1

		else:
			leftTmp.append(items)
	return [items for subLists in [qbTmp, rbTmp, wrTmp, teTmp, flexTmp, kTmp, defTmp, leftTmp] for items in subLists]


#####################################################################################################################################
def evaluate(allPlayers, dicTotal, curTeamVar, tk, ttk):
	"""Evaluate players involved in a trade."""

	### Doing checks if full teams are included
	if int(curTeamVar.get()) == 1:
		if not any("Before" in key for key in allPlayers.keys()):
			pop_up_msg('"Include before rosters" is checked,\nbut no before rosters were included')
			return
		
		### Checking correct number of players
		numBeforeLen = {}
		nonBeforeTeams = []
		awayRos = {"Player 1": [], "Player 2" : [], "Player 3" : [], "Player 4" : []}
		beforeRos = {"Player 1": [], "Player 2" : [], "Player 3" : [], "Player 4" : []}
		for key in allPlayers.keys():
			tmpPlayer = key[:8]
			if "Before" in key:
				numBeforeLen.update({tmpPlayer : len(allPlayers[key])})
				beforeRos[tmpPlayer].extend([allPlayers[key][key2] for key2 in allPlayers[key]])

				### Ensuring correct number of players
				if len(allPlayers[key]) < numStarters:
					pop_up_msg('Please include (at least) your starters for {} or uncheck "Include before rosters"\n'.format(tmpPlayer)+
								'Starters: {}\nBench: {}\n(Per your settings under plot/mock parameters)'.format(numStarters, benchNum))
					break
					return
			else:
				if tmpPlayer not in nonBeforeTeams:
					nonBeforeTeams.append(tmpPlayer)

			### Creaint players that will be traded away
			if "Away" in key:
				awayRos[tmpPlayer].extend([allPlayers[key][key2] for key2 in allPlayers[key]])

		### Ensuring before teams are the same length
		maxB4 = sorted(numBeforeLen.items(), key = lambda x: x[1], reverse = True)[0]
		for key in numBeforeLen.keys():
			if numBeforeLen[key] < maxB4[1]:
				pop_up_msg("{} before roster has {} more player(s) than {}.\nThey must be equal.".format(maxB4[0], maxB4[1]-numBeforeLen[key], key))
				return

		### Ensuring that the same teams in non before rosters are the same in the before rosters
		for key in numBeforeLen.keys():
			if key not in nonBeforeTeams:
				pop_up_msg("{} has a before roster but not inluded elsewhere in the trade.".format(key))
				return
		for items in nonBeforeTeams:
			if items not in list(numBeforeLen.keys()):
				pop_up_msg("{} is included in the trade but does not have a before roster.".format(items)+
						   '\nAnd "Include before rosters" is checked')
				return

		### Enuring players traded away are on the correct before rosters
		for key in awayRos.keys():
			for items in awayRos[key]:
				if items not in beforeRos[key]:
					name = items[1].split()[:2]
					pop_up_msg("{} is trading away {} {}, but he is not in his before roster".format(key, name[0], name[1]))				
					return			
	
		### Ensuring that at least two teams are involved in the trade
		if len(numBeforeLen) < 2:
			pop_up_msg("Is {} trading with themself?\nOnly before roster was included".format(list(numBeforeLen.keys())[0]))
			return	

	### Doing my checks to avoid bugs
	if allPlayers == {}:
		pop_up_msg("I guess trading nothing for nothing isn't a bad trade...\nTry again...")
		return
	elif len(allPlayers.keys()) == 1:
		key = list(allPlayers.keys())[0]
		tmpSplit = allPlayers[key][0][1].split()
		fname = tmpSplit[0]
		lname = tmpSplit[1]
		if "Away" in key:
			pop_up_msg("What are you trading {} {} for?\nA washing machine?".format(fname, lname))
			return
		elif "For" in key:
			pop_up_msg("What are you trading away?".format(fname, lname))
			return		
		elif "Drop" in key:
			pop_up_msg("Yeah, I would drop {} {} for no reason too...".format(fname, lname), "Screw {} {}...".format(fname, lname))
			return

#####################################################################################################################################
	def more_checks(tmpPlayer):
		"""Making sure players are not repeated, when they shouldn't be"""

		### Sitting up dicts to run through
		tmpDrop = {}
		tmpFor = {}
		tmpAway = {}

		tmpDropAll = {}
		tmpForAll = {}
		tmpAwayAll = {}
		for num, key in enumerate(allPlayers.keys()):
			if tmpPlayer in key and "Drop" in key:
				tmpDrop.update(allPlayers[key])
			if tmpPlayer in key and "For" in key:
				tmpFor.update(allPlayers[key])
			if tmpPlayer in key and "Away" in key:
				tmpAway.update(allPlayers[key])


			### Creating all tmp
			tmpKey = num+100
			if "Drop" in key:
				tmpDropAll.update(allPlayers[key])
				tmpDropAll[tmpKey] = tmpDropAll.pop(list(allPlayers[key].keys())[0])
			if "For" in key:
				tmpForAll.update(allPlayers[key])
				tmpForAll[tmpKey] = tmpForAll.pop(list(allPlayers[key].keys())[0])
			if "Away" in key:
				tmpAwayAll.update(allPlayers[key])
				tmpAwayAll[tmpKey] = tmpAwayAll.pop(list(allPlayers[key].keys())[0])


		### Running the checks
		for key in allPlayers.keys():
			for key2 in allPlayers[key].keys():
				tmpSplit = allPlayers[key][key2][1].split()
				fname = tmpSplit[0]
				lname = tmpSplit[1]
				if tmpPlayer not in key:
					### Ensuring a player is dropped more than once
					if "Drop" in key:
						for key3 in tmpDrop.keys():
							if tmpDrop[key3] == allPlayers[key][key2]:
								pop_up_msg("{} and {} are both dropping {} {}?\n#AboutToGoOff...".format(tmpPlayer, key[:8], fname, lname))
								return

					### Ensuring a player is traded for more than once
					if "For" in key:
						for key3 in tmpDrop.keys():
							if tmpDrop[key3] == allPlayers[key][key2]:
								pop_up_msg("{} is trading for {} {}, but {} is dropping him...How?".format(key[:8], fname, lname, tmpPlayer))
								return

						for key3 in tmpFor.keys():
							if tmpFor[key3] == allPlayers[key][key2]:
								pop_up_msg("{} and {} are both trading for {} {}?\nIs he that good?".format(tmpPlayer, key[:8], fname, lname))
								return

					### Ensuring a player is traded away more than once
					if "Away" in key:
						for key3 in tmpAway.keys():
							if tmpAway[key3] == allPlayers[key][key2]:
								pop_up_msg("{} and {} are both trading away {} {}?\nMan, he must sucks...".format(tmpPlayer, key[:8], fname, lname))
								return


				### Ensuring if a player is being traded away, someone is trading for.
				if tmpPlayer in key:
					if "Away" in key:

						### Ensuring the same team isn't trading for the same player
						for key3 in tmpFor.keys():
							if tmpFor[key3] == allPlayers[key][key2]:   ### Ensuring the same team isn't trading for the same player
								pop_up_msg("{} is trading away and trading for {} {}...".format(tmpPlayer, fname, lname))

						### Ensuring if a player is being traded away, someone is trading for...
						for key3 in tmpForAll.keys():
							if tmpForAll[key3] == allPlayers[key][key2]:
								break
						else:
							pop_up_msg("{} is trading away {} {} to no one...".format(key[:8], fname, lname))
							return

					### Ensuring if a player is being traded away, someone is trading for or dropping him.
					if "For" in key:
						for key3 in tmpAway.keys():
							if tmpAway[key3] == allPlayers[key][key2]:   ### Ensuring the same team isn't trading for the same player
								pop_up_msg("{} is trading away and trading for {} {}...".format(tmpPlayer, fname, lname))

						### Ensuring if a player is being traded for, someone is trading away...
						for key3 in tmpAwayAll.keys():
							if tmpAwayAll[key3] == allPlayers[key][key2]:
								break
						else:
							pop_up_msg("{} is trading for {} {} from no one...".format(key[:8], fname, lname))
							return
		return

#####################################################################################################################################
	### Only running checks I need to, and hope avoid bugs from useless run through the more_check...
	for key in allPlayers.keys():
		if "Player 1" in key:
			more_checks("Player 1")
			break
	for key in allPlayers.keys():
		if "Player 2" in key:
			more_checks("Player 2")
			break
	for key in allPlayers.keys():
		if "Player 3" in key:
			more_checks("Player 3")
			break
	for key in allPlayers.keys():
		if "Player 4" in key:
			more_checks("Player 4")
			break

##################################################################################################################################
	### Ensuring there are at least two teams in away, for and there is an even numbers of teams.
	numTeamsAway = []
	numTeamsFor = []
	diffTeams = [] 
	for num, key in enumerate(allPlayers.keys()):
		tmpPlayer = key[:8]
	
		### Seeing if their is more than one player.
		if tmpPlayer not in diffTeams:
			diffTeams.append(tmpPlayer)

		### Ensuring numbers of teams
		if tmpPlayer not in numTeamsAway and "Away" in key:
			numTeamsAway.append(tmpPlayer)
		if tmpPlayer not in numTeamsFor and "For" in key:
			numTeamsFor.append(tmpPlayer)


	### Warning to ensure at least two teams are involved in the trade
	if len(numTeamsAway) < 2 and len(numTeamsFor) < 2:
		if len(diffTeams) == 1:
			pop_up_msg("Are you trying to try with yourself?	","Don't Worry, I'll be your friend. :)")
	
		else:
			pop_up_msg("Trying to do a one way trade...")
		return

	### Warning to ensure at same numbers of teams involved
	if len(numTeamsAway) != len(numTeamsFor):
		if len(numTeamsAway) > len(numTeamsFor):
			pop_up_msg("There are more away teams...\nShould be even...")
		elif len(numTeamsAway) < len(numTeamsFor):
			pop_up_msg("There are more for teams...\nShould be even...")
		return

	### Creating new dicts with fantasy points, pos, first and last name
	tmpAway = {}
	tmpFor = {}
	tmpDrop = {}
	tmpB4Player1 = [];
	tmpB4Player2 = [];
	tmpB4Player3 = [];
	tmpB4Player4 = [];
	tmpValues = []  ## For combo boxes
	tmpAwayPlayers = {"Player 1": [], "Player 2": [], "Player 3": [], "Player 4": [] }
	tmpForPlayers = {"Player 1": [], "Player 2": [], "Player 3": [], "Player 4": [] }
	tmpDropPlayers = {"Player 1": [], "Player 2": [], "Player 3": [], "Player 4": [] }
	for key in allPlayers.keys():
		for key2 in allPlayers[key].keys():
			pos = allPlayers[key][key2][0]
			tmpSplit = allPlayers[key][key2][1].split()
			fname = tmpSplit[0]
			lname = tmpSplit[1]
			bDay = int(tmpSplit[-1][-5:-1])
			tmpKey = key + "{}".format(key2)

			### Creating the tmp dictionaries
			if "Away" in key:
				tmpAway.update({tmpKey:(pos, fname, lname, items[-2]) 
							    for items in dicTotal[pos] if items[2] == lname and items[3] == bDay and items[1] == fname})

				### Getting Away after rosters in their own lists
				if "Player 1" in key:
					tmpAwayPlayers["Player 1"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
					if "Player 1" not in tmpValues:
						tmpValues.append("Player 1")

				elif "Player 2" in key:
					tmpAwayPlayers["Player 2"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
					if "Player 2" not in tmpValues:
						tmpValues.append("Player 2")

				elif "Player 3" in key:
					tmpAwayPlayers["Player 3"].append([(pos,fname,lname,items[-2]) 
			  		  			  					  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
					if "Player 3" not in tmpValues:
						tmpValues.append("Player 3")

				elif "Player 4" in key:
					tmpAwayPlayers["Player 4"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
					if "Player 4" not in tmpValues:
						tmpValues.append("Player 4")

			### Creating for tmp dict
			elif "For" in key:
				tmpFor.update({tmpKey:(pos, fname, lname, items[-2]) 
							   for items in dicTotal[pos] if items[2] == lname and items[3] == bDay and items[1] == fname})

				### Getting for after rosters in their own lists
				if "Player 1" in key:
					tmpForPlayers["Player 1"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
				elif "Player 2" in key:
					tmpForPlayers["Player 2"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
				elif "Player 3" in key:
					tmpForPlayers["Player 3"].append([(pos,fname,lname,items[-2]) 
			  		  			  					  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
				elif "Player 4" in key:
					tmpForPlayers["Player 4"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])

			### Creating drop tmp dict
			elif "Drop" in key:
				tmpDrop.update({tmpKey:(pos,fname,lname,items[-2]) 
								for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname})

				### Getting drop after rosters in their own lists
				if "Player 1" in key:
					tmpDropPlayers["Player 1"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
				elif "Player 2" in key:
					tmpDropPlayers["Player 2"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
				elif "Player 3" in key:
					tmpDropPlayers["Player 3"].append([(pos,fname,lname,items[-2]) 
			  		  			  					  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
				elif "Player 4" in key:
					tmpDropPlayers["Player 4"].append([(pos,fname,lname,items[-2]) 
								  		  			  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])

			### Getting before rosters in their own lists
			elif "Before" in key and "Player 1" in key:
				tmpB4Player1.append([(pos,fname,lname,items[-2]) 
								  		  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
			elif "Before" in key and "Player 2" in key:
				tmpB4Player2.append([(pos,fname,lname,items[-2]) 
								  		  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
			elif "Before" in key and "Player 3" in key:
				tmpB4Player3.append([(pos,fname,lname,items[-2]) 
								  		  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
			elif "Before" in key and "Player 4" in key:
				tmpB4Player4.append([(pos,fname,lname,items[-2]) 
								  		  for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname])
	tmpBefore = {"Player 1" : tmpB4Player1, "Player 2" : tmpB4Player2, "Player 3" : tmpB4Player3, "Player 4" : tmpB4Player4}

#####################################################################################################################################
	if int(curTeamVar.get()) == 1:
		### Creating after rosters
		tmpRosterAway = {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []};
		tmpRosterDrop = {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []};
		## Removing away players
		[tmpRosterAway[key].append([items]) for key in tmpBefore.keys() for items in tmpBefore[key] if items not in tmpAwayPlayers[key]]
		### Adding for players
		[tmpRosterAway[key].append(tmpForPlayers[key]) for key in tmpForPlayers.keys()]
		### Removing dropped players
		[tmpRosterDrop[key].extend(items) for key in tmpRosterAway.keys() for items in tmpRosterAway[key] if items not in tmpDropPlayers[key]]
		tmpAfter = {"Player 1" : tmpRosterDrop["Player 1"],"Player 2" : tmpRosterDrop["Player 2"],
														   "Player 3" : tmpRosterDrop["Player 3"], "Player 4" : tmpRosterDrop["Player 4"]}
		### Changes tables to view results of another player
		def change_table(whatPlayer, tmpBeforeTeam, tmpTeamAfter, tmpColNum = 0):
			[item.grid_remove() for item in evalPop.grid_slaves() if 99>int(item.grid_info()["row"])>3 
																  if tmpColNum+2 >= int(item.grid_info()["column"]) >= tmpColNum]
			### creating tmp number for indexing
			tmpNum = 0 if tmpColNum == 0 else 1

			### Creating labels
			startersLT2["before"][tmpNum].grid()
			startersLT2["after"][tmpNum].grid()
			startersLT2["points"][tmpNum].grid()

			def table_maker(tmpB4Item, tmpAfterItem):
				### Before trade rosters
				playersVarLT2["before"][tmpNum][tmpNum2].set((tmpB4Item[0], tmpB4Item[1], tmpB4Item[2]))
				playersLT2["before"][tmpNum][tmpNum2].grid(row=num+5)

				### after trade rosters
				playersVarLT2["after"][tmpNum][tmpNum2].set((tmpAfterItem[0], tmpAfterItem[1], tmpAfterItem[2]))
				playersLT2["after"][tmpNum][tmpNum2].grid(row=num+5)

				### Calculating change in points
				tmpPointsDiff = round(tmpAfterItem[-1] - tmpB4Item[-1], 2)
				if tmpPointsDiff >= 10:	bgColor = "green"
				elif tmpPointsDiff <= -10: bgColor = "red"
				else: bgColor = "lightgrey"
				playersVarLT2["points"][tmpNum][tmpNum2].set("{}".format(tmpPointsDiff))
				playersLT2["points"][tmpNum][tmpNum2].grid(row=num+5)
				playersLT2["points"][tmpNum][tmpNum2].configure(bg=bgColor)
				return

			### Creating loop to run through table_maker function
			for num in range(len(tmpBeforeTeam[whatPlayer])+1):
				if num < numStarters:
					tmpNum2 = num
					tmpB4Item  = tmpBeforeTeam[whatPlayer][num]
					tmpAfterItem  = tmpTeamAfter[whatPlayer][num]
					table_maker(tmpB4Item, tmpAfterItem)

				elif num == numStarters:
					backUpsLT2["before"][tmpNum].grid(row=num+5)
					backUpsLT2["after"][tmpNum].grid(row=num+5)
					backUpsLT2["points"][tmpNum].grid(row=num+5)

				elif num > numStarters:
					tmpNum2 = num-1
					tmpB4Item  = tmpBeforeTeam[whatPlayer][num-1]
					tmpAfterItem  = tmpTeamAfter[whatPlayer][num-1]
					table_maker(tmpB4Item, tmpAfterItem)

			### Createing total and grades for each users
			plusMinus["starters"][tmpNum].grid(row = num+6)
			plusMinus["backups"][tmpNum].grid(row = num+7)

			### Adding in results
			tmpStart = round(pointsDiff["Starters"][whatPlayer], 2)
			tmpBack = round(pointsDiff["Back Ups"][whatPlayer], 2)
			if tmpStart >= 10:	bgColorStart = "green"
			elif tmpStart <= -10: bgColorStart = "red"
			else: bgColorStart = "lightgrey"
			if tmpBack >= 10:	bgColorBack = "green"
			elif tmpBack <= -10: bgColorBack = "red"
			else: bgColorBack = "lightgrey"
			plusMinus["startVar"][tmpNum].set("{}".format(pointsDiff["Starters"][whatPlayer]))
			plusMinus["backVar"][tmpNum].set("{}".format(pointsDiff["Back Ups"][whatPlayer]))
			plusMinus["startPoints"][tmpNum].grid(row = num+6)
			plusMinus["backPoints"][tmpNum].grid(row = num+7)
			plusMinus["startPoints"][tmpNum].configure(bg=bgColorStart)
			plusMinus["backPoints"][tmpNum].configure(bg=bgColorBack)

			### Lasty, adding the grades
			grade = gradesTable2[whatPlayer]
			if  grade != None:
				if grade in ["A", "A-"]: bgColor = "green"
				elif grade in ["B+", "B", "B-"]: bgColor = "#00b300"
				elif grade in ["C+", "C", "C-"]: bgColor = "grey"
				elif grade in ["D+", "D", "D-"]: bgColor = "#ff8080"
				elif grade == "F": bgColor = "red"
				plusMinus["grade"][tmpNum].grid(row = num+8)
				plusMinus["grade"][tmpNum].configure(text=grade, bg=bgColor)
			return

		### Organizing teams to display
		teamBefore = {}
		teamAfter = {}
		for key in tmpBefore.keys():
			if "Player 1" in key and tmpBefore[key] != []: 
				teamBefore["Player 1"] = team_organizer(tmpBefore[key])
				teamAfter["Player 1"] = team_organizer(tmpAfter[key])
			elif "Player 2" in key and tmpBefore[key] != []: 
				teamBefore["Player 2"] = team_organizer(tmpBefore[key])
				teamAfter["Player 2"] = team_organizer(tmpAfter[key])
			elif "Player 3" in key and tmpBefore[key] != []: 
				teamBefore["Player 3"] = team_organizer(tmpBefore[key])
				teamAfter["Player 3"] = team_organizer(tmpAfter[key])
			elif "Player 4" in key and tmpBefore[key] != []: 
				teamBefore["Player 4"] = team_organizer(tmpBefore[key])
				teamAfter["Player 4"] = team_organizer(tmpAfter[key])

		### To find changes in points
		pointsDiff = {"Starters" : {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []}}
		pointsDiff.update({"Back Ups" : {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []}})
		for num, key in enumerate(teamBefore.keys()):
			for num, items in enumerate(teamBefore[key]):
				tmpB4Item  = items[-1]
				tmpAfterItem  = teamAfter[key][num][-1]
				if numStarters > num:
					pointsDiff["Starters"][key].append(round(tmpAfterItem - tmpB4Item, 2))
				else:
					pointsDiff["Back Ups"][key].append(round(tmpAfterItem - tmpB4Item, 2))

#####################################################################################################################################
	### Calculating totals
	def calculate_totals(tmpDic):
		tmp1 = 0
		tmp2 = 0
		tmp3 = 0
		tmp4 = 0
		for key in tmpDic:
			if "Player 1" in key:
				tmp1 += tmpDic[key][3]
			elif "Player 2" in key:
				tmp2 += tmpDic[key][3]
			elif "Player 3" in key:
				tmp3 += tmpDic[key][3]
			elif "Player 4" in key:
				tmp4 += tmpDic[key][3]
		totals = [tmp1, tmp2, tmp3, tmp4]
		return totals
	totalAway = calculate_totals(tmpAway)
	totalDrop = calculate_totals(tmpDrop)
	totalFor = calculate_totals(tmpFor)
	pointsLost = [item1 + item2 for item1, item2 in zip(totalAway, totalDrop)]

	if int(curTeamVar.get()) == 0:
		tmpPointsDiff = [item1 - item2 for item1, item2 in zip(totalFor, pointsLost)]
		pointsDiff = {"Player {}".format(num+1): round(items, 2) for num, items in enumerate(tmpPointsDiff)}

	### Creating mini pop up to for evaluation results
	evalPop = tk.Tk()
	evalPop.wm_title("Trade Evaluation Results")

#####################################################################################################################################
	### Creating labels for table 2, to stop a memory leak
	if int(curTeamVar.get()) == 1:
		idx = list(teamBefore.keys())[0]
		startersLT2 = {"before":{}, "after":{}, "points":{}}
		backUpsLT2 = {"before":{}, "after":{}, "points":{}}
		playersVarLT2 = {"before":{num:{num2:tk.StringVar(evalPop) for num2 in range(len(teamBefore[idx]))} for num in range(2)},
						 "after":{num:{num2:tk.StringVar(evalPop) for num2 in range(len(teamBefore[idx]))} for num in range(2)},
						 "points":{num:{num2:tk.StringVar(evalPop) for num2 in range(len(teamBefore[idx]))} for num in range(2)}}
		playersLT2 = {"before": {num:{num2: {} for num2 in range(len(teamBefore[idx]))} for num in range(2)},
					  "after" : {num:{num2: {} for num2 in range(len(teamBefore[idx]))} for num in range(2)},
					  "points" : {num:{num2: {} for num2 in range(len(teamBefore[idx]))} for num in range(2)}}
		plusMinus = {"starters":{num : {} for num in range(2)},
					 "backups":{num : {} for num in range(2)},
					 "startPoints":{num : {} for num in range(2)},
					 "backPoints":{num : {} for num in range(2)},
					 "startVar":{num : tk.StringVar(evalPop) for num in range(2)},
					 "backVar":{num : tk.StringVar(evalPop) for num in range(2)},
					 "grade":{num : {} for num in range(2)}}

		for num in range(2):
			startersLT2["before"].update({num:ttk.Label(evalPop,text="Before Trade: Starters:",font=lFont,relief="groove",
																							anchor="center",justify="center")})
			startersLT2["before"][num].grid(row = 4, column = num*3, ipadx = 3,  sticky = "nesw")
			startersLT2["after"].update({num:ttk.Label(evalPop,text="After Trade: Starters:",font=lFont,relief="groove",
																						  anchor="center",justify="center")})
			startersLT2["after"][num].grid(row = 4, column = num*3+1, ipadx = 3,  sticky = "nesw")
			startersLT2["points"].update({num:ttk.Label(evalPop,text="Points +/-:", font=lFont, relief="groove", anchor="center", justify="center")})
			startersLT2["points"][num].grid(row = 4, column = num*3+2, ipadx = 3,  sticky = "nesw")

			### Back up labels
			backUpsLT2["before"].update({num:ttk.Label(evalPop,text="Before Trade: Back Ups:",font=lFont,relief="groove",
																							  anchor="center",justify="center")})
			backUpsLT2["before"][num].grid(row = 6, column = num*3, ipadx = 3,  sticky = "nesw")
			backUpsLT2["after"].update({num:ttk.Label(evalPop,text="After Trade: Back Ups:",font=lFont,relief="groove",
																						 	 anchor="center",justify="center")})
			backUpsLT2["after"][num].grid(row = 6, column = num*3+1, ipadx = 3,  sticky = "nesw")
			backUpsLT2["points"].update({num:ttk.Label(evalPop,text="Points +/-:", font=lFont, relief="groove", anchor="center", justify="center")})
			backUpsLT2["points"][num].grid(row = 6, column = num*3+2, ipadx = 3,  sticky = "nesw")

			### creating players before labels, 0 for row below here, because row is reconfirgured above in grid
			for num2 in range(len(teamBefore[idx])):
				playersLT2["before"][num].update({num2:tk.Label(evalPop, textvariable=playersVarLT2["before"][num][num2],relief="sunken",bg="grey")})
				playersLT2["before"][num][num2].grid(row = 0, column = num*3,  sticky = "nesw")

				playersLT2["after"][num].update({num2:tk.Label(evalPop, textvariable=playersVarLT2["after"][num][num2],relief="sunken",bg="grey")})
				playersLT2["after"][num][num2].grid(row = 0, column = num*3+1,  sticky = "nesw")

				playersLT2["points"][num].update({num2:tk.Label(evalPop, textvariable=playersVarLT2["points"][num][num2],relief="sunken",bg="grey")})
				playersLT2["points"][num][num2].grid(row = 0, column = num*3+2,  sticky = "nesw")

			### Labels below players
			plusMinus["starters"].update({num:ttk.Label(evalPop,text="Starters +/-:", relief="groove",font=lFont,anchor="center",justify="center")})
			plusMinus["starters"][num].grid(row = 0, column = num*3, columnspan = 2, sticky = "nesw")
			plusMinus["backups"].update({num:ttk.Label(evalPop,text="Back Ups +/-:", relief="groove",font=lFont,anchor="center",justify="center")})
			plusMinus["backups"][num].grid(row = 0, column = num*3, columnspan = 2, sticky = "nesw")

			### Points
			plusMinus["startPoints"].update({num:tk.Label(evalPop,textvariable=plusMinus["startVar"][num],relief="sunken",font=lFont,
																										anchor="center",justify="center")})
			plusMinus["startPoints"][num].grid(row = 0, column = num*3+2, sticky = "nesw")
			plusMinus["backPoints"].update({num:tk.Label(evalPop,textvariable=plusMinus["backVar"][num],relief="sunken",font=lFont,
																									  anchor="center",justify="center")})
			plusMinus["backPoints"][num].grid(row = 0, column = num*3+2, sticky = "nesw")

			### Grade
			plusMinus["grade"].update({num:tk.Label(evalPop,text = "", relief = "sunken", font = lFont, anchor="center", justify="center")})
			plusMinus["grade"][num].grid(row = 0, column = num*3, columnspan = 3,sticky = "nesw")

#####################################################################################################################################
	### calculating row(s) needed
	maxRow = {"away" : [0,0,0,0]}
	maxRow.update({"drop" : [0,0,0,0]})
	maxRow.update({"for" : [0,0,0,0]})
	for key in tmpAway.keys():
		if "Player 1" in key: maxRow["away"][0] += 1
		elif "Player 2" in key: maxRow["away"][1] += 1
		elif "Player 3" in key: maxRow["away"][2] += 1
		elif "Player 4" in key: maxRow["away"][3] += 1

	for key in tmpDrop.keys():
		if "Player 1" in key: maxRow["drop"][0] += 1
		elif "Player 2" in key: maxRow["drop"][1] += 1
		elif "Player 3" in key: maxRow["drop"][2] += 1
		elif "Player 4" in key: maxRow["drop"][3] += 1

	for key in tmpFor.keys():
		if "Player 1" in key: maxRow["for"][0] += 1
		elif "Player 2" in key: maxRow["for"][1] += 1
		elif "Player 3" in key: maxRow["for"][2] += 1
		elif "Player 4" in key: maxRow["for"][3] += 1
	maxRow["away"] = max(maxRow["away"])
	maxRow["drop"] = max(maxRow["drop"])
	maxRow["for"] = max(maxRow["for"])

#####################################################################################################################################
	### Creating labels and grades for point totals
	playerGrades = [None, None, None, None]
	if int(curTeamVar.get()) == 0:
		for num, tot in enumerate(totalAway):
			if tot != 0:

				### Grades are based off points gained... 80/5=16...So an A, would be, you gained 5 points agame.
				if int(curTeamVar.get()) == 0:
					tmpPoints = pointsDiff["Player {}".format(num+1)]
					if tmpPoints >= 80:	tmpGrade = "A"
					elif tmpPoints >= 25: tmpGrade = "A-"
					elif tmpPoints >= 20: tmpGrade = "B+"
					elif tmpPoints >= 15: tmpGrade = "B"
					elif tmpPoints >= 10: tmpGrade = "B-"
					elif tmpPoints >= 5: tmpGrade = "C+"
					elif tmpPoints >= 0: tmpGrade = "C"
					elif tmpPoints >= -5: tmpGrade = "C-"
					elif tmpPoints >= -10: tmpGrade = "D+"
					elif tmpPoints >= -15: tmpGrade = "D"
					elif tmpPoints >= -20: tmpGrade = "D-"
					else: tmpGrade = "F"
					playerGrades[num] = tmpGrade

	### Grading if you includes before rosters
	if int(curTeamVar.get()) == 1:
		tmpPoints = {"Starters" : {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []}}
		tmpPoints.update({"Back Ups" : {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []}})
		for key in pointsDiff.keys():
			pointsDiff[key]["Player 1"] = sum(pointsDiff[key]["Player 1"])
			pointsDiff[key]["Player 2"] = sum(pointsDiff[key]["Player 2"])
			pointsDiff[key]["Player 3"] = sum(pointsDiff[key]["Player 3"])
			pointsDiff[key]["Player 4"] = sum(pointsDiff[key]["Player 4"])
		
			### Times by two for starters, to make their points worth more. Then /16 to get it down to per game.
			timesBy = 2 if key == "Starters" else 1
			tmpPoints[key]["Player 1"] = pointsDiff[key]["Player 1"]*timesBy/16
			tmpPoints[key]["Player 2"] = pointsDiff[key]["Player 2"]*timesBy/16
			tmpPoints[key]["Player 3"] = pointsDiff[key]["Player 3"]*timesBy/16
			tmpPoints[key]["Player 4"] = pointsDiff[key]["Player 4"]*timesBy/16

		### Calculating grades
		tmpPointsGrade = {"Player 1" : [], "Player 2" : [], "Player 3" : [], "Player 4" : []}
		gradesTable2 = {"Player 1" : None, "Player 2" : None, "Player 3" : None, "Player 4" : None}
		for key in tmpPoints["Starters"].keys():
			tmpPointsGrade[key] = tmpPoints["Starters"][key] + tmpPoints["Back Ups"][key]

		for num, key in enumerate(tmpPointsGrade.keys()):
			tmpScore = tmpPointsGrade[key]
			if tmpScore != 0.0:
				if tmpScore >= 15:	tmpGrade = "A"
				elif tmpScore >= 13: tmpGrade = "A-"
				elif tmpScore >= 10: tmpGrade = "B+"
				elif tmpScore >= 8: tmpGrade = "B"
				elif tmpScore >= 5: tmpGrade = "B-"
				elif tmpScore >= 3: tmpGrade = "C+"
				elif tmpScore >= 0: tmpGrade = "C"
				elif tmpScore >= -3: tmpGrade = "C-"
				elif tmpScore >= -5: tmpGrade = "D+"
				elif tmpScore >= -8: tmpGrade = "D"
				elif tmpScore >= -10: tmpGrade = "D-"
				else: tmpGrade = "F"
				gradesTable2[key] = tmpGrade
				playerGrades[num] = tmpGrade

	### Storing grades
	gradeBgColor = [None, None, None, None]
	for num, grade in enumerate(playerGrades):
		if  grade != None:
			if grade in ["A", "A-"]: bgColor = "green"
			elif grade in ["B+", "B", "B-"]: bgColor = "#00b300"
			elif grade in ["C+", "C", "C-"]: bgColor = "grey"
			elif grade in ["D+", "D", "D-"]: bgColor = "#ff8080"
			elif grade == "F": bgColor = "red"
			gradeBgColor[num] = bgColor

	### Creating labels for table 1, L1T1 == Label 1 for Table 1
	labelsVar = {num2 : {num : tk.StringVar(evalPop) for num in range(2)} for num2 in range(3)}
	labelsL = {"away":{}, "drop":{}, "for":{}}
	for num in range(2):
		labelsL["away"].update({num:ttk.Label(evalPop, textvariable=labelsVar[0][num], font=lFont, relief="groove",anchor="center",justify="left")})
		labelsL["away"][num].grid(row = 4, column = num*3, columnspan = 3, ipadx = 2, sticky = "nesw")

		labelsL["drop"].update({num:ttk.Label(evalPop, textvariable=labelsVar[1][num], font=lFont, relief="groove",anchor="center",justify="left")})
		labelsL["drop"][num].grid(row = maxRow["away"]+8, column = num*3, columnspan = 3, ipadx = 2, sticky = "nesw")

		labelsL["for"].update({num:ttk.Label(evalPop, textvariable=labelsVar[2][num], font=lFont, relief="groove",anchor="center",justify="left")})
		labelsL["for"][num].grid(row = maxRow["away"]+maxRow["drop"]+21, column = num*3, columnspan = 3, ipadx = 2, sticky = "nesw")

#####################################################################################################################################
	### Creating labels for table one, mainly players' labels
	tmpPlayers = {"away": {"Player 1":{num: {} for num in range(2)},
						   "Player 2":{num: {} for num in range(2)},
						   "Player 3":{num: {} for num in range(2)},
						   "Player 4":{num: {} for num in range(2)}},
				 "drop":  {"Player 1":{num: {} for num in range(2)},
						   "Player 2":{num: {} for num in range(2)},
						   "Player 3":{num: {} for num in range(2)},
						   "Player 4":{num: {} for num in range(2)}},
				 "for":   {"Player 1":{num: {} for num in range(2)},
						   "Player 2":{num: {} for num in range(2)},
						   "Player 3":{num: {} for num in range(2)},
						   "Player 4":{num: {} for num in range(2)}}} 

	playersPoints = {"away": {"Player 1":{num: {} for num in range(2)},
						      "Player 2":{num: {} for num in range(2)},
						      "Player 3":{num: {} for num in range(2)},
						      "Player 4":{num: {} for num in range(2)}},
					 "drop": {"Player 1":{num: {} for num in range(2)},
							  "Player 2":{num: {} for num in range(2)},
							  "Player 3":{num: {} for num in range(2)},
							  "Player 4":{num: {} for num in range(2)}},
					 "for":  {"Player 1":{num: {} for num in range(2)},
							  "Player 2":{num: {} for num in range(2)},
							  "Player 3":{num: {} for num in range(2)},
							  "Player 4":{num: {} for num in range(2)}}} 

	tmpTotalsL = {"away": {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "drop": {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "for":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "losing":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "total":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "grade":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}}}

	tmpTotalsP = {"away": {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "drop": {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "for" :  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "losing":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "total":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}},
				  "grade":  {"Player 1":{}, "Player 2":{}, "Player 3":{}, "Player 4":{}}}

	### Creating a gap, for easy on the eyes
	gap = {"away": {num:tk.LabelFrame(evalPop) for num in range(2)},
		   "drop": {num:tk.LabelFrame(evalPop) for num in range(2)},
		   "for" : {num:tk.LabelFrame(evalPop) for num in range(2)}}

	### Create labels for both columns
	for num in range(2):
		count = [-1,-1,-1,-1]
		count1 = [-1,-1,-1,-1]
		count2 = [-1,-1,-1,-1]
		for key in tmpAway.keys():
			if "Player 1" in key: count[0] += 1; tmpCount = count[0]
			elif "Player 2" in key: count[1] += 1; tmpCount = count[1]
			elif "Player 3" in key: count[2] += 1; tmpCount = count[2]
			elif "Player 4" in key: count[3] += 1; tmpCount = count[3]
			tmpPlayers["away"][key[:8]][num].update({tmpCount:tk.Label(evalPop, text=tmpAway[key][1:3],
																		font=lFont,anchor="center",justify="left",bg="grey",relief="ridge")})
			tmpPlayers["away"][key[:8]][num][tmpCount].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			playersPoints["away"][key[:8]][num].update({tmpCount:tk.Label(evalPop,text=tmpAway[key][-1],
																		font=lFont,anchor="center",justify="center",bg="grey",relief="ridge")})
			playersPoints["away"][key[:8]][num][tmpCount].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

		### Creating labels for, players dropped
		for key in tmpDrop.keys():
			if "Player 1" in key: count1[0] += 1; tmpCount = count1[0]
			elif "Player 2" in key: count1[1] += 1; tmpCount = count1[1]
			elif "Player 3" in key: count1[2] += 1; tmpCount = count1[2]
			elif "Player 4" in key: count1[3] += 1; tmpCount = count1[3]
			tmpPlayers["drop"][key[:8]][num].update({tmpCount:tk.Label(evalPop, text=tmpDrop[key][1:3],
																		font=lFont,anchor="center",justify="left",bg="grey",relief="ridge")})
			tmpPlayers["drop"][key[:8]][num][tmpCount].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			playersPoints["drop"][key[:8]][num].update({tmpCount:tk.Label(evalPop,text=tmpDrop[key][-1],
																		font=lFont,anchor="center",justify="center",bg="grey",relief="ridge")})
			playersPoints["drop"][key[:8]][num][tmpCount].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

		### Creating labels for, players for
		for key in tmpFor.keys():
			if "Player 1" in key: count2[0] += 1; tmpCount = count2[0]
			elif "Player 2" in key: count2[1] += 1; tmpCount = count2[1]
			elif "Player 3" in key: count2[2] += 1; tmpCount = count2[2]
			elif "Player 4" in key: count2[3] += 1; tmpCount = count2[3]
			tmpPlayers["for"][key[:8]][num].update({tmpCount:tk.Label(evalPop, text=tmpFor[key][1:3],
																		font=lFont,anchor="center",justify="left",bg="grey",relief="ridge")})
			tmpPlayers["for"][key[:8]][num][tmpCount].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			playersPoints["for"][key[:8]][num].update({tmpCount:tk.Label(evalPop,text=tmpFor[key][-1],
																		font=lFont,anchor="center",justify="center",bg="grey",relief="ridge")})
			playersPoints["for"][key[:8]][num][tmpCount].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

		### Creating total points traded away labels
		for num2 in range(4):	
			tmpKey = "Player {}".format(num2+1)
			tmpTotalsL["away"][tmpKey].update({num:tk.Label(evalPop, text = "Total Points Trading Away:",
																 font=lFont,anchor="center",justify="left",bg="lightgrey", relief="groove")})
			tmpTotalsL["away"][tmpKey][num].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			tmpTotalsP["away"][tmpKey].update({num:tk.Label(evalPop, text=round(totalAway[num2], 2), 
																 font=lFont,anchor="center",justify="center",bg="lightgrey",relief="ridge")})
			tmpTotalsP["away"][tmpKey][num].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

			### Creating total dropping dictionary
			tmpTotalsL["drop"][tmpKey].update({num:tk.Label(evalPop, text = "Total Points Dropping:",
																 font=lFont,anchor="center",justify="left",bg="lightgrey", relief="groove")})
			tmpTotalsL["drop"][tmpKey][num].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			tmpTotalsP["drop"][tmpKey].update({num:tk.Label(evalPop, text=round(totalDrop[num2], 2), 
																 font=lFont,anchor="center",justify="center",bg="lightgrey",relief="ridge")})
			tmpTotalsP["drop"][tmpKey][num].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

			tmpTotalsL["losing"][tmpKey].update({num:tk.Label(evalPop, text = "Total Points Losing:",
																 font=lFont,anchor="center",justify="left",bg="lightgrey", relief="groove")})
			tmpTotalsL["losing"][tmpKey][num].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			tmpTotalsP["losing"][tmpKey].update({num:tk.Label(evalPop, text=round(pointsLost[num2], 2), 
																 font=lFont,anchor="center",justify="center",bg="lightgrey",relief="ridge")})
			tmpTotalsP["losing"][tmpKey][num].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

			### Creating total fordictionary
			tmpTotalsL["for"][tmpKey].update({num:tk.Label(evalPop, text = "Total Points Gaining:",
																 font=lFont,anchor="center",justify="left",bg="lightgrey", relief="groove")})
			tmpTotalsL["for"][tmpKey][num].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			tmpTotalsP["for"][tmpKey].update({num:tk.Label(evalPop, text=round(totalFor[num2], 2), 
																 font=lFont,anchor="center",justify="center",bg="lightgrey",relief="ridge")})
			tmpTotalsP["for"][tmpKey][num].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")


			### Creating labels for totals
			totalDiff = round(totalFor[num] - pointsLost[num], 2)
			tmpTotalsL["total"][tmpKey].update({num:tk.Label(evalPop, text = "Total +/-:",
																 font=lFont,anchor="center",justify="left",bg="lightgrey", relief="groove")})
			tmpTotalsL["total"][tmpKey][num].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			tmpTotalsP["total"][tmpKey].update({num:tk.Label(evalPop, text=totalDiff, 
																 font=lFont,anchor="center",justify="center",bg="lightgrey",relief="ridge")})
			tmpTotalsP["total"][tmpKey][num].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")


			### Creating labels for grades
			tmpTotalsL["grade"][tmpKey].update({num:tk.Label(evalPop, text="Grade:",
																 font=lFont,anchor="center",justify="left",bg=gradeBgColor[num2], relief="flat")})
			tmpTotalsL["grade"][tmpKey][num].grid(row = 0, column = num*3, columnspan = 2, ipadx = 2, sticky = "nesw")

			tmpTotalsP["grade"][tmpKey].update({num:tk.Label(evalPop, text=playerGrades[num2], 
																 font=lFont,anchor="center",justify="center",bg=gradeBgColor[num2],relief="flat")})
			tmpTotalsP["grade"][tmpKey][num].grid(row = 0, column = num*3+2, ipadx = 2, sticky = "nesw")

		### Creating a gap, for easy on the eyes
		gap["away"][num].grid(row = 0, column = num*3, columnspan = 3, sticky = "nesw", pady = 5)
		gap["drop"][num].grid(row = 0, column = num*3, columnspan = 3, sticky = "nesw", pady = 5)
		gap["for"][num].grid(row = 0, column = num*3, columnspan = 3, sticky = "nesw", pady = 5)

	### Removing everything from grid to be reset later
	[item.grid_remove() for item in evalPop.grid_slaves()]

#####################################################################################################################################
	def make_table(e, whatPlayer, colNum = 0):
		### Resitting Grid, only do once, hence why under the away tag, but before the making players
		[item.grid_remove() for item in evalPop.grid_slaves() if 99>int(item.grid_info()["row"])>3 
																  if colNum+2 >= int(item.grid_info()["column"]) >= colNum]
		### Setting tmpNum for indexing
		tmpNum = 0 if colNum == 0 else 1

		### Creating labels for players and total points
		tmpRow = 5
		for num,key in enumerate(tmpPlayers["away"][whatPlayer][tmpNum].keys()):
			tmpPlayers["away"][whatPlayer][tmpNum][key].grid(row = tmpRow)
			playersPoints["away"][whatPlayer][tmpNum][key].grid(row = tmpRow)
			tmpRow += 1

		tmpRow = maxRow["away"] + 5
		labelsVar[0][tmpNum].set("{}: Trading Away".format(whatPlayer))
		labelsL["away"][tmpNum].grid()
		tmpTotalsL["away"][whatPlayer][tmpNum].grid(row=tmpRow+1)
		tmpTotalsP["away"][whatPlayer][tmpNum].grid(row=tmpRow+1)
		gap["away"][tmpNum].grid(row=tmpRow+2)

		### Creating all the for information
		tmpRow = tmpRow+8
		startRow = tmpRow
		for num,key in enumerate(tmpPlayers["drop"][whatPlayer][tmpNum].keys()):
			tmpPlayers["drop"][whatPlayer][tmpNum][key].grid(row = tmpRow)
			playersPoints["drop"][whatPlayer][tmpNum][key].grid(row = tmpRow)
			tmpRow += 1

		tmpRow = maxRow["drop"] + startRow
		labelsVar[1][tmpNum].set("{}: Dropping".format(whatPlayer))
		labelsL["drop"][tmpNum].grid()
		tmpTotalsL["drop"][whatPlayer][tmpNum].grid(row=tmpRow+1)
		tmpTotalsP["drop"][whatPlayer][tmpNum].grid(row=tmpRow+1)
		tmpTotalsL["losing"][whatPlayer][tmpNum].grid(row=tmpRow+2)
		tmpTotalsP["losing"][whatPlayer][tmpNum].grid(row=tmpRow+2)
		gap["drop"][tmpNum].grid(row=tmpRow+3)

		### Creating all the for and grade information
		tmpRow = tmpRow+9
		startRow = tmpRow
		for num,key in enumerate(tmpPlayers["for"][whatPlayer][tmpNum].keys()):
			tmpPlayers["for"][whatPlayer][tmpNum][key].grid(row = tmpRow)
			playersPoints["for"][whatPlayer][tmpNum][key].grid(row = tmpRow)
			tmpRow += 1

		tmpRow = maxRow["for"] + startRow
		labelsVar[2][tmpNum].set("{}: Trading For".format(whatPlayer))
		labelsL["for"][tmpNum].grid()
		tmpTotalsL["for"][whatPlayer][tmpNum].grid(row=tmpRow+1)
		tmpTotalsP["for"][whatPlayer][tmpNum].grid(row=tmpRow+1)
		gap["for"][tmpNum].grid(row=tmpRow+3)
		tmpTotalsL["total"][whatPlayer][tmpNum].grid(row=tmpRow+4)
		tmpTotalsP["total"][whatPlayer][tmpNum].grid(row=tmpRow+4)
		tmpTotalsL["grade"][whatPlayer][tmpNum].grid(row=tmpRow+5)
		tmpTotalsP["grade"][whatPlayer][tmpNum].grid(row=tmpRow+5)
		return

########################################################################################################################################
	### Actually running the dics through, to display in gui
	tmpValues.sort(key=lambda tmpValues: tmpValues[-1])
	if int(curTeamVar.get()) == 0:
		make_table(None, tmpValues[0])
		make_table(None, tmpValues[1], colNum = 3)

		### Current team combo box
		combo1 = ttk.Combobox(evalPop, values = tmpValues, state="readonly")
		combo1.grid(row = 3, column = 0,  columnspan = 3, sticky = "nesw")
		combo1.set(tmpValues[0])
		combo1.bind('<<ComboboxSelected>>', lambda e: make_table(e, combo1.get()))

		### Combo for the second table
		combo2 = ttk.Combobox(evalPop, values = tmpValues, state="readonly")
		combo2.grid(row = 3, column = 3,  columnspan = 3, sticky = "nesw")
		combo2.set(tmpValues[1])
		combo2.bind('<<ComboboxSelected>>', lambda e: make_table(e, combo2.get(), colNum = 3))

	### Creating a couple of needed labels
	ttk.Label(evalPop,text="Select a Team:", font = lFont, relief = "groove", anchor = "center", justify="center"
																	 ).grid(row = 2, column = 0, columnspan = 3, ipadx = 3, sticky = "nesw")
	ttk.Label(evalPop,text="Select a Team:", font = lFont, relief = "groove", anchor = "center", justify="center"
																	 ).grid(row = 2, column = 3, columnspan = 3, ipadx = 3, sticky = "nesw")
	### Label for team results
	if int(curTeamVar.get()) == 1:

		### Current team combo box
		combo1 = ttk.Combobox(evalPop, values = tmpValues, state="readonly")
		combo1.grid(row = 3, column = 0,  columnspan = 3, sticky = "nesw")
		combo1.set(tmpValues[0])
		combo1.bind('<<ComboboxSelected>>', lambda e: pick_table(e, comboTable.get(), 1))

		### Combo for the second table
		combo2 = ttk.Combobox(evalPop, values = tmpValues, state="readonly")
		combo2.grid(row = 3, column = 3,  columnspan = 3, sticky = "nesw")
		combo2.set(tmpValues[1])
		combo2.bind('<<ComboboxSelected>>', lambda e: pick_table(e, comboTable.get(), 2))

		### Letting the user pick a table to view
		def pick_table(e, whatTable, side = None):
			if whatTable == "Table 1":
				make_table(None, combo1.get())
				make_table(None, combo2.get(), colNum = 3)
			elif whatTable == "Table 2" and side == None:
				change_table(combo1.get(), teamBefore, teamAfter, 0)
				change_table(combo2.get(), teamBefore, teamAfter, 3)

			### For when a single player is selected
			elif whatTable == "Table 1" and side == 1: make_table(None, combo1.get())
			elif whatTable == "Table 1" and side == 2: make_table(None, combo2.get(), colNum = 3)
			elif whatTable == "Table 2" and side == 1: change_table(combo1.get(), teamBefore, teamAfter, 0)
			elif whatTable == "Table 2" and side == 2: change_table(combo2.get(), teamBefore, teamAfter, 3)
			return
		pick_table(None, "Table 2")

		### Combo box two, what table... for first side
		ttk.Label(evalPop,text="What Table?", font = lFont, relief = "groove", anchor = "center", justify="center"
																	 ).grid(row = 0, column = 0, columnspan = 6, ipadx = 3, sticky = "nesw")
		comboTable = ttk.Combobox(evalPop, values = ["Table 1", "Table 2"], state="readonly")
		comboTable.grid(row = 1, column = 0,  columnspan = 6, sticky = "nesw")
		comboTable.set("Table 2")
		comboTable.bind('<<ComboboxSelected>>', lambda e: pick_table(e, comboTable.get()))

	### Finishing up results pop up
	ttk.Button(evalPop, text="Exit", command = evalPop.destroy).grid(row=100,column=3,columnspan=3,sticky="nwes")
	evalPop.mainloop()
	return

#####################################################################################################################################
def tradeEvalu(bio_and_combine, playersStats, dicTotal, tk, ttk):
	"""Evaluate suggested trades for the user"""
	tradeE = tk.Tk()
	tradeE.wm_title("Trade Evaluator")
	num_row = (0, 50)
	num_col = num_row

	### Creating list of players
	qbList = set([items[:3] for items in playersStats["QB"]])
	rbList = set([items[:3] for items in playersStats["RB"]])
	wrList = set([items[:3] for items in playersStats["WR"]])
	teList = set([items[:3] for items in playersStats["TE"]])

	### Putting in readable order for user: first name, last name, birthday: year
	qbList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in qbList]
	qbList.sort(key=lambda qbList: qbList[0]) 	   ### Sorting by last name
	rbList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in rbList]
	rbList.sort(key=lambda rbList: rbList[0]) 	   ### Sorting by last name
	wrList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in wrList]
	wrList.sort(key=lambda wrList: wrList[0]) 	   ### Sorting by last name
	teList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in teList]
	teList.sort(key=lambda teList: teList[0]) 	   ### Sorting by last name

	### For trade players, to view stats
	tmpStatsPopUp = {}

#####################################################################################################################################
	def select_players(e, lstBox, whatPlayer, doWhat = None, lstBoxB4 = False):
		"""Select players to be traded."""

		### getting the current team for before trade rosters
		if whatPlayer == "getPlayers":
			whatPlayer = curTeams.get()

		### Creating a better Key, for knowing when to add, drop and trade away players
		dicKey = "{} {}".format(whatPlayer, doWhat)

		### Allows for stats to pop up, for main trade evaluator, 
		### must be different from trade_stats below, because, it also allows to select different players for trading
		if lstBox.curselection()!=() and any(dicKey==key for key in tmpStatsPopUp) and lstBox.curselection()[0]<len(tmpStatsPopUp[dicKey]):
			pos = tmpStatsPopUp[dicKey][lstBox.curselection()[0]][0]
			tmpSplit = tmpStatsPopUp[dicKey][lstBox.curselection()[0]][1].split()
			fname = tmpSplit[0]
			lname = tmpSplit[1]
			bDay = int(tmpSplit[-1][-5:-1])
			player = (lname, fname, bDay)
			mock_pop_up(pos, player, playersStats, bio_and_combine, tk, ttk)
			return

#####################################################################################################################################
		def trade_stats(e):
			"""Allows for stats to pop up in tmp trade player selection."""
			if tmpLstBox.curselection() != ():
				pos = tmpPlayer[tmpLstBox.curselection()[0]][0]
				tmpSplit = tmpPlayer[tmpLstBox.curselection()[0]][1].split()
				fname = tmpSplit[0]
				lname = tmpSplit[1]
				bDay = int(tmpSplit[-1][-5:-1])
				player = (lname, fname, bDay)
				mock_pop_up(pos, player, playersStats, bio_and_combine, tk, ttk)
			return

#####################################################################################################################################
		tmp = tk.Tk()
		tmp.wm_title(whatPlayer + ": " + doWhat)
		tmpLstBox = tk.Listbox(tmp, bg = "white")
		if "Before" in doWhat: tmpLstBox.grid(row = 0, column = 0, columnspan = 6, ipady = 100, sticky = "nesw")
		else: tmpLstBox.grid(row = 0, column = 0, columnspan = 6, sticky = "nesw")
		tmpLstBox.bind("<Double-1>", lambda e:trade_stats(e))

		### Creating checkbox variables so they can check position(s) they want to view
		posVar = tk.IntVar(tmp)
		qb = tk.Radiobutton(tmp, text="QB", variable=posVar, value=1)
		qb.grid(row=1,column=0, sticky="w")
		rb = tk.Radiobutton(tmp, text="RB", variable=posVar, value=2)
		rb.grid(row=1,column=1, sticky="w")
		wr = tk.Radiobutton(tmp, text="WR", variable=posVar, value=3)
		wr.grid(row=1,column=2, sticky="w")
		te = tk.Radiobutton(tmp, text="TE", variable=posVar, value=4)
		te.grid(row=1,column=3, sticky="w")

		### Creating a buttons so people can update the player's combo box
		fBtn = ttk.Button(tmp, text = "Order by First Name", command = lambda: combo_players("fName"))
		fBtn.grid(row=2, column = 0, columnspan = 3, sticky = "nesw", ipadx = 10, ipady = 5)
		lBtn = ttk.Button(tmp, text = "Order by Last Name", command = lambda: combo_players("lName"))
		lBtn.grid(row=2, column = 3, columnspan = 3, sticky = "nesw", ipadx = 10, ipady = 5)
		fanBtn = ttk.Button(tmp, text = "Order by Last Year's Fantasy points", command = lambda: combo_players("fanStats"))
		fanBtn.grid(row=3, column = 0, columnspan = 6, sticky = "nesw", ipadx = 10, ipady = 5)
		
#####################################################################################################################################
		### Add people to list box
		def update_listbox(addRemove, exit = False, updateTmpBox = False):
			nonlocal tmpPlayer
			### For exiting, adds the players to main trade evaluation
			if exit == True:
				lstBox.delete(0, "end")
				if tmpPlayer != {}:
#					if "Before" in doWhat: tmpPlayer = team_organizer(tmpStatsPopUp[tmpKey])
					[lstBox.insert(0, tmpPlayer[key][1]) for key in sorted(tmpPlayer.keys(), reverse=True)]
					lstBox.insert(len(tmpPlayer), "")  ### To allow double click for stats or update list
					
					### To update before rosters too
					if "Away" in doWhat:
						tmpKey = "{} Roster (Before Trade)".format(whatPlayer)

						### Updating roster that is transfer through and is used to change list boxes for before rosters
						if tmpKey not in tmpStatsPopUp.keys():
							tmpStatsPopUp.update({tmpKey: tmpPlayer}) 
						else: 
							dicValues = [value for value in tmpStatsPopUp[tmpKey].values()]
							tmpLst = [items for key, items in tmpStatsPopUp[tmpKey].items()]
							tmpLst.extend([items for key, items in tmpPlayer.items() if items not in dicValues])
							tmpStatsPopUp[tmpKey] = {num: list(items) for num, items in enumerate(tmpLst)}
#							tmpStatsPopUp[tmpKey] = team_organizer(tmpLst)
							tmpStatsPopUp[tmpKey] = {num: items for num, items in enumerate(team_organizer([tmpLst]))}

						### If current list box is showed, it is updated
						if curTeams.get() == whatPlayer:
							lstBoxB4.delete(0, "end")
							[lstBoxB4.insert(0, tmpStatsPopUp[tmpKey][key][1]) for key in sorted(tmpStatsPopUp[tmpKey].keys(), reverse=True)]
							lstBoxB4.insert(len(tmpStatsPopUp[tmpKey]), "")

				else:
					lstBox.insert(0)  ### To allow double after a list has been cleared
					if dicKey in tmpStatsPopUp.keys(): del tmpStatsPopUp[dicKey]  ### To remove the key, of players no longer apart of the trade
				tmp.destroy()
				return

			### Ensuring limits to number of players per team
			def update_listbox_view():
				nonlocal count
				if "Before" in doWhat: countLimit = 20
				else: countLimit = 5

				if count < countLimit:
					tmpLstBox.delete(0, "end")
					[tmpLstBox.insert(0, tmpPlayer[key][1]) for key in sorted(tmpPlayer.keys(), reverse=True)]
					tmpStatsPopUp.update({ dicKey : {num : tmpPlayer[items] for num, items in enumerate(sorted(tmpPlayer.keys()))}})
				else:
					del tmpPlayer[count]
					if "Before" in doWhat: pop_up_msg("Max limit is 20")
					else: pop_up_msg("Five is the max number of players per team.")

				if addRemove != "remove":
					count += 1
				return
			
			### Update tmp list box if players were already selected before
			if updateTmpBox == True:
				update_listbox_view()
				return

			### Allow for the removal of players after added
			nonlocal count
			if addRemove == "remove":
				try:
					del tmpPlayer[tmpLstBox.curselection()[0]]
					tmpPlayer = {num : tmpPlayer[key] for num, key in enumerate(tmpPlayer.keys())}
					count -= 1
					update_listbox_view()
				except IndexError:
					pop_up_msg("Please click on a player to remove")
				return
			
			### Adding position
			tmpPos = posVar.get()
			if tmpPos == 0 or tmpPos == 1: pos = "QB"
			elif tmpPos == 2: pos = "RB"
			elif tmpPos == 3: pos = "WR"
			elif tmpPos == 4: pos = "TE"


			### Making sure a player is selected
			if globalCombo.get() == "":
				pop_up_msg("Please select a player.")
				return

			### Ensuring the same player is not picked twice
			if count > 0:
				for key in range(count):
					if tmpPlayer[key][1] == globalCombo.get():
						tmpPlayer2 = globalCombo.get().split()
						pop_up_msg("You're trying to trade {} {} twice...".format(tmpPlayer2[0], tmpPlayer2[1]))
						return

			### Adding player to tmpPlayer
			tmpPlayer.update({count : (pos, globalCombo.get())})
			update_listbox_view()
			return

#####################################################################################################################################
		### Updating tmpPlayer with current selection
		tmpPlayer = {}
		count = 0
		if dicKey in tmpStatsPopUp.keys():# and "Away" in doWhat: 
			count = sorted(tmpStatsPopUp[dicKey].keys())[-1]
			tmpPlayer = {key: items for key, items in tmpStatsPopUp[dicKey].items()}
			update_listbox(None, updateTmpBox = True)

#####################################################################################################################################
		def combo_players(orderBy, toDo = None, tmpLstBox = None):
			if orderBy != None:
				### Allowing user to pick order of players in drop down lists
				if orderBy == "fName": numOrder = 0; revOrder = False
				elif orderBy == "lName": numOrder = 1; revOrder = False
				elif orderBy == "fanStats": numOrder = 3; revOrder = True

				### Creating list of players
				qbList = set([(items[1:4], items[-2]) for items in dicTotal["QB"]])
				rbList = set([(items[1:4], items[-2]) for items in dicTotal["RB"]])
				wrList = set([(items[1:4], items[-2]) for items in dicTotal["WR"]])
				teList = set([(items[1:4], items[-2]) for items in dicTotal["TE"]])

				### Putting in readable order for user: first name, last name, birthday: year, and fantasy points
				qbList = [[items[0][0], items[0][1], "Birthday Year: {}".format(items[0][2]), items[1]] for items in qbList]
				qbList.sort(key=lambda qbList: qbList[numOrder], reverse=revOrder) 	   ### Sorting by last name
				rbList = [[items[0][0], items[0][1], "Birthday Year: {}".format(items[0][2]), items[1]] for items in rbList]
				rbList.sort(key=lambda rbList: rbList[numOrder], reverse=revOrder) 	   ### Sorting by last name
				wrList = [[items[0][0], items[0][1], "Birthday Year: {}".format(items[0][2]), items[1]] for items in wrList]
				wrList.sort(key=lambda wrList: wrList[numOrder], reverse=revOrder) 	   ### Sorting by last name
				teList = [[items[0][0], items[0][1], "Birthday Year: {}".format(items[0][2]), items[1]] for items in teList]
				teList.sort(key=lambda teList: teList[numOrder], reverse=revOrder) 	   ### Sorting by last name

				### Creating lists for the drop down menus and the menus
				if posVar.get() == 2: dropLst = [items[:3] for items in rbList[:]]
				elif posVar.get() == 3: dropLst = [items[:3] for items in wrList[:]]
				elif posVar.get() == 4: dropLst = [items[:3] for items in teList[:]]
				else: dropLst = [items[:3] for items in qbList[:]]

				### Creating the combo box
				global globalCombo
				globalCombo =  ttk.Combobox(tmp, values = dropLst, state="readonly")
				globalCombo.grid(row=4, column=0, columnspan = 6, sticky="nwes")
				globalCombo.bind("<Return>", update_listbox)
				globalCombo.bind('<<ComboboxSelected>>', update_listbox)
			return

		### Creating default combo box
		combo_players("fanStats")

		### Remove all players in the pop up player selection box
		def reset():
			nonlocal tmpPlayer, count
			tmpPlayer = {}
			if dicKey in tmpStatsPopUp.keys(): del tmpStatsPopUp[dicKey]
			update_listbox(None, updateTmpBox = True)
			count = 0 ### Must be after update_listbox
			return

		### Finishing up mini instance
		ttk.Button(tmp, text = "Remove Player", command = lambda:update_listbox("remove")).grid(row=5, column=0, columnspan=3, sticky = "nesw")
		ttk.Button(tmp, text = "Reset Players", command = reset).grid(row=5, column=3, columnspan=3, sticky = "nesw")
		ttk.Button(tmp, text = "Exit", command = lambda: update_listbox(None,True)).grid(row = 6, column = 0, columnspan = 6, sticky = "nesw")
		tmp.mainloop()
		return

#####################################################################################################################################
	### Class to create number of players
	class Num_of_Players:
		def __init__(self, num, whatPlayer, tradeE, num_row, num_col, doWhat, tk, ttk, plusRow = 0, lb2 = None):

			if doWhat == "Trading Away":
				### Creating the labels for players to trade
				self.tmp = "For {}\nSelect players to be traded away:\n(Max. 5)".format(whatPlayer)
				self.selLabel = ttk.Label(tradeE, text = self.tmp, font = norm_font, relief = "groove", anchor = "center", justify="center")
				self.selLabel.grid(row = num_row[0]+plusRow, column = num_col[0]+3+(num*4), columnspan = 4, ipadx = 2, sticky = "nesw")

			elif doWhat == "Trading For":
				### Creating the labels for players to trade
				self.tmp = "For {}\nSelect players to be traded for:\n(Max. 5)".format(whatPlayer)
				self.selLabel = ttk.Label(tradeE, text = self.tmp, font = norm_font, relief = "groove", anchor = "center", justify="center")
				self.selLabel.grid(row = num_row[0]+plusRow, column = num_col[0]+3+(num*4), columnspan = 4, ipadx = 2, sticky = "nesw")

			elif doWhat == "Dropping":
				### Creating the labels for players to trade
				self.tmp = "For {}\nSelect players that will be dropped:\n(Max. 5)".format(whatPlayer)
				self.selLabel = ttk.Label(tradeE, text = self.tmp, font = norm_font, relief = "groove", anchor = "center", justify="center")
				self.selLabel.grid(row = num_row[0]+plusRow, column = num_col[0]+3+(num*4), columnspan = 4, ipadx = 2, sticky = "nesw")

			### Creating the listboxes for the players to be traded
			self.lstBox = tk.Listbox(tradeE, bg = "white")
			self.lstBox.grid(row = num_row[0]+1+plusRow, column = num_col[0]+3+(num*4), rowspan = 10, columnspan = 4, sticky = "nesw")
			
			### Allows away to include list box for currnt rosters
			if "Away" not in doWhat:
				self.lstBox.bind("<Double-1>", lambda e: select_players(e, self.lstBox, whatPlayer, doWhat))
			else:
				self.lstBox.bind("<Double-1>", lambda e: select_players(e, self.lstBox, whatPlayer, doWhat, lb2))
			return

	### Creating current roster listbox
	curTeamlstBox = tk.Listbox(tradeE, bg = "white")
	curTeamlstBox.grid(row = 2, column = 19, rowspan = 40, ipadx = 33, sticky = "nesw")
	curTeamlstBox.bind("<Double-1>", lambda e: select_players(e, curTeamlstBox, "getPlayers", "Roster (Before Trade)"))

	### Create four list boxes, max number of teams involved in a trade
	numPlayers = {}
	numPlayersDrop = {}
	numPlayersFor = {}
	for num in range(4):
		numPlayers.update({num : Num_of_Players(num, "Player {}".format(num+1), tradeE, num_row, num_col, "Trading Away",tk,ttk,lb2=curTeamlstBox)})
		numPlayersDrop.update({num : Num_of_Players(num, "Player {}".format(num+1), tradeE, num_row, num_col, "Dropping", tk, ttk, 11)})
		numPlayersFor.update({num : Num_of_Players(num, "Player {}".format(num+1), tradeE, num_row, num_col, "Trading For", tk, ttk, 31)})

 	### Changes list box for players team, showing their roster before trade
	def change_listbox(e):
		tmpWhatPlayer = curTeams.get()
		dictTmpKey = "{} Roster (Before Trade)".format(tmpWhatPlayer)
		try:
			curTeamlstBox.delete(0, "end")
			[curTeamlstBox.insert(0, tmpStatsPopUp[dictTmpKey][key][1]) for key in tmpStatsPopUp[dictTmpKey]]
			curTeamlstBox.insert(len(tmpStatsPopUp[dictTmpKey]), "")
		except KeyError:
			curTeamlstBox.delete(0, "end")
		return
	
    ### Current rosters
	ttk.Label(tradeE,text="Enter Before\nTrade Rosters:\n(optional)", font = norm_font, relief = "groove", anchor = "center", justify="center"
																	   ).grid(row = num_row[0], column = 19,  sticky = "nesw")
	curTeamValues = ["Player 1", "Player 2", "Player 3", "Player 4"]
	curTeams = ttk.Combobox(tradeE, values = curTeamValues, state="readonly")
	curTeams.grid(row = num_row[0]+1, column = 19,  sticky = "nesw")
	curTeams.set(curTeamValues[0])
	curTeams.bind('<<ComboboxSelected>>', lambda e: change_listbox(e))

#	### Creating current roster listbox
#	curTeamlstBox = tk.Listbox(tradeE, bg = "white")
#	curTeamlstBox.grid(row = 2, column = 19, rowspan = 40, ipadx = 33, sticky = "nesw")
#	curTeamlstBox.bind("<Double-1>", lambda e: select_players(e, curTeamlstBox, "getPlayers", "Roster (Before Trade)"))

	### Allows for users to account for injuries
	injuryVar = tk.StringVar(tradeE, value = 1)
	tk.Checkbutton(tradeE, text = "Include an often injured penalty\nNot live yet..", variable = injuryVar, 
																	 onvalue=1).grid(row=num_row[-1], column=3, columnspan=4, sticky = "nwes")
	### Allows for users to account for current teams
	curTeamVar = tk.StringVar(tradeE, value = 1)
	tk.Checkbutton(tradeE, text = "Include before rosters\n(Recommended)", variable = curTeamVar, 
																	 onvalue=1).grid(row=num_row[-1], column=7, columnspan=4, sticky = "nwes")

	### Finishing up trade pop up
	ttk.Button(tradeE, text = "Evaluate", command = lambda: evaluate(tmpStatsPopUp, dicTotal, curTeamVar, tk, ttk)
															  		 ).grid(row = num_row[-1], column = 15, columnspan=4, sticky = "nesw")
	ttk.Button(tradeE, text = "Trade Recommendations", command = lambda: pop_up_msg("Not live yet...")
															  		 ).grid(row = num_row[-1], column = 11, columnspan=4, sticky = "nesw")
	ttk.Button(tradeE, text="Exit", command=tradeE.destroy).grid(row =num_row[-1],column=19,columnspan=4,sticky="nesw")
	tradeE.mainloop()
	return




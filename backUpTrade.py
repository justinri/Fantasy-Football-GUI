




#######################################################################################################################################
##def evaluate(allPlayers, dicTotal, tk, ttk):
##	"""Evaluate players involved in a trade."""

##	### Doing my checks to avoid bugs
##	if allPlayers == {}:
##		pop_up_msg("I guess trading nothing for nothing isn't a bad trade...\nTry again...")
##		return
##	elif len(allPlayers.keys()) == 1:
##		key = list(allPlayers.keys())[0]
##		tmpSplit = allPlayers[key][0][1].split()
##		fname = tmpSplit[0]
##		lname = tmpSplit[1]
##		if "Away" in key:
##			pop_up_msg("What are you trading {} {} for?\nA washing machine?".format(fname, lname))
##			return
##		elif "For" in key:
##			pop_up_msg("What are you trading away?".format(fname, lname))
##			return		
##		elif "Drop" in key:
##			pop_up_msg("Yeah, I would drop {} {} for no reason too...".format(fname, lname), "Screw {} {}...".format(fname, lname))
##			return

#######################################################################################################################################
##	def more_checks(tmpPlayer):
##		"""Making sure players are not repeated, when they shouldn't be"""

##		### Sitting up dicts to run through
##		tmpDrop = {}
##		tmpFor = {}
##		tmpAway = {}

##		tmpDropAll = {}
##		tmpForAll = {}
##		tmpAwayAll = {}
##		for num, key in enumerate(allPlayers.keys()):
##			if tmpPlayer in key and "Drop" in key:
##				tmpDrop.update(allPlayers[key])
##			if tmpPlayer in key and "For" in key:
##				tmpFor.update(allPlayers[key])
##			if tmpPlayer in key and "Away" in key:
##				tmpAway.update(allPlayers[key])


##			### Creating all tmp
##			tmpKey = num+100
##			if "Drop" in key:
##				tmpDropAll.update(allPlayers[key])
##				tmpDropAll[tmpKey] = tmpDropAll.pop(list(allPlayers[key].keys())[0])
##			if "For" in key:
##				tmpForAll.update(allPlayers[key])
##				tmpForAll[tmpKey] = tmpForAll.pop(list(allPlayers[key].keys())[0])
##			if "Away" in key:
##				tmpAwayAll.update(allPlayers[key])
##				tmpAwayAll[tmpKey] = tmpAwayAll.pop(list(allPlayers[key].keys())[0])


##		### Running the checks
##		for key in allPlayers.keys():
##			for key2 in allPlayers[key].keys():
##				tmpSplit = allPlayers[key][key2][1].split()
##				fname = tmpSplit[0]
##				lname = tmpSplit[1]
##				if tmpPlayer not in key:
##					### Ensuring a player is dropped more than once
##					if "Drop" in key:
##						for key3 in tmpDrop.keys():
##							if tmpDrop[key3] == allPlayers[key][key2]:
##								pop_up_msg("{} and {} are both dropping {} {}?\n#AboutToGoOff...".format(tmpPlayer, key[:8], fname, lname))
##								return

##					### Ensuring a player is traded for more than once
##					if "For" in key:
##						for key3 in tmpDrop.keys():
##							if tmpDrop[key3] == allPlayers[key][key2]:
##								pop_up_msg("{} is trading for {} {}, but {} is dropping him...How?".format(key[:8], fname, lname, tmpPlayer))
##								return

##						for key3 in tmpFor.keys():
##							if tmpFor[key3] == allPlayers[key][key2]:
##								pop_up_msg("{} and {} are both trading for {} {}?\nIs he that good?".format(tmpPlayer, key[:8], fname, lname))
##								return

##					### Ensuring a player is traded away more than once
##					if "Away" in key:
##						for key3 in tmpAway.keys():
##							if tmpAway[key3] == allPlayers[key][key2]:
##								pop_up_msg("{} and {} are both trading away {} {}?\nMan, he must sucks...".format(tmpPlayer, key[:8], fname, lname))
##								return


##				### Ensuring if a player is being traded away, someone is trading for.
##				if tmpPlayer in key:
##					if "Away" in key:

##						### Ensuring the same team isn't trading for the same player
##						for key3 in tmpFor.keys():
##							if tmpFor[key3] == allPlayers[key][key2]:   ### Ensuring the same team isn't trading for the same player
##								pop_up_msg("{} is trading away and trading for {} {}...".format(tmpPlayer, fname, lname))

##						### Ensuring if a player is being traded away, someone is trading for...
##						for key3 in tmpForAll.keys():
##							if tmpForAll[key3] == allPlayers[key][key2]:
##								break
##						else:
##							pop_up_msg("{} is trading away {} {} to no one...".format(key[:8], fname, lname))
##							return

##					### Ensuring if a player is being traded away, someone is trading for or dropping him.
##					if "For" in key:
##						for key3 in tmpAway.keys():
##							if tmpAway[key3] == allPlayers[key][key2]:   ### Ensuring the same team isn't trading for the same player
##								pop_up_msg("{} is trading away and trading for {} {}...".format(tmpPlayer, fname, lname))

##						### Ensuring if a player is being traded for, someone is trading away...
##						for key3 in tmpAwayAll.keys():
##							if tmpAwayAll[key3] == allPlayers[key][key2]:
##								break
##						else:
##							pop_up_msg("{} is trading for {} {} from no one...".format(key[:8], fname, lname))
##							return
##		return

#######################################################################################################################################
##	### Only running checks I need to, and hope avoid bugs from useless run through the more_check...
##	for key in allPlayers.keys():
##		if "Player 1" in key:
##			more_checks("Player 1")
##			break
##	for key in allPlayers.keys():
##		if "Player 2" in key:
##			more_checks("Player 2")
##			break
##	for key in allPlayers.keys():
##		if "Player 3" in key:
##			more_checks("Player 3")
##			break
##	for key in allPlayers.keys():
##		if "Player 4" in key:
##			more_checks("Player 4")
##			break

#######################################################################################################################################
##	### Ensuring there are at least two teams in away, for and there is an even numbers of teams.
##	numTeamsAway = []
##	numTeamsFor = []
##	diffTeams = [] 
##	for num, key in enumerate(allPlayers.keys()):
##		tmpPlayer = key[:8]
##	
##		### Seeing if their is more than one player.
##		if tmpPlayer not in diffTeams:
##			diffTeams.append(tmpPlayer)

##		### Ensuring numbers of teams
##		if tmpPlayer not in numTeamsAway and "Away" in key:
##			numTeamsAway.append(tmpPlayer)
##		if tmpPlayer not in numTeamsFor and "For" in key:
##			numTeamsFor.append(tmpPlayer)


##	### Warning to ensure at least two teams are involved in the trade
##	if len(numTeamsAway) < 2 and len(numTeamsFor) < 2:
##		if len(diffTeams) == 1:
##			pop_up_msg("Are you trying to try with yourself?	","Don't Worry, I'll be your friend. :)")
##	
##		else:
##			pop_up_msg("Trying to do a one way trade...")
##		return

##	### Warning to ensure at same numbers of teams involved
##	if len(numTeamsAway) != len(numTeamsFor):
##		if len(numTeamsAway) > len(numTeamsFor):
##			pop_up_msg("There are more away teams...\nShould be even...")
##		elif len(numTeamsAway) < len(numTeamsFor):
##			pop_up_msg("There are more for teams...\nShould be even...")
##		return

##	### Creating new dicts with fantasy points, pos, first and last name
##	tmpAway = {}
##	tmpFor = {}
##	tmpDrop = {}
##	for key in allPlayers.keys():
##		for key2 in allPlayers[key].keys():
##			pos = allPlayers[key][key2][0]
##			tmpSplit = allPlayers[key][key2][1].split()
##			fname = tmpSplit[0]
##			lname = tmpSplit[1]
##			bDay = int(tmpSplit[-1][-5:-1])
##			tmpKey = key + "{}".format(key2)

##			### Creating the tmp dictionaries
##			if "Away" in key:
##				tmpAway.update({tmpKey:(pos, fname, lname, items[-2]) 
##							    for items in dicTotal[pos] if items[2] == lname and items[3] == bDay and items[1] == fname})
##			elif "For" in key:
##				tmpFor.update({tmpKey:(pos, fname, lname, items[-2]) 
##							   for items in dicTotal[pos] if items[2] == lname and items[3] == bDay and items[1] == fname})
##			elif "Drop" in key:
##				tmpDrop.update({tmpKey:(pos,fname,lname,items[-2]) 
##								for items in dicTotal[pos] if items[2]==lname and items[3]==bDay and items[1]==fname})

##	### Calculating totals
##	def calculate_totals(tmpDic):
##		tmp1 = 0
##		tmp2 = 0
##		tmp3 = 0
##		tmp4 = 0
##		for key in tmpDic:
##			if "Player 1" in key:
##				tmp1 += tmpDic[key][3]
##			elif "Player 2" in key:
##				tmp2 += tmpDic[key][3]
##			elif "Player 3" in key:
##				tmp3 += tmpDic[key][3]
##			elif "Player 4" in key:
##				tmp4 += tmpDic[key][3]
##		totals = [tmp1, tmp2, tmp3, tmp4]
##		return totals
##	totalAway = calculate_totals(tmpAway)
##	totalDrop = calculate_totals(tmpDrop)
##	totalFor = calculate_totals(tmpFor)
##	pointsLost = [item1 + item2 for item1, item2 in zip(totalAway, totalDrop)]
##	pointsDiff = [item1 - item2 for item1, item2 in zip(totalFor, pointsLost)]

##	### Creating mini pop up to for evaluation results
##	evalPop = tk.Tk()
##	evalPop.wm_title("Trade Evaluation Results")

#######################################################################################################################################
##	### Table making class
##	class Make_Table:
##		def __init__(self, evalPop, player, total, rowNum, colNum, tk, ttk, bgColor = "lightgrey"):
##			tmp = tk.Label(evalPop, text = player, font = lFont, anchor = "center", justify="left", bg=bgColor)
##			tmp.grid(row = rowNum, column = colNum, ipadx = 2, sticky = "nesw")
##			tmp = tk.Label(evalPop, text = total, font = lFont, anchor = "center", justify="center", bg=bgColor)
##			tmp.grid(row = rowNum, column = colNum+1, ipadx = 2, sticky = "nesw")
##			return

##	def make_table(tmpDic2, rowStart):
##		### Calling class to make tables
##		rowNum1 = rowStart
##		rowNum2 = rowStart
##		rowNum3 = rowStart
##		rowNum4 = rowStart
##		for key in tmpDic2:
##			if "Player 1" in key:
##				if rowNum1 % 2 != 0: bgColor = "grey"
##				else: bgColor = "lightgrey"
##				colNum = 0
##				Make_Table(evalPop, tmpDic2[key][1:3], tmpDic2[key][-1], rowNum1, colNum, tk, ttk, bgColor)
##				rowNum1 += 1

##			elif "Player 2" in key:
##				if rowNum2 % 2 != 0: bgColor = "grey"
##				else: bgColor = "lightgrey"
##				colNum = 2
##				Make_Table(evalPop, tmpDic2[key][1:3], tmpDic2[key][-1], rowNum2, colNum, tk, ttk, bgColor)
##				rowNum2 += 1

##			elif "Player 3" in key:
##				if rowNum3 % 2 != 0: bgColor = "grey"
##				else: bgColor = "lightgrey"
##				colNum = 4
##				Make_Table(evalPop, tmpDic2[key][1:3], tmpDic2[key][-1], rowNum3, colNum, tk, ttk, bgColor)
##				rowNum3 += 1

##			elif "Player 4" in key:
##				if rowNum4 % 2 != 0: bgColor = "grey"
##				else: bgColor = "lightgrey"
##				colNum = 6
##				Make_Table(evalPop, tmpDic2[key][1:3], tmpDic2[key][-1], rowNum4, colNum, tk, ttk, bgColor)
##				rowNum4 += 1
##		maxRow = max(rowNum1, rowNum2, rowNum3, rowNum4)
##		return maxRow

##	### Actually running the dics through, to display in gui
##	awayMaxRow = make_table(tmpAway, 1)
##	dropMaxRow = make_table(tmpDrop, awayMaxRow+4)
##	forMaxRow = make_table(tmpFor, dropMaxRow+5)

##	### Creating labels and grades for point totals
##	playerGrades = [0, 0, 0, 0]
##	for num, tot in enumerate(totalAway):
##		if tot != 0:
##			Make_Table(evalPop, "Total Points Trading Away:", round(tot, 2), awayMaxRow+1, num*2, tk, ttk)
##			Make_Table(evalPop, "Total Points Dropping:", round(totalDrop[num], 2), dropMaxRow+1, num*2, tk, ttk)
##			Make_Table(evalPop, "Total Points Losing:", round(pointsLost[num], 2), dropMaxRow+2, num*2, tk, ttk)
##			Make_Table(evalPop, "Total Points Gaining:", round(totalFor[num], 2), forMaxRow+1, num*2, tk, ttk)

##			### Grades are based off points gained... 80/5=16...So an A, would be, you gained 5 points agame.
##			tmpPoints = pointsDiff[num]
##			if tmpPoints >= 80:	tmpGrade = "A"
##			elif tmpPoints >= 25: tmpGrade = "A-"
##			elif tmpPoints >= 20: tmpGrade = "B+"
##			elif tmpPoints >= 15: tmpGrade = "B"
##			elif tmpPoints >= 10: tmpGrade = "B-"
##			elif tmpPoints >= 5: tmpGrade = "C+"
##			elif tmpPoints >= 0: tmpGrade = "C"
##			elif tmpPoints >= -5: tmpGrade = "C-"
##			elif tmpPoints >= -10: tmpGrade = "D+"
##			elif tmpPoints >= -15: tmpGrade = "D"
##			elif tmpPoints >= -20: tmpGrade = "D-"
##			else: tmpGrade = "F"
##			playerGrades[num] = tmpGrade

##	for num, grade in enumerate(playerGrades):
##			if  grade != 0:
##				if grade in ["A", "A-"]: bgColor = "green"
##				elif grade in ["B+", "B", "B-"]: bgColor = "#00b300"
##				elif grade in ["C+", "C", "C-"]: bgColor = "grey"
##				elif grade in ["D+", "D", "D-"]: bgColor = "#ff8080"
##				elif grade == "F": bgColor = "red"
##				Make_Table(evalPop, "Grade:", grade, forMaxRow+3, num*2, tk, ttk, bgColor)

##	### Creaing main labels
##	class Main_Labels:
##		def __init__(self, evalPop, string, rowNum, colNum, cspan, tk, ttk):
##			tmp = ttk.Label(evalPop, text = string, font = lFont, relief = "groove", anchor = "center", justify="left")
##			tmp.grid(row = rowNum, column = colNum, columnspan = 2, ipadx = 2, sticky = "nesw")
##			return

##	if any("Player 1" in items for items in tmpAway.keys()):
##		Main_Labels(evalPop, "Player 1: Trading Away", 0, 0, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 1: Dropping", awayMaxRow+3, 0, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 1: Trading For", dropMaxRow+4, 0, 2, tk, ttk)
##	if any("Player 2" in items for items in tmpAway.keys()):
##		Main_Labels(evalPop, "Player 2: Trading Away", 0, 2, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 2: Dropping", awayMaxRow+3, 2, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 2: Trading For", dropMaxRow+4, 2, 2, tk, ttk)
##	if any("Player 3" in items for items in tmpAway.keys()):
##		Main_Labels(evalPop, "Player 3: Trading Away", 0, 4, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 3: Dropping", awayMaxRow+3, 4, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 3: Trading For", dropMaxRow+4, 4, 2, tk, ttk)
##	if any("Player 4" in items for items in tmpAway.keys()):
##		Main_Labels(evalPop, "Player 4: Trading Away", 0, 6, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 4: Dropping", awayMaxRow+3, 6, 2, tk, ttk)
##		Main_Labels(evalPop, "Player 4: Trading For", dropMaxRow+4, 6, 2, tk, ttk)

##	### Creating nothings for the eyes
##	tk.LabelFrame(evalPop).grid(row = awayMaxRow+2, column = 0, columnspan = 10, sticky = "nesw", pady = 5)
##	tk.LabelFrame(evalPop).grid(row = dropMaxRow+3, column = 0, columnspan = 10, sticky = "nesw", pady = 5)

##	### Finishing up results pop up
##	ttk.Button(evalPop, text="Exit", command = evalPop.destroy).grid(row=100,column=100,sticky="nwes")
##	evalPop.mainloop()
##	return

#######################################################################################################################################
##def tradeEvalu(bio_and_combine, playersStats, dicTotal, tk, ttk):
##	"""Evaluate suggested trades for the user"""
##	tradeE = tk.Tk()
##	tradeE.wm_title("Trade Evaluator")
##	num_row = (0, 50)
##	num_col = num_row

##	### Creating list of players
##	qbList = set([items[:3] for items in playersStats["QB"]])
##	rbList = set([items[:3] for items in playersStats["RB"]])
##	wrList = set([items[:3] for items in playersStats["WR"]])
##	teList = set([items[:3] for items in playersStats["TE"]])

##	### Putting in readable order for user: first name, last name, birthday: year
##	qbList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in qbList]
##	qbList.sort(key=lambda qbList: qbList[0]) 	   ### Sorting by last name
##	rbList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in rbList]
##	rbList.sort(key=lambda rbList: rbList[0]) 	   ### Sorting by last name
##	wrList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in wrList]
##	wrList.sort(key=lambda wrList: wrList[0]) 	   ### Sorting by last name
##	teList = [[items[1], items[0], "Birthday Year: {}".format(items[2])] for items in teList]
##	teList.sort(key=lambda teList: teList[0]) 	   ### Sorting by last name

##	### For trade players, to view stats
##	tmpStatsPopUp = {}

#######################################################################################################################################
##	def select_players(e, lstBox, whatPlayer, doWhat = None):
##		"""Select players to be traded."""


###select_players(e, curTeamlstBox, "getPlayers", "Roster (Before Trade)"))
##		### getting the current team for before trade rosters
##		if whatPlayer == "getPlayers":
##			whatPlayer = curTeams.get()

##		### Creating a better Key, for knowing when to add, drop and trade away players
##		dicKey = whatPlayer + " " + doWhat

##		### Allows for stats to pop up, for main trade evaluator, 
##		### must be different from trade_stats below, because, it also allows to select different players for trading
##		if lstBox.curselection()!=() and any(dicKey==key for key in tmpStatsPopUp) and lstBox.curselection()[0]<len(tmpStatsPopUp[dicKey]):
##			pos = tmpStatsPopUp[dicKey][lstBox.curselection()[0]][0]
##			tmpSplit = tmpStatsPopUp[dicKey][lstBox.curselection()[0]][1].split()
##			fname = tmpSplit[0]
##			lname = tmpSplit[1]
##			bDay = int(tmpSplit[-1][-5:-1])
##			player = (lname, fname, bDay)
##			mock_pop_up(pos, player, playersStats, bio_and_combine, tk, ttk)
##			return

#######################################################################################################################################
##		def trade_stats(e):
##			"""Allows for stats to pop up in tmp trade player selection."""
##			if tmpLstBox.curselection() != ():
##				pos = tmpPlayer[tmpLstBox.curselection()[0]][0]
##				tmpSplit = tmpPlayer[tmpLstBox.curselection()[0]][1].split()
##				fname = tmpSplit[0]
##				lname = tmpSplit[1]
##				bDay = int(tmpSplit[-1][-5:-1])
##				player = (lname, fname, bDay)
##				mock_pop_up(pos, player, playersStats, bio_and_combine, tk, ttk)
##			return

#######################################################################################################################################
##		tmp = tk.Tk()
##		tmp.wm_title(whatPlayer + ": " + doWhat)
##		tmpLstBox = tk.Listbox(tmp, bg = "white")
##		tmpLstBox.grid(row = 0, column = 0, columnspan = 6, sticky = "nesw")
##		tmpLstBox.bind("<Double-1>", lambda e:trade_stats(e))

##		### Creating checkbox variables so they can check position(s) they want to view
##		posVar = tk.IntVar(tmp)
##		qb = tk.Radiobutton(tmp, text="QB", variable=posVar, value=1)
##		qb.grid(row=1,column=0, sticky="w")
##		rb = tk.Radiobutton(tmp, text="RB", variable=posVar, value=2)
##		rb.grid(row=1,column=1, sticky="w")
##		wr = tk.Radiobutton(tmp, text="WR", variable=posVar, value=3)
##		wr.grid(row=1,column=2, sticky="w")
##		te = tk.Radiobutton(tmp, text="TE", variable=posVar, value=4)
##		te.grid(row=1,column=3, sticky="w")

##		### Creating a buttons so people can update the player's combo box
##		fBtn = ttk.Button(tmp, text = "Order by First Name", command = lambda: combo_players("fName"))
##		fBtn.grid(row=2, column = 0, columnspan = 3, sticky = "nesw", ipadx = 10, ipady = 5)
##		lBtn = ttk.Button(tmp, text = "Order by Last Name", command = lambda: combo_players("lName"))
##		lBtn.grid(row=2, column = 3, columnspan = 3, sticky = "nesw", ipadx = 10, ipady = 5)
##		fanBtn = ttk.Button(tmp, text = "Order by Last Year's Fantasy points", command = lambda: combo_players("fanStats"))
##		fanBtn.grid(row=3, column = 0, columnspan = 6, sticky = "nesw", ipadx = 10, ipady = 5)
##		
#######################################################################################################################################
##		### Add people to list box
##		count = 0
##		tmpPlayer = {}
###		tmpStatsPlayers = {}
##		def update_listbox(addRemove, exit = False):
##			nonlocal tmpPlayer#, tmpStatsPlayers
##			### For exiting, adds the players to main trade evaluation
##			if exit == True:
##				try:
##					lstBox.delete(0, "end")
##					if tmpPlayer != {}:
##						[lstBox.insert(0, tmpPlayer[key][1]) for key in tmpPlayer.keys()]
##						lstBox.insert(len(tmpPlayer), "")  ### To allow double click for stats or update list
##					else:
##						lstBox.insert(0)  ### To allow double after a list has been cleared
##						del tmpStatsPopUp[dicKey]  ### To remove the key, if the players are no longer apart of the trade
##				except: pass ### I know, I know... bad...
##				tmp.destroy()
##				return

##			### Ensuring limits to number of players per team
##			def update_listbox_view():
##				nonlocal count
##				if count < 5:
##					tmpLstBox.delete(0, "end")
##					[tmpLstBox.insert(0, tmpPlayer[key][1]) for key in sorted(tmpPlayer.keys(), reverse=True)]
##					tmpStatsPopUp.update({ dicKey : {num : tmpPlayer[items] for num, items in enumerate(sorted(tmpPlayer.keys(), reverse=True))}})
##				else:
##					del tmpPlayer[count]
##					pop_up_msg("Five is the max number of players per team.")
##				if addRemove != "remove":
##					count += 1
##				return

##			### Allow for the removal of players after added
##			nonlocal count
##			if addRemove == "remove":
##				try:
##					del tmpPlayer[tmpLstBox.curselection()[0]]
##					tmpPlayer = {num : tmpPlayer[key] for num, key in enumerate(tmpPlayer.keys())}
##					count -= 1
##					update_listbox_view()
##				except IndexError:
##					pop_up_msg("Please click on a player to remove")
##				return
##			
##			### Adding position
##			tmpPos = posVar.get()
##			if tmpPos == 0 or tmpPos == 1:
##				pos = "QB"
##			elif tmpPos == 2:
##				pos = "RB"
##			elif tmpPos == 3:
##				pos = "WR"
##			elif tmpPos == 4:
##				pos = "TE"
##	
##			tmpPlayer.update({count : (pos, globalCombo.get())})
##			if tmpPlayer[count][1] == "":
##				pop_up_msg("Please select a player.")
##				return

##			### Ensuring the same player is not picked twice
##			if count > 0:
##				for key in range(count):
##					if tmpPlayer[key][1] == tmpPlayer[count][1]:
##						tmpPlayer2 = tmpPlayer[count][1].split()
##						pop_up_msg("You're trying to trade {} {} twice...".format(tmpPlayer2[0], tmpPlayer2[1]))
##						return
##			update_listbox_view()
##			return

#######################################################################################################################################
##		def combo_players(orderBy, toDo = None, tmpLstBox = None):
##			
##			if orderBy != None:
##				### Allowing user to pick order of players in drop down lists
##				if orderBy == "fName": numOrder = 0; revOrder = False
##				elif orderBy == "lName": numOrder = 1; revOrder = False
##				elif orderBy == "fanStats": numOrder = 3; revOrder = True

##				### Creating list of players
##				qbList = set([(items[1:4], items[-2]) for items in dicTotal["QB"]])
##				rbList = set([(items[1:4], items[-2]) for items in dicTotal["RB"]])
##				wrList = set([(items[1:4], items[-2]) for items in dicTotal["WR"]])
##				teList = set([(items[1:4], items[-2]) for items in dicTotal["TE"]])

##				### Putting in readable order for user: first name, last name, birthday: year, and fantasy points
##				qbList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in qbList]
##				qbList.sort(key=lambda qbList: qbList[numOrder], reverse=revOrder) 	   ### Sorting by last name
##				rbList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in rbList]
##				rbList.sort(key=lambda rbList: rbList[numOrder], reverse=revOrder) 	   ### Sorting by last name
##				wrList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in wrList]
##				wrList.sort(key=lambda wrList: wrList[numOrder], reverse=revOrder) 	   ### Sorting by last name
##				teList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in teList]
##				teList.sort(key=lambda teList: teList[numOrder], reverse=revOrder) 	   ### Sorting by last name

##				### Creating lists for the drop down menus and the menus
##				if posVar.get() == 2: dropLst = [items[:3] for items in rbList[:]]
##				elif posVar.get() == 3: dropLst = [items[:3] for items in wrList[:]]
##				elif posVar.get() == 4: dropLst = [items[:3] for items in teList[:]]
##				else: dropLst = [items[:3] for items in qbList[:]]

##				### Creating the combo box
##				global globalCombo
##				globalCombo =  ttk.Combobox(tmp, values = dropLst, state="readonly")
##				globalCombo.grid(row=4, column=0, columnspan = 6, sticky="nwes")
##				globalCombo.bind("<Return>", update_listbox)
##			return

##		### Creating default combo box
##		combo_players("fanStats")

##		### Finishing up mini instance
##		ttk.Button(tmp, text = "Add Player", command = lambda:update_listbox("add")).grid(row = 5, column = 0, columnspan = 2, sticky = "nesw")
##		ttk.Button(tmp, text = "Remove Player", command = lambda:update_listbox("remove")).grid(row=5, column=2, columnspan=2, sticky = "nesw")
##		ttk.Button(tmp, text = "Exit", command = lambda: update_listbox(None,True)).grid(row = 5, column = 4, columnspan = 2, sticky = "nesw")
##		tmp.mainloop()
##		return

#######################################################################################################################################
##	### Class to create number of players
##	class Num_of_Players:
##		def __init__(self, num, whatPlayer, tradeE, num_row, num_col, doWhat, tk, ttk, plusRow = 0):

##			if doWhat == "Trading Away":
##				### Creating the labels for players to trade
##				self.tmp = "For {}\nSelect players to be traded away:\n(Max. 5)".format(whatPlayer)
##				self.selLabel = ttk.Label(tradeE, text = self.tmp, font = norm_font, relief = "groove", anchor = "center", justify="center")
##				self.selLabel.grid(row = num_row[0]+plusRow, column = num_col[0]+3+(num*4), columnspan = 4, ipadx = 2, sticky = "nesw")

##			elif doWhat == "Trading For":
##				### Creating the labels for players to trade
##				self.tmp = "For {}\nSelect players to be traded for:\n(Max. 5)".format(whatPlayer)
##				self.selLabel = ttk.Label(tradeE, text = self.tmp, font = norm_font, relief = "groove", anchor = "center", justify="center")
##				self.selLabel.grid(row = num_row[0]+plusRow, column = num_col[0]+3+(num*4), columnspan = 4, ipadx = 2, sticky = "nesw")

##			elif doWhat == "Dropping":
##				### Creating the labels for players to trade
##				self.tmp = "For {}\nSelect players that will be dropped:\n(Max. 5)".format(whatPlayer)
##				self.selLabel = ttk.Label(tradeE, text = self.tmp, font = norm_font, relief = "groove", anchor = "center", justify="center")
##				self.selLabel.grid(row = num_row[0]+plusRow, column = num_col[0]+3+(num*4), columnspan = 4, ipadx = 2, sticky = "nesw")

##			### Creating the listboxes for the players to be traded
##			self.lstBox = tk.Listbox(tradeE, bg = "white")
##			self.lstBox.grid(row = num_row[0]+1+plusRow, column = num_col[0]+3+(num*4), rowspan = 10, columnspan = 4, sticky = "nesw")
##			self.lstBox.bind("<Double-1>", lambda e: select_players(e, self.lstBox, whatPlayer, doWhat))
##			return

##	### Create four list boxes, max number of teams involved in a trade
##	numPlayers = {}
##	numPlayersDrop = {}
##	for num in range(4):
##		numPlayers.update({num : Num_of_Players(num, "Player {}".format(num+1), tradeE, num_row, num_col, "Trading Away", tk, ttk)})
##		numPlayersDrop.update({num : Num_of_Players(num, "Player {}".format(num+1), tradeE, num_row, num_col, "Dropping", tk, ttk, 11)})
##		numPlayersDrop.update({num : Num_of_Players(num, "Player {}".format(num+1), tradeE, num_row, num_col, "Trading For", tk, ttk, 31)})


##    ### Current rosters
##	ttk.Label(tradeE,text="Enter Before\nTrade Rosters:\n(optional)", font = norm_font, relief = "groove", anchor = "center", justify="center"
##																	   ).grid(row = num_row[0], column = 19,  sticky = "nesw")
##	curTeamValues = ["Player 1", "Player 2", "Player 3", "Player 4"]
##	curTeams = ttk.Combobox(tradeE, values = curTeamValues, state="readonly")
##	curTeams.grid(row = num_row[0]+1, column = 19,  sticky = "nesw")
##	curTeams.set(curTeamValues[0])

##	### Creating the listboxes for before trade teams
##	curTeamlstBox = tk.Listbox(tradeE, bg = "white")
##	curTeamlstBox.grid(row = num_row[0]+2, column = 19, rowspan = 40, ipadx = 33, sticky = "nesw")
##	curTeamlstBox.bind("<Double-1>", lambda e: select_players(e, curTeamlstBox, "getPlayers", "Roster (Before Trade)"))

##	### Allows for users to account for injuries
##	injuryVar = tk.StringVar(tradeE)
##	injuryVar.set(1)
##	tk.Checkbutton(tradeE, text = "Include an often injured penalty\nNot live yet..", variable = injuryVar, 
##																	 onvalue=1).grid(row=num_row[-1], column=3, sticky = "nwes")

##	### Allows for users to account for current teams
##	curTeamVar = tk.StringVar(tradeE)
##	curTeamVar.set(1)
##	tk.Checkbutton(tradeE, text = "Include before rosters\n(Recommended)\nNot live yet..", variable = curTeamVar, 
##																	 onvalue=1).grid(row=num_row[-1], column=7, sticky = "nwes")

##	### Finishing up trade pop up
##	ttk.Button(tradeE, text = "Evaluate", command = lambda: evaluate(tmpStatsPopUp, dicTotal, tk, ttk)
##															  		 ).grid(row = num_row[-1], column = 15, columnspan=4, sticky = "nesw")
##	ttk.Button(tradeE, text="Exit", command=tradeE.destroy).grid(row =num_row[-1],column=19,columnspan=4,sticky="nesw")
##	tradeE.mainloop()
##	return


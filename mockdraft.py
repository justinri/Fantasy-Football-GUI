from help_options import pop_up_msg
from fun_file import stats_pop_up, mock_pop_up
from mockFun import updateMockPara, mockData
from simulatemock import sim_mock
from random import shuffle
from mocksearchresults import *

### Creating default fonts
large_font = ("Helvetica", 12)
lFont = large_font
small_font = ("Helvetica", 8)

### setting up number of players to show in the table
numPlayersTable = 8

#####################################################################################################################################
def showMockDraft(dicTotal, players_stats, currentRos, bio_and_combine, num_row, num_col, curYear, tk, ttk, self):
	"""Creates the mock draft page and does the mock draft."""

	### stop for redo after every draft.
	positions = ["QB","RB","WR","TE"]
	labels = ["Current Team", "Player's Name", "Age", "Position", "Last Year's Stats", 
							  "Total Fantasy Points\nLast Year", "Two Years Trends", "Pick Player"]

	for num, items in enumerate(labels):
		titleL = tk.Label(self, text = items, font = small_font, relief = "groove")
		if num == 0 or num == 1:
			titleL.grid(row = num_row[0]+1, column = num_col[0]+num*2, columnspan = 2, sticky = "nesw", ipadx = 5, ipady = 5)
		else: 
			titleL.grid(row = num_row[0]+1, column = num_col[0]+2+num, sticky = "nesw", ipadx = 5, ipady = 5)

	### Creating drop down for draft information columns on the right
	draftInfoL = tk.Label(self, text = "Draft Information", font=large_font, anchor = "center", relief = "sunken", bg = "grey", fg = "white")
	draftInfoL.grid(row = 0, column = 15, columnspan = 3, sticky = "nesw")

	playersLeftD = ttk.Combobox(self, values = ["All Players", "QB", "RB", "WR", "TE", "RB/WR/TE", "WR/TE", "Rookies"], state="readonly")
	playersLeftD.grid(row = 1, column = 16, sticky = "nesw")
	playersLeftD.set("All Players")

	### Player remove list
	playerRemove = dicTotal["allPlayers"]
	posRemove = {"QB" : dicTotal["QB"]}
	posRemove["RB"] = dicTotal["RB"] 
	posRemove["WR"] = dicTotal["WR"] 
	posRemove["TE"] = dicTotal["TE"] 

	### Importing mock parameters for number of teams and team name	
	mockParas = updateMockPara()
	numTeams = 2#mockParas[-2]
	teamName = mockParas[-1]
	mockRunning = False
	numStarters = 8 ### Need to beable to adjust
	numRounds = 2
	mockCount = -1
	idxCount = -1
	roundIdx = 1

	### Sitting up starter numders for each position
	qbNum = 1
	rbNum = 2
	wrNum = 3
	teNum = 1
	flexNum = 1
	kNum = 1
	defNum = 1
	posNums = [qbNum, rbNum, wrNum, teNum, flexNum, kNum, defNum]
	numMockDraft = 0

	### Setting up team information
	teamPlayers = {teamName : ""}
	teamNames = ["Computer {}".format(num) for num in range(1, numTeams)]
	teamNames.insert(0, teamName)
	teamPlayers.update({items : "" for items in teamNames})

	playersPickD = ttk.Combobox(self, values = teamNames, state="readonly")
	playersPickD.grid(row = 1, column = 15, sticky = "nesw")
	playersPickD.set(teamName)

	### Sitting up list boxes for players on players' teams and players left
	playersTeams = {items : tk.Listbox(self) for items in teamNames}
	playersLeft = tk.Listbox(self)
	playersLeft.grid(row = 2, column = 16, rowspan = 18, ipadx = 30, sticky = "nwes")

	### Sitting up draft order list box
	tk.Label(self, text = "Draft Order:", font = ("Helvetica", 12, "bold"), relief = "groove").grid(row = 1, column = 17, sticky = "nwes")
	draftOrderBox = tk.Listbox(self)
	for num, items in enumerate(teamNames):
		draftOrderBox.insert(num, items)
	draftOrderBox.grid(row = 2, column = 17, rowspan = 18, sticky = "nwes")

#####################################################################################################################################
	def pickPlayer(player = None, whoPicked = teamName, draftOrder = None):
		"""Adds a player to the human team that selected him. And removes the player from the players left list box."""
	
		nonlocal mockRunning
		### Finding out if the user is next to update tables
		userNext = False
		if draftOrder != None:# and whoPicked != teamName:
			for num, items in enumerate(teamOrder):
				if items == whoPicked:
					if roundIdx % 2 != 0:
						if num < len(teamOrder)-1 and teamOrder[num+1] == teamName:
							userNext = True
							break
						elif num == len(teamOrder)-1 and  teamOrder[-1] == teamName:
							userNext = True
							break
					else:
						if num < len(teamOrder)-1 and teamOrder[num-1] == teamName:
							userNext = True
							break
						elif num == len(teamOrder)-1 and teamOrder[0] == teamName:
							userNext = True
							break

		### Add players to player selected list
		if player != None:   ### position, first and last name, and birth year
			playerSel = [[player[4], player[1], player[2], player[3], player[-2], player[-1]]]
			tmpPos = player[4]
	
			if mockCount > numTeams - 1:
				tmp = [items for items in teamPlayers[whoPicked]]
				playerSel = tmp + playerSel

			### Remove player from player left list
			for num, items in enumerate(playerRemove): ### last name, birth year, position, first name
				if (player[2] == items[2]) and (player[3] == items[3]) and (tmpPos == items[4]) and (player[1] == items[1]):
					del playerRemove[num]
					break

			### updating player remove for search all players 
			for num, items in enumerate(posRemove[tmpPos]): ### last name, birth year, position, first name
				if (player[2] == items[2]) and (player[3] == items[3]) and (tmpPos == items[4]) and (player[1] == items[1]):
					del posRemove[tmpPos][num]	
					break

			### display last player picked, try and catch needed for when the playersel list does not exist, i.e. []
			showStats = tk.Label(self, text = "Last Pick: {} {} - By: {}".
							format(items[1],items[2], draftOrder[idxCount]),font=lFont,relief="sunken",bg="grey",fg="white")
			showStats.grid(row = 22, column = 0, columnspan = len(labels)*2-1, sticky = "nwes")
		else:
			playerSel = []

		### Setting up counter for human user
		if player != None:
			if tmpPos == "QB":
				tmpNum = int(allPlayerCountDict[whoPicked][0][0].get()[-1])+1
				allPlayerCountDict[whoPicked][0][0].set("QB Count: {}".format(tmpNum))
				
				if tmpNum > qbNum + 2: bgColorDict[whoPicked][0][0].set("red")
				elif tmpNum == qbNum + 2: bgColorDict[whoPicked][0][0].set("#00b300")
				elif tmpNum == qbNum + 1: bgColorDict[whoPicked][0][0].set("green")
				elif tmpNum == qbNum: bgColorDict[whoPicked][0][0].set("#00b300")
				elif tmpNum == qbNum-1 and qbNum -1 != 0: bgColorDict[whoPicked][0][0].set("#ff8080")
				else: bgColorDict[whoPicked][0][0].set("red")

			elif tmpPos == "RB":
				tmpNum = int(allPlayerCountDict[whoPicked][0][1].get()[-1])+1
				allPlayerCountDict[whoPicked][0][1].set("RB Count: {}".format(tmpNum))

				if tmpNum > rbNum + 4: bgColorDict[whoPicked][0][1].set("red")
				elif tmpNum >= rbNum + 3: bgColorDict[whoPicked][0][1].set("#00b300")
				elif tmpNum >= rbNum + 1: bgColorDict[whoPicked][0][1].set("green")
				elif tmpNum == rbNum: bgColorDict[whoPicked][0][1].set("#00b300")
				elif tmpNum == rbNum-1 and rbNum -1 != 0: bgColorDict[whoPicked][0][1].set("#ff8080")
				else: bgColorDict[whoPicked][0][1].set("red")

			elif tmpPos == "WR":
				tmpNum = int(allPlayerCountDict[whoPicked][0][2].get()[-1])+1
				allPlayerCountDict[whoPicked][0][2].set("WR Count: {}".format(tmpNum))

				if tmpNum > wrNum + 4: bgColorDict[whoPicked][0][2].set("red")
				elif tmpNum >= wrNum + 3: bgColorDict[whoPicked][0][2].set("#00b300")
				elif tmpNum >= wrNum + 1: bgColorDict[whoPicked][0][2].set("green")
				elif tmpNum == wrNum: bgColorDict[whoPicked][0][2].set("#00b300")
				elif tmpNum == wrNum-1 and wrNum -1 != 0: bgColorDict[whoPicked][0][2].set("#ff8080")
				else: bgColorDict[whoPicked][0][2].set("red")

			elif tmpPos == "TE":
				tmpNum = int(allPlayerCountDict[whoPicked][1][0].get()[-1])+1
				allPlayerCountDict[whoPicked][1][0].set("TE Count: {}".format(tmpNum))

				if tmpNum > teNum + 3: bgColorDict[whoPicked][1][0].set("red")
				elif tmpNum >= teNum + 2: bgColorDict[whoPicked][1][0].set("#00b300")
				elif tmpNum >= teNum + 1: bgColorDict[whoPicked][1][0].set("green")
				elif tmpNum == teNum: bgColorDict[whoPicked][1][0].set("#00b300")
				elif tmpNum == teNum-1 and teNum -1 != 0: bgColorDict[whoPicked][1][0].set("#ff8080")
				else: bgColorDict[whoPicked][1][0].set("red")

			elif tmpPos == "DEF":
				tmpNum = int(allPlayerCountDict[whoPicked][1][1].get()[-1])+1
				allPlayerCountDict[whoPicked][1][1].set("DEF Count: {}".format(tmpNum))

				if tmpNum >= DEFNum + 2: bgColorDict[whoPicked][1][1].set("red")
				elif tmpNum == DEFNum + 1: bgColorDict[whoPicked][1][1].set("#00b300")
				elif tmpNum == DEFNum: bgColorDict[whoPicked][1][1].set("green")
				elif tmpNum == DEFNum-1 and DEFNum -1 != 0: bgColorDict[whoPicked][1][1].set("#ff8080")
				else: bgColorDict[whoPicked][1][1].set("red")

			elif tmpPos == "K":
				tmpNum = int(allPlayerCountDict[whoPicked][1][2].get()[-1])+1
				allPlayerCountDict[whoPicked][1][2].set("K Count: {}".format(tmpNum))

				if tmpNum >= kNum + 2: bgColorDict[whoPicked][1][2].set("red")
				elif tmpNum == kNum + 1: bgColorDict[whoPicked][1][2].set("#00b300")
				elif tmpNum == kNum: bgColorDict[whoPicked][1][2].set("green")
				elif tmpNum == kNum-1 and kNum -1 != 0: bgColorDict[whoPicked][1][2].set("#ff8080")
				else: bgColorDict[whoPicked][1][2].set("red")
			player_counter(None, countL.get())

		### Put the starters in order to display in the teams' players listbox 
		qbCount = 0;  qbTmp = []
		rbCount = 0;  rbTmp = []
		wrCount = 0;  wrTmp = []
		teCount = 0;  teTmp = []
		flexCount=0;  flexTmp = []
		kCount = 0;   kTmp = []
		defCount = 0; defTmp = []
		leftTmp = []
		for num, items in enumerate(playerSel):
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
		allTempLists = [items for subLists in [qbTmp, rbTmp, wrTmp, teTmp, flexTmp, kTmp, defTmp, leftTmp] for items in subLists]
		teamPlayers.update({whoPicked : allTempLists})

#####################################################################################################################################
		def get_stats_mock(event, whatList, playersView = None, playersLeft = None, whatPlayer = None):
			"""Selects the player that was doubled clicked, and has all their stats pop up. In an mini instance. For the Mock Draft page"""

			if whatList == "playersLeft":
				clicked = playersView[int(playersLeft.curselection()[0])]
				clicked = (clicked[4], clicked[1], clicked[2], clicked[3])
			elif whatList == "playerPicked":
				clicked = teamPlayers[whatPlayer][int(playersTeams[whatPlayer].curselection()[0])]

			pos = clicked[0]								### Check lastname then first name then  birth year
			playersStats=[items for items in players_stats[pos] if clicked[2]==items[0] if clicked[1]==items[1] if clicked[3]==items[2]]
			comb_results=[items for items in  bio_and_combine[pos] if clicked[2]==items[4] if clicked[1]==items[5] if clicked[3]==items[6]]
			stats_pop_up(pos, playersStats, comb_results, tk, ttk)
			return

#####################################################################################################################################		
		### Update the playersleft list
		def player_left_list(event = None):
			### Creates list box for players that are left
			if playersLeftD.get() == '' or playersLeftD.get() == "All Players":
				playersView = playerRemove
			elif playersLeftD.get() in ["QB", "RB", "WR", "TE"]: 
				posPicked = playersLeftD.get()
				playersView = [items for items in playerRemove if items[4] == posPicked]
			elif playersLeftD.get() == "RB/WR/TE": 
				playersView = [items for items in playerRemove if items[4] == "RB" or items[4] == "WR" or items[4] == "TE"]
			elif playersLeftD.get() == "WR/TE":
				playersView = [items for items in playerRemove if items[4] == "WR" or items[4] == "TE"]
			elif playersLeftD.get() == "Rookies":
				playersView = [[".", ".", ".", ".", "Coming."], [".", ".", ".", ".", "Soon."]]

			### Players left list box
			playersLeft.delete(0, "end")
			for num, items in enumerate(playersView):
				playersLeft.insert(num, (items[4], items[1], items[2]))
				playersLeft.bind('<Double-1>', lambda event: get_stats_mock(event, "playersLeft", playersView, playersLeft))
				if num == 50: break
			return

#####################################################################################################################################
		### Creating title for Mock Draft Page
		if mockRunning == False or userNext == True:
			player_left_list()

			### Creating start mock draft button
			def mock_resetter():
				tk.Label(self).grid(row = 23, column = 0, columnspan = len(labels)*2-1, sticky = "nwes")
				tk.Label(self).grid(row = 22, column = 0, columnspan = len(labels)*2-1, sticky = "nwes")
				tmpDicTotal = mockData(players_stats, currentRos, True)
				showMockDraft(tmpDicTotal, players_stats, currentRos, bio_and_combine, num_row, num_col, curYear, tk, ttk, self)
				return

			### Creating start mock label
			nonlocal numMockDraft
			if numMockDraft == 0:
				mockButton = tk.Button(self, text = "Start Mock Draft", font = ("Times", "12", "bold"), command = lambda: start_mock("yes"))
				mockButton.grid(row = num_row[0], column = num_col[0], columnspan = 10, ipady = 5, sticky = "nwe")

			### Binds enter to up draft playerLeft drop down list based on position(s) selected
			playersLeftD.bind('<<ComboboxSelected>>', player_left_list)	

#####################################################################################################################################
			def make_table():
				"""Creates the table in the mock draft page."""
				try:
					if allVar.get() == 1 or (allVar.get() == 0 and qbVar.get() == 0 and rbVar.get() == 0 and wrVar.get() == 0 and teVar.get() == 0):
						ListTotal = playerRemove
						qbVar.set(0)
						rbVar.set(0)
						wrVar.set(0)
						teVar.set(0)
					elif qbVar.get() != 0 and rbVar.get() != 0 and wrVar.get() != 0 and teVar.get() != 0: 
						ListTotal = playerRemove
						allVar.set(1)
						qbVar.set(0)
						rbVar.set(0)
						wrVar.set(0)
						teVar.set(0)
					else:
						showPos = [qbVar.get(), rbVar.get(), wrVar.get(), teVar.get()]
						showPos = list(filter(lambda nonZero: nonZero != 0, showPos))
						showPos = [positions[idx-2] for idx in showPos]
						ListTotal = [items for items in playerRemove if items[4] in showPos]
						ListTotal.sort(key=lambda ListTotal: ListTotal[-2], reverse=True)
				except NameError:
					ListTotal = playerRemove

				### Table showing players
				for num, items in enumerate(ListTotal):
					teamVarDict[num].set(items[0])
					pos = items[4]
					posVarDict[num].set(items[4])
					nameVarDict[num].set((items[1], items[2]))
					playerVarDict[num].set((items[2], items[1], items[3]))
					bdayVarDict[num].set("~ {}".format(curYear - items[3]))

					### show stats
					if pos == "QB":
						statsVarDict[num].set("Total Yards: {}\n".format(items[5] + items[-6]) +
										      "Total TDs: {}\n".format(items[6] + items[-5]) + 
										      "Total Turnover: {}".format(items[-6] + items[-4]))

					elif pos == "RB":
						statsVarDict[num].set("Receptions: {}\n".format(items[-6]) + 
											  "Total Yards: {}\n".format(items[-5] + items[5]) +
											  "Total TDs: {}".format(items[-4] + items[6]))  

					elif pos == "WR" or pos == "TE":
						statsVarDict[num].set("Receptions: {}\n".format(items[-6]) +
											  "Receiving Yards: {}\n".format(items[-5]) +
											  "Receiving TDs: {}".format(items[-4]))
					fanPointsVarDict[num].set(items[-2])

					### Two year Trends
					trend = items[-1]
					### For when the two year trend is N/A
					if isinstance(items[-1], str) == False:
						if trend >= 10:	bgColor = "green"
						elif trend <= -10: bgColor = "red"
						else: bgColor = "grey"
					else:
						bgColor = "grey"
					trendVarDict[num].set(items[-1])
					twoTrend[num].config(bg=bgColor)
#					bgColorVarDict[num].set(bgColor)

					### pick button
					if mockRunning == True:
						pickVarDict[num] = "yes"
						allStatsVarDict[num].set(items)
						draftOrderVarDict[num].set(teamOrder)
					else:
						pickVarDict[num] = "no"

					### Break at a pick number of players
					if num == numPlayersTable-1:
						break
				return
			make_table()

			### submits buttons to update tables based off positions picked, only need to run it once.
			if player == None:
				subButton = ttk.Button(self, text = "Submit", command = make_table)
				subButton.grid(row = 1, column = num_col[0]+5, sticky = "nswe")
#####################################################################################################################################
		def start_mock(startMock):
			"""Starts a mock draft"""

			### Setting up global varibles
			nonlocal mockRunning

			def view_team(event, whatPlayer=teamName):
				### Allowing players to view a team
				playersTeams[whatPlayer].delete(0, "end")
				[items.grid_forget() for items in self.grid_slaves() if int(items.grid_info()["row"]) ==2 and int(items.grid_info()["column"]) ==15]
				for num, items in enumerate(teamPlayers[whatPlayer]):
					playersTeams[whatPlayer].insert(num, items[:3])
					playersTeams[whatPlayer].bind('<Double-1>', lambda event,tmp=whatPlayer:get_stats_mock(event, "playerPicked", None, None, tmp))
				playersTeams[whatPlayer].grid(row = 2, column = 15, rowspan = 18, sticky = "nwes")
				return

			### Allowing used to view what team they want
			playersPickD.bind('<<ComboboxSelected>>', lambda event: view_team(event, playersPickD.get()))	
			if mockRunning == False or userNext == True:
				view_team(None, playersPickD.get())
			if startMock == "yes":

				if mockRunning == True:
					pop_up_msg("Mock draft is already running...")
					return
			
				### Changes start mock button to "reset mock"
				mockButton = tk.Button(self, text = "Reset Mock Draft", font = ("Times", "12", "bold"), command = mock_resetter, bg="red")
				mockButton.grid(row = num_row[0], column = num_col[0], columnspan = 5, ipady = 5, sticky = "nesw")
				tipStr="Not live yet...\nBut will offer tips based off who has been drafted (and by who) and who is left."
				tipButton =tk.Button(self,text="Draft Tip",font=("Times","12","bold"),command=lambda:pop_up_msg(tipStr,"Coming Soon..."), bg="green")
				tipButton.grid(row = num_row[0], column = 10, columnspan = 5, ipady = 5, sticky = "nesw")

				### Allows for resetter of mock
				nonlocal numMockDraft
				if numMockDraft == 0:
					numMockDraft += 1

				draftIdx = [num for num in range(numTeams)]
				shuffle(draftIdx)
				global teamOrder
				teamOrder = [teamNames[idx] for idx in draftIdx]
				draftOrderBox.delete(0, "end")
				for num, items in enumerate(teamOrder):
					draftOrderBox.insert(num, items)

				### Starting mock
				mockRunning = True
				make_table()

			### Running mock draft
			if mockRunning == True:
				### Indexing the whoPicked correctly via a snake draft
				nonlocal mockCount, idxCount, roundIdx
				mockCount += 1

				if roundIdx % 2 != 0 and mockCount/roundIdx != numTeams:
					idxCount += 1
				elif mockCount/roundIdx == numTeams:
					roundIdx += 1
				else:
					idxCount -= 1

				nonlocal whoPicked
				whoPicked = teamOrder[idxCount]

				### display who on the clock.	
				tmpStr = "{} is on the clock for pick number {}".format(whoPicked, roundIdx),	
				onClockL = tk.Label(self, text = tmpStr[0], font=large_font, relief="sunken", bg="green", fg="white")
				onClockL.grid(row = 21, column = 0, columnspan = len(labels)*2-1, sticky = "nwes")

				if whoPicked == teamName:
					return	

				### Picking player for computer players
				pick = sim_mock(playerRemove, teamPlayers, whoPicked)
				pickPlayer(pick, whoPicked, teamOrder)
			return

		### Finishing mock draft
		if mockCount == numRounds*numTeams-1:
			player_left_list() ### Updating playersleft list at end of mock
			mockRunning = False
			start_mock("no")   ### Updating players picked table list at end of mock
			try: make_table()       ### Update table, so the pick button won't let you pick
			except UnboundLocalError: pass
			mock_results(teamPlayers, teamName, posNums, tk, ttk)
		else:
			start_mock("no")
		return

#####################################################################################################################################
	### Setting up varibles, for mock table
	teamVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	posVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	nameVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	playerVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	bdayVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	statsVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	fanPointsVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	trendVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	bgColorVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	pickVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	allStatsVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}
	draftOrderVarDict = {num : tk.StringVar(self) for num in range(numPlayersTable)}

	### Setting up varibles, for player count
	playerCountDict = {num2:{num:tk.StringVar(self) for num in range(3)} for num2 in range(2)}
	allPlayerCountDict = {items : {num2:{num:tk.StringVar(self) for num in range(3)} for num2 in range(2)} for items in teamNames}
	for key in allPlayerCountDict.keys():
		allPlayerCountDict[key]
		allPlayerCountDict[key][0][0].set("QB Count: 0")
		allPlayerCountDict[key][0][1].set("RB Count: 0")
		allPlayerCountDict[key][0][2].set("WR Count: 0")
		allPlayerCountDict[key][1][0].set("TE Count: 0")
		allPlayerCountDict[key][1][1].set("DEF Count: 0")
		allPlayerCountDict[key][1][2].set("K Count: 0")
	
	### Applying colors to the player counter
	bgColorDict = {items : {num2:{num:tk.StringVar(self) for num in range(3)} for num2 in range(2)} for items in teamNames}
	[bgColorDict[key][key1][key2].set("red") for key in bgColorDict.keys() for key1 in bgColorDict[key].keys() 
											 for key2 in bgColorDict[key][key1].keys()]

	### Allow the pick button change based off mock running or not
	def for_pick_button(isMockRunning, pickNum):

		if isMockRunning == "yes":
			playersStats = [items.strip() for items in allStatsVarDict[pickNum].get().split(",")]

			### Pulling information from one long string...
			player = []
			for num, items in enumerate(playersStats):
				if num > 4 or num == 3:
					if items.isdigit():
						player.append(int(items))

					### For two year trend
					elif num == len(playersStats)-1:
						try:
							player.append(float(items[:-1]))
						except ValueError:
							player.append(items[1:-2])

					else:
						player.append(float(items))
					continue
				else:
					if num == 0:
						player.append(items[2:-1])
					else:
						player.append(items[1:-1])

			### Getting draft order
			tmpDraftOrder = [items.strip() for items in draftOrderVarDict[pickNum].get().split(",")]
			teamOrder = []
			for num, items in enumerate(tmpDraftOrder):
				if num == 0:
					teamOrder.append(items[2:-1])
				elif num == len(tmpDraftOrder)-1:
					teamOrder.append(items[1:-2])
				else:
					teamOrder.append(items[1:-1])
			pickPlayer(player, teamName, teamOrder)

		elif isMockRunning == "no":
			pop_up_msg("A mock draft has not been started...")
		return


	### Making table to pick someone
	twoTrend = []
	for num in range(numPlayersTable):
		### Because the first index of the ListTotal is the team's name
		tmpL = tk.Label(self, textvariable = teamVarDict[num], font = large_font, relief = "sunken", bg = "grey", fg = "white")
		tmpL.grid(row = num_row[0]+2+num, column = num_col[0], columnspan = 2, sticky = "nwes")

		### Creating a pushable button for people to view the players stats
		tmpL = tk.Button(self, textvariable = nameVarDict[num],font=large_font,relief="sunken",bg="grey",
			fg="white",command=lambda pos=posVarDict[num], player=playerVarDict[num]: mock_pop_up(pos, player,players_stats,bio_and_combine,tk,ttk))
		tmpL.grid(row = num_row[0]+2+num, column = num_col[0]+2, columnspan = 2, sticky = "nwes")

		### Age
		tmpL = tk.Label(self, textvariable = bdayVarDict[num], font=large_font, relief="sunken", bg="grey", fg="white")
		tmpL.grid(row = num_row[0]+2+num, column = num_col[0]+4, sticky = "nwes")

		## Position
		tmpL = tk.Label(self, textvariable = posVarDict[num], font = large_font, relief = "sunken", bg = "grey", fg = "white")
		tmpL.grid(row = num_row[0]+2+num, column = num_col[0]+5, sticky = "nwes")

		### show stats
		tmpL=tk.Label(self,textvariable=statsVarDict[num],font=("Helvetica",10),relief="sunken",bg="grey",fg="white",justify="left", anchor="w")
		tmpL.grid(row = num_row[0]+2+num, column = num_col[0]+6, sticky = "nwes")

		### Fantasy points
		tmpL = tk.Label(self, textvariable = fanPointsVarDict[num], font = large_font, relief = "sunken", bg = "grey", fg = "white")
		tmpL.grid(row = num_row[0]+2+num, column = num_col[0]+7, sticky = "nwes")

		### Two year Trends
		twoTrend.append(tk.Label(self, textvariable = trendVarDict[num], font = large_font, relief="sunken", bg="grey", fg="white"))
		twoTrend[num].grid(row = num_row[0]+2+num, column = num_col[0]+8, sticky = "nwes")

		### pick button
		pickButton = ttk.Button(self, text = "Pick", command = lambda num=num: for_pick_button(pickVarDict[num], num))
		pickButton.grid(row = num_row[0]+2+num, column = num_col[0]+9, sticky = "nwes")
	pickPlayer()

#####################################################################################################################################
	### Making player count table
	storeLabel = {num2:{num:None for num in range(3)} for num2 in range(2)}
	for num2 in range(2):
		for num in range(3):
			countL = tk.Label(self,textvariable=playerCountDict[num2][num],font=lFont,relief="sunken",bg="grey",fg="white")
			countL.grid(row = 21+num2, column = len(labels)*2-1+num, ipady = 5, sticky = "nwes")
			storeLabel[num2][num] = countL

	### Changer counter based on player selected
	def player_counter(e, tmpTeam):
		for num2 in range(2):
			for num in range(3):
				playerCountDict[num2][num].set(allPlayerCountDict[tmpTeam][num2][num].get())
				storeLabel[num2][num].config(background=bgColorDict[tmpTeam][num2][num].get())
		return
	player_counter(None, teamName)

	### Creating combo box for count
	countL = ttk.Combobox(self, values = teamNames, state="readonly")
	countL.set(teamName)
	countL.grid(row = 20, column = len(labels)*2-1, columnspan = 3, ipady = 5, sticky = "nwes")
	countL.bind("<<ComboboxSelected>>", lambda e: player_counter(e, countL.get()))

#####################################################################################################################################
	def mock_search_all():
		"""Creating a pop up for someone to search all players for the mock draft."""

		### Creating pop up for search all of the mock draft
		searchAll = tk.Tk()
		searchAll.wm_title("Select a Player")
		num_row = (0, 20)
		num_col = (0, 20)

		### Creating Labels
		tk.Label(searchAll, text="Quarterbacks", relief="groove").grid(row=num_row[0]+1,column=num_col[0],ipadx=10,sticky="nesw")
		tk.Label(searchAll, text="Running Backs", relief="groove").grid(row=num_row[0]+1,column=num_col[0]+1,sticky="nesw")
		tk.Label(searchAll, text="Wide Receivers", relief="groove").grid(row=num_row[0]+1,column=num_col[0]+2,sticky="nesw")
		tk.Label(searchAll, text="Tight Ends", relief="groove").grid(row=num_row[0]+1,column=num_col[0]+3,sticky="nesw")

		### QB table
		qb_listBox = tk.Listbox(searchAll)
		qbs = [items for items in posRemove["QB"]]
		[qb_listBox.insert(num, (items[4], items[1], items[2])) for num, items in enumerate(qbs)]
		qb_listBox.grid(row = num_row[0]+2, column = num_col[0], sticky = "nwes")

		### RB table
		rb_listBox = tk.Listbox(searchAll)
		rbs = [items for items in posRemove["RB"]]
		[rb_listBox.insert(num, (items[4], items[1], items[2])) for num, items in enumerate(rbs)]
		rb_listBox.grid(row = num_row[0]+2, column = num_col[0]+1, sticky = "nwes")

		### WR table
		wr_listBox = tk.Listbox(searchAll)
		wrs = [items for items in posRemove["WR"]]
		[wr_listBox.insert(num, (items[4], items[1], items[2])) for num, items in enumerate(wrs)]
		wr_listBox.grid(row = num_row[0]+2, column = num_col[0]+2, sticky = "nwes")

		### TE table
		te_listBox = tk.Listbox(searchAll)
		tes = [items for items in posRemove["TE"]]
		[te_listBox.insert(num, (items[4], items[1], items[2])) for num, items in enumerate(tes)]
		te_listBox.grid(row = num_row[0]+2, column = num_col[0]+3, sticky = "nwes")

		### Allowing users to view stats of each player
		def getStats(event, pos, bio_and_combine):
			"""Gets stats to pass through the pop up stats functions"""

			if pos == "QB":
				clicked = qbs[int(qb_listBox.curselection()[0])]
				playersStats = [player for player in players_stats[pos] if clicked[0] and  clicked[1] in player if clicked[3] == player[2]]
				comb_results = [player for player in bio_and_combine[pos] if clicked[0] and  clicked[1] in player if clicked[3] in player]

			elif pos == "RB":	
				clicked = rbs[int(rb_listBox.curselection()[0])]
				playersStats = [player for player in players_stats[pos] if clicked[0] and  clicked[1] in player if clicked[3] == player[2]]
				comb_results = [player for player in bio_and_combine[pos] if clicked[0] and  clicked[1] in player if clicked[3] in player]

			elif pos == "WR":
				clicked = wrs[int(wr_listBox.curselection()[0])]
				playersStats = [player for player in players_stats[pos] if clicked[0] and  clicked[1] in player if clicked[3] == player[2]]
				comb_results = [player for player in bio_and_combine[pos] if clicked[0] and  clicked[1] in player if clicked[3] in player]

			else: ## Must be TE
				clicked = tes[int(te_listBox.curselection()[0])]
				playersStats = [player for player in players_stats[pos] if clicked[0] and  clicked[1] in player if clicked[3] == player[2]]
				comb_results = [player for player in bio_and_combine[pos] if clicked[0] and  clicked[1] in player if clicked[3] in player]
			stats_pop_up(pos, playersStats, comb_results, tk, ttk)
			return

		### Listens for an event, doulbe click, to happen on the list box
		qb_listBox.bind('<Double-1>', lambda event: getStats(event, 'QB', bio_and_combine))
		rb_listBox.bind('<Double-1>', lambda event: getStats(event, 'RB', bio_and_combine))
		wr_listBox.bind('<Double-1>', lambda event: getStats(event, 'WR', bio_and_combine))
		te_listBox.bind('<Double-1>', lambda event: getStats(event, 'TE', bio_and_combine))

		### If mock is not running, no need to search all
		tk.Label(searchAll, text="Draft:", relief="groove").grid(row=num_row[0],column=num_col[0],ipadx=10,sticky="nesw")

		### Update a pick label, so the user now you they are drafting.
		def updatePick(e, pos):
			global globalPick
			try:
				if pos == "QB":
					globalPick = qbs[int(qb_listBox.curselection()[0])]
					tmpPick = (globalPick[0].split(" ")[-1].strip(), ":", globalPick[4], globalPick[1], globalPick[2])
				elif pos == "RB":
					globalPick = rbs[int(rb_listBox.curselection()[0])]
					tmpPick = (globalPick[0].split(" ")[-1].strip(), ":", globalPick[4], globalPick[1], globalPick[2])
				elif pos == "WR":
					globalPick = wrs[int(wr_listBox.curselection()[0])]
					tmpPick = (globalPick[0].split(" ")[-1].strip(), ":", globalPick[4], globalPick[1], globalPick[2])
				elif pos == "TE":
					globalPick = tes[int(te_listBox.curselection()[0])]
					tmpPick = (globalPick[0].split(" ")[-1].strip(), ":", globalPick[4], globalPick[1], globalPick[2])
				else: 
					globalPick = None
					tmpPick = "Select a Player"
			except (IndexError, TypeError):
				pop_up_msg("Right clicking must take place in the box where the player is selected.")

			tk.Label(searchAll, text=tmpPick,relief="sunken",bg="white"
													).grid(row=num_row[0],column=num_col[0]+1,columnspan=3,ipadx=10,sticky="nesw")
			return
		updatePick(None, None)

		### Listens for an event, enter click, to happen on the list box
		qb_listBox.bind('<Return>', lambda event: updatePick(event, 'QB'))
		rb_listBox.bind('<Return>', lambda event: updatePick(event, 'RB'))
		wr_listBox.bind('<Return>', lambda event: updatePick(event, 'WR'))
		te_listBox.bind('<Return>', lambda event: updatePick(event, 'TE'))

		qb_listBox.bind('<Button-3>', lambda event: updatePick(event, 'QB'))
		rb_listBox.bind('<Button-3>', lambda event: updatePick(event, 'RB'))
		wr_listBox.bind('<Button-3>', lambda event: updatePick(event, 'WR'))
		te_listBox.bind('<Button-3>', lambda event: updatePick(event, 'TE'))

		### Allows for drafting a player
		def draft_player():
			"""Draft the player for the user from search all. And exits from the search all menu."""

			### Ensure the mock is running... and ensures a player was selected...
			if mockRunning == False:
				pop_up_msg("A mock draft has not been started...")
				return
			elif globalPick == None:
				pop_up_msg("Select a Player")
				return

			searchAll.destroy()
			pickPlayer(globalPick, teamName, teamOrder)
			return

		### Finishing pop up for search all players
		tk.Button(searchAll, text="Pick", command = draft_player).grid(row = num_row[0]+3, column = num_col[0]+2,sticky="news")
		tk.Button(searchAll, text="Exit", command = searchAll.destroy).grid(row = num_row[0]+3, column = num_col[0]+3,sticky="news")
		searchAll.mainloop()
		return

#####################################################################################################################################
	### Search all button:
	searchAllL = ttk.Button(self, text = "Search All Players", command = mock_search_all)
	searchAllL.grid(row = 20, column = 0, columnspan = len(labels)*2-1, ipady = 5, sticky = "nwes")

	### Creating checkbox variables so they can check position(s) they want to view
	allVar = tk.IntVar(self)
	qbVar = tk.IntVar(self)
	rbVar = tk.IntVar(self)
	wrVar = tk.IntVar(self)
	teVar = tk.IntVar(self)

	### Creating checkbox so they can check position(s) they want to view
	selLabel = tk.Label(self, text = "Select Position(s) To View:", font = large_font, relief = "sunken", bg = "grey", fg = "white")
	selLabel.grid(row =0, column = num_col[0], columnspan = 3, sticky = "nwes")
	allCB = tk.Checkbutton(self, text = "All Players", variable = allVar, onvalue = 1).grid(row = 1, column = num_col[0], sticky = "nwes")
	qbCB = tk.Checkbutton(self, text = "QB's", variable = qbVar, onvalue = 2).grid(row = 1, column = num_col[0]+1, sticky = "nwes")
	rbCB = tk.Checkbutton(self, text = "RB's", variable = rbVar, onvalue = 3).grid(row = 1, column = num_col[0]+2, sticky = "nwes")
	wrCB = tk.Checkbutton(self, text = "WR's", variable = wrVar, onvalue = 4).grid(row = 1, column = num_col[0]+3, sticky = "nwes")
	teCB = tk.Checkbutton(self, text = "TE's", variable = teVar, onvalue = 5).grid(row = 1, column = num_col[0]+4, sticky = "nwes")
	return

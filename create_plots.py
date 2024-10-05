import tkinter as tk
from tkinter import ttk  ### Kind of like the CSS for tkinter
import matplotlib.pyplot as plt ### Needed to have plot expand to size of the gui's window
from matplotlib import style
import matplotlib.ticker as ticker
from help_options import pop_up_msg

from mockFun import updateMockPara
### Importing saved mock draft parameters
mockParas = updateMockPara()

### fantasypoints
passYards = mockParas[0]  		### 1 point per 25 yards
passTDs = mockParas[1] 	 		### 4 points per passing touchdown
picks = mockParas[2]				### -2 points for each picked pass
fumble = mockParas[3]			### -2 points for fumble lost
recYards = mockParas[4]   		### 1 point per 10 yards
recTDs = mockParas[5]  			### 6 points per receiving TDs
rec = mockParas[6]				### 1 point per reception
rushYards = mockParas[7]			### 1 point per 10 yards
rushTDs = mockParas[8]	 		### 6 points per rushing TDs

### Creating default fonts
large_font = ("Helvetica", 12)
norm_font = ("Helvetica", 10)
small_font = ("Helvetica", 8)

### Style for plots
style.use("ggplot")

### figsize (width, height)
f = plt.figure(figsize = (10,6))

def plotting(players_stats, players, showWhat = "fantasy"):
	"""Creates the plots for the GUIs. Takes in names, up to 4, and plots them."""
	def cal_fantasy(items, pos):
		"""Calculates fantasy points for the players"""

		### getting fantasy points for QBs
		if pos == "QB":
			pYards = items[10]*passYards
			pTDs = items[11]*passTDs
			numPicks = items[12]*picks
			numFumble = items[-1]*fumble
			rYards = items[-3]*rushYards
			rTDs = items[-2]*rushTDs
			fanPoints = pYards + pTDs + numPicks + numFumble + rYards + rTDs

			try: 
				fanPointsGame =  fanPoints/items[6] ### Games played in stored in the 6 spot in database
			except ZeroDivisionError: 
				fanPointsGame = 0  ### If they played didn't play, they got 0 points per game.

		### getting fantasy points for RBs
		if pos == "RB":
			numFumble = items[11]*fumble
			rYards = items[9]*rushYards
			rTDs = items[10]*rushTDs

			reYards = items[-2]*recYards
			reTDs = items[-1]*recTDs
			catch = items[-3]*rec
			fanPoints = numFumble + rYards + rTDs + reYards + reTDs + catch

			try: 
				fanPointsGame =  fanPoints/items[6] ### Games played in stored in the 6 spot in database
			except ZeroDivisionError: 
				fanPointsGame = 0  ### If they played didn't play, they got 0 points per game

		### getting fantasy points for WRs and TE's
		if pos == "WR" or pos == "TE":
			rYards = items[-2]*recYards
			rTDs = items[-1]*recTDs
			catch = items[-3]*rec
			fanPoints = rYards + rTDs + catch

			try: 
				fanPointsGame =  fanPoints/items[6] ### Games played in stored in the 6 spot in database
			except ZeroDivisionError: 
				fanPointsGame = 0  ### If they played didn't play, they got 0 points per game
		
		return fanPoints, fanPointsGame

	### Creating the plots
	a = plt.subplot2grid((10,13),(0,0), rowspan = 6, colspan = 6)
	a2 = plt.subplot2grid((10,13),(0,7), rowspan = 6, colspan = 6)
	a3 = plt.subplot2grid((10,13),(7,0), rowspan = 5, colspan = 13)

	### Getting stats of all players
	allStats = {}
	for key in players.keys():
		tmpVar = players[key]
		tmpList = [item for item in players_stats[tmpVar[3]] if item[0] == tmpVar[1] if item[1] == tmpVar[0] if item[2] == tmpVar[2]]
		if tmpList[0][3] == 0:
			pop_up_msg("{} {} has no stats...".format(tmpList[0][1], tmpList[0][0]))
			return
		allStats.update({tmpVar[3] + " " + key : tmpList})

	if showWhat == "fantasy":
		### Stats to plot
		yearsPlayed = {}
		fantasyStatsDic = {}
		fantasyStatsPerGameDic = {}
		gamesPlayedDic = {}
		for key in allStats.keys():
			tmpVar = allStats[key]
			years = [years[3] for years in tmpVar] 
			fantasyStats = [cal_fantasy(items, key[:2]) for items in tmpVar]
			gamesPlayed = [items[6] for items in tmpVar]   ### Games played in stored in the 6 spot in database

			### Including first and last name in the key for plotting legend
			tmpKey = key + " " + str(tmpVar[0][1]) + " " + str(tmpVar[0][0])
			yearsPlayed.update({tmpKey : years})  
			fantasyStatsDic.update({tmpKey : [items[0] for items in fantasyStats]})
			fantasyStatsPerGameDic.update({tmpKey : [items[1] for items in fantasyStats]})
			gamesPlayedDic.update({tmpKey : gamesPlayed})

	### Plotting
	a.clear()   ### Clears out hold plot
	numColor = 0;
	for key in fantasyStatsDic:
		tmpKey = key.split(" ")
		tmpLabel = tmpKey[-2] + " " + tmpKey[-1]
		if numColor == 0: color = "red"
		elif numColor == 1: color = "green"
		elif numColor == 2: color = "magenta"
		elif numColor == 3: color = "blue"
		a.plot(yearsPlayed[key], fantasyStatsDic[key], c = color, linewidth = 1)
		a2.plot(yearsPlayed[key], fantasyStatsPerGameDic[key], c = color, linewidth = 1)
		a3.plot(yearsPlayed[key], gamesPlayedDic[key], c = color, linewidth = 1, label = tmpLabel)
		numColor += 1

	if showWhat == "fantasy":
		### Creating titles, done down here, because they don't all show up above.
		a.set_title("Total Fantasy Stats")
		a2.set_title("Fantasy Stats Per Game")
		a3.set_title("Games Played Per Year")


	### Setting axis'
	a.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
	a2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
	a3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
	
	### Ensuring all x axis are int only
	a.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
	a2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
	a3.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
	
	### Adding legend and drawing to canvas
	a3.legend(bbox_to_anchor=(0,-.43), loc=3, ncol=4, borderaxespad = 0)
	f.canvas.draw()
	return


#####################################################################################################################################
class playersDropDown:
	def __init__(self, selPlayers, numRow, numCol, values, whatPlayer):
		self.frame = selPlayers
		self.label = tk.Label(self.frame, text = "Select a " + whatPlayer, font = norm_font, relief = "groove", anchor = "center", bg = "white")
		self.label.grid(row = numRow-4, column = numCol, columnspan = 4, sticky = "nswe", padx = 5, ipadx = 10, ipady = 5)
		self.combo = ttk.Combobox(self.frame, values = values, state = "readonly")
		self.combo.grid(row = numRow, column = numCol, columnspan = 4, sticky = "nswe", padx = 5, ipadx = 40)

def selPlayersFun(self, players_stats, bio_and_combine, currentRos, dicTotal, num_row, num_col):
	"""Creates a pop up for the user select up to four players for plotting."""

	### Creaiting radio buttons
	posVar0 = tk.IntVar(self)
	tk.Radiobutton(self, text = "QB", variable = posVar0, value = 1).grid(row = num_row[0]+2, column = num_col[0])
	tk.Radiobutton(self, text = "RB", variable = posVar0, value = 2).grid(row = num_row[0]+2, column = num_col[0]+1)
	tk.Radiobutton(self, text = "WR", variable = posVar0, value = 3).grid(row = num_row[0]+2, column = num_col[0]+2)
	tk.Radiobutton(self, text = "TE", variable = posVar0, value = 4).grid(row = num_row[0]+2, column = num_col[0]+3)

	posVar1 = tk.IntVar(self)
	tk.Radiobutton(self, text = "QB", variable = posVar1, value = 1).grid(row = num_row[0]+8, column = num_col[0])
	tk.Radiobutton(self, text = "RB", variable = posVar1, value = 2).grid(row = num_row[0]+8, column = num_col[0]+1)
	tk.Radiobutton(self, text = "WR", variable = posVar1, value = 3).grid(row = num_row[0]+8, column = num_col[0]+2)
	tk.Radiobutton(self, text = "TE", variable = posVar1, value = 4).grid(row = num_row[0]+8, column = num_col[0]+3)

	posVar2 = tk.IntVar(self)
	tk.Radiobutton(self, text = "QB", variable = posVar2, value = 1).grid(row = num_row[0]+14, column = num_col[0])
	tk.Radiobutton(self, text = "RB", variable = posVar2, value = 2).grid(row = num_row[0]+14, column = num_col[0]+1)
	tk.Radiobutton(self, text = "WR", variable = posVar2, value = 3).grid(row = num_row[0]+14, column = num_col[0]+2)
	tk.Radiobutton(self, text = "TE", variable = posVar2, value = 4).grid(row = num_row[0]+14, column = num_col[0]+3)

	posVar3 = tk.IntVar(self)
	tk.Radiobutton(self, text = "QB", variable = posVar3, value = 1).grid(row = num_row[0]+20, column = num_col[0])
	tk.Radiobutton(self, text = "RB", variable = posVar3, value = 2).grid(row = num_row[0]+20, column = num_col[0]+1)
	tk.Radiobutton(self, text = "WR", variable = posVar3, value = 3).grid(row = num_row[0]+20, column = num_col[0]+2)
	tk.Radiobutton(self, text = "TE", variable = posVar3, value = 4).grid(row = num_row[0]+20, column = num_col[0]+3)

	def pickPlayers(orderBy, radButtonPushed = False, startUp = None):
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
		qbList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in qbList]
		qbList.sort(key=lambda qbList: qbList[numOrder], reverse=revOrder) 	   ### Sorting by last name
		rbList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in rbList]
		rbList.sort(key=lambda rbList: rbList[numOrder], reverse=revOrder) 	   ### Sorting by last name
		wrList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in wrList]
		wrList.sort(key=lambda wrList: wrList[numOrder], reverse=revOrder) 	   ### Sorting by last name
		teList = [[items[0][0], items[0][1], "Birthday Year: " + str(items[0][2]), items[1]] for items in teList]
		teList.sort(key=lambda teList: teList[numOrder], reverse=revOrder) 	   ### Sorting by last name
		
		global playerDropDown0, playerDropDown1, playerDropDown2, playerDropDown3

		### Creating lists for the drop down menus and the menus
		if radButtonPushed == "radBut0" or startUp == "makeDropDowns":
			if posVar0.get() == 2: dropList0 = [items[:3] for items in rbList[:]]
			elif posVar0.get() == 3: dropList0 = [items[:3] for items in wrList[:]]
			elif posVar0.get() == 4: dropList0 = [items[:3] for items in teList[:]]
			else: dropList0 = [items[:3] for items in qbList[:]]
			playerDropDown0 = playersDropDown(self, num_row[0]+5, num_col[0], dropList0, "Player 1:")

		if radButtonPushed == "radBut1" or startUp == "makeDropDowns":
			if posVar1.get() == 2: dropList1 = [items[:3] for items in rbList[:]]
			elif posVar1.get() == 3: dropList1 = [items[:3] for items in wrList[:]]
			elif posVar1.get() == 4: dropList1 = [items[:3] for items in teList[:]]
			else: dropList1 = [items[:3] for items in qbList[:]]
			playerDropDown1 = playersDropDown(self, num_row[0]+11, num_col[0], dropList1, "Player 2:")

		if radButtonPushed == "radBut2" or startUp == "makeDropDowns":
			if posVar2.get() == 2: dropList2 = [items[:3] for items in rbList[:]]
			elif posVar2.get() == 3: dropList2 = [items[:3] for items in wrList[:]]
			elif posVar2.get() == 4: dropList2 = [items[:3] for items in teList[:]]
			else: dropList2 = [items[:3] for items in qbList[:]]
			playerDropDown2 = playersDropDown(self, num_row[0]+17, num_col[0], dropList2, "Player 3:")

		if radButtonPushed == "radBut3" or startUp == "makeDropDowns":
			if posVar3.get() == 2: dropList3 = [items[:3] for items in rbList[:]]
			elif posVar3.get() == 3: dropList3 = [items[:3] for items in wrList[:]]
			elif posVar3.get() == 4: dropList3 = [items[:3] for items in teList[:]]
			else: dropList3 = [items[:3] for items in qbList[:]]
			playerDropDown3 = playersDropDown(self, num_row[0]+23, num_col[0], dropList3, "Player 4:")

		def getInfo(whatInfo = "fan"):
			"""Collects stats to send to the plotting function above."""
		
			### Esuring at last one player is picked
			if playerDropDown0.combo.get() == "" and playerDropDown1.combo.get() == "":
				if playerDropDown2.combo.get() == "" and playerDropDown3.combo.get() == "":
					pop_up_msg("So you want to plot nothing? Why? Try again...", "Maybe pick something to plot?")
					return

			### Getting info to send to the plotting function
			playersDic = {}
			for num in range(4):
				if num == 0: playerVar = playerDropDown0.combo.get(); posVar = posVar0.get()
				elif num == 1: playerVar = playerDropDown1.combo.get(); posVar = posVar1.get()
				elif num == 2: playerVar = playerDropDown2.combo.get(); posVar = posVar2.get()
				elif num == 3: playerVar = playerDropDown3.combo.get(); posVar = posVar3.get()

				if playerVar != "":
					Player = playerVar.split(" "); 
					BDYear = ''.join([items for items in Player[-1] if items.isdigit()]);
					BDYear = int(BDYear.strip())

					if posVar == 1 or posVar == 0: pos = "QB"
					elif posVar == 2: pos = "RB"
					elif posVar == 3: pos = "WR"
					elif posVar == 4: pos = "TE"
					Player = [Player[0], Player[1], BDYear, pos]
					tempDic = { "Player {}".format(num) : Player}
					playersDic.update(tempDic)
				else: 
					continue

			plotting(players_stats, playersDic)
			return

		### Only create button on start up else you get a name error
		ttk.Button(self, text="Update Plots", command = getInfo).grid(row=num_row[0]+25,column=num_col[0],columnspan =4, sticky = "nesw")
		return
	pickPlayers("fanStats", None, "makeDropDowns")

	### creating buttons for sorting lists
	for num in range(4):
		tmpButton = "radBut" + str(num)
		tmp = ttk.Button(self, text = "Order by First Name", command = lambda tmpButton = tmpButton: pickPlayers("fName", tmpButton))
		tmp.grid(row = num_row[0]+3+num*6, column = num_col[0], columnspan = 2, sticky = "nswe")
		tmp = ttk.Button(self, text = "Order by Last Name", command = lambda tmpButton = tmpButton: pickPlayers("lName", tmpButton))
		tmp.grid(row = num_row[0]+3+num*6, column = num_col[0]+2, columnspan = 2, sticky = "nswe")
		tmp = ttk.Button(self, text = "Order by Last Year's Fantasy points", command=lambda tmpButton=tmpButton: pickPlayers("fanStats", tmpButton))
		tmp.grid(row = num_row[0]+4+num*6, column = num_col[0], columnspan = 4, sticky = "nswe")

		### Creating gap between two sides
		nothing = tk.LabelFrame(self)
		nothing.grid(row = num_row[0]+6+num*6, column = num_col[0], columnspan = 4, sticky = "nesw", pady = 5)

		### Creating a clear names button
		ttk.Button(self, text="Clear Names", command = lambda: selPlayersFun(self, players_stats, bio_and_combine, currentRos, 
						 dicTotal, num_row, num_col)).grid(row=num_row[0]+26,column=num_col[0],columnspan=4, sticky = "nesw")	
	return





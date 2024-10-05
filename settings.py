import tkinter as tk
from tkinter import ttk  ### Kind of like the CSS for tkinter
from help_options import pop_up_msg

large_font = ("Helvetica", 12)
norm_font = ("Verdana", 10)
small_font = ("Verdana", 8)

### Getting saved mock parameters
from data_open import saved_mock_data
saved_mock = saved_mock_data()

### Default Values, yes I know globals are bad and getter/setters should be used
number_teams = saved_mock[0][0]
number_teams_default = (number_teams,)  ### Allows me to reset number of teams when needed, do to global setting
team_name = saved_mock[0][1]
team_name_deafult = team_name
####
pass_yards = saved_mock[0][2]    		### 1 point per 25 yards
pass_tds = saved_mock[0][3] 	 		### 4 points per passing touchdown
pass_picks = saved_mock[0][4]			### -2 points for each picked pass
fumble = saved_mock[0][5]				### -2 points for fumble lost
rec_yards = saved_mock[0][6]   			### 1 point per 10 yards
rec_tds = saved_mock[0][7]  			### 6 points per receiving TDs
rec_catches = saved_mock[0][8]			### 1 point per reception
rush_yards = saved_mock[0][9]			### 1 point per 10 yards
rush_tds = saved_mock[0][10]	 		### 6 points per rushing TDs


### Defense needs to be added



### For creating table with for loop
names = ['Number of Teams','Team Name', 'Passing Yards', 'Passing Touchdowns', 'Interceptions', 'Fumbles', 'Receiving Yards']
names.extend(['Receiving Touchdowns', 'Reception', 'Rushing Yards', 'Rushing Touchdowns',])
#global values
values = [number_teams, team_name, pass_yards, pass_tds, pass_picks, fumble, rec_yards, rec_tds, rec_catches, rush_yards, rush_tds]

### Class for creating entries
class plot_mock_settings:
	def __init__(self, frame, string, btnCommand, entryVar, tk, ttk):
		### Creates an entry for number of teams
		self.lab = tk.Label(frame, text = string, justify = "center", relief = "groove", bg = "white")
		self.ent = ttk.Entry(frame)
		self.ent.insert(0, entryVar)   ### Inserting 10 at default value
		self.btn = ttk.Button(frame, text = "Submit", command = btnCommand)
		self.tmpLabel = tk.Label(frame)
		return

#####################################################################################################################################
def place_objects(mock_pop_up, whatObject, rowNum, colNum, first = False):
	### Removing old grid
	if first == True:
		for items in mock_pop_up.grid_slaves():
			if 30 > int(items.grid_info()["row"]) >  1:
				if int(items.grid_info()["column"]) < 5:
					items.grid_forget()

	### Regridding the wanted entry boxes
	whatObject.lab.grid(row = rowNum+1, column = colNum, columnspan = 4, sticky = "nesw", padx = 5, pady = 5)
	whatObject.ent.grid(row = rowNum+2, column = colNum, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)
	whatObject.btn.grid(row = rowNum+2, column = colNum+3, sticky = "nsw", padx = 5, pady = 5)
	return

#####################################################################################################################################
def mock_draft_settings(whatPara):
	"""Creates a pop up window for the user to enter/adjust mock draft settings."""

	### Creating instance
	mock_pop_up = tk.Tk()
	if whatPara == "plots":
		mock_pop_up.wm_title("Plot Settings")
		warnLabel = "*Same as mock draft settings"
		changeSetting  = "Change Plot Settings"
	elif whatPara == "mock":
		mock_pop_up.wm_title("Mock Draft Settings")
		warnLabel = "*Same as plot settings "
		changeSetting  = "Change settings for your mock draft."

	### Creating a container, for gridding, making it a 10 by 11 grid (really 11x12 because python starts at 0)
	num_row = (2, 30)
	num_col = (0, 13) 
	container = tk.Frame()
	container.grid_rowconfigure(0, weight = 1)
	container.grid_columnconfigure(0, weight = 1)

#####################################################################################################################################
	#### Recreates draft parameters
	def re_enter_draft_parameters(para_to_change, stats_entry = "None", default_value = "None"):
		"""Replacments the entry for either one or all the draft parameters depeding if you pick one or all as para_to_change.
		   If the first input = 'one', stats_entry and default_value must be entered to know what parameter to change and to what."""

		if para_to_change == "one":
			### Re-enter the default values due to a bad entry
			if stats_entry == "pass_yards":
				passYards.ent.delete(0, "end")
				passYards.ent.insert(0, default_value)
			elif stats_entry == "pass_tds":
				passTDs.ent.delete(0, "end")
				passTDs.ent.insert(0, default_value)
			elif stats_entry == "pass_picks":
				passPicks.ent.delete(0, "end")
				passPicks.ent.insert(0, default_value)
			elif stats_entry == "rec_yards":
				recYards.ent.delete(0, "end")
				recYardsent.ent.insert(0, default_value)
			elif stats_entry == "rec_tds":
				recTDs.ent.delete(0, "end")
				recTDs.ent.insert(0, default_value)
			elif stats_entry == "rec_catches":
				PPR.delete(0, "end")
				PPR.insert(0, default_value)
			elif stats_entry == "rush_yards":
				rushYards.ent.delete(0, "end")
				rushYards.ent.insert(0, default_value)
			elif stats_entry == "rush_tds":
				rushTDs.ent.delete(0, "end")
				rushTDs.ent.insert(0, default_value)
			elif stats_entry == "fumble_lost":
				fumbleObject.ent.delete(0, "end")
				fumbleObject.ent.insert(0, default_value)

		elif para_to_change == "all":
			### re-enter all entries due to loading default values
			### Team information
			numTeams.ent.delete(0, "end")
			numTeams.ent.insert(0, values[0])
			teamName.ent.delete(0, "end")
			teamName.ent.insert(0, values[1])

			### Passing
			passYards.ent.delete(0, "end")
			passYards.ent.insert(0, values[2])
			passTDs.ent.delete(0, "end")
			passTDs.ent.insert(0, values[3])
			passPicks.ent.delete(0, "end")
			passPicks.ent.insert(0, values[4])
			fumbleObject.ent.delete(0, "end")
			fumbleObject.ent.insert(0, values[5])

			### Receiving
			recYards.ent.delete(0, "end")
			recYards.ent.insert(0, values[6])
			recTDs.ent.delete(0, "end")
			recTDs.ent.insert(0, values[7])
			PPR.ent.delete(0, "end")
			PPR.ent.insert(0, values[8])

			### Rushing
			rushYards.ent.delete(0, "end")
			rushYards.ent.insert(0, values[9])
			rushTDs.ent.delete(0, "end")
			rushTDs.ent.insert(0, values[10])
		return

#####################################################################################################################################
	def update_side_table():
		for num, items in enumerate(values):
			### To add creating floats so the .0 is there by default, the try is because team name is a string
			if isinstance(values[num], int) or isinstance(values[num], float):
				values_label = tk.Label(mock_pop_up, text = str(float(values[num])), font = large_font, relief = "sunken")
				values_label.grid(row = num_row[0]+2+num, column = num_col[-1], sticky = "nswe", ipadx = 15, ipady = 5)
			else:
				values_label = tk.Label(mock_pop_up, text = str(values[num]), font = large_font, relief = "sunken")
				values_label.grid(row = num_row[0]+2+num, column = num_col[-1], sticky = "nswe", ipadx = 15, ipady = 5)
		return

#####################################################################################################################################
	def save_mock():
		"""Saving draft parameters."""
		### Default Fantasy Values
		from save_data_db import store_mock_parameters
		store_mock_parameters(values)
		pop_up_msg("Submitted mock draft parameters were saved.", "Mock Parameters")
		return

#####################################################################################################################################
	def load_default():
		"""Reloading default draft parameters."""
		### Default Fantasy Values
		from data_open import default_mock_data
		default_mock = default_mock_data()

		### Changing the varible values which is used for the draft parameters
		global values
		values = [list(parameters) for parameters in default_mock][0]

		### Re-enter the default values due to a bad entry
		re_enter_draft_parameters("all")

		### Need to update side table after deafaults are stored
		update_side_table()
		return

#####################################################################################################################################
	def select_num_teams():
		"""A check for number of teams select. Ensuring it's a whole number."""
		### Allowing varbiles to be changed, should use getters, and setters
		global number_teams

		try:
			number_teams = int(numTeams.ent.get())
			values[names.index('Number of Teams')] = number_teams
			if number_teams == 0 or number_teams == 1:
				number_teams = number_teams_default
				values[names.index('Number of Teams')] = number_teams
				numTeams.ent.delete(0, "end")
				numTeams.ent.insert(0, number_teams_default)
				pop_up_msg("This isn't the amount of friends you have,\nit's the number of teams you want in your mock draft.\nTry Again!")

			elif number_teams < 0:
				number_teams = number_teams_default
				values[names.index('Number of Teams')] = number_teams
				numTeams.ent.delete(0, "end")
				numTeams.ent.insert(0, number_teams_default)
				pop_up_msg("Dude, that's a negative number... try again...")

			elif 30 > number_teams > 20:
				values[names.index('Number of Teams')] = number_teams
				pop_up_msg("{} teams, That's a man's (or woman's) league...".format(number_teams))

			elif number_teams >= 30:
				string = str(numTeams.ent.get())
				number_teams = number_teams_default
				values[names.index('Number of Teams')] = number_teams
				numTeams.ent.delete(0, "end")
				numTeams.ent.insert(0, number_teams_default)
				pop_up_msg("I don't believe you,\nno way your league has {} teams...\nTry Again...(Limit is 29)".format(string))

			### Updating side table to view current Defaults	
			update_side_table()

		except ValueError:
			number_teams = number_teams_default
			numTeams.ent.delete(0, "end")
			numTeams.ent.insert(0, number_teams_default)
			pop_up_msg("Come on bro, how can number of teams not be a whole number?")
		return

#####################################################################################################################################
	def select_team_name():
		"""A check for vailding team names."""
		### Allowing varbiles to be changed, should use getters, and setters
		global team_name
		team_name = str(teamName.ent.get())
		values[names.index('Team Name')] = team_name

		if len(team_name) == 0:
			team_name = "Player 1"
			teamName.ent.delete(0, "end")
			teamName.ent.insert(0, team_name)
			values[names.index('Team Name')] = team_name
			update_side_table()
			pop_up_msg("Really, no team name???\nThat's lame, I'm going to call you Player 1.\nSee, I can be lame too.")

		elif len(team_name) > 30:
			team_name = team_name_deafult
			teamName.ent.delete(0, "end")
			teamName.ent.insert(0, team_name)
			values[names.index('Team Name')] = team_name
			update_side_table()
			pop_up_msg("You're team name is too long..... (that's what she said)\nCharacter Limit: 30")

		### Updating side table to view current Defaults	
		update_side_table()
		return

#####################################################################################################################################
	##### Break point on my eyes
	def check_points(default_value,stats_entry):
		"""A Check for number of teams select. Ensuring it's a whole number."""
		### Allowing varbiles to be changed, should use getters, and setters
		global pass_yards, pass_tds, pass_picks, fumble, rec_yards, rec_tds, rec_catches, rush_tds, rush_yards

		### Checking to ensure it's a float
		try:
			### passing
			if stats_entry == "pass_yards":
				pass_yards = float(passYards.ent.get())
				values[names.index('Passing Yards')] = pass_yards
				value_to_test = pass_yards
				string = "QB's??? Screw QB's!!\nThey get all the glory in real life.\nThey don't deserve it in fantasy too."
			elif stats_entry == "pass_tds":
				pass_tds = float(passTDs.ent.get())
				values[names.index('Passing Touchdowns')] = pass_tds
				value_to_test = pass_yards
				string = "QB's??? Screw QB's!!\nThey get all the glory in real life.\nThey don't deserve it in fantasy too."
			elif stats_entry == "pass_picks":
				pass_picks = float(passPicks.ent.get())
				values[names.index('Interceptions')] = pass_picks
				value_to_test = pass_picks

			#### receiving
			elif stats_entry == "rec_yards":
				rec_yards = float(recYards.ent.get())
				values[names.index('Receiving Touchdowns')] = rec_yards
				value_to_test = rec_yards
				string = "WR's are a bunch of prima donnas anyways, they don't deserve no stinkin points!"
			elif stats_entry == "rec_tds":
				rec_tds = float(recTDs.ent.get())
				values[names.index('Receiving Touchdowns')] = rec_tds
				value_to_test = rec_tds
				string = "WR's are a bunch of prima donnas anyways, they don't deserve no stinkin points!"
			elif stats_entry == "rec_catches":
				rec_catches = float(PPR.ent.get())
				values[names.index('Reception')] = rec_catches
				value_to_test = rec_catches

			#### rushing
			elif stats_entry == "rush_yards":
				rush_yards = float(rushYards.ent.get())
				values[names.index('Rushing Yards')] = rush_yards
				value_to_test = rush_yards
				string = "How are RB's still a part of the NFL, am I right???"
				string2 = "That many points for rushing yards?\nWhat is this, the 1980's??"
			elif stats_entry == "rush_tds":
				rush_tds = float(rushTDs.ent.get())
				values[names.index('Rushing Touchdowns')] = rush_tds
				value_to_test = rush_tds
				string = "How are RB's still a part of the NFL, am I right???"
				string2 = "Some people say the RB position is a dying position,\nto them, you raise a big middle finger!"
			elif stats_entry == "fumble_lost":
				fumble = float(fumbleObject.ent.get())
				values[names.index('Fumbles')] = fumble
				value_to_test = fumble

			### Updating side table to view current Defaults	
			update_side_table()

		except ValueError:
			### Re-enter the default values due to a bad entry
			re_enter_draft_parameters("one", stats_entry, default_value)
			### After re-entering default values, pop up this message
			pop_up_msg("Really man? That's not even a number... Try again")

		if stats_entry != "fumble_lost" and stats_entry != "pass_picks":
			if value_to_test > 20: 
				if stats_entry != "rush_yards" and stats_entry != "rush_tds":
					pop_up_msg("That's a lot of points, but you do you.....")
				else:
					pop_up_msg(string2)
			elif value_to_test == 0 and stats_entry != "rec_catches":
				pop_up_msg(string)
			elif value_to_test < 0:
				pop_up_msg("Negative points, seems wrong,\nbut I'm not going to tell you how to live your life!")
		else:
			if value_to_test < -20:
				pop_up_msg("Man, {} for a turn over!\nMust not be a Giant's fan.".format(value_to_test))
			elif value_to_test > 0:
				pop_up_msg("Points for a turnover?\nLet me guess, everyone deserves a participation trophy?")
			elif value_to_test == 0:
				pop_up_msg("Hey, mistakes happen... No need to be punished.")
		return

#####################################################################################################################################
	### A tmp fucntionds for entries that are not supported yet
	def tmp(whatTmp):
		if whatTmp == "Humans":
			numHumans.ent.delete(0, "end")
			numHumans.ent.insert(0,1)
			pop_up_msg("Currently only one human team is supported.")

		elif whatTmp == "PAT":
			kickPAT.ent.delete(0, "end")
			kickPAT.ent.insert(0,1)
			pop_up_msg("Currently kickers are not supported.\nIn my defense, are kickers even people?")

		elif whatTmp == 20:
			kickPAT.ent.delete(0, "end")
			kickPAT.ent.insert(0,3)
			pop_up_msg("Currently kickers are not supported.\nIn my defense, are kickers even people?")

		elif whatTmp == 30:
			kickPAT.ent.delete(0, "end")
			kickPAT.ent.insert(0,3)
			pop_up_msg("Currently kickers are not supported.\nIn my defense, are kickers even people?")

		elif whatTmp == 40:
			kickPAT.ent.delete(0, "end")
			kickPAT.ent.insert(0,4)
			pop_up_msg("Currently kickers are not supported.\nIn my defense, are kickers even people?")

		elif whatTmp == 50:
			kickPAT.ent.delete(0, "end")
			kickPAT.ent.insert(0,5)
			pop_up_msg("Currently kickers are not supported.\nIn my defense, are kickers even people?")

		elif whatTmp == "miss":
			kickPAT.ent.delete(0, "end")
			kickPAT.ent.insert(0,0)
			pop_up_msg("Currently kickers are not supported.\nIn my defense, are kickers even people?")

		elif whatTmp == "points0":
			dPointsAllowed0.ent.delete(0, "end")
			dPointsAllowed0.ent.insert(0,10)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "points6":
			dPointsAllowed6.ent.delete(0, "end")
			dPointsAllowed6.ent.insert(0,7)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "points13":
			dPointsAllowed13.ent.delete(0, "end")
			dPointsAllowed13.ent.insert(0,4)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "points20":
			dPointsAllowed20.ent.delete(0, "end")
			dPointsAllowed20.ent.insert(0,1)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "points27":
			dPointsAllowed27.ent.delete(0, "end")
			dPointsAllowed27.ent.insert(0,0)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "points34":
			dPointsAllowed34.ent.delete(0, "end")
			dPointsAllowed34.ent.insert(0,-1)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "points35":
			dPointsAllowed35.ent.delete(0, "end")
			dPointsAllowed35.ent.insert(0,-4)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "dSacks":
			dSacks.ent.delete(0, "end")
			dSacks.ent.insert(0,1)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "dPicks":
			dPicks.ent.delete(0, "end")
			dPicks.ent.insert(0,2)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "dFumbles":
			dFumbles.ent.delete(0, "end")
			dFumbles.ent.insert(0,2)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "dSafeties":
			dSafeties.ent.delete(0, "end")
			dSafeties.ent.insert(0,2)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "dTDs":
			dTDs.ent.delete(0, "end")
			dTDs.ent.insert(0,6)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "dSpecialTDs":
			dSpecialTDs.ent.delete(0, "end")
			dSpecialTDs.ent.insert(0,6)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "d2Points":
			d2Points.ent.delete(0, "end")
			d2Points.ent.insert(0,2)
			pop_up_msg("Currently defenses are not supported.\nIn my defense, just stream a defense...")

		elif whatTmp == "qb":
			numQB.ent.delete(0, "end")
			numQB.ent.insert(0,1)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "rb":
			numRB.ent.delete(0, "end")
			numRB.ent.insert(0,2)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "wr":
			numWR.ent.delete(0, "end")
			numWR.ent.insert(0,3)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "te":
			numTE.ent.delete(0, "end")
			numTE.ent.insert(0,1)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "def":
			numDEF.ent.delete(0, "end")
			numDEF.ent.insert(0,1)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "k":
			numKick.ent.delete(0, "end")
			numKick.ent.insert(0,1)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "flex":
			numFlex.ent.delete(0, "end")
			numFlex.ent.insert(0,1)
			pop_up_msg("Currently not supported.")

		elif whatTmp == "bench":
			numBench.ent.delete(0, "end")
			numBench.ent.insert(0,7)
			pop_up_msg("Currently not supported.")
		return

#####################################################################################################################################
	def item_selector(e, changeWhat, colNum):
		"""When the user selects an item in the combo box. This will change what they are looking at."""

		### Allow users to select what they want to choose, and change
		if changeWhat == "Team Info":
			for num, items in enumerate([numTeams, teamName, numHumans]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "Number of Players":
			for num, items in enumerate([numQB, numRB, numWR, numTE, numDEF, numKick, numFlex, numBench]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "QB":
			for num, items in enumerate([numQB, passYards, passTDs, passPicks]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "RB":
			for num, items in enumerate([numRB, rushYards, rushTDs, fumbleObject]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "WR/TE":
			for num, items in enumerate([numWR, numTE, recYards, recTDs, PPR]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "DEF Misc":
			for num, items in enumerate([numDEF, dSacks, dPicks, dFumbles, dSafeties, dTDs, dSpecialTDs, d2Points]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "DEF Points Allowed":
			dList = [dPointsAllowed0,dPointsAllowed6,dPointsAllowed13,dPointsAllowed20,dPointsAllowed27,dPointsAllowed34,dPointsAllowed35]
			for num, items in enumerate(dList):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)

		elif changeWhat == "K":
			for num, items in enumerate([numKick, kickPAT,kick20,kick30,kick40,kick50,kickMiss]):
				if num == 0: place_objects(mock_pop_up, items, num*2+2, colNum, True)
				else: place_objects(mock_pop_up, items, num*2+2, colNum)
		return

#####################################################################################################################################
	### Creates an entry for number of teams and team name
	numFlex = plot_mock_settings(mock_pop_up, "Number of Flex Player(s):", lambda: tmp("flex"), 1, tk, ttk)	
	numBench = plot_mock_settings(mock_pop_up, "Number of Bench Player(s):", lambda: tmp("bench"), 7, tk, ttk)
	numTeams = plot_mock_settings(mock_pop_up, "Number of teams in your mock draft?", select_num_teams, number_teams, tk, ttk)
	teamName = plot_mock_settings(mock_pop_up, "Pick your team name:", select_team_name, team_name, tk, ttk)
	tmpLamb = lambda: pop_up_msg("Currently only one human team is supported.")
	numHumans = plot_mock_settings(mock_pop_up, "Number of human teams in the mock draft:", lambda: tmp("Humans"), 1, tk, ttk)

	### Creating passing entries
	tmpStrs = ["Passing Yards\nPoints per 25 yards:", "Passing TDs\nPoints per passing touchdown:",
													  "Passing Interceptions\nPoints per interception:"]
	numQB = plot_mock_settings(mock_pop_up, "Number of QB(s):", lambda: tmp("qb"), 1, tk, ttk)
	passYards = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(pass_yards, "pass_yards"), pass_yards, tk, ttk)
	passTDs = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(pass_tds, "pass_tds"), pass_tds, tk, ttk)
	passPicks = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: check_points(pass_picks, "pass_picks"), pass_picks, tk, ttk)

	### Creating rushing entries
	tmpStrs = ["Rushing Yards\nPoints per 10 yards:", "Rushing TDs\nPoints per rushing touchdown:","Points per fumble"]
	numRB = plot_mock_settings(mock_pop_up, "Number of RB(s):", lambda: tmp("rb"), 2, tk, ttk)
	rushYards = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(rush_yards, "rush_yards"), rush_yards, tk, ttk)
	rushTDs = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(rush_tds, "rush_tds"), rush_tds, tk, ttk)
	fumbleObject = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: check_points(fumble, "fumble_lost"), fumble, tk, ttk)

	### Creating receiving entries
	tmpStrs = ["Receiving Yards\nPoints per 10 yards:", "Receiving TDs\nPoints per receiving touchdown:", 
			   "Receptions\nPoints per reception:"]
	numWR = plot_mock_settings(mock_pop_up, "Number of WR(s):", lambda: tmp("wr"), 3, tk, ttk)
	numTE = plot_mock_settings(mock_pop_up, "Number of TE(s):", lambda: tmp("te"), 1, tk, ttk)
	recYards = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(rec_yards, "rec_yards"), rec_yards, tk, ttk)
	recTDs = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(rec_tds, "rec_tds"), rec_tds, tk, ttk)
	PPR = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: check_points(rec_catches, "rec_catches"), rec_catches, tk, ttk)

	### Creating DEF Misc entries
	tmpStrs = ["Sacks", "Interceptions","Fumbles Recovered","Safeties","Defensive Touchdowns", "Kick and Punt Return Touchdowns",
			   "2-Point Conversion Returns", ]
	numDEF = plot_mock_settings(mock_pop_up, "Number of Defense(s):", lambda: tmp("def"), 1, tk, ttk)
	dSacks = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: tmp("dSacks"), 1, tk, ttk)
	dPicks = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: tmp("dPicks"), 2, tk, ttk)
	dFumbles = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: tmp("dFumbles"), 2, tk, ttk)
	dSafeties = plot_mock_settings(mock_pop_up, tmpStrs[3], lambda: tmp("dSafeties"), 2, tk, ttk)
	dTDs = plot_mock_settings(mock_pop_up, tmpStrs[4], lambda: tmp("dTDs"), 6, tk, ttk)
	dSpecialTDs = plot_mock_settings(mock_pop_up, tmpStrs[5], lambda: tmp("dSpecialTDs"), 6, tk, ttk)
	d2Points = plot_mock_settings(mock_pop_up, tmpStrs[6], lambda: tmp("d2Points"), 2, tk, ttk)

	### Creating DEF points allowed entries
	tmpStrs = ["Points Allowed (0)","Points Allowed (1-6)","Points Allowed (7-13)","Points Allowed (14-20)",
			   "Points Allowed (21-27)","Points Allowed (28-34)","Points Allowed (35+)"]
	dPointsAllowed0 = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: tmp("points0"), 10, tk, ttk)
	dPointsAllowed6 = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: tmp("points6"), 7, tk, ttk)
	dPointsAllowed13 = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: tmp("points13"), 4, tk, ttk)
	dPointsAllowed20 = plot_mock_settings(mock_pop_up, tmpStrs[3], lambda: tmp("points20"), 1, tk, ttk)
	dPointsAllowed27 = plot_mock_settings(mock_pop_up, tmpStrs[4], lambda: tmp("points27"), 0, tk, ttk)
	dPointsAllowed34 = plot_mock_settings(mock_pop_up, tmpStrs[5], lambda: tmp("points34"), -1, tk, ttk)
	dPointsAllowed35 = plot_mock_settings(mock_pop_up, tmpStrs[6], lambda: tmp("points35"), -4, tk, ttk)

	### Creating rushing entries
	tmpStrs = ["Points per PAT", "FG Made (0-29 yards)","FG Made (30-39 yards)","FG Made (40-49 yards)",
			   "FG Made (50+ yards)", "FG Missed (any distance)"]
	numKick = plot_mock_settings(mock_pop_up, "Number of Kicker(s):", lambda: tmp("k"), 1, tk, ttk)
	kickPAT = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: tmp("PAT"), 1, tk, ttk)
	kick20 = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: tmp(20), 3, tk, ttk)
	kick30 = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: tmp(30), 3, tk, ttk)
	kick40 = plot_mock_settings(mock_pop_up, tmpStrs[3], lambda: tmp(40), 4, tk, ttk)
	kick50 = plot_mock_settings(mock_pop_up, tmpStrs[4], lambda: tmp(50), 5, tk, ttk)
	kickMiss = plot_mock_settings(mock_pop_up, tmpStrs[5], lambda: tmp("miss"), 0, tk, ttk)

	### Creating gap between two sides, nothings below
	tk.LabelFrame(mock_pop_up).grid(row = num_row[0]+1, column = num_col[0]+4, rowspan = num_row[-1], sticky = "nesw", padx = 5, pady = 5)
	tk.LabelFrame(mock_pop_up).grid(row = num_row[0]+1, column = num_col[0]+9, rowspan = num_row[-1], sticky = "nesw", padx = 5, pady = 5)
	tk.LabelFrame(mock_pop_up).grid(row = num_row[-1]-1, column = num_col[-1], columnspan = num_col[-1], sticky = "nesw", padx = 5, pady = 5)

	### Creating label for side table to view current Defaults
	defaults_label = tk.Label(mock_pop_up, text = "Current Defaults:", font = large_font, relief = "groove", bg = "white")
	defaults_label.grid(row = num_row[0]+1, column = num_col[-1]-1, columnspan = 2, sticky = "nswe", padx = 5, pady = 5)

	### Creating side table to view current Defaults	
	for num, items in enumerate(names):
		name_label = tk.Label(mock_pop_up, text = items, font = large_font, relief = "sunken", justify = "right")
		name_label.grid(row = num_row[0]+2+num, column = num_col[-1]-1, sticky = "nswe", ipadx = 5, ipady = 5)
		### To add creating floats so the .0 is there by default, the try is because team name is a string
		if isinstance(values[num], int) or isinstance(values[num], float):
			values_label = tk.Label(mock_pop_up, text = str(float(values[num])), font = large_font, relief = "sunken")
			values_label.grid(row = num_row[0]+2+num, column = num_col[-1], sticky = "nswe", ipadx = 15, ipady = 5)
		else:
			values_label = tk.Label(mock_pop_up, text = str(values[num]), font = large_font, relief = "sunken")
			values_label.grid(row = num_row[0]+2+num, column = num_col[-1], sticky = "nswe", ipadx = 15, ipady = 5)

	### Setting up combo boxes
	tk.Label(mock_pop_up, text="Select Item to Change:").grid(row = 0, column = 0,  columnspan = 4, sticky = "nesw")
	comboValues = ["Team Info", "Number of Players", "QB", "RB", "WR/TE", "DEF Misc", "DEF Points Allowed", "K"]
	combo1= ttk.Combobox(mock_pop_up, values = comboValues, state="readonly")
	combo1.grid(row = 1, column = 0,  columnspan = 4, sticky = "nesw")
	combo1.set(comboValues[0])
	combo1.bind('<<ComboboxSelected>>', lambda e: item_selector(None, combo1.get(), 0))

	### Starting the parameters with team info in one column and QB info in the other
	item_selector(None, "Team Info", 0)

	### Creates a buttons
	ttk.Button(mock_pop_up, text = "Load Default Settings", command=load_default).grid(row=num_row[-1], column=num_col[0], sticky="ne", pady=5)
	ttk.Button(mock_pop_up, text = "Save", command = save_mock).grid(row = num_row[-1], column = num_col[-1]-1, sticky = "ne", pady = 5)

	### Creating warning label
	ttk.Label(mock_pop_up, text = warnLabel).grid(row = num_row[-1]+1, column = num_col[0], sticky = "n", pady = 5)
	ttk.Button(mock_pop_up, text = "Exit", command = mock_pop_up.destroy).grid(row = num_row[-1], column = num_col[-1], sticky = "n", pady = 5)
	mock_pop_up.mainloop()
	return



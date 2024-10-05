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
	def __init__(self, frame, string, btnCommand, entryVar, rowNum, colNum, tk, ttk):
		### Creates an entry for number of teams
		self.lab = tk.Label(frame, text = string, justify = "center", relief = "groove", bg = "white")
		self.lab.grid(row = rowNum+1, column = colNum, columnspan = 4, sticky = "nesw", padx = 5, pady = 5)
		self.ent = ttk.Entry(frame)
		self.ent.insert(0, entryVar)   ### Inserting 10 at default value
		self.ent.grid(row = rowNum+2, column = colNum, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)
		self.btn = ttk.Button(frame, text = "Submit", command = btnCommand)
		self.btn.grid(row = rowNum+2, column = colNum+3, sticky = "nsw", padx = 5, pady = 5)
		return

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
	num_row = (2, 15)
	num_col = (0, 13) 
	container = tk.Frame()
	container.grid_rowconfigure(0, weight = 1)
	container.grid_columnconfigure(0, weight = 1)

	def re_enter_draft_parameters(para_to_change, stats_entry = "None", default_value = "None"):
		"""Replacments the entry for either one or all the draft parameters depeding if you pick one or all as para_to_change.
		   If the first input = 'one', stats_entry and default_value must be entered to know what parameter to change and to what."""
		
		if para_to_change == "one":
			### Re-enter the default values due to a bad entry
			if stats_entry == "pass_yards":
				pass_yards_entry.delete(0, len(str(pass_yards_entry.get())))
				pass_yards_entry.insert(0, default_value)
			elif stats_entry == "pass_tds":
				pass_tds_entry.delete(0, len(str(pass_tds_entry.get())))
				pass_tds_entry.insert(0, default_value)
			elif stats_entry == "pass_picks":
				pass_picks_entry.delete(0, len(str(pass_picks_entry.get())))
				pass_picks_entry.insert(0, default_value)
			elif stats_entry == "rec_yards":
				rec_yards_entry.delete(0, len(str(rec_yards_entry.get())))
				rec_yards_entry.insert(0, default_value)
			elif stats_entry == "rec_tds":
				rec_tds_entry.delete(0, len(str(rec_tds_entry.get())))
				rec_tds_entry.insert(0, default_value)
			elif stats_entry == "rec_catches":
				rec_catch_entry.delete(0, len(str(rec_catch_entry.get())))
				rec_catch_entry.insert(0, default_value)
			elif stats_entry == "rush_yards":
				rush_yards_entry.delete(0, len(str(rush_yards_entry.get())))
				rush_yards_entry.insert(0, default_value)
			elif stats_entry == "rush_tds":
				rush_tds_entry.delete(0, len(str(rush_tds_entry.get())))
				rush_tds_entry.insert(0, default_value)
			elif stats_entry == "fumble_lost":
				fumble_entry.delete(0, len(str(fumble_entry.get())))
				fumble_entry.insert(0, default_value)

		elif para_to_change == "all":
			### re-enter all entries due to loading default values
			### Team information
			numTeams.ent.delete(0, len(str(numTeams.ent.get())))
			numTeams.ent.insert(0, values[0])
			teamName.ent.delete(0, len(str(teamName.ent.get())))
			teamName.ent.insert(0, values[1])

			### Passing
			passYards.ent.delete(0, len(str(passYards.ent.get())))
			passYards.ent.insert(0, values[2])
			passTDs.ent.delete(0, len(str(passTDs.ent.get())))
			passTDs.ent.insert(0, values[3])
			passPicks.ent.delete(0, len(str(passPicks.ent.get())))
			passPicks.ent.insert(0, values[4])
			fumbleObject.ent.delete(0, len(str(fumbleObject.ent.get())))
			fumbleObject.ent.insert(0, values[5])
	
			### Receiving
			recYards.ent.delete(0, len(str(recYards.ent.get())))
			recYards.ent.insert(0, values[6])
			recTDs.ent.delete(0, len(str(recTDs.ent.get())))
			recTDs.ent.insert(0, values[7])
			PPR.ent.delete(0, len(str(PPR.ent.get())))
			PPR.ent.insert(0, values[8])

			### Rushing
			rushYards.ent.delete(0, len(str(rushYards.ent.get())))
			rushYards.ent.insert(0, values[9])
			rushTDs.ent.delete(0, len(str(rushTDs.ent.get())))
			rushTDs.ent.insert(0, values[10])
		return

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

	def save_mock():
		"""Saving draft parameters."""
		### Default Fantasy Values
		from save_data_db import store_mock_parameters
		store_mock_parameters(values)
		pop_up_msg("Submitted mock draft parameters were saved.", "Mock Parameters")
		return

	def load_default():
		"""Reloading default draft parameters."""
		### Default Fantasy Values
		from data_open import default_mock_data
		default_mock = default_mock_data()

		### Changing the varible values which is used for the draft parameters
#		global values
		values = [list(parameters) for parameters in default_mock][0]

		### Re-enter the default values due to a bad entry
		re_enter_draft_parameters("all")
		
		### Need to update side table after deafaults are stored
		update_side_table()
		return

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
				num_teams.delete(0, len(str(numTeams.ent.get())))
				num_teams.insert(0, number_teams_default)
				pop_up_msg("This isn't the amount of friends you have,\nit's the number of teams you want in your mock draft.\nTry Again!")

			elif number_teams < 0:
				number_teams = number_teams_default
				values[names.index('Number of Teams')] = number_teams
				num_teams.delete(0, len(str(numTeams.ent.get())))
				num_teams.insert(0, number_teams_default)
				pop_up_msg("Dude, that's a negative number... try again...")

			elif 30 > number_teams > 20:
				values[names.index('Number of Teams')] = number_teams
				pop_up_msg(str(number_teams) + " teams, That's a man's (or woman's) league...")

			elif number_teams >= 30:
				string = str(num_teams.get())
				number_teams = number_teams_default
				values[names.index('Number of Teams')] = number_teams
				num_teams.delete(0, len(str(numTeams.ent.get())))
				num_teams.insert(0, number_teams_default)
				pop_up_msg("I don't believe you,\nno way your league has " + string + " teams...\nTry Again")

			### Updating side table to view current Defaults	
			update_side_table()

		except ValueError:
			number_teams = number_teams_default
			num_teams.delete(0, len(str(numTeams.ent.get())))
			num_teams.insert(0, number_teams_default)
			pop_up_msg("Come on bro, how can number of teams not be a whole number?")
		return

	def select_team_name():
		"""A check for vailding team names."""
		### Allowing varbiles to be changed, should use getters, and setters
		global team_name
		team_name = str(teamName.ent.get())
		values[names.index('Team Name')] = team_name

		if len(team_name) == 0:
			team_name = "Player 1"
			team_name_entry.delete(0, "end")#len(str(teamName.ent.get())))
			team_name_entry.insert(0, team_name)
			values[names.index('Team Name')] = team_name
			pop_up_msg("Really, no team name???\nThat's lame, I'm going to call you Player 1.\nSee, I can be lame too.")
			
		elif len(team_name) > 30:
			team_name = team_name_deafult
			team_name_entry.delete(0, "end")
			team_name_entry.insert(0, team_name)
			values[names.index('Team Name')] = team_name
			pop_up_msg("You're team name is too long, try again..... (that's what she said)")

		### Updating side table to view current Defaults	
		update_side_table()
		return

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


	### Creating gap between two sides
	tk.LabelFrame(mock_pop_up).grid(row = num_row[0]+1, column = num_col[0]+4, rowspan = num_row[-1], sticky = "nesw", padx = 5, pady = 5)
	tk.LabelFrame(mock_pop_up).grid(row = num_row[0]+1, column = num_col[0]+9, rowspan = num_row[-1], sticky = "nesw", padx = 5, pady = 5)

	def change_values(e, changeWhat, colNum):
		"""When the user selects an item in the combo box. This will change what they are looking at."""

		if changeWhat == "Team Info":
			### Creates an entry for number of teams and team name
			numTeams = plot_mock_settings(mock_pop_up, "Number of teams in your mock draft?", select_num_teams, number_teams, 2, 0, tk, ttk)
			teamName = plot_mock_settings(mock_pop_up, "Pick your team name:", select_team_name, team_name, 2, 5, tk, ttk)

		elif changeWhat == "QB":
			### Creating passing entries
			tmpStrs = ["Passing Yards\nPoints per 25 yards:", "Passing TDs\nPoints per passing touchdown:"]
			passYards = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(pass_yards, "pass_yards"), pass_yards, 2, 0, tk, ttk)
			passTDs = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(pass_tds, "pass_tds"), pass_tds, 2, 5, tk, ttk)
		return

#	### Creating turnover entries
#	tmpStrs = ["Passing Interceptions\nPoints per interception:", "Receiving TDs\nPoints per receiving touchdown:"]
#	passPicks = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(pass_picks, "pass_picks"), pass_picks, 4, 0, tk, ttk)
#	fumbleObject = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(fumble, "fumble_lost"), fumble, 4, 5, tk, ttk)

#	### Creating receiving entries
#	tmpStrs = ["Receiving Yards\nPoints per 10 yards:", "Receiving TDs\nPoints per receiving touchdown:", "Receptions\nPoints per reception:"]
#	recYards = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(rec_yards, "rec_yards"), rec_yards, 6, 0, tk, ttk)
#	recTDs = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(rec_tds, "rec_tds"), rec_tds, 6, 5, tk, ttk)
#	PPR = plot_mock_settings(mock_pop_up, tmpStrs[2], lambda: check_points(rec_catches, "rec_catches"), rec_catches, 8, 5, tk, ttk)

	### Creating rushing entries
	tmpStrs = ["Rushing Yards\nPoints per 10 yards:", "Rushing TDs\nPoints per rushing touchdown:"]
	rushYards = plot_mock_settings(mock_pop_up, tmpStrs[0], lambda: check_points(rush_yards, "rush_yards"), rush_yards, 10, 0, tk, ttk)
	rushTDs = plot_mock_settings(mock_pop_up, tmpStrs[1], lambda: check_points(rush_tds, "rush_tds"), rush_tds, 10, 5, tk, ttk)

#	### Creating label for side table to view current Defaults
#	defaults_label = tk.Label(mock_pop_up, text = "Current Defaults:", font = large_font, relief = "groove", bg = "white")
#	defaults_label.grid(row = num_row[0]+1, column = num_col[-1]-1, columnspan = 2, sticky = "nswe", padx = 5, pady = 5)

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
	comboValues = ["Team Info", "QB", "RB", "WR", "TE", "DEF", "K"]
	combo1= ttk.Combobox(mock_pop_up, values = comboValues, state="readonly")
	combo1.grid(row = 1, column = 0,  columnspan = 4, sticky = "nesw")
	combo1.set(comboValues[0])
	combo1.bind('<<ComboboxSelected>>', lambda e: change_values(e, combo1.get(), 0))

	### The second combo box
	tk.Label(mock_pop_up, text="Select Item to Change:").grid(row = 0, column = 5,  columnspan = 4, sticky = "nesw")
	curTeams = ttk.Combobox(mock_pop_up, values = comboValues, state="readonly")
	curTeams.grid(row = 1, column = 5, columnspan = 4, sticky = "nesw")
	curTeams.set(comboValues[1])
#	curTeams.bind('<<ComboboxSelected>>', lambda e: change_listbox(e))

	### Creates a buttons
	ttk.Button(mock_pop_up, text = "Load Default Settings", command=load_default).grid(row=num_row[-1], column=num_col[0], sticky="ne", pady=5)
	ttk.Button(mock_pop_up, text = "Save", command = save_mock).grid(row = num_row[-1], column = num_col[-1]-1, sticky = "ne", pady = 5)
	ttk.Button(mock_pop_up, text = "Exit", command = mock_pop_up.destroy).grid(row = num_row[-1], column = num_col[-1], sticky = "n", pady = 5)

	### Creating warning label
	ttk.Label(mock_pop_up, text = warnLabel).grid(row = num_row[-1]+1, column = num_col[0], sticky = "n", pady = 5)
	mock_pop_up.mainloop()
	return



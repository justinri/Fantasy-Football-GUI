### Creating default fonts
large_font = ("Helvetica", 12)
lFont = large_font
norm_font = ("Helvetica", 10)
small_font = ("Helvetica", 8)
from help_options import pop_up_msg
from save_data_db import update_fav_team

#####################################################################################################################################
def stats_pop_up(pos, players_stats, comb_results, tk, ttk):
	"""Creates a pop up window for the selected player. Showing all his stats, bio, and combine information.
	   The player_stats and comb_results must be for the player that is being showed."""

	### Starting mini instance for stats
	num_row = (0,45)  ### 50 for max row to ensure exit button is on the bottom
	num_col = (0,15)
	stats_pop_up = tk.Tk()
	stats_pop_up.geometry("1190x540")

	### Creating a scroll bar
	myframe = tk.Frame(stats_pop_up)
	myframe.place( x = 10, y = 10)

	canvas = tk.Canvas(myframe, width = 1195, height = 485, relief = "groove")
	frame = tk.Frame(canvas)
	myscrollbar = tk.Scrollbar(myframe, orient="vertical", command = canvas.yview)
	canvas.configure(yscrollcommand = myscrollbar.set)

	myscrollbar.pack(side = "right", fill = "y")
	canvas.pack( side = "left")
	canvas.create_window((0,0), window=frame, anchor='nw')

	### Need a try and except for people with no stats like rookies
	try:
		stats_pop_up.wm_title("Complete Stats for " + players_stats[0][1] + " " + players_stats[0][0])	
		### Creates a label for the player that was selected, their name		
		player_label = ttk.Label(frame, 
								text = players_stats[0][1] +' '+ players_stats[0][0], font = ("Times", "14", "bold"), relief = "groove")
		player_label.grid(row = num_row[0], column = num_col[0], sticky = "nesw", ipadx = 10, pady = 5)

		### Creates a label for the player's birth year			
		birth_label = ttk.Label(frame, 
								text = 'Year Born: '+ str(players_stats[0][2]), font = ("Times", "14", "bold"), relief = "groove")
		birth_label.grid(row = num_row[0], column = num_col[0]+1, sticky = "nesw", ipadx = 10, pady = 5)

		### if weight and height are zero, do not show them
		add1 = 0
		if float(comb_results[0][1]) != float(0):
			### Create Height
			h_string = 'Height [in]: '+ str(comb_results[0][1])
			height_label = ttk.Label(frame, text = h_string, font = ("Times", "14", "bold"), relief = "groove")
			height_label.grid(row = num_row[0], column = num_col[0]+2+add1, sticky = "nesw", ipadx = 10, pady = 5)
			add1 += 1   ### So if height is zero but weight is not, weight will move over

		if float(comb_results[0][1]) != float(0):
			### Create Weight
			w_string = 'Weight [lbs]: '+ str(comb_results[0][0])
			weight_label = ttk.Label(frame, text = w_string, font = ("Times", "14", "bold"), relief = "groove")
			weight_label.grid(row = num_row[0], column = num_col[0]+3, sticky = "nesw", ipadx = 10, pady = 5)

	except IndexError:
		### If no stats, give a warning and exit
		stats_pop_up.destroy()
		pop_up_msg("No stats were found", "No Stats")

	### Creating labels for stats, year	
	qb_pass_labels = ["Year", "Age", "Team", "Games Played", "Games Started", \
					  "Attempts", "Completions", "Yards", "Touchdowns", "Interceptions"]

	qb_rush_labels = ["Year", "Rushing Attempts", "Rushing Yards", "Rushing Touchdowns", "Fumbles"]

	rb_rush_labels = ["Year", "Age", "Team", "Games Played", "Games Started", \
				      "Attempts", "Yards", "Touchdowns", "Fumbles"]
	rb_rec_labels = ["Year","Targets", "Receptions", "Receiving Yards", "Receiving Touchdowns"]	


	wr_labels = ["Year", "Age", "Team", "Games Played", "Games Started", \
				 "Targets", "Receptions", "Yards", "Touchdowns"]

	if pos == "QB":
		labels_for_stats = qb_pass_labels
		labels_for_stats2 = qb_rush_labels
		stats_2 = [(items[3], items[-4], items[-3], items[-2], items[-1]) for items in players_stats]
		text_label = "Passing Stats"
		text_label2 = "Rushing Stats"
		num_to_minus = 0
	elif pos == "RB":
		labels_for_stats = rb_rush_labels
		labels_for_stats2 = rb_rec_labels
		stats_2 = [(items[3], items[-4], items[-3], items[-2], items[-1]) for items in players_stats] 
		text_label = "Rushing Stats"
		text_label2 = "Receiving Stats"
		num_to_minus = len(rb_rec_labels) - 1 ### Minus one because I want year in both
	elif pos == "WR":
		labels_for_stats = wr_labels
		num_to_minus = 0
	else: ### Must be TE
		labels_for_stats = wr_labels  ### WR's and TE's have the same labels
		num_to_minus = 0

	### Rushing stats are at the end of passing stats, do
	lenOfStats = len(players_stats[0])-3-num_to_minus ### -3: no need for first name, last name and birth year
	if pos == "QB": lenOfStats = lenOfStats - 4 ### 4 rushing stats (not counting years)

	### Inserting labels into the mini instance
	for num, items in enumerate(labels_for_stats):
		table_labels = ttk.Label(frame, text = items, font = ("Times", "12", "bold"), relief = "groove")
		table_labels.grid(row = num_row[0]+1, column = num_col[0]+num, sticky = "nesw", ipadx = 5)

	### Creating table of players stats
	for num, items in enumerate(players_stats):
		for num_2 in range(lenOfStats): ### -3: no need for first name, last name and birth year
			stats_label = ttk.Label(frame, text = items[num_2+3], font = ("Times", "12", "bold"), relief = "groove")
			stats_label.grid(row = num_row[0]+2+num, column = num_col[0]+num_2, sticky = "nesw", ipadx = 5)

	### Creating second stats table for Qb's and RB's
	if pos == "QB" or pos == "RB": 
		### Creating gap between two sides
		nothing = tk.LabelFrame(frame)
		nothing.grid(row = num_row[0]+3+num, column = num_col[0], columnspan = num_col[-1], sticky = "nesw", pady = 5)

		#### add year, it could be help full
		### Inserting labels into the mini instance
		for num_3, items in enumerate(labels_for_stats2):
			table2_labels = ttk.Label(frame, text = items, font = ("Times", "12", "bold"), relief = "groove")
			table2_labels.grid(row = num_row[0]+4+num, column = num_col[0]+num_3, sticky = "nesw", ipadx = 5)

		### Creating table of players stats (stats_2)
		for num_4, items in enumerate(stats_2):
			for num_5 in range(len(stats_2[0])):
				stats2_label = ttk.Label(frame, text = items[num_5], font = ("Times", "12", "bold"), relief = "groove")
				stats2_label.grid(row = num_row[0]+5+num+num_4, column = num_col[0]+num_5, sticky = "nesw", ipadx = 5)

	def combine_pop_up():
		"""Creates the combine results pop up. This shows the combine results for a given player."""
		cb_pop_up = tk.Tk()
		cb_pop_up.wm_title("Combine Results for " + players_stats[0][1] + " " + players_stats[0][0])
		comb_labels = ["Forty [s]", "Vertical [in]", "Bench", "Broad Jump [in]", "Shuttle [s]", "Cone [s]", "Combine Weight [lbs]"]

		### Creating complete combine table
		for num_6, items in enumerate(comb_labels):
			cbL = ttk.Label(cb_pop_up, text = items, font = ("Times", "12", "bold"), relief = "groove")
			cbL.grid(row = num_row[0]+1, column = num_col[0]+num_6, sticky = "nesw", ipadx = 5)

			cbStats = ttk.Label(cb_pop_up, text = comb_results[0][num_6 + 7], font = ("Times", "12", "bold"), relief = "groove")
			cbStats.grid(row = num_row[0]+2, column = num_col[0]+num_6, sticky = "nesw", ipadx = 5)

		### Creating gap between two sides, nothing
		tk.LabelFrame(cb_pop_up).grid(row = num_row[0]+3, column = num_col[0], columnspan = num_col[-1], sticky = "nesw", padx = 5, pady = 5)

		### Input draft labels
		idl = ttk.Label(cb_pop_up, text = "Round Selected", font = ("Times", "12", "bold"), relief = "groove")
		idl.grid(row = num_row[0]+4, column = num_col[0]+1, sticky = "sew", ipadx = 5)

		idl2 = ttk.Label(cb_pop_up, text = "Overall Pick", font = ("Times", "12", "bold"), relief = "groove")
		idl2.grid(row = num_row[0]+4, column = num_col[0]+2, sticky = "esw", ipadx = 5)

		### Input draft results
		idr = ttk.Label(cb_pop_up, text = comb_results[0][2], font = ("Times", "12", "bold"), relief = "groove")
		idr.grid(row = num_row[0]+5, column = num_col[0]+1, sticky = "new", ipadx = 5)

		idr2 = ttk.Label(cb_pop_up, text = comb_results[0][3], font = ("Times", "12", "bold"), relief = "groove")
		idr2.grid(row = num_row[0]+5, column = num_col[0]+2, sticky = "new", ipadx = 5)

		## Exit button to leave loop
		cb_pop_up.bind("<Return>", lambda e: cb_pop_up.destroy())
		ttk.Button(cb_pop_up, text = "Exit", command = cb_pop_up.destroy).grid(row = num_row[-1], column = num_col[0]+num_6, sticky = "s", pady = 5)
		cb_pop_up.mainloop()
		return

	### Exit button to leave loop
	tk.Button(stats_pop_up, text = "Combine Results", command = combine_pop_up).place(x = 10, y = 500)
	stats_pop_up.bind("<Return>", lambda e: stats_pop_up.destroy())
	ttk.Button(stats_pop_up, text = "Exit", command = stats_pop_up.destroy).place(x = 1102, y = 500)

	def reConfig(event):
		canvas.configure(scrollregion=canvas.bbox("all"), width=1150, height = 485)
		return

	frame.bind("<Configure>", reConfig)
	stats_pop_up.mainloop()
	return
#####################################################################################################################################
def mock_pop_up(pos, player, players_stats, comb_results, tk, ttk):
	"""Creates the stats needed for the pop up stats, when people click on a player's name on the draft table."""

	### Accounting for tk inter set varibles
	if isinstance(player, tk.StringVar):
		pos = pos.get()
		player = player.get().split()
		fName = player[1][1:-2]
		lName = player[0][2:-2]
		bday = int("".join(num for num in player[2] if num.isdigit()))
		player = (lName, fName, bday)

	playersStats = [items for items in players_stats[pos] if player[0] and  player[1] in items if player[2] == items[2]]
	comb_results = [items for items in  comb_results[pos] if player[0] and  player[1] in items if player[2] == items[6]]
	stats_pop_up(pos, playersStats, comb_results, tk, ttk)
	return

#####################################################################################################################################
def pop_up_stats(event, pos):
	"""Selects the player that was doubled clicked, and has all their stats pop up. In an mini instance."""

	### I changed the last clicked to two, to account for birth year
	if pos == "QB":
		clicked = fav_QBs[int(qb_listBox.curselection()[0])]
		players_stats = [player for player in fav_qbs_stats if clicked[0] and  clicked[1] in player if clicked[2] in player]
		comb_results = [player for player in fav_qbs_comb if clicked[0] and  clicked[1] in player if clicked[2] in player]

	elif pos == "RB":
		clicked = fav_RBs[int(rb_listBox.curselection()[0])]
		players_stats = [player for player in fav_rbs_stats if clicked[0] and  clicked[1] in player if clicked[2] in player]
		comb_results = [player for player in fav_rbs_comb if clicked[0] and  clicked[1] in player if clicked[2] in player]

	elif pos == "WR":
		clicked = fav_WRs[int(wr_listBox.curselection()[0])]
		players_stats = [player for player in fav_wrs_stats if clicked[0] and  clicked[1] in player if clicked[2] in player]
		comb_results = [player for player in fav_wrs_comb if clicked[0] and  clicked[1] in player if clicked[2] in player]

	else: ## Must be TE
		clicked = fav_TEs[int(te_listBox.curselection()[0])]
		players_stats = [player for player in fav_tes_stats if clicked[0] and  clicked[1] in player if clicked[2] in player]
		comb_results = [player for player in fav_tes_comb if clicked[0] and  clicked[1] in player if clicked[2] in player]

	### What to do on click
	if click_type == "single": 
		return ### No need to continue on single clicks
	elif click_type == "double":
		stats_pop_up(pos, players_stats, comb_results, tk, ttk)
		return

#####################################################################################################################################
def team_stats_pop_up(favTeam, teamStats, team_names_gap, tk, ttk):
	"""This creates a pop up showing all the stats for their favorite team"""

	### Setting up gui
	fav = tk.Tk()
	num_row = (0, 100)
	num_col = num_row
	team = favTeam.get() ### First name in team_names_gap is always the favorite team.

	def update_team(e, team, whatTeam = "fav"):
		### On start up, should show favorite teams' stats
		if whatTeam == "fav":
			team_stats = teamStats[team.replace(" ","_")] 
			teamVarDict.set(team)
		elif whatTeam == "update":
			team = newTeam.get()
			teamVarDict.set(team)
			team_stats = teamStats[team.replace(" ","_")] 

		### Setting up gui
		fav.wm_title("Team Stats for the " + team)
		num_row = (0, 100)
		num_col = num_row

		### All labels I have
		all_labels = ["Year", "For or Against", "Total Points", "Total Yards", "Total Plays", "Total Yards\nPer Play", \
					  "Passing\nCompleted", "Passing\nAttempts", "Passing\nYards", "Passing\nTouchdowns", "Passing\nInterceptions", \
					  "Rushing Attempts", "Rushing Yards", "Rushing TDs", "Rushing Yards\nPer Attempt", \
					  "Average Starting\nField Position", "Time Per Drive", "Number of Plays\nPer Drive", "Yards Per Drive", "Points Per Drive"]

		### Getting Info for tables
		### For total table
		totalStats = [items[idx] for items in team_stats[::2] for idx in (0,2,3,4,5)]
		totalOppStats  = [items[idx] for items in team_stats[1::2] for idx in (0,2,3,4,5)]
		totalLabels = [all_labels[idx] for idx in (0,2,3,4,5)]
		totalStr = "Total Stats"

		### For passing table
		passStats = [items[idx] for items in team_stats[::2] for idx in (0,6,7,8,9,10)]
		passOppStats = [items[idx] for items in team_stats[1::2] for idx in (0,6,7,8,9,10)]
		passLabels = [all_labels[idx] for idx in (0,6,7,8,9,10)]
		passStr = "Passing Stats"

		### For passing table
		rushStats = [items[idx] for items in team_stats[::2] for idx in (0, 11,12,13,14)]
		rushOppStats = [items[idx] for items in team_stats[1::2] for idx in (0, 11,12,13,14)]
		rushLabels = [all_labels[idx] for idx in (0, 11,12,13,14)]
		rushStr = "Rushing Stats"

		### For passing table
		perDriveStats = [items[idx] for items in team_stats[::2] for idx in (0, 15, 16, 17, 18, 19)]
		perDriveOppstats = [items[idx] for items in team_stats[1::2] for idx in (0, 15, 16, 17, 18, 19)]
		perDriveLabels = [all_labels[idx] for idx in (0, 15, 16, 17, 18, 19)]
		perDriveStr = "Stats Per Drive"

		def display_stats(whatStats = "Total"):
			"""Creates a pop up to show team stats."""

			### Getting the stats and label I need
			if whatStats == "Total":
				t_stats = totalStats
				t_o_stats = totalOppStats
				t_labels = totalLabels
				strVarDict.set(totalStr)
			elif whatStats == "Pass":
				t_stats = passStats
				t_o_stats = passOppStats
				t_labels = passLabels
				strVarDict.set(passStr)
			elif whatStats == "Rush":
				t_stats = rushStats
				t_o_stats = rushOppStats
				t_labels = rushLabels
				strVarDict.set(rushStr)
			elif whatStats == "perDrive":
				t_stats = perDriveStats
				t_o_stats = perDriveOppstats
				t_labels = perDriveLabels
				strVarDict.set(perDriveStr)

			### Creating nothing labels to cover up stats left over from passing and per drive
			if whatStats == "Total" or whatStats == "Rush":
				favLabelVarDict[0].set("")
				oLabelVarDict[5].set("")
				[favLabelVarDict[num+1].set(items) for num, items in enumerate(t_labels)]
				[oLabelVarDict[num].set(items) for num, items in enumerate(t_labels)]
				[favStatsVarDict[num][0].set("") for num in range(10)]
				[OStatsVarDict[num][0].set("") for num in range(10)]

			else:
				[favLabelVarDict[num].set(items) for num, items in enumerate(t_labels)]
				[oLabelVarDict[num].set(items) for num, items in enumerate(t_labels)]

			### Set varibles
			add1 = len(t_labels)*9
			for num2 in range(10):
				for num3 in range(6):
					if num2 % 2 == 0: bgColorVarDict[num2][num3].set("grey")
					else: bgColorVarDict[num2][num3].set("lightgrey")

					if whatStats == "Total" or whatStats == "Rush":
						if num3 == 0:
							favStatsVarDict[num2][num3].set("")
							OStatsVarDict[num2][num3].set(t_o_stats[num3+add1])
							continue
						elif num3 == 5:
							OStatsVarDict[num2][num3].set("")
							favStatsVarDict[num2][num3].set(t_stats[num3-1+add1])
							continue
						favStatsVarDict[num2][num3].set(t_stats[num3-1+add1])
						OStatsVarDict[num2][num3].set(t_o_stats[num3+add1])

					else:
						favStatsVarDict[num2][num3].set(t_stats[num3+add1])
						OStatsVarDict[num2][num3].set(t_o_stats[num3+add1])
				add1 -= len(t_labels)
			return
		display_stats()
	
		### Creating gap between two sides
		tk.LabelFrame(fav).grid(row = num_row[-1]-1, column = num_col[0], columnspan = num_col[-1], sticky = "nesw", pady = 5)

		### Creating an stats buttons
		ttk.Button(fav, text = "Total Stats", command = lambda: display_stats("Total")).grid(row=num_row[-1], column=num_col[0], sticky = "nesw")
		ttk.Button(fav, text="Passing Stats", command = lambda: display_stats("Pass")).grid(row=num_row[-1], column=num_col[0]+1, sticky = "nesw")
		ttk.Button(fav, text="Rushing Stats", command = lambda: display_stats("Rush")).grid(row=num_row[-1], column=num_col[0]+2, sticky = "nesw")
		ttk.Button(fav, text = "Stats Per Drive", command=lambda: display_stats("perDrive")).grid(row=num_row[-1], column=num_col[0]+3,sticky="nesw")
		return

	### Setting up varibles
	favStatsVarDict = {num2:{num3:tk.StringVar(fav) for num3 in range(6)} for num2 in range(10)}
	OStatsVarDict = {num2:{num3:tk.StringVar(fav) for num3 in range(6)} for num2 in range(10)}
	bgColorVarDict = {num2:{num3:tk.StringVar(fav) for num3 in range(6)} for num2 in range(10)}
	for key1 in bgColorVarDict.keys(): 
		for key2 in bgColorVarDict[key1].keys(): 
			bgColorVarDict[key1][key2].set("lightgrey")
	favLabelVarDict = {num : tk.StringVar(fav) for num in range(6)}
	oLabelVarDict = {num : tk.StringVar(fav) for num in range(6)}
	teamVarDict = tk.StringVar(fav)
	strVarDict = tk.StringVar(fav)
	update_team(None, team, "fav")

	### Creating Labels
	[ttk.Label(fav, textvariable=favLabelVarDict[num], font = ("Times", "10"), relief = "groove", anchor = "center"
			).grid(row = num_row[0]+2, column = num_col[0]+num, sticky = "nsew", ipadx = 10, ipady = 5) for num in range(6)]
	[ttk.Label(fav, textvariable=oLabelVarDict[num], font = ("Times", "10"), relief = "groove", anchor = "center"
			).grid(row = num_row[0]+2, column = num_col[0]+6+num, sticky = "nsew", ipadx = 10, ipady = 5) for num in range(6)]

	### Creating labels into put varibles
	tmpFont = ("Times","10")
	for num2 in range(10):
		for num3 in range(6):
			favStatsL = tk.Label(fav, textvariable=favStatsVarDict[num2][num3], font=tmpFont,anchor="center",bg=bgColorVarDict[num2][num3].get())
			favStatsL.grid(row = num_row[0]+num2+3, column = num_col[0]+num3, sticky = "nsew", ipadx = 5, ipady = 5)	
			OStatsL = tk.Label(fav, textvariable=OStatsVarDict[num2][num3], font=tmpFont, anchor = "center",bg=bgColorVarDict[num2][num3].get())
			OStatsL.grid(row = num_row[0]+num2+3, column = num_col[0]+6+num3, sticky = "nsew", ipadx = 5, ipady = 5)

	### Saying who's stats they are
	teamLabel = ttk.Label(fav, textvariable = teamVarDict, font = ("Times", "12"), relief = "groove", anchor = "center")
	teamLabel.grid(row = num_row[0]+1, column = num_col[0], columnspan = 6, sticky = "nsew", ipadx = 10, ipady = 5)
	oppLabel = ttk.Label(fav, text = "Opponent's stats", font = ("Times", "12"), relief = "groove", anchor = "center")
	oppLabel.grid(row = num_row[0]+1, column = 6, columnspan = 6, sticky = "nsew", ipadx = 10, ipady = 5)

	### Creating total stats label
	totalStatsL = ttk.Label(fav, textvariable = strVarDict, font = ("Times", "14"), relief = "groove", anchor = "center")
	totalStatsL.grid(row = num_row[0], column = num_col[0], columnspan = num_col[-1], sticky = "nsew", ipadx = 10, ipady = 5)

	### Creating combobox to select player
	newTeam = ttk.Combobox(fav, values=team_names_gap[1:], state = "readonly")
	newTeam.grid(row = num_row[-1], column = 9, columnspan = 2, sticky = "nesw")
	newTeam.bind('<<ComboboxSelected>>', lambda e: update_team(e, team,"update"))

	### Creating an exit button
	ttk.Button(fav, text = "Exit", command = fav.destroy).grid(row = num_row[-1], column = 11, sticky = "nesw")
	fav.mainloop()
	return

#####################################################################################################################################
def pop_up_drop(dropList, pos, playersStats, bio_and_combine, tk, ttk):
	"""Allows the user to select their player for a list of players with the same name."""
	### Setting up pop up for favorite team select
	dropDown = tk.Tk()
	dropDown.wm_title("Pick a player")
	
	def returnWhat(event = None):
		player = drop_down_menu.get().split(" ")
		del player[2:4]

		### Removing birthday string and pulling out the int
		grabBDYear = ''.join([items for items in player[2] if items.isdigit()])

		### What what ever reason I made RB's year's a string in the data base
		player = [player[1].strip(), player[0].strip(), int(grabBDYear)]  ### Putting last name first again.
		comb_results = [items for items in bio_and_combine[pos] if player[0] and player[1] in items if player[2] in items]
		players_stats = [items for items in playersStats[pos] if player[0] == items[0] if player[1] == items[1] if player[2] == items[2]]

		dropDown.destroy()
		stats_pop_up(pos, players_stats, comb_results, tk, ttk)
		return

	### Creating drop down information
	Var = tk.StringVar(dropDown)
	drop_down_label = ttk.Label(dropDown, text="Select the player you are looking for:", relief = "groove", anchor = "center")
	drop_down_label.grid(row = 0, column = 0, sticky = "nesw", ipadx = 50, ipady = 5)

	drop_down_menu = ttk.Combobox(dropDown, values = dropList, state="readonly")
	drop_down_menu.grid(row = 1, column = 0, sticky = "nesw")

	### Binding on enter(return)
	dropDown.bind("<Return>", returnWhat)

	### Creating buttons for the select favorite team pop up
	ttk.Button(dropDown, text = "Submit", command = returnWhat).grid(row = 3, column = 0, sticky = "nesw")
	ttk.Button(dropDown, text = "Exit", command = dropDown.destroy).grid(row = 4, column = 0, sticky = "nesw")
	dropDown.mainloop()
	return

#####################################################################################################################################
def all_players_stats(bio_and_combine, playersStats, tk, ttk):
	"""This function creates a pop so the user can look through past and current players"""
	players = tk.Tk()
	players.wm_title("Players' Stats")
	
	### Creating name label
	f_name_l = ttk.Label(players, text = "First Name: ", font = ("Times", "12"), relief = "groove")
	f_name_l.grid(row = 2, column = 0, sticky = "nesw", columnspan = 2, ipadx = 10, ipady = 5)
	l_name_l = ttk.Label(players, text = "Last Name: ", font = ("Times", "12"), relief = "groove")
	l_name_l.grid(row = 2, column = 4, sticky = "nesw", columnspan = 2, ipadx = 10, ipady = 5)

	### Creating name entry
	f_name_e = ttk.Entry(players)
	f_name_e.insert(0, "Tony")
	f_name_e.grid(row = 2, column = 2, columnspan = 2, sticky = "nesw", ipadx = 5, ipady = 5)
	l_name_e = ttk.Entry(players, text = "Last Name: ")
	l_name_e.insert(0, "Romo")
	l_name_e.grid(row = 2, column = 6, columnspan = 2, sticky = "nesw", ipadx = 5, ipady = 5)

	def find_player(event = None, findAll = None):
		"""Find the player the user wanted based off first and last name."""
		f_name = f_name_e.get().title().strip()
		l_name = l_name_e.get().title().strip()

		if posVar.get() == 0:
			pos = "QB"
		elif posVar.get() == 1:
			pos = "RB"
		elif posVar.get() == 2:
			pos = "WR"
		elif posVar.get() == 3:
			pos = "TE"
		else:
			### To make sure they are selecting a position
			pop_up_msg("Please select a position...")

		### Creating a drop down list for all players based off position
		if findAll == "findAll":
			if pos == "QB":
				playerList = set([items[:3] for items in playersStats[pos]])
				pos = "QB"
			else:
				playerList = set([items[:3] for items in playersStats[pos]])

			### Putting in readable order for user: first name, last name, birthday: year
			playerList = [[items[1], items[0], "Birthday Year: " + str(items[2])] for items in playerList]
			playerList.sort(key=lambda playerList: playerList[0]) 	   ### Sorting by last name
			pop_up_drop(playerList, pos, playersStats, bio_and_combine, tk, ttk) 
			return
			
		### find all players by name, last then first
		lname_search = [items for items in playersStats[pos] if l_name in items[0]]
		fname_search = [items for items in lname_search if f_name[:3] in items[1][:3]] ### Only doing first there to account for nicknames
		getUpToBirthdays = set([items[:3] for items in fname_search]) 				   ### elimating same players

		if len(getUpToBirthdays) == 1:
			playerList = [fname_search[0]]

		elif len(getUpToBirthdays) > 1: 
			playerList = getUpToBirthdays

		elif len(getUpToBirthdays) < 1: 
			pop_up_msg("No player was found with that name. :/")
			return

		if len(playerList) == 1:
			player = playerList[0]
			comb_results = [items for items in bio_and_combine[pos] if player[0] and player[1] in items if player[2] in items]
			stats_pop_up(pos, fname_search, comb_results, tk, ttk)

		elif len(playerList) < 1:
			pop_up_msg("No player was found. :*(")

		elif len(playerList) > 1:
			### Putting in readable order for user: first name, last name, birthday: year
			playerList = [[items[1], items[0], "Birthday Year: " + str(items[2])] for items in playerList]
			playerList.sort(key=lambda playerList: playerList[2][-4:]) ### Sorting by birth year
			pop_up_drop(playerList, pos, playersStats, bio_and_combine, tk, ttk) 
		return

	### Creating a label for player selection
	sel_l = ttk.Label(players, text = "Select a position: ", font = ("Times", "12"), relief = "groove")
	sel_l.grid(row = 0, column = 0, columnspan = 8, sticky = "nesw")

	### Creating check boxes for position:
	posVar = tk.IntVar(players)
	tk.Radiobutton(players, text = "QB", variable = posVar, value = 0).grid(row = 1, column = 0, sticky = "w")
	tk.Radiobutton(players, text = "RB", variable = posVar, value = 1).grid(row = 1, column = 1, sticky = "w")
	tk.Radiobutton(players, text = "WR", variable = posVar, value = 2).grid(row = 1, column = 2, sticky = "w")
	tk.Radiobutton(players, text = "TE", variable = posVar, value = 3).grid(row = 1, column = 3, sticky = "w")	

	### Binding on enter(return)
	players.bind("<Return>", find_player)

	### Creating an buttons
	ttk.Button(players, text = "Find All", command = lambda: find_player(None, findAll = "findAll")).grid(row = 3, column = 0, sticky = "nesw")
	ttk.Button(players, text = "Submit", command = find_player).grid(row = 3, column = 6, sticky = "nesw")
	ttk.Button(players, text = "Exit", command = players.destroy).grid(row = 3, column = 7, sticky = "nesw")
	players.mainloop()
	return

#####################################################################################################################################
def past_ros(team_names_gap, current_rosters, past_rosters, bio_and_combine, players_stats, tk, ttk):
	"""Creates a pop up window showing past rosters."""
	pastRos = tk.Tk()
	pastRos.wm_title("Past Rosters")
	del team_names_gap[0]
	num_row = (0,50)
	num_col = num_row

	### Getting the years of data I have
	yearKeys = []
	for items in past_rosters.keys():
		yearKeys.append(items[-4:])
		if len(yearKeys) > 1:
			if yearKeys[-1] < yearKeys[-2]:
				del yearKeys[-1]
				yearKeys.append(str(int(yearKeys[-1])+1)) ### Adding current year
				break

	def displayTeam():
		"""Display the roster for the selected team and year."""
		
		if team.get() == "" or year.get() == "":
			pop_up_msg("Please Select a Team and Year.", "Select Both!")
		else:
			selTeam = team.get().replace(" ", "_").title().strip()
			selYear = year.get().strip()

		### If statement for if its the current roster
		try: 
			if selYear == yearKeys[-1]: 
				displayRos = current_rosters[selTeam]
			else: 
				displayRos = past_rosters[selTeam + "_" + selYear]
		except KeyError:
			pop_up_msg("Either spell the names(and enter a year) correctly or\nPick from the dropdown lists...")

		### Creating titles for the positions
		positions = ["Quarterbacks", "Running Backs", "Wide Receivers", "Tight Ends"]
		for num, items in enumerate(positions):
			label = ttk.Label(pastRos, text = items, font = ("Times", "24", "bold"), anchor = "center", relief = "groove")
			label.grid(row = num_row[0]+1, column = num_col[0]+num, sticky = "nesw", ipadx = 10)

		### QB table
		qb_listBox = tk.Listbox(pastRos)
		qbs = [items for items in displayRos if items[2] == "QB"]
		if len(qbs) > 0:
			[qb_listBox.insert(num, (items[1].replace(".",""), items[0])) for num, items in enumerate(qbs)]
			qb_listBox.grid(row = num_row[0]+2, column = num_col[0], sticky = "nwes")
		
		else: 
			qb_listBox.insert(0, "None")
			qb_listBox.grid(row = num_row[0]+2, column = num_col[0], sticky = "nwes")


		### RB table
		rb_listBox = tk.Listbox(pastRos)
		rbs = [items for items in displayRos if items[2] == "RB"]
		if len(rbs) > 0:
			[rb_listBox.insert(num, (items[1].replace(".",""), items[0])) for num, items in enumerate(rbs)]
			rb_listBox.grid(row = num_row[0]+2, column = num_col[0]+1, sticky = "nwes")
		
		else: 
			rb_listBox.insert(0, "None")
			rb_listBox.grid(row = num_row[0]+2, column = num_col[0]+1, sticky = "nwes")

		### WR table
		wr_listBox = tk.Listbox(pastRos)
		wrs = [items for items in displayRos if items[2] == "WR"]
		if len(wrs) > 0:
			[wr_listBox.insert(num, (items[1].replace(".",""), items[0])) for num, items in enumerate(wrs)]
			wr_listBox.grid(row = num_row[0]+2, column = num_col[0]+2, sticky = "nwes")
			
		else:
			wr_listBox.insert(0, "None")
			wr_listBox.grid(row = num_row[0]+2, column = num_col[0]+2, sticky = "nwes")


		### TE table
		te_listBox = tk.Listbox(pastRos)
		tes = [items for items in displayRos if items[2] == "TE"]
		if len(tes) > 0:
			[te_listBox.insert(num, (items[1].replace(".",""), items[0])) for num, items in enumerate(tes)]
			te_listBox.grid(row = num_row[0]+2, column = num_col[0]+3, sticky = "nwes")
	
		else: 
			te_listBox.insert(0, "None")
			te_listBox.grid(row = num_row[0]+2, column = num_col[0]+3, sticky = "nwes")


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
		return

	### Creating drop down of team names
	ttk.Label(pastRos, text = "Select a team: ", anchor = "center", relief = "groove").grid(row = num_row[0], column = num_col[0], sticky = "nesw")
	team = ttk.Combobox(pastRos, values = team_names_gap, state="readonly")
	team.grid(row = num_row[0], column = num_col[0]+1,  sticky = "nesw")

	### Creating drop down of team names
	ttk.Label(pastRos, text = "Select a Year: ", anchor = "center", relief = "groove").grid(row = num_row[0], column = num_col[0]+2, sticky = "nesw")
	year = ttk.Combobox(pastRos, values = yearKeys, state="readonly")
	year.grid(row = num_row[0], column = num_col[0]+3, sticky = "nesw")

	### Binding on enter(return)
	pastRos.bind("<Return>", displayTeam)

	### Creating needed buttons
	ttk.Button(pastRos, text = "Submit", command = displayTeam).grid(row = num_row[-1], column = 2, sticky = "nesw")
	ttk.Button(pastRos, text = "Exit", command = pastRos.destroy).grid(row = num_row[-1], column = 3, sticky = "nesw")
	pastRos.mainloop()
	return

#####################################################################################################################################
def warning(tk, ttk):
	"""Creates a warning for users at first use of the program until they hit accept."""
	warn = tk.Tk()
	warn.wm_title("Warning!!!")
	
	def accept():
		"""Saves the fact they accepted the warning, Therefore, they never have to see the warning again."""
		warn.destroy()
		quit()		
		return

	def decline():
		"""If they decline the warning, quits out of the program completely. And will do so until they accept."""
		warn.destroy()
		quit()		
		return
	### Creating buttons for the select favorite team pop up
	ttk.Button(warn, text = "Accept", command = accept).grid(row = 3, column = 0, sticky = "nesw")
	ttk.Button(warn, text = "Decline", command = decline).grid(row = 4, column = 0, sticky = "nesw")
#	while True:
#		continue
	return

#####################################################################################################################################
def select_favorite_team(favTeam, favTeamStatsView, listBox, favLst, current_rosters, team_stats, team_names_gap, tk, ttk):
	"""Allows the user to select their favorite team. Favorite team is relative to start/home page."""
	### Setting up pop up for favorite team select
	fav_team = tk.Tk()
	fav_team.wm_title("Favorite Team")

	### Creating current favorite team
	favTeamVar = tk.StringVar(fav_team)
	favTeamVar.set(favTeam.get())

	### Creating drop down information
	dropDownL = ttk.Label(fav_team, text="Select Favorite Team:", relief = "groove", anchor = "center")
	dropDownL.grid(row = 0, column = 0, sticky = "nesw", ipadx = 50, ipady = 5)
	dropDownM = ttk.OptionMenu(fav_team, favTeamVar, *team_names_gap)
	dropDownM.grid(row = 1, column = 0, sticky = "nesw")

	def saveFavTeam():
		### Resetting variables
		favTeam.set(favTeamVar.get())
		favTeamStats = team_stats[favTeamVar.get().replace(" ","_")] 
		favTeamStatsTmp = [items[idx] for items in favTeamStats[-6:] for idx in (0,2,3,8,9,12,13,19)]
		[favTeamStatsView[num].set(items) for num, items in enumerate(favTeamStatsTmp)]
		favTeamRoster = current_rosters[favTeam.get().replace(" ","_")]

		### Resitting listbox varibles
		tmpQBs = [(QBs[1].replace(".",""), QBs[0], QBs[3]) for QBs in favTeamRoster if "QB" in QBs]
		tmpRBs = [(RBs[1].replace(".",""), RBs[0], RBs[3]) for RBs in favTeamRoster if "RB" in RBs]
		tmpWRs = [(WRs[1].replace(".",""), WRs[0], WRs[3]) for WRs in favTeamRoster if "WR" in WRs]
		tmpTEs = [(TEs[1].replace(".",""), TEs[0], TEs[3]) for TEs in favTeamRoster if "TE" in TEs]
		listBox["QB"].set(value = [(items[1].replace(".",""), items[0]) for items in favTeamRoster if "QB" in items])
		listBox["RB"].set(value = [(items[1].replace(".",""), items[0]) for items in favTeamRoster if "RB" in items]) 
		listBox["WR"].set(value = [(items[1].replace(".",""), items[0]) for items in favTeamRoster if "WR" in items]) 
		listBox["TE"].set(value = [(items[1].replace(".",""), items[0]) for items in favTeamRoster if "TE" in items]) 
		[favLst["QB"][num].set(items) for num, items in enumerate(tmpQBs)]
		[favLst["RB"][num].set(items) for num, items in enumerate(tmpRBs)]
		[favLst["WR"][num].set(items) for num, items in enumerate(tmpWRs)]
		[favLst["TE"][num].set(items) for num, items in enumerate(tmpTEs)]

		### Changeing favorite team in the database
		update_fav_team(favTeamVar.get())
		fav_team.destroy()
		pop_up_msg("Favorite team was updated.", "Hopefully you didn't pick philly...")
		return

	### Creating buttons for the select favorite team pop up
	ttk.Button(fav_team, text = "Save & Exit", command = saveFavTeam).grid(row = 3, column = 0, sticky = "nesw")
	ttk.Button(fav_team, text = "Exit", command = fav_team.destroy).grid(row = 5, column = 0, sticky = "nesw")
	fav_team.mainloop()
	return

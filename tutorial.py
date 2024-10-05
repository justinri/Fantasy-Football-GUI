from help_options import pop_up_msg, emailMe, gamblingCal
from savingInfo import saveResults
from fun_file import all_players_stats, past_ros, stats_pop_up, team_stats_pop_up, select_favorite_team
from trade import tradeEvalu
from settings import mock_draft_settings

### Creating default fonts
lFont = ("Helvetica", 10, "bold")
norm_font = ("Times", 10)
small_font = ("Times", 12, "bold")

#####################################################################################################################################

def tutorial(tutItems, fav_team_var, tk, ttk):
	"""Creates a walk through tutorial for users to learn the program. Also has a FAQ."""

	### Items to pass in:
	statsForTut = tutItems[0]
	combResultTut = tutItems[1]
	team_stats = tutItems[2]
	fav_team = tutItems[3]
	team_names_gap = tutItems[4]
	licensingStr = tutItems[5]
	creatorStr = tutItems[6]
	bio_and_combine = tutItems[7]
	players_stats = tutItems[8]
	current_rosters = tutItems[9]
	past_rosters = tutItems[10]
	currentRos = tutItems[10]
	dicTotal = tutItems[11]

#####################################################################################################################################
	def help_help(skipToPage, preTut = None):
		### If we skip ahead, homeTut will not be maded
		try: preTut.destroy()
		except AttributeError: pass

		helpTut = tk.Tk()
		helpTut.wm_title("Help Help :)")

		helpMess = ["1) Update: This is just a button to update the database. All software updates will be done via the website.",
					"2) Email Me: This allows for direct contact with the creator. There are three options, please pick one that fits your email best. The three options are: General, Got an Idea?, and Bug?.",
					"3) Tutorial: If you got this far, you clearly know how this works....",
					"4) About the Creator: This is just a quick blurb about the creator.",
					"5) Licensing Info: Allows the user to understand the licensing infomation associated with this software."]

		### Creating message boxes
		tk.Message(helpTut, text=helpMess[0], relief="groove", font=lFont,anchor="w",width=700).grid(row=0, column=0, columnspan=3, sticky="nesw")
		tk.Message(helpTut, text=helpMess[1], relief="groove", font=lFont,anchor="w",width=700).grid(row=2, column=0,columnspan=3, sticky="nesw")
		tk.Message(helpTut, text=helpMess[2], relief="groove", font=lFont,anchor="w",width=700).grid(row=4, column=0, columnspan=3,sticky="nesw")
		tk.Message(helpTut,text=helpMess[3],relief="groove",font=lFont,anchor="w",width=700).grid(row=5, column=0,columnspan=3, sticky = "nesw")
		tk.Message(helpTut,text=helpMess[4],relief="groove",font=lFont,anchor="w",width=700).grid(row=7, column=0,columnspan=3, sticky = "nesw")

		### Creating button for this help tutorial
		tk.Button(helpTut, text="Update",font=lFont,command=lambda:pop_up_msg("Not live yet")).grid(row=1, column = 1, sticky = "nesw")
		tk.Button(helpTut, text="General",font=lFont,command=lambda:emailMe("General")).grid(row=3, column = 0, sticky = "nesw")
		tk.Button(helpTut, text="Got an Idea?",font=lFont,command=lambda:emailMe("Idea")).grid(row=3, column = 1, sticky = "nesw")
		tk.Button(helpTut, text="Bug?",font=lFont,command=lambda:emailMe("Bug")).grid(row=3, column = 2, sticky = "nesw")
		creStr = "About the Creator"
		linStr = "Licensing Info"
		tk.Button(helpTut, text=creStr,font=lFont,command=lambda:pop_up_msg(creatorStr, creStr)).grid(row=6, column = 1, sticky="nesw")
		tk.Button(helpTut, text=linStr,font=lFont,command=lambda:pop_up_msg(licensingStr, linStr)).grid(row=8, column = 1, sticky="nesw")

	

		### Finishing up the mini instance with an exit and next button
		tk.Button(helpTut, text="Exit", font=lFont, command = helpTut.destroy).grid(row=8, column = 2, sticky = "nesw")
		helpTut.mainloop()
		return

#####################################################################################################################################
	def mock_draft_help(skipToPage, preTut = None):
		### If we skip ahead, homeTut will not be maded
		try: preTut.destroy()
		except AttributeError: pass

		### Skipping ahead if they do not want a complete overview
		if skipToPage in ["help"]:
			help_help(skipToPage)
			return

		### Creating mini instance for Stats Predictions help page
		mockTut = tk.Tk()
		mockTut.wm_title("Mock Draft Help")

		mess = ["1) Mock Drafts: This is the tab that takes you to the mock draft page.",
				"2) Mock Drafts Parameters: This tab pops up a window that allows you to change values for calculating fantasy points.\n			 Note: These are the same values used for the plotting page.",
				'On the Mock Draft Page:\n	Coming soon...']

		### Creating message boxes
		tk.Message(mockTut, text=mess[0], relief="groove", font=lFont,anchor="w",width=800).grid(row=0, column=0, columnspan = 3, sticky = "nesw")
		tk.Message(mockTut, text=mess[1], relief="groove", font=lFont,anchor="w",width=800).grid(row=1, column=0,columnspan=3, sticky="nesw")
		tk.Message(mockTut, text=mess[2], relief="groove", font=lFont,anchor="w",width=800).grid(row=3, column=0,columnspan=3, sticky="nesw")

		### Creating button for this help tutorial
		tk.Button(mockTut, text="Plotting Parameters",font=lFont,command= lambda:mock_draft_settings("mock")).grid(row=2, column=1, sticky="nesw")

		### Finishing up the mini instance with an exit and next button
		tk.Button(mockTut, text="Next", font=lFont, command = lambda: help_help(skipToPage, mockTut)).grid(row=4, column=0, sticky="nesw")
		tk.Button(mockTut, text="Exit", font=lFont, command = mockTut.destroy).grid(row=4, column=2, sticky = "nesw")
		mockTut.mainloop()
		return

#####################################################################################################################################
	def plot_comp_help(skipToPage, preTut = None):
		### If we skip ahead, homeTut will not be maded
		try: preTut.destroy()
		except AttributeError: pass

		### Skipping ahead if they do not want a complete overview
		if skipToPage in ["mock", "help"]:
			mock_draft_help(skipToPage)
			return

		### Creating mini instance for Stats Predictions help page
		plotTut = tk.Tk()
		plotTut.wm_title("Plotting Comparison Help")

		mess = ["1) Plotting Page: This is the tab that takes you to the plotting page.",
				"2) Plotting Parameters: This tab pops up a window that allows you to change values for calculating fantasy points.\nNote: These are the same values used for mock drafts.",
				'On the Plotting Page:\n	The user can plot up to four players (positions can be different).\n	To select a player, pick from the drop down menu(s).\n	This menu can be ordered from the buttons below it.\n	To change the positions for that box, click on the check box above the drop down menu(s).\n	The default position is QB and the default ordering is "Order by Last Year\'s Fantasy points"']

		### Creating message boxes
		tk.Message(plotTut, text=mess[0], relief="groove", font=lFont,anchor="w",width=800).grid(row=0, column=0, columnspan = 3, sticky = "nesw")
		tk.Message(plotTut, text=mess[1], relief="groove", font=lFont,anchor="w",width=800).grid(row=1, column=0,columnspan=3, sticky="nesw")
		tk.Message(plotTut, text=mess[2], relief="groove", font=lFont,anchor="w",width=800).grid(row=3, column=0,columnspan=3, sticky="nesw")

		### Creating button for this help tutorial
		tk.Button(plotTut, text="Plotting Parameters",font=lFont,command= lambda:mock_draft_settings("plots")).grid(row=2, column=1, sticky="nesw")

		### Finishing up the mini instance with an exit and next button
		tk.Button(plotTut, text="Next", font=lFont, command = lambda: mock_draft_help(skipToPage, plotTut)).grid(row=4, column=0, sticky="nesw")
		tk.Button(plotTut, text="Exit", font=lFont, command = plotTut.destroy).grid(row=4, column = 2, sticky = "nesw")
		plotTut.mainloop()
		return

#####################################################################################################################################
	def stats_predict_help(skipToPage, preTut = None):
		### If we skip ahead, homeTut will not be maded
		try: preTut.destroy()
		except AttributeError: pass

		### Skipping ahead if they do not want a complete overview
		if skipToPage in ["plot", "mock", "help"]:
			plot_comp_help(skipToPage)
			return

		### Creating mini instance for Stats Predictions help page
		predictTut = tk.Tk()
		predictTut.wm_title("Stats Predictions Help")
		ttk.Label(predictTut, text = "Not Live Yet...", font=lFont).grid(row=0,column=0,columnspan=2,ipadx = 100, sticky="nesw")

		### Finishing up the mini instance with an exit and next button
		tk.Button(predictTut, text="Next",font=lFont,command=lambda: plot_comp_help(skipToPage, predictTut)).grid(row=1, column=0, sticky="nesw")
		tk.Button(predictTut, text="Exit",font=lFont, command=predictTut.destroy).grid(row=1, column = 1, sticky = "nesw")
		predictTut.mainloop()
		return

#####################################################################################################################################
	def home_page_help(skipToPage, preTut = None):
			### If we skip ahead, fileTut will not be maded
			try: preTut.destroy()
			except AttributeError: pass

			### Skipping ahead if they do not want a complete overview
			if skipToPage in ["stats", "plot", "mock", "help"]:
				stats_predict_help(skipToPage)
				return

			### Creating mini instance for home help page
			homeTut = tk.Tk()
			homeTut.wm_title('Home Page Help')

			mess = \
	   ['1) Home: Just takes you to the home page.',
		'2) Favorite Team: Allows you to select your favorite team.\n		To view this, click "Set Favorite Team" button below.',
		'On this Page:\n	You see the fantasy players of your favorite team.\n	If you double click on their name, you can see their stats via a pop up display.\n	In this display, there is also a "Combine Results" button.\n	If this is clicked, you can view their combine results and draft information.\n	To view an example, click "View Player\'s Stats" button below',
		'Next:\n	Is your favorite teams\' stats over the last three years.\n	Followed by, their opponents\' stats against them.',
		'Next:\n	Is a button to see your favorite teams\' complete stats.\n	This button is called, creatively, "Complete Team Stats".\n	To View this, click the "Complete Team Stats" below.',
		'Lasty:\n	Is a button that takes you to the website, where presumably, you downloaded this from.\n	To go there now, click the "Click to view website and for more information" button below.']


			### Creating message boxes
			tk.Message(homeTut, text=mess[0], relief="groove", font=lFont,anchor="w",width=700).grid(row=0, column=0,columnspan=3, sticky="nesw")
			tk.Message(homeTut, text=mess[1], relief="groove", font=lFont,anchor="w",width=700).grid(row=1, column=0,columnspan=3, sticky="nesw")
			tk.Message(homeTut, text=mess[2], relief="groove", font=lFont,anchor="w",width=700).grid(row=3, column=0, columnspan=3,sticky="nesw")
			tk.Message(homeTut, text=mess[3], relief="groove", font=lFont,anchor="w",width=700).grid(row=5, column=0, columnspan=3,sticky="nesw")
			tk.Message(homeTut, text=mess[4], relief="groove", font=lFont,anchor="w",width=700).grid(row=6, column=0, columnspan=3,sticky="nesw")
			tk.Message(homeTut, text=mess[5], relief="groove", font=lFont,anchor="w",width=700).grid(row=8, column=0, columnspan=3,sticky="nesw")

			### Creating button for this tutorial
			tmpButton = tk.Button(homeTut, text="Set Favorite Team", font=lFont,
								  command =	lambda: select_favorite_team(fav_team, fav_team_var, team_names_gap, tk, ttk))
			tmpButton.grid(row=2, column = 1, sticky = "nesw")
			tmpButton = tk.Button(homeTut, text="View Player's Stats",font=lFont,command=lambda:stats_pop_up("QB",statsForTut,combResultTut,tk,ttk))
			tmpButton.grid(row=4, column = 1, sticky = "nesw")
			tmpButton = tk.Button(homeTut, text="Complete Team Stats",font=lFont, 
					   			  command=lambda: team_stats_pop_up(team_stats,team_names_gap,tk,ttk))
			tmpButton.grid(row=7, column = 1, sticky = "nesw")
			tmpButton = tk.Button(homeTut, text="Click to view website and for more information",font=lFont, 
					   			  command=lambda: pop_up_msg("Website not up yet..."))
			tmpButton.grid(row=9, column = 1, sticky = "nesw")
			tk.Button(homeTut, text="Next",font=lFont,command=lambda:stats_predict_help(skipToPage,homeTut)).grid(row=9, column=0, sticky="nesw")
			tk.Button(homeTut, text="Exit", font=lFont, command = homeTut.destroy).grid(row=9, column = 2, sticky = "nesw")
			homeTut.mainloop()
			return


#####################################################################################################################################
	def file_help(skipToPage):
		### Skipping ahead if they do not want a complete overview
		if skipToPage in ["home", "stats", "plot", "mock", "help"]:
			home_page_help(skipToPage)
			return

		### Creating mini instance for file tab
		fileTut = tk.Tk()					
		fileTut.wm_title('File Tab Help')

		Mess = ["1) Select a Sport: This is where you select what sport you want. Currently, only football is supported.",
				"2) Trade Evaluator: This allows you to evaluate potential trades.\n    (Double click in the white boxes to select players,\n    you can also double click on the player to view their stats.)",
				"3) Gambling Calculator: This is where you can see how to split up the pot for fantasy.\n    If gambling is illegal in your country/state, then this calculator is for hypothetical purposes only ;)...",
				"4) Players Stats: Allows the user to look up player stats by name (First and Last).\n    If the same position has multiple players with the same name, a drop down menu will appear.\n    This list includes their birthday to ensure you have the correct player.",
				"5) Past Starters: Allows you to select a year and a team to view their starters at that time.",
				"6) Save: There is three types of data you can save: Prediction Stats, Last Year's Stats, and Fantasy Information.\n    For each, you can select by position or can select all players.\n    For the buttons below, all players is selected. This data can be saved to your computer via four formats\n    options: csv, ods, txt, and xlsx...",
				"7) Exit: Allows you to leave the program..."]

		### Creating message boxes
		tk.Message(fileTut, text=Mess[0], relief="groove", font=lFont,anchor="w",width=700).grid(row=0, column=0, columnspan = 3, sticky = "nesw")
		tk.Message(fileTut, text=Mess[1], relief="groove", font=lFont,anchor="w",width=700).grid(row=1, column=0,columnspan=3, sticky="nesw")
		tk.Message(fileTut, text=Mess[2], relief="groove", font=lFont,anchor="w",width=700).grid(row=3, column=0, columnspan=3,sticky="nesw")
		tk.Message(fileTut,text=Mess[3],relief="groove",font=lFont,anchor="w",width=700).grid(row=5, column=0,columnspan=3, sticky = "nesw")
		tk.Message(fileTut,text=Mess[4],relief="groove",font=lFont,anchor="w",width=700).grid(row=7, column=0,columnspan=3, sticky = "nesw")
		tk.Message(fileTut, text=Mess[5], relief="groove", font=lFont,anchor="w",width=700).grid(row=9, column=0, columnspan=3,sticky="nesw")
		tk.Message(fileTut,text=Mess[6],relief="groove",font=lFont,anchor="w",width=700).grid(row=11, column=0,columnspan=3, sticky = "nesw")

		### Creating button for this help tutorial
		tk.Button(fileTut, text="Trade Evaluator",font=lFont,command=
			lambda: tradeEvalu(bio_and_combine, players_stats, dicTotal, tk, ttk)).grid(row=2, column = 1, sticky = "nesw")
		tk.Button(fileTut, text="Gambling Calculator",font=lFont,command = gamblingCal).grid(row=4, column = 1, sticky = "nesw")
		tk.Button(fileTut, text="Players Stats",font=lFont,command = 
			lambda: all_players_stats(bio_and_combine, players_stats, tk, ttk)).grid(row=6, column = 1, sticky = "nesw")
		tk.Button(fileTut, text="Past Starters",font=lFont,command = 
			lambda: past_ros(team_names_gap,current_rosters,past_rosters,bio_and_combine, players_stats, tk,ttk)).grid(row=8, column=1,sticky="nesw")
		tk.Button(fileTut, text="Save\nPrediction Stats",font=lFont,command = 
			lambda: pop_up_msg("Not Yet Supported")).grid(row=10, column = 0, sticky = "nesw")
		tk.Button(fileTut, text="Save\nLast Year's Stats",font=lFont,command = 
			lambda: saveResults("allPlayers", players_stats, "lastStats")).grid(row=10, column = 1, sticky = "nesw")
		tk.Button(fileTut, text="Save\nFantasy Information",font=lFont,command = 
			lambda: saveResults("allPlayers", players_stats, "fanStats", currentRos)).grid(row=10, column = 2, sticky = "nesw")

		### Finishing up the mini instance with an exit and next button
		tk.Button(fileTut, text="Next", font=lFont, command = lambda: home_page_help(skipToPage, fileTut)).grid(row=12, column=0, sticky="nesw")
		tk.Button(fileTut, text="Exit\n(Pop Up)", font=lFont, command = fileTut.destroy).grid(row=12, column = 2, sticky = "nesw")
		fileTut.mainloop()
		return

#####################################################################################################################################
	### For gridding
	row_num = (0,10)
	col_num = row_num

	tut = tk.Tk()
	tut.wm_title("Tutorial")
	label = tk.Label(tut, text = "What do you need help with?\n(Click a button below)", font = norm_font, anchor = "center", relief = "raised")
	label.grid(row = row_num[0], column = col_num[0], sticky = "nesw", ipadx = 10, ipady = 5)

	### Creating the help buttons
	ttk.Button(tut, text = "Complete Overview?", command=lambda:file_help("complete")).grid(row=row_num[0]+1, column=col_num[0], sticky="nesw")
	ttk.Button(tut, text = "File Menu?", command=lambda: file_help("file")).grid(row = row_num[0]+2, column = col_num[0], sticky = "nesw")
	ttk.Button(tut, text = "Home Page?", command = lambda: file_help("home")).grid(row = row_num[0]+3, column = col_num[0], sticky = "nesw")
	ttk.Button(tut, text = "Stats Predictions?", command=lambda:file_help("stats")).grid(row=row_num[0]+4, column=col_num[0], sticky="nesw")
	ttk.Button(tut, text = "Plotting Comparison?", command=lambda:file_help("plot")).grid(row=row_num[0]+5, column=col_num[0], sticky="nesw")
	ttk.Button(tut, text = "Mock Drafts?", command=lambda:file_help("mock")).grid(row = row_num[0]+6, column = col_num[0], sticky = "nesw")
	ttk.Button(tut, text = "Help?", command=lambda:file_help("help")).grid(row = row_num[0]+7, column = col_num[0], sticky = "nesw")

	### Finish the pop for tutorial
	ttk.Button(tut, text = "Exit", command = tut.destroy).grid(row = row_num[0]+8, column = col_num[0], sticky = "nesw")
	tut.mainloop()
	return

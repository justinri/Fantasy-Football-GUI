### Justin is Awesome
import tkinter as tk
from tkinter import ttk  ### Kind of like the CSS for tkinter
import matplotlib
matplotlib.use("TkAgg")  ### Backend of matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation ### Only needed if I want to make the graph live??
from datetime import datetime
from tkinter import messagebox
import sys
curYear = datetime.now().year

### My files
from help_options import *
from create_plots import *
from settings import *
from fun_file import *
from save_data_db import update_fav_team
from mockFun import mockData
from savingInfo import *
from tutorial import tutorial
from mockdraft import showMockDraft
from trade import tradeEvalu 

### Import data
from data_open import get_data
team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats, fav_team = get_data()

### Information for selecting your favorite team
team_names_gap = [team.replace('_',' ') for team in team_names]
team_names_gap.insert(0, team_names_gap[team_names_gap.index(fav_team)])

### Getting players from your favorite team
favTeamIdx = fav_team.replace(" ","_")
favTeamRoster = current_rosters[favTeamIdx]
fav_QBs = [(QBs[1].replace(".",""), QBs[0], QBs[3]) for QBs in favTeamRoster if "QB" in QBs]
fav_RBs = [(RBs[1].replace(".",""), RBs[0], RBs[3]) for RBs in favTeamRoster if "RB" in RBs]
fav_WRs = [(WRs[1].replace(".",""), WRs[0], WRs[3]) for WRs in favTeamRoster if "WR" in WRs]
fav_TEs = [(TEs[1].replace(".",""), TEs[0], TEs[3]) for TEs in favTeamRoster if "TE" in TEs]

### Current list of current rosters with the first item being the team name
tmp = [[items.replace("_", " "), item] for items in current_rosters.keys() for item in current_rosters[items]]
currentRos = {"QB": [items for items in tmp if "QB" == items[1][2]]}
currentRos.update({"RB" : [items for items in tmp if "RB" == items[1][2]]})
currentRos.update({"WR" : [items for items in tmp if "WR" == items[1][2]]})
currentRos.update({"TE" : [items for items in tmp if "TE" == items[1][2]]})

### Getting stats from favorite team/players
favTeamStatsView = [items[idx] for items in team_stats[favTeamIdx][-6:] for idx in (0,2,3,8,9,12,13,19)]

### Import stats in the correct format
dicTotal = mockData(players_stats, currentRos, returnAll = True)	

### Creating default fonts
large_font = ("Helvetica", 12)
norm_font = ("Helvetica", 10)
small_font = ("Helvetica", 8)
sFont = small_font

### Allows users to close windows and stop the process of the gui.
def closing():
	if tk.messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
		GUI.destroy
		sys.exit()
	return

class Fantasy_GUI(tk.Tk):
	def __init__(self, *args, **kwargs):

		### Initializing tkinker too
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "587846-47-2937663")

		### Setting up needed variables
		self.favTeam = tk.StringVar(self)
		self.favTeam.set(fav_team)
		self.favTeamStatsView = [tk.StringVar(self) for num in range(len(favTeamStatsView))]
		[self.favTeamStatsView[num].set(items) for num, items in enumerate(favTeamStatsView)]
		self.listBox = {"QB" : tk.StringVar(self, value = [items[:2] for items in fav_QBs]),
						"RB" : tk.StringVar(self, value = [items[:2] for items in fav_RBs]), 
						"WR" : tk.StringVar(self, value = [items[:2] for items in fav_WRs]), 
						"TE" : tk.StringVar(self, value = [items[:2] for items in fav_TEs])} 
		self.favLst = {"QB" : [tk.StringVar(self) for _ in range(25)], ### 25 was choosen, because a no position would have that many players
					   "RB" : [tk.StringVar(self) for _ in range(25)], 
					   "WR" : [tk.StringVar(self) for _ in range(25)],
					   "TE" : [tk.StringVar(self) for _ in range(25)]}
		[self.favLst["QB"][num].set(items) for num, items in enumerate(fav_QBs)]
		[self.favLst["RB"][num].set(items) for num, items in enumerate(fav_RBs)]
		[self.favLst["WR"][num].set(items) for num, items in enumerate(fav_WRs)]
		[self.favLst["TE"][num].set(items) for num, items in enumerate(fav_TEs)]

		### Creating a container for the frames		
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand = True) ### Pack to the top, fill all the packing area. Expand if more white space exist
		container.grid_rowconfigure(0, weight = 1) 	### 0, is the minimum size, Weight is giving priority when given different number
		container.grid_columnconfigure(0, weight = 1)

		### Creates menu bar and file tap		
		menu_bar = tk.Menu(container)
		file_menu = tk.Menu(menu_bar, tearoff = 0)
		
		### Create submenu for select a sport
		subMenu = tk.Menu(self, tearoff = 1)
		subMenu.add_command(label="NFL", command = lambda: pop_up_msg("Dude, you're already here..."))
		subMenu.add_command(label="NBA", command = lambda: pop_up_msg("Not Yet Supported"))
		subMenu.add_command(label="MLB", command = lambda: pop_up_msg("Not Yet Supported"))
		subMenu.add_command(label="NHL", command = lambda: pop_up_msg("Not Yet Supported"))
		file_menu.add_cascade(label = "Select a Sport", menu = subMenu)
	
#### add wwarning here about gambling
		file_menu.add_command(label = "Trade Evaluator", command = lambda: tradeEvalu(bio_and_combine, players_stats, dicTotal, tk, ttk))
		file_menu.add_command(label = "Gambling Calculator", command = gamblingCal)
		file_menu.add_separator()  ### Adds a separator
		file_menu.add_command(label = "Players Stats", command = lambda: all_players_stats(bio_and_combine, players_stats, tk, ttk))
		file_menu.add_command(label = "Past Starters", 
							  command = lambda: past_ros(team_names_gap, current_rosters, past_rosters, bio_and_combine, players_stats, tk, ttk))
		file_menu.add_separator()  ### Adds a separator

		### Create submenu for saving stats
		subMenuSave = tk.Menu(self, tearoff = 0)
		subMenuSave.add_command(label="Prediction Stats", command = lambda: pop_up_msg("Not Yet Supported"))
		file_menu.add_cascade(label = "Save", menu = subMenuSave)

		### Create submenu for saving what position
		subMenuPos = tk.Menu(self, tearoff = 1)
		subMenuPos.add_command(label="All Players", command = lambda: saveResults("allPlayers", players_stats, "lastStats"))
		subMenuPos.add_command(label="QBs", command = lambda: saveResults("QB", players_stats, "lastStats"))
		subMenuPos.add_command(label="RBs", command = lambda: saveResults("RB", players_stats, "lastStats"))
		subMenuPos.add_command(label="WRs", command = lambda: saveResults("WR", players_stats, "lastStats"))
		subMenuPos.add_command(label="TEs", command = lambda: saveResults("TE", players_stats, "lastStats"))
		subMenuSave.add_cascade(label = "Last Year's Stats", menu = subMenuPos)

		### Create submenu for saving what position
		subMenuPosFan = tk.Menu(self, tearoff = 1)
		subMenuPosFan.add_command(label="All Players", command = lambda: saveResults("allPlayers", players_stats, "fanStats", currentRos))
		subMenuPosFan.add_command(label="QBs", command = lambda: saveResults("QB", players_stats, "fanStats", currentRos))
		subMenuPosFan.add_command(label="RBs", command = lambda: saveResults("RB", players_stats, "fanStats", currentRos))
		subMenuPosFan.add_command(label="WRs", command = lambda: saveResults("WR", players_stats, "fanStats", currentRos))
		subMenuPosFan.add_command(label="TEs", command = lambda: saveResults("TE", players_stats, "fanStats", currentRos))
		subMenuSave.add_cascade(label="Fantasy Information", menu = subMenuPosFan)
		
#		file_menu.add_separator()  ### Adds a separator
		file_menu.add_command(label = "Exit", command = closing)
		menu_bar.add_cascade(label="File", menu = file_menu)

		### Creating Main tap
		main_menu = tk.Menu(menu_bar, tearoff = 0)
		main_menu.add_command(label = "Home", command = lambda: self.show_frame(Start_Page))
		main_menu.add_command(label = "Favorite Team", command = lambda: select_favorite_team(self.favTeam, self.favTeamStatsView, 
													   self.listBox, self.favLst, current_rosters, team_stats, team_names_gap, tk, ttk))
		menu_bar.add_cascade(label = "Home", menu = main_menu)

		### Creating Stats prediction tap
		stats_menu = tk.Menu(menu_bar, tearoff = 0)
		stats_menu.add_command(label = "Stats Predictions Page", command = lambda: self.show_frame(Stats_Prediction_Page))
		stats_menu.add_command(label = "Stats Predictions Parameters", command = lambda: pop_up_msg("Not Yet Supported"))
		menu_bar.add_cascade(label = "Stats Predictions", menu = stats_menu)

		### Creating plots tap
		plot_menu = tk.Menu(menu_bar, tearoff = 0)
		plot_menu.add_command(label = "Plotting Page", command = lambda: self.show_frame(Plotting_Page))
		plot_menu.add_command(label = "Plotting Parameters", command = lambda: mock_draft_settings("plots"))
		menu_bar.add_cascade(label = "Plotting Comparison", menu = plot_menu)

		### Creating mock tap
		mock_menu = tk.Menu(menu_bar, tearoff = 0)
		mock_menu.add_command(label = "Mock Drafts", command = lambda: self.show_frame(Mock_Draft_Page))
		mock_menu.add_command(label = "Mock Drafts Parameters", command = lambda: mock_draft_settings("mock"))
		menu_bar.add_cascade(label = "Mock Drafts", menu = mock_menu)

		### Creating Help tap
		help_menu = tk.Menu(menu_bar, tearoff = 0)
		help_menu.add_command(label = "Update", command = lambda: pop_up_msg("Not Yet Supported"))

		### Create submenu for select a emails
		subMenuEmail = tk.Menu(self, tearoff = 0)
		subMenuEmail.add_command(label="General", command = lambda:  emailMe("General"))
		subMenuEmail.add_command(label="Got an idea?", command = lambda:  emailMe("Idea"))
		subMenuEmail.add_command(label="Bug?", command = lambda: emailMe("Bug"))
		help_menu.add_cascade(label = "Email Me?", menu = subMenuEmail)

		### Tutorial part of the help menu
		creatorStr = "Just a dude with a laptop..."
		licensingStr = "I don't know yet, perhaps MIT.....\nbut (almost) for sure a copyleft license..."
		statsForTut = [items for items in players_stats["QB"] if items[0] == "Romo" if items[1] == "Tony" if items[2] == 1980]
		combResultTut = [items for items in bio_and_combine["QB"] if items[4] == "Romo" if items[5] == "Tony" if items[6] == 1980]
		tutItems = (statsForTut, combResultTut, team_stats, fav_team,  team_names_gap, licensingStr, creatorStr, bio_and_combine, players_stats,\
					current_rosters,past_rosters, currentRos, dicTotal)
		help_menu.add_command(label = "Tutorial", command = lambda: tutorial(tutItems, self.favTeam, tk, ttk))


		help_menu.add_command(label = "About the Creator", command = lambda: pop_up_msg(creatorStr,"About the Creator"))
		### rememeber to read the copyright for any License i pick
		help_menu.add_command(label = "Licensing Info", command = lambda: pop_up_msg(licensingStr,"Licensing Info"))
		menu_bar.add_cascade(label = "Help", menu = help_menu)

		### Adding menu bar
		tk.Tk.config(self, menu = menu_bar)

		### Empty dictionary to store frames
		### frames are windows you interact with 
		self.frames = {}
		for FRAMES in (Start_Page, Stats_Prediction_Page, Plotting_Page, Mock_Draft_Page):
			### Start page is the page we start on
			frame = FRAMES(container, self)
			self.frames[FRAMES] = frame

			### Sticky nsew will stretch everything to the size of the window
			frame.grid(row = 0, column = 0, sticky = "nsew")

		self.show_frame(Start_Page)
#		tk.Tk.iconbitmap(self, default="pic_name.ico")
		return

	def show_frame(self, cont):
		"""Raises the frame wanted to be current frame."""
		frame = self.frames[cont]
		### Raises frame to top
		frame.tkraise()
		return

#####################################################################################################################################
class Start_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller=controller

		#### Input for grids
		num_row = (0,10)
		num_col = num_row
		favTeam = self.controller.favTeam

#### put in a windows showing random facts about their favorite team

		### Setting up favorite team label
		homeL = tk.Label(self, textvariable = favTeam, font = ("Times", "24", "bold"), anchor = "center", relief = "groove")
		homeL.grid(row = num_row[0], column = num_col[0], columnspan = num_col[-1], sticky = "nesw")

		### Creating titles for the positions
		positions = ["Quarterbacks", "Running Backs", "Wide Receivers", "Tight Ends"]
		for num, items in enumerate(positions):
			posL = ttk.Label(self, text = items, font = ("Times", "24", "bold"), anchor = "center", relief = "groove")
			posL.grid(row = num_row[0]+1, column = num_col[0]+1+num, sticky = "nesw", ipadx = 10)

		### QB table
		qb_listBox = tk.Listbox(self, bg = "white", listvariable=self.controller.listBox["QB"])
		qb_listBox.grid(row = num_row[0]+2, column = num_col[0]+1, sticky = "nwes")

		### RB table
		rb_listBox = tk.Listbox(self, bg = "white", listvariable=self.controller.listBox["RB"])
		rb_listBox.grid(row = num_row[0]+2, column = num_col[0]+2, sticky = "nwes")

		### WR table
		wr_listBox = tk.Listbox(self, bg = "white", listvariable=self.controller.listBox["WR"])
		wr_listBox.grid(row = num_row[0]+2, column = num_col[0]+3, sticky = "nwes")

		### TE table
		te_listBox = tk.Listbox(self, bg = "white", listvariable=self.controller.listBox["TE"])
		te_listBox.grid(row = num_row[0]+2, column = num_col[0]+4, sticky = "nwes")

		### Shows stats to table, buggy, "Exception in Tkinter callback" why: "IndexError: tuple index out of range"?
		def pop_up_stats(event, pos):
			"""Selects the player that was doubled clicked, and has all their stats pop up. In an mini instance."""
			if pos == "QB":
				tmpClick = self.controller.favLst["QB"][int(qb_listBox.curselection()[0])].get()
				clicked = [tmpClick.split(",")[0][2:-1], tmpClick.split(",")[1][2:-1], int(tmpClick.split(",")[2].strip()[:-1])]
				playersStats = [player for player in players_stats["QB"] if clicked[0] and  clicked[1] in player if clicked[2] == player[2]]
				comb_results = [player for player in bio_and_combine["QB"] if clicked[0] and  clicked[1] in player if clicked[2] in player]

			elif pos == "RB":
				tmpClick = self.controller.favLst["RB"][int(rb_listBox.curselection()[0])].get()
				clicked = [tmpClick.split(",")[0][2:-1], tmpClick.split(",")[1][2:-1], int(tmpClick.split(",")[2].strip()[:-1])]
				playersStats = [player for player in players_stats["RB"] if clicked[0] and  clicked[1] in player if clicked[2] == player[2]]
				comb_results = [player for player in bio_and_combine["RB"] if clicked[0] and  clicked[1] in player if clicked[2] in player]

			elif pos == "WR":
				tmpClick = self.controller.favLst["WR"][int(wr_listBox.curselection()[0])].get()
				clicked = [tmpClick.split(",")[0][2:-1], tmpClick.split(",")[1][2:-1], int(tmpClick.split(",")[2].strip()[:-1])]
				playersStats = [player for player in players_stats["WR"] if clicked[0] and  clicked[1] in player if clicked[2] == player[2]]
				comb_results = [player for player in bio_and_combine["WR"] if clicked[0] and  clicked[1] in player if clicked[2] in player]

			else: ## Must be TE
				tmpClick = self.controller.favLst["TE"][int(te_listBox.curselection()[0])].get()
				clicked = [tmpClick.split(",")[0][2:-1], tmpClick.split(",")[1][2:-1], int(tmpClick.split(",")[2].strip()[:-1])]
				playersStats = [player for player in players_stats["TE"] if clicked[0] and  clicked[1] in player if clicked[2] == player[2]]
				comb_results = [player for player in bio_and_combine["TE"] if clicked[0] and  clicked[1] in player if clicked[2] in player]

			stats_pop_up(pos, playersStats, comb_results, tk, ttk)
			return

		### Listens for an event, doulbe click, to happen on the list box
		qb_listBox.bind('<Double-1>', lambda event: pop_up_stats(event, 'QB'))
		rb_listBox.bind('<Double-1>', lambda event: pop_up_stats(event, 'RB'))
		wr_listBox.bind('<Double-1>', lambda event: pop_up_stats(event, 'WR'))
		te_listBox.bind('<Double-1>', lambda event: pop_up_stats(event, 'TE'))

		### Creating gap between two sides, nothing
		tk.LabelFrame(self).grid(row = num_row[-1]-5, column = num_col[0], columnspan = num_col[-1], sticky = "nesw", pady = 10)

		### Starting the team stats section
		statsL = ttk.Label(self, text = "Team Stats", font = large_font, relief = "groove", anchor = "center")
		statsL.grid(row = num_row[-1]-4, column = num_col[0], columnspan = num_col[-1], sticky = "nsew", ipadx = 10, ipady = 5)

		favL = ttk.Label(self, textvariable = favTeam, font = large_font, relief = "groove", anchor = "center")
		favL.grid(row = num_row[-1]-2, column = num_col[0], columnspan = num_col[-1], sticky = "nsew", ipadx = 10, ipady = 5)

		### Create labels for team stats
		for_l = ["Year", "Total Points", "Total Yards", "Passing Yards", "Passing Touchdowns", "Rushing Yards", "Rushing TDs", "Points Per Drive"]
		for num, items in enumerate(for_l):
			favL = ttk.Label(self, text = items, font = small_font, relief = "groove", anchor = "center")
			favL.grid(row = num_row[-1]-1, column = num_col[0]+num, sticky = "nsew", ipadx = 10, ipady = 5)

		### Favorite team stats
		add1 = 32
		for num2 in range(0,3):
			for num3 in range(len(for_l)):
				statsL = ttk.Label(self,textvariable=self.controller.favTeamStatsView[num3+add1],font=sFont,relief="groove", anchor="center")
				statsL.grid(row = num_row[-1]+num2, column = num_col[0]+num3, sticky = "nsew", ipadx = 10, ipady = 5)
			add1 -= len(for_l)*2

		### Creating gap between two sides, nothing
		tk.LabelFrame(self).grid(row = num_row[-1]+num2+1, column = num_col[0], columnspan = num_col[-1], sticky = "nesw", pady = 20)

		#### Creating the seciotn for Opponents stats
		favL = ttk.Label(self, text = "Opponent's stats", font = large_font, relief = "groove", anchor = "center")
		favL.grid(row = num_row[-1]+num2+2, column = num_col[0], columnspan = num_col[-1], sticky = "nsew", ipadx = 10, ipady = 5)

		### Create labels for team stats
		for num, items in enumerate(for_l):
			favL = ttk.Label(self, text = for_l[num], font = small_font, relief = "groove", anchor = "center")
			favL.grid(row = num_row[-1]+num2+3, column = num_col[0]+num, sticky = "nsew", ipadx = 10, ipady = 5)

		add1 = 40
		for num4 in range(0,3):
			for num3 in range(len(for_l)):
				statsL = ttk.Label(self,textvariable=self.controller.favTeamStatsView[num3+add1],font=sFont,relief="groove", anchor="center")
				statsL.grid(row = num_row[-1]+num2+4+num4, column = num_col[0]+num3, sticky = "nsew", ipadx = 10, ipady = 5)
			add1 -= len(for_l)*2

		### Button for complete team stats
		compStats = ttk.Button(self, text="Complete Team Stats", command=lambda: team_stats_pop_up(favTeam, team_stats,team_names_gap,tk,ttk))
		compStats.grid(row = num_row[-1]+num2+5+num4, column = num_col[0], columnspan = num_col[-1], sticky = "we", ipady = 5, pady = 15)

		### Label to website
		webL = ttk.Button(self, text = "Click to view website and for more information", command = lambda: pop_up_msg("Website not up yet..."))
		webL.grid(row = num_row[-1]+num2+6+num4, column = num_col[0], columnspan = num_col[-1])
		return

#####################################################################################################################################
class Stats_Prediction_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller=controller
		label = tk.Label(self, text = "Not Supported Yet", font = large_font)
		label.grid(pady = 10, padx = 10)

		return

#####################################################################################################################################
class Plotting_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller=controller

		### creating row and column variables for easy moving later
		num_row = (0, 50)
		num_col = num_row

		### Creating frame for plot(s)
		plotFrame = tk.Frame(self)
		plotFrame.grid(row = num_row[0]+1, column = num_col[0]+4, rowspan = 50, columnspan = 4)

		## Have to do what plt.show() does
		canvas = FigureCanvasTkAgg(f, master = plotFrame)
		canvas.draw()
		canvas.get_tk_widget().pack()

		### Adding navs bar	
		toolbar = NavigationToolbar2TkAgg(canvas, plotFrame)
		toolbar.update()
		canvas._tkcanvas.pack()

		selPlayersFun(self, players_stats, bio_and_combine, currentRos, dicTotal, num_row, num_col)
		return

#####################################################################################################################################
class Mock_Draft_Page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller=controller
		## Createing a grid
		num_row = (5, 20)
		num_col = (5, 13)
		
		### All mock draft stuff in done in function files
		showMockDraft(dicTotal, players_stats, currentRos, bio_and_combine, num_row, num_col, curYear, tk, ttk, self)
		return

GUI = Fantasy_GUI()
GUI.protocol("WM_DELETE_WINDOW", closing)

### Size of app
#GUI.geometry('900x500')
#GUI.geometry('1280x720')

### Creates starting plot
plotting(players_stats, {"RomoIsAmazing" : ["Tony", "Romo", 1980, "QB"]})
GUI.mainloop()

### How to create a button that links apage
#		home_button = ttk.Button(self, text = "Home", command = lambda: controller.show_frame(Start_Page))
#		home_button.pack() 

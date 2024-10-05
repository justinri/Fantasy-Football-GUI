from help_options import pop_up_msg
from fun_file import stats_pop_up

#####################################################################################################################################
def mock_results(teamPlayers, teamName, posNums, tk, ttk):
	"""Creates a pop up for mock draft results"""

	### Starting pop up for mock draft results
	results = tk.Tk()
	results.geometry("675x675")
	results.wm_title("Mock Draft Results")
	lFont = ("Helvetica", 12)

	### Creating a scroll bar
	myframe = tk.Frame(results)
	myframe.place(x = 5, y = 5)
	canvas = tk.Canvas(myframe, width = 625+25, height = 620, relief = "groove")
	frame = tk.Frame(canvas)

	### Y scroll bar
	myscrollbar = tk.Scrollbar(myframe, orient="vertical", command = canvas.yview)
	canvas.configure(yscrollcommand = myscrollbar.set)
	myscrollbar.pack(side = "right", fill = "y")

	### Finishing up canvas
	canvas.pack( side = "left")
	canvas.create_window((0,0), window=frame, anchor='nw')

	### Number of starters on a team, default is 8
	numStarters = 1

	### Finding highest and lowerest fantasy points and trends
	best = {}
	worst = {}
	for num, key in enumerate(teamPlayers.keys()):
		for num1, items in enumerate(teamPlayers[key]):
			### Restting the varibles
			if num1 == 0:
				tmpStatsBest = items[-2]
				tmpStatsWorst = items[-2]
				statsBest = items
				statsWorst = items
				tmpTrendsBest = items[-1]
				tmpTrendsWorst = items[-1]
				trendBest = items
				trendWorst = items

				### Inlcuing N/As
				if items[-1] == "N/A":
					tmpTrendsBest = 0
					tmpTrendsWorst = 0

			### For fantasy points
			if items[-2] > tmpStatsBest:
				tmpStatsBest = items[-2]
				statsBest = items

			if items[-2] < tmpStatsWorst:
				tmpStatsWorst = items[-2]
				statsWorst = items

			### To keep N/A in there, for worst case
			if items[-1] == "N/A":
				if tmpTrendsWorst > 0:
					tmpTrendsWorst = 0
					trendWorst = items

			elif items[-1] < tmpTrendsWorst:
					tmpTrendsWorst = items[-1]
					trendWorst = items


			### For fantasy trends for best case
			if items[-1] != "N/A":
				if tmpTrendsBest == "N/A":
					tmpTrendsBest = 0
				if items[-1] > tmpTrendsBest:
					tmpTrendsBest  = items[-1]
					trendBest = items

			### Updating dictionary for every player
			if num1 == len(teamPlayers[key]) - 1:
				best.update({key : [statsBest, trendBest]})
				worst.update({key : [statsWorst, trendWorst]})		

	### Adding up results for two year trends and total fantasy points... Did the same for loop(s) twice for readability
	startFantasyStats = {}
	startTrends = {}
	backFantasyStats = {}
	backTrends = {}
	fantasyStats = {}
	trends = {}
	qbNum = posNums[0]
	rbNum = posNums[1]
	wrNum = posNums[2]
	teNum = posNums[3]
	flexNum = posNums[4]
	kNum = posNums[5]
	defNum = posNums[6]
	for num, key in enumerate(teamPlayers.keys()):
		tmpStatsStart = 0
		tmpTrendsStart = 0
		tmpStatsAll = 0
		tmpTrendsAll = 0

		### Resitting counters
		qbCount = 0;
		rbCount = 0; 
		wrCount = 0;
		teCount = 0;
		flexCount=0;
		kCount = 0;  
		defCount = 0;
		for num1, items in enumerate(teamPlayers[key]):
			tmpStatsAll = tmpStatsAll + items[-2]
			
			### For when the trend is N/A
			if items[-1] != "N/A":
				tmpTrendsAll = tmpTrendsAll + items[-1]
				tmpTrend = items[-1]

			else:
				tmpTrendsAll = tmpTrendsAll + 0
				tmpTrend = 0

			### Getting Stats for starters
			tmpPos = items[0]
			if tmpPos == "QB" and qbCount < qbNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				qbCount += 1

			elif tmpPos == "RB" and rbCount < rbNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				rbCount += 1

			elif tmpPos == "WR" and wrCount < wrNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				wrCount += 1

			elif tmpPos == "TE" and teCount < teNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				teCount += 1
		
			elif tmpPos in ["RB", "WR", "TE"] and flexCount < flexNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				flexCount=+ 1

			elif tmpPos == "K" and kCount < kNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				kCount += 1

			elif tmpPos == "DEF" and defCount < defNum:
				tmpStatsStart = tmpStatsStart + items[-2]
				tmpTrendsStart = tmpTrendsStart + tmpTrend
				defCount += 1

		### Getting Stats for Starters
		startFantasyStats.update({key : round(tmpStatsStart,2)})
		startTrends.update({key : round(tmpTrendsStart,2)})
	
		### Getting Stats for full team and back-ups
		backFantasyStats.update({key : round(tmpStatsAll - tmpStatsStart,2)})
		backTrends.update({key : round(tmpTrendsAll - tmpTrendsStart,2)})

		### Full Team
		fantasyStats.update({key : round(tmpStatsAll,2)})
		trends.update({key : round(tmpTrendsAll,2)})

	### Creating a small penalty of 2% for not having a back up at each position, except kicker and defense
	for key in teamPlayers.keys():
		qbCount = 0;
		rbCount = 0; 
		wrCount = 0;
		teCount = 0;
		flexCount=0;
		kCount = 0;  
		defCount = 0;
		for items in teamPlayers[key]:
			tmpPos = items[0]
			if tmpPos == "QB":
				qbCount += 1

			elif tmpPos == "RB":
				rbCount += 1

			elif tmpPos == "WR":
				wrCount += 1

			elif tmpPos == "TE":
				teCount += 1
		
			elif tmpPos in ["RB", "WR", "TE"]:
				flexCount=+ 1

		### Ensuring at least one back for each position, be esuring count is greater than number of starters
		if qbCount <= qbNum or rbCount <= rbNum  or wrCount <= wrNum  or teCount <= teNum  or flexCount <= flexNum:
			backFantasyStats.update({key : round(backFantasyStats[key]*.98,2)})
			backTrends.update({key : round(backTrends[key]*.98,2)})
 
	### Creating grades, 63% of Fantasy Starters grades counts, back-ups 30%, 5% of the Two year counts, back-ups 2%
	playerGrades = {}
	tmpTotal = {}
	for key in startFantasyStats.keys():
		if startTrends[key] == "N/A":
			tmpStartTrend = 0
		else: 
			tmpStartTrend = startTrends[key]*.05

		if backTrends[key] == "N/A":
			tmpBackTrend = 0
		else:
			tmpBackTrend = backTrends[key]*.02
		
		tmpTotal.update({key : startFantasyStats[key]*.63 + backFantasyStats[key]*.3 + tmpStartTrend + tmpBackTrend})
	key_maxGrade = max(tmpTotal.keys(), key=(lambda k: tmpTotal[k]))
	maxGradeNum = tmpTotal[key_maxGrade]

	for key in tmpTotal.keys():
		tmpPercent = round(tmpTotal[key]/maxGradeNum*100,2)
		if tmpPercent >= 93:	tmpGrade = "A"
		elif tmpPercent >= 90: tmpGrade = "A-"
		elif tmpPercent >= 87: tmpGrade = "B+"
		elif tmpPercent >= 83: tmpGrade = "B"
		elif tmpPercent >= 80: tmpGrade = "B-"
		elif tmpPercent >= 77: tmpGrade = "C+"
		elif tmpPercent >= 73: tmpGrade = "C"
		elif tmpPercent >= 70: tmpGrade = "C-"
		elif tmpPercent >= 67: tmpGrade = "D+"
		elif tmpPercent >= 63: tmpGrade = "D"
		elif tmpPercent >= 60: tmpGrade = "D-"
		else: tmpGrade = "F"
		playerGrades.update({key : tmpGrade})

	def change_table(e, key, num):
		### Updating labels with new players
		nameL[num].config(text = key)
		for num1, items in enumerate(teamPlayers[key]):
			bgColor = "grey" if num1 % 2 == 0 else "lightgrey" 
			labels[0][num1].config(text = items[1:3], bg=bgColor)
#			labels[1][num].config()
#			labels[2][num].config()

		### Showing results of trends and total fantasy points
		if startTrends[key] >= 10:	bgColor = "green"
		elif startTrends[key] <= -10: bgColor = "red"
		else: bgColor = "grey"
#		labels[3][num].config()
		labels[4][num].config(text = startFantasyStats[key])
		labels[5][num].config(text = startTrends[key], bg=bgColor)


		if backTrends[key] >= 10:	bgColor = "green"
		elif backTrends[key] <= -10: bgColor = "red"
		else: bgColor = "grey"
#		labels[6][num].config()
		labels[7][num].config(text = backFantasyStats[key])
		labels[8][num].config(text = backTrends[key], bg=bgColor)

		if trends[key] >= 10:	bgColor = "green"
		elif trends[key] <= -10: bgColor = "red"
		else: bgColor = "grey"
#		labels[9][num].config()
		labels[10][num].config(text = fantasyStats[key])
		labels[11][num].config(text = trends[key], bg=bgColor)


		### Creates best and worst fantasy points
#		labels[12][num].config()
		labels[13][num].config(text = "{} {}".format(best[key][0][1], best[key][0][2]))
		labels[14][num].config(text = best[key][0][-2])
		labels[15][num].config(text = "{} {}".format(worst[key][0][1], worst[key][0][2]))
		labels[16][num].config(text = worst[key][0][-2])

#		### Creates best and worst trends
#		labels[17][num].config()
		labels[18][num].config(text = "{} {}".format(best[key][1][1], best[key][1][2]))
		labels[19][num].config(text = best[key][1][-1])
		labels[20][num].config(text = "{} {}".format(worst[key][1][1], worst[key][1][2]))
		labels[21][num].config(text = worst[key][1][-1])

		### Creates Grades
		if playerGrades[key] in ["A", "A-"]: bgColor = "green"
		elif playerGrades[key] in ["B+", "B", "B-"]: bgColor = "#00b300"
		elif playerGrades[key] in ["C+", "C", "C-"]: bgColor = "grey"
		elif playerGrades[key] in ["D+", "D", "D-"]: bgColor = "#ff8080"
		elif playerGrades[key] == "F": bgColor = "red"
		labels[23][num].config(text = playerGrades[key], bg=bgColor)
		return

	### Current team combo box
	teamNames = [key for key in teamPlayers.keys() if key != teamName]
	teamNames.sort(key=lambda teamNames: teamNames[-1])
	teamNames.insert(0, teamName)
	ttk.Label(frame,text="Select a Team:", font = lFont, relief = "groove", anchor = "center", justify="center"
										   ).grid(row = 0, column = 0, columnspan = 3, ipadx = 3, sticky = "nesw")
	combo = ttk.Combobox(frame, values = teamNames, state="readonly")
	combo.grid(row=1, column=0, columnspan = 3, sticky = "nesw")
	combo.set(teamNames[0])
	combo.bind('<<ComboboxSelected>>', lambda e: change_table(e, combo.get(), 0))
#	change_table(None, combo.get(), 0)

	### Current team combo box 2
	ttk.Label(frame,text="Select a Team:", font = lFont, relief = "groove", anchor = "center", justify="center"
										   ).grid(row = 0, column = 3, columnspan = 3, ipadx = 3, sticky = "nesw")
	combo2 = ttk.Combobox(frame, values = teamNames, state="readonly")
	combo2.grid(row=1, column=3, columnspan = 3, sticky = "nesw")
	combo2.set(teamNames[1])
	combo2.bind('<<ComboboxSelected>>', lambda e: change_table(e, combo2.get(), 1))
#	change_table(None, combo2.get(), 3)


#	if playerGrades[teamName] == "A":
#		gradeStr
#		bgColor
#	elif playerGrades[teamName] == "A-":
#	elif playerGrades[teamName] == "B+":
#	elif playerGrades[teamName] == "B":
#	elif playerGrades[teamName] == "B-":
#	elif playerGrades[teamName] == "C+":
#	elif playerGrades[teamName] == "C":
#	elif playerGrades[teamName] == "C-":
#	elif playerGrades[teamName] == "D+":
#	elif playerGrades[teamName] == "D":
#	elif playerGrades[teamName] == "D-":
#	elif playerGrades[teamName] == "F":

#	tk.Label(frame,text=gradeStr,font=lFont,relief="groove",bg=bgColor).grid(row=num1+12,column=0,columnspan = 10,ipadx=2,sticky="nesw")


	### Creating Tables
	nameL = {}
	labels = {num:{} for num in range(25)}
	for num in range(2):
		nameL.update({num: tk.Label(frame, text=teamNames[num], font=lFont,relief="groove")})
		nameL[num].grid(row=2,column=num*3,columnspan=3, sticky="nesw")
		for num1, items in enumerate(teamPlayers[teamNames[num]]):
			bgColor = "grey" if num1 % 2 == 0 else "lightgrey" 
			labels[0].update({num1: tk.Label(frame, text=items[1:3], font=lFont, bg=bgColor)})
			labels[0][num1].grid(row=num1+3, column=num*3, columnspan = 3, ipadx=2, sticky = "nesw")

		### Showing results of trends and total fantasy points
		labels[1].update({num: tk.Label(frame, text="Fantasy Points", font=lFont, relief="groove")})
		labels[1][num].grid(row=num1+4, column=num*3+1, ipadx=2, sticky = "nesw")
		labels[2].update({num: tk.Label(frame, text="Two Year Trend", font=lFont, relief="groove")})
		labels[2][num].grid(row=num1+4, column=num*3+2, ipadx=2, sticky = "nesw")

		if startTrends[teamNames[num]] >= 10:	bgColor = "green"
		elif startTrends[teamNames[num]] <= -10: bgColor = "red"
		else: bgColor = "grey"
		labels[3].update({num: tk.Label(frame, text="Starters:", font=lFont, relief="groove")})
		labels[3][num].grid(row=num1+5, column=num*3, ipadx=2, sticky = "nesw")
		labels[4].update({num: tk.Label(frame, text=startFantasyStats[teamNames[num]], font=lFont, relief="sunken")})
		labels[4][num].grid(row=num1+5, column=num*3+1, ipadx=2, sticky="nesw")
		labels[5].update({num: tk.Label(frame, text=startTrends[teamNames[num]],font=lFont,bg=bgColor,relief="sunken")})
		labels[5][num].grid(row=num1+5,column=num*3+2,ipadx=2,sticky="nesw")

		if backTrends[teamNames[num]] >= 10:	bgColor = "green"
		elif backTrends[teamNames[num]] <= -10: bgColor = "red"
		else: bgColor = "grey"
		labels[6].update({num: tk.Label(frame, text="Back Ups:", font=lFont, relief="groove")})
		labels[6][num].grid(row=num1+6, column=num*3, ipadx=2, sticky = "nesw")
		labels[7].update({num: tk.Label(frame, text=backFantasyStats[teamNames[num]], font=lFont, relief="sunken")})
		labels[7][num].grid(row=num1+6, column=num*3+1, ipadx=2, sticky = "nesw")
		labels[8].update({num: tk.Label(frame, text=backTrends[teamNames[num]], font=lFont, bg=bgColor,relief="sunken")})
		labels[8][num].grid(row=num1+6,column=num*3+2,ipadx=2,sticky="nesw")

		if trends[teamNames[num]] >= 10:	bgColor = "green"
		elif trends[teamNames[num]] <= -10: bgColor = "red"
		else: bgColor = "grey"
		labels[9].update({num: tk.Label(frame, text="Full Team:", font=lFont, relief="groove")})
		labels[9][num].grid(row=num1+7, column=num*3, ipadx=2, sticky="nesw")
		labels[10].update({num: tk.Label(frame, text=fantasyStats[teamNames[num]], font=lFont, relief="sunken")})
		labels[10][num].grid(row=num1+7, column=num*3+1, ipadx=2, sticky="nesw")
		labels[11].update({num: tk.Label(frame, text=trends[teamNames[num]], font=lFont, bg=bgColor, relief="sunken")})
		labels[11][num].grid(row=num1+7, column=num*3+2, ipadx=2, sticky="nesw")

		### Creates best and worst fantasy points
		fanStr = "Best/Worst Fantasy Points"
		labels[12].update({num: tk.Label(frame, text=fanStr, font=lFont, relief="groove")})
		labels[12][num].grid(row=num1+8, column=num*3, columnspan = 3, ipadx=2, sticky="nesw")
		labels[13].update({num:tk.Label(frame,text="{} {}".format(
										best[teamNames[num]][0][1],best[teamNames[num]][0][2]),font=lFont,relief="groove")})
		labels[13][num].grid(row=num1+9,column=num*3,columnspan=2,ipadx=2,sticky="nesw")
		labels[14].update({num: tk.Label(frame, text=best[teamNames[num]][0][-2],font=lFont,bg="green")})
		labels[14][num].grid(row=num1+9,column=num*3+2,ipadx=2, sticky="nesw")
		labels[15].update({num: tk.Label(frame, text="{} {}".format(
										 worst[teamNames[num]][0][1], worst[teamNames[num]][0][2]),font=lFont,relief="groove")})
		labels[15][num].grid(row=num1+10,column=num*3,columnspan=2,ipadx=2,sticky="nesw")
		labels[16].update({num: tk.Label(frame, text=worst[teamNames[num]][0][-2], font=lFont, bg="red")})
		labels[16][num].grid(row=num1+10, column=num*3+2, ipadx=2, sticky="nesw")

		### Creates best and worst trends
		trendStr = "Best/Worst Two Year Trend"
		labels[17].update({num: tk.Label(frame, text=trendStr, font=lFont, relief="groove")})
		labels[17][num].grid(row=num1+11, column=num*3, columnspan = 3,ipadx=2,sticky="nesw")
		labels[18].update({num: tk.Label(frame, text=best[teamNames[num]][1][1] +" "+ best[teamNames[num]][1][2],font=lFont,relief="groove")})
		labels[18][num].grid(row=num1+12,column=num*3,columnspan=2,ipadx=2,sticky="nesw")
		labels[19].update({num: tk.Label(frame, text=best[teamNames[num]][1][-1],font=lFont,bg="green")})
		labels[19][num].grid(row=num1+12,column=num*3+2,ipadx=2,sticky="nesw")
		labels[20].update({num: tk.Label(frame, text=worst[teamNames[num]][1][1] +" "+ worst[teamNames[num]][1][2],font=lFont,relief="groove")})
		labels[20][num].grid(row=num1+13,column=num*3,columnspan=2,ipadx=2,sticky="nesw")
		labels[21].update({num: tk.Label(frame,text=worst[teamNames[num]][1][-1],font=lFont,bg="red")})
		labels[21][num].grid(row=num1+13,column=num*3+2,ipadx=2,sticky="nesw")

		### Creates Grades
		if playerGrades[teamNames[num]] in ["A", "A-"]: bgColor = "green"
		elif playerGrades[teamNames[num]] in ["B+", "B", "B-"]: bgColor = "#00b300"
		elif playerGrades[teamNames[num]] in ["C+", "C", "C-"]: bgColor = "grey"
		elif playerGrades[teamNames[num]] in ["D+", "D", "D-"]: bgColor = "#ff8080"
		elif playerGrades[teamNames[num]] == "F": bgColor = "red"
		labels[22].update({num: tk.Label(frame,text="Grade:",font=lFont,relief="groove")})
		labels[22][num].grid(row=num1+14,column=num*3,columnspan = 3,ipadx=2,sticky="nesw")
		labels[23].update({num: tk.Label(frame,text=playerGrades[teamNames[num]],font=lFont,relief="sunken",bg=bgColor)})
		labels[23][num].grid(row=num1+15,column=num*3,columnspan = 3,ipadx=2,sticky="nesw")

		### Creating a gap between the two rows
		labels[24].update({num: tk.LabelFrame(frame)})
		labels[24][num].grid(row = num1+16, column = num*3, columnspan = 3, pady = 5, sticky = "nesw")


	### Recreates the canvas
	def reConfig(event):
		canvas.configure(scrollregion=canvas.bbox("all"), width=625+25, height = 620)
		return

	frame.bind("<Configure>", reConfig)

	tk.Button(results, text="Exit", command = results.destroy).place(x = 585, y = 640, height=30, width=85)
	results.mainloop()
	return


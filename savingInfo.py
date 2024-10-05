from tkinter.filedialog import asksaveasfilename
#####################################################################################################################################
def saveResults(pos, players_stats,  whatStats, currentRos = None):
	"""Allows users to save last years stats in either csv, txt, odt, xlsx."""
	fTypes = (("Comma-Separated Values", "*.csv"), ("Open Document Spreadsheet", "*.ods"),
			  ("Text Files", "*.txt"),("Windows Stuff", "*.xlsx"), ("All Files", "*.*"))

	filename = asksaveasfilename(title="I don't support proprietary formats... Not my style...", filetypes = fTypes)

	if whatStats == "lastStats": 
		saveLabels = []
		saveStats = []
		if pos == "QB" or pos == "allPlayers":
			saveLabels.append(["Last Name", "First Name", "Year Born", "Year", "Age", "Team", "Games Played", "Games Started",
							   "Passing Attempts", "Passing Completion", "Passing Yards", "Passing Touchdowns", "Interception",
							   "Rushing Attempts", "Rushing Yards", "Rushing Touchdowns", "Fumbles"])
			saveStats.append((items for items in players_stats["QB"] if items[3] == 2017))

		if pos == "RB" or pos == "allPlayers":
			saveLabels.append(["Last Name", "First Name", "Year Born", "Year", "Age", "Team", "Games Played", "Games Started",
							   "Rushing Attempts", "Rushing Yards", "Rushing Touchdowns", "Fumbles",
							   "Targets", "Receptions", "Receiving Yards", "Receiving Touchdowns"])
			saveStats.append((items for items in players_stats["RB"] if items[3] == 2017))

		if pos == "WR" or pos == "allPlayers":
			saveLabels.append(["Last Name", "First Name", "Year Born", "Year", "Age", "Team", "Games Played", "Games Started",
							   "Targets", "Receptions", "Receiving Yards", "Receiving Touchdowns"])
			saveStats.append((items for items in players_stats["WR"] if items[3] == 2017))

		if pos == "TE" or pos == "allPlayers":
			saveLabels.append(["Last Name", "First Name", "Year Born", "Year", "Age", "Team", "Games Played", "Games Started",
							   "Targets", "Receptions", "Receiving Yards", "Receiving Touchdowns"])
			saveStats.append((items for items in players_stats["TE"] if items[3] == 2017))


		if filename[-3:] == "csv":
			with open(filename, "w") as f:
				add1 = 0
				for num, items in enumerate(saveStats):
					if num == add1:
						[f.write(itemsL + ",") for itemsL in saveLabels[add1]]
						f.write('\n')
						add1 +=1

					for item in items:
						f.write(str(item).replace("'", "").replace("(", "").replace(")", "").replace(" ", "") + '\n')

		elif filename[-3:] == "txt":
			with open(filename, "w") as f:
				add1 = 0
				for num, items in enumerate(saveStats):
					if num == add1:
						[f.write(itemsL + " ") for itemsL in saveLabels[add1]]
						f.write('\n')
						add1 +=1

					for item in items:
						f.write(str(item).replace("'", "").replace("(", "").replace(")", "").replace(",", "") + '\n')


		elif filename[-3:] == "ods" or filename[-4:] == "xlsx":
			from collections import OrderedDict
			dicTotal = OrderedDict()

			if pos == "QB" or pos == "allPlayers":
				tmpList = [items for items in saveStats[0]]
				tmpList.insert(0, saveLabels[0])
				dicTotal.update({"QB": tmpList})

			elif pos == "RB":
				tmpList = [items for items in saveStats[0]]
				tmpList.insert(0, saveLabels[0])
				dicTotal.update({"RB": tmpList})

			elif pos == "WR":
				tmpList = [items for items in saveStats[0]]
				tmpList.insert(0, saveLabels[0])
				dicTotal.update({"WR": tmpList})

			elif pos == "TE":
				tmpList = [items for items in saveStats[0]]
				tmpList.insert(0, saveLabels[0])
				dicTotal.update({"TE": tmpList})

			if pos == "allPlayers":
				tmpList = [items for items in saveStats[1]]
				tmpList.insert(0, saveLabels[1])
				dicTotal.update({"RB": tmpList})

				tmpList = [items for items in saveStats[2]]
				tmpList.insert(0, saveLabels[2])
				dicTotal.update({"WR": tmpList})

				tmpList = [items for items in saveStats[3]]
				tmpList.insert(0, saveLabels[3])
				dicTotal.update({"TE": tmpList})

	### If they want fantastic information
	elif whatStats == "fanStats":

		### Getting information from mocn function files
		from mockFun import mockData
		if pos != "allPlayers":
			dicTotal = mockData(players_stats, currentRos)
			fanStatsLabels = ["Last Name", "First Name", "Team", "Two Year Trend (Percent Difference)", "Fantasy Points Last Year"]
			tmpList = [(items[2], items[1], items[0], items[-1], items[-2]) for items in dicTotal[pos]]

		else:
			dicTotal = mockData(players_stats, currentRos, True)
			fanStatsLabels = ["Last Name", "First Name", "Position", "Team", "Two Year Trend (Percent Difference)", "Fantasy Points Last Year"]
			tmpList = [(items[2], items[1], items[4], items[0], items[-1], items[-2]) for items in dicTotal[pos]]

		### Getting Stats based on position wanted
		if filename[-3:] == "ods" or filename[-4:] == "xlsx":
			tmpList.insert(0, fanStatsLabels)
		dicTotal = {pos : tmpList}

		### Creating CSV or TXT files
		if filename[-3:] == "csv":
			with open(filename, "w") as f:
				[f.write(items + ",") for items in fanStatsLabels]; f.write('\n')
				for items in dicTotal[pos]:
					f.write(str(items).replace("'", "").replace("(", "").replace(")", "") + '\n')

		elif filename[-3:] == "txt":
			with open(filename, "w") as f:
				[f.write(items + " ") for items in fanStatsLabels]; f.write('\n')
				for items in dicTotal[pos]:
					f.write(str(items).replace("'", "").replace("(", "").replace(")", "").replace(",", "") + '\n')


	if filename[-3:] == "ods":	
		from pyexcel_ods import save_data
		save_data(filename, dicTotal)

	elif filename[-4:] == "xlsx":
		import xlsxwriter
		workbook = xlsxwriter.Workbook(filename)

		for key in dicTotal.keys():
			worksheet = workbook.add_worksheet(key)
			row = 0
			for items in dicTotal[key]:
				worksheet.write_row(row, 0, items)
				row += 1
		workbook.close()
	return

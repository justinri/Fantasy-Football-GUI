#####################################################################################################################################
def sim_mock(playerRemove, teamPlayers, whoPicked):
	"""Picks the player for the computer, for the mock drafts"""

	### Setting up varibles
	qbCount = 0; qbNum = 1
	rbCount = 0; rbNum = 2
	wrCount = 0; wrNum = 3
	teCount = 0; teNum = 1

	### Creating counts for each position
	for items in teamPlayers[whoPicked]:
		if items[0] == "QB":
			qbCount += 1
		elif items[0] == "RB":
			rbCount += 1
		elif items[0] == "WR":
			wrCount += 1
		elif items[0] == "TE":
			teCount += 1

	### Only pick one QB for now
	for items in playerRemove:
		pos = items[4]
		
		### Get all starters first
		if qbCount < qbNum and pos == "QB":
			pick = items
			break
		elif rbCount < rbNum and pos == "RB":
			pick = items
			break
		elif wrCount < wrNum and pos == "WR":
			pick = items
			break
		elif teCount < teNum and pos == "TE":
			pick = items
			break

		### Ensuring all positions their starters
		elif pos != "QB" and qbCount < qbNum:
			continue
		elif pos != "RB" and rbCount < rbNum:
			continue
		elif pos != "WR" and wrCount < wrNum:
			continue
		elif pos != "TE" and teCount < teNum:
			continue

		### drafting a back up for positions, in order of importances
		elif rbCount < rbNum + 2 and pos == "RB":
			pick = items
			break
		elif wrCount < wrNum + 2 and pos == "WR":
			pick = items
			break
		elif qbCount < qbNum + 1 and pos == "QB":
			pick = items
			break
		elif teCount < teNum + 1 and pos == "TE":
			pick = items
			break

		### Ensuring all positions are picked with atleast one back up
		elif pos != "QB" and qbCount < qbNum + 1:
			continue
		elif pos != "RB" and rbCount < rbNum + 1:
			continue
		elif pos != "WR" and wrCount < wrNum + 1:
			continue
		elif pos != "TE" and teCount < teNum + 1:
			continue

		else:
			pick = items
			break


	return pick

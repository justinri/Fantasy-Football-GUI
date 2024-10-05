import sqlite3

def connect_to_database(db_file):
	"""Create a connection to a SQLite Database. The Data base of choice must be imported"""
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	return 	conn, cur

def close_to_database(conn):
	"""Closes a connection to a SQLite Database. The connection must be imported"""
	conn.close()
	return

def default_parameters(cur):
	"""Loads default mock draft parameters."""
	cur.execute("SELECT * FROM default_mock_parameters")
	default_mock = cur.fetchall()
	return default_mock

def saved_parameters(cur):
	"""Loads default mock draft parameters."""
	cur.execute("SELECT * FROM saved_mock_parameters")
	saved_mock = cur.fetchall()
	return saved_mock

def favorite_team(cur):
	"""Loading favorite team from data base"""
	cur.execute("SELECT * FROM fav_team")
	fav_team = cur.fetchall()
	return fav_team[0][0]

def getting_team_names(cur):
	"""Creating a list of team names from a database."""
	cur.execute("SELECT * FROM Team_Names")
	names = cur.fetchall()
	team_names = [team[0] for team in names]
	return team_names

def loading_team_stats(cur,team_names):
	"""Loading team stats for up to (if applicable) the previous three years from a database."""
	team_stats = {}
	for team in team_names:
		### Getting data
		cur.execute("SELECT * FROM team_stats_" + team)
		team_stats[team] = cur.fetchall()
	return team_stats

def getting_current_rosters(cur,team_names):
	"""Loading past and current team rosters from a database."""

	### Roster years data collection, first year of data is 2008, last year of data was 2017
	years = ['20' + str(year).zfill(2) for year in range(8,18)]

	### Creating dictionary of current and past rosters for 2018
	current_rosters = {}
	past_rosters = {}
	for team in team_names:
		### Getting data from current rosters
		cur.execute("SELECT * FROM current_rosters_" + team)
		current_rosters[team] = cur.fetchall()

		for past_year in years[:]:
			## Getting data from past rosters
			cur.execute("SELECT * FROM past_rosters_" + team + '_' + past_year)
			past_rosters[team + '_' + past_year] = cur.fetchall()

	return current_rosters, past_rosters

def getting_bio_and_combine_info(cur):
	"""Creating a dictionary for player's bio and draft informaion."""	

	### Will need all positions
	position = ['QB','RB','WR','TE']

	### Getting bio and draft information from the database and placing it in a dictionary
	bio_and_combine = {}
	for pos in position:	
		cur.execute("SELECT * FROM bio_and_combine_info_" + pos + "s")
		bio_and_combine[pos] = cur.fetchall()

	return bio_and_combine

def getting_players_stats(cur):
	"""Creating a dictionary for player's bio and draft informaion."""	

	### Getting stats information from the database for all positions but QB's and placing it in a dictionary
	player_stats = {}
	position = ['QB','RB','WR','TE']
	for pos in position:	
		cur.execute("SELECT * FROM player_stats_" + pos + "s")
		player_stats[pos] = cur.fetchall()

	return player_stats





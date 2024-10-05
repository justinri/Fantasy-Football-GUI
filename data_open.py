from loading_data import *
import sys

def get_data():
	## Year is for the year you want the results for, is only for testing
	db_file = 'databases/info_database.db'

	### Opening Connection to database
	[conn, cur] = connect_to_database(db_file)

	### Getting Team names
	team_names = getting_team_names(cur)

	### Getting team stats and placing them in a dictionary
	team_stats = loading_team_stats(cur,team_names)

	### Getting past and current rosters
	[current_rosters, past_rosters] = getting_current_rosters(cur,team_names)

	### Getting all players bio and combine inforomation
	bio_and_combine = getting_bio_and_combine_info(cur)

	### Getting all players stats
	players_stats = getting_players_stats(cur)

	### Getting favorite team
	fav_team = favorite_team(cur)

	### closing Connection to database
	close_to_database(conn)

	return team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats, fav_team

def upDateFavTeam():
	"""Allows the user to update his favorite team."""
	## Year is for the year you want the results for, is only for testing
	db_file = 'databases/info_database.db'

	### Opening Connection to database
	[conn, cur] = connect_to_database(db_file)

	### Getting favorite team
	fav_team = favorite_team(cur)

	### closing Connection to database
	close_to_database(conn)
	return fav_team

def default_mock_data():
	## Year is for the year you want the results for, is only for testing
	db_file = 'databases/info_database.db'

	### Opening Connection to database
	[conn, cur] = connect_to_database(db_file)

	### Loading Default parameters for mock drafts
	default_mock = default_parameters(cur)

	### closing Connection to database
	close_to_database(conn)

	return default_mock

def saved_mock_data():
	## Year is for the year you want the results for, is only for testing
	db_file = 'databases/info_database.db'

	### Opening Connection to database
	[conn, cur] = connect_to_database(db_file)

	### Loading Saved parameters for mock drafts
	saved_mock = saved_parameters(cur)

	### closing Connection to database
	close_to_database(conn)

	return saved_mock

if __name__ == '__main__':
	year = 2018
	[team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats, fav_team] = get_data()
#	print(past_rosters['Dallas_Cowboys_2015'])

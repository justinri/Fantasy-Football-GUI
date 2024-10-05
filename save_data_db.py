import sqlite3
#####################################################################################################################################
def close_db(conn):
	## Saving data to database
	conn.commit()
	## Closing Connection
	conn.close()
	return

#####################################################################################################################################
def update_fav_team(fav_team):
	"""Allows the user to update their favorite team, by updating the database."""
	### connecting to datab base and creating a cursor
	conn = sqlite3.connect("databases/info_database.db")
	cur = conn.cursor() 
	cur.execute("UPDATE fav_team set team=?", (fav_team,))
	close_db(conn)
	return

#####################################################################################################################################
def store_mock_parameters(para_to_save):
	"""Updates table were saved mock draft parameters was stored in the database"""
	### connecting to datab base and creating a cursor
	conn = sqlite3.connect("databases/info_database.db")
	cur = conn.cursor() 
	cur.execute("UPDATE saved_mock_parameters set \
				 number_teams = ?, \
				 team_name = ?, \
				 pass_yards = ?, \
				 pass_tds = ?, \
				 pass_picks = ?, \
				 fumble = ?,\
			     rec_yards = ?, \
				 rec_tds = ?, \
				 rec_catches = ?, \
				 rush_yards = ?, \
				 rush_tds = ?", tuple(para_to_save))

	close_db(conn)
	return

#####################################################################################################################################
def delete_table():
	"""Allows me to delete tables (in the database) when needed."""
	### connecting to datab base and creating a cursor
	conn = sqlite3.connect("databases/info_database.db")
	cur = conn.cursor() 
	cur.execute("DROP TABLE saved_mock_parameters")
	close_db(conn)
	return

if __name__ == "__main__":
	update_fav_team("Dallas Cowboys")
#	load_default_mock_parameters()



### How to create a database
### connecting to datab base and creating a cursor
###	conn = sqlite3.connect("databases/info_database.db")
###	cur = conn.cursor() 
###	cur.execute("""CREATE TABLE fav_team (team text) """)
###	cur.execute("""INSERT INTO fav_team VALUES (?)""", ("Dallas Cowboys",))

###	## Saving data to database
###	conn.commit()
###	## Closing Connection
###	conn.close()

import sqlite3
import csv

with open("./members.csv", "r") as f:
	csv_reader = csv.DictReader(f)
	members = [(row['名字'], row['團體']) for row in csv_reader]

with open("./create_db.sql", "r") as f1:
	create_db_sql = f1.read()

db = sqlite3.connect('members.db')

#create database
# executescript vs execute
# executescript can run many command but execute only run one command
with db:
	db.executescript(create_db_sql)
# is equal to
# c = db.cursor()
# c.executescript(create_db_sql)
# c.commit()


# insert data from csv file
with db:
	db.executemany(
		"INSERT INTO members (name, group_name) VALUES (?,?)",
		members
	)

c = db.execute("SELECT * FROM members")
for row in c:
	print(row)

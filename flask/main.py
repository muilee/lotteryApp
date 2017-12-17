from flask import Flask, g, render_template, request
from config import DevConfig
import csv
import sqlite3
import random
from datetime import datetime


app = Flask(__name__)
app.config.from_object(DevConfig)
SQLITE_DB_PATH = 'members.db'
SQLITE_DB_SCHEMA = 'create_db.sql'
MEMBER_CSV_PATH = 'members.csv'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db
 
def reset_db():
	with open(SQLITE_DB_SCHEMA, "r") as f:
		create_db_sql = f.read()

	db = get_db()

	with db:
		db.execute("DROP TABLE IF EXISTS draw_histories")
		db.execute("DROP TABLE IF EXISTS members")
		db.executescript(create_db_sql)

	with open(MEMBER_CSV_PATH, "r") as f:
		csv_reader = csv.DictReader(f)
		members = [
            (row['名字'], row['團體'])
            for row in csv_reader
        ]

	with db:
		db.executemany(
            'INSERT INTO members (name, group_name) VALUES (?, ?)',
            members
        )


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, "_database", None)
	if db is not None:
		db.close()


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/draw", methods=["POST"])
def draw():
	# Get the database connection
	db = get_db()
	group_name = request.form.get("group_name", "ALL")
	valid_members_sql = "SELECT id FROM members"

	if group_name == "ALL":
		cursor = db.execute(valid_members_sql)
	else:
		valid_members_sql += " WHERE group_name = ?"
		cursor = db.execute(valid_members_sql, (group_name, ))

	valid_members_ids = [row[0] for row in cursor]

	if not valid_members_ids:
		err_msg = "<p>No members in group '%s'</p>" % group_name
		return err_msg, 404

	lucky_member_id = random.choice(valid_members_ids)
	member_name, member_group_name = db.execute(
		"SELECT name, group_name FROM members WHERE id = ?", 
		(lucky_member_id, )
	).fetchone()

	with db:
		db.execute("INSERT INTO draw_histories (memberid) VALUES (?)", (lucky_member_id,))


	return render_template("draw.html", name=member_name, group=member_group_name)


@app.route("/history")
def history():
	db = get_db()
	data = db.execute(
		"""SELECT m.name, m.group_name, d.time 
		FROM draw_histories AS d 
		INNER JOIN members AS m ON m.id == d.memberid 
		ORDER BY d.time DESC 
		LIMIT 10"""
	).fetchall()

	recent_histories = []
	for row in data:
		recent_histories.append({
            'name': row[0],
            'group': row[1],
            'draw_time': datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
        })

	return render_template("history.html", recent_histories=recent_histories)


@app.route("/reset")
def reset():
 	reset_db()

 	return render_template("reset.html")


if __name__ == "__main__":
	app.run(debug=True)
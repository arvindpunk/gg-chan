import os
import psycopg2
import sqlite3
import misc

DATABASE_URL = os.environ['DATABASE_URL']

class User:
	def __init__(self, uid, handle, rating):
		self.uid = uid
		self.handle = handle
		self.rating = rating

def addUser(user):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c.execute("INSERT INTO users VALUES (%s, %s, %s)", (user.uid, user.handle, user.rating))
	conn.commit()
	conn.close()

def remUser(user):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c.execute("DELETE FROM users WHERE uid = %s", (user.uid,))
	print("User removed: " + user.uid + " " + user.handle)
	conn.commit()
	conn.close()

async def updateUsers():
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c1 = conn.cursor()
	c.execute("SELECT * FROM users")
	users = []
	for row in c:
		# print(row)
		rating = await misc.getRating(row[1])
		rating = str(rating)
		print(row[1] + ' - ' + row[2] + ' | ' + str(rating))
		c1.execute("UPDATE users SET rating = %s WHERE uid = %s", (rating, row[0]))
		users.append(User(row[0], row[1], rating))
	conn.commit()
	conn.close()
	return users

async def updateSpecificUser(user):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c1 = conn.cursor()
	c.execute("SELECT * FROM users WHERE uid = %s", (user.uid,))
	row = c.fetchone()
	rating = await misc.getRating(row[1])
	rating = str(rating)
	print(row[1] + ' - ' + row[2] + ' | ' + str(rating))
	c1.execute("UPDATE users SET rating = %s WHERE uid = %s", (rating, row[0]))
	conn.commit()
	conn.close()
	return rating

async def transferDB():
	connsq3 = sqlite3.connect('userdata.db')
	csq3 = connsq3.cursor()

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c.execute("DROP TABLE users")
	c.execute("CREATE TABLE users (uid text PRIMARY KEY, handle text, rating text)")

	csq3.execute("SELECT * FROM users")
	for row in csq3:
		c.execute("INSERT INTO users VALUES (%s, %s, %s)", (str(row[0]), str(row[1]), str(row[2])))
	conn.commit()
	conn.close()
	connsq3.close()
	c.close()

def searchUsers(uid):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c.execute("SELECT * FROM users WHERE uid = %s", (uid,))
	row = c.fetchone()
	if row == None:
		u = None
	else:
		u = User(row[0], row[1], row[2])
	conn.close()
	return u

def printdb():
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	c.execute("SELECT * FROM users")
	for row in c:
		print(row)
	conn.close()
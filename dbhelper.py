import sqlite3
import misc

class User:
	def __init__(self, uid, handle, rating):
		self.uid = uid
		self.handle = handle
		self.rating = rating

def addUser(user):
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c.execute("INSERT INTO users VALUES (?, ?, ?)", (user.uid, user.handle, user.rating))
	conn.commit()
	conn.close()

def remUser(user):
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c.execute("DELETE FROM users WHERE uid = ?", (user.uid,))
	print("User removed: " + user.uid + " " + user.handle)
	conn.commit()
	conn.close()

async def updateUsers():
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c1 = conn.cursor()
	c.execute("SELECT * FROM users")
	users = []
	for row in c:
		# print(row)
		rating = await misc.getRating(row[1])
		print(row[1] + ' - ' + str(row[2]) + ' | ' + str(rating))
		c1.execute("UPDATE users SET rating = ? WHERE uid = ?", (rating, row[0]))
		users.append(User(row[0], row[1], row[2]))
	conn.commit()
	conn.close()
	return users

def searchUsers(uid):
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
	row = c.fetchone()
	if row == None:
		u = None
	else:
		u = User(row[0], row[1], row[2])
	conn.close()
	return u

def printdb():
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c.execute("SELECT * FROM users")
	print(c.fetchall())
	conn.close()

def dbsize():
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c.execute("SELECT COUNT(*) FROM users")
	count = c.fetchone()
	conn.close()
	return count

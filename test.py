import dbhelper as db
import misc
import sqlite3

class User:
	def __init__(self, uid, handle, rating):
		self.uid = uid
		self.handle = handle
		self.rating = rating

# db.addUser(User('219439471991586816', 'arvindpunk', 1889))
# db.addUser(User('219439471991586816', 'arvindpunk', 1889))

def createDB():
	conn = sqlite3.connect('userdata.db')
	c = conn.cursor()
	c.execute("CREATE TABLE users (uid text PRIMARY KEY, handle text, rating number)")
	conn.commit()
	conn.close()
db.printdb()


id = '219439471991586816'
user = db.searchUsers(id)
db.remUser(user)
print('Removed user ' + user.handle)
# for row1, row2 in zip(open('users', 'r'), open('handles', 'r')):
# 	try:
# 		u = User(row1.strip(), row2.strip(), misc.getRating(row2.strip()))
# 		print(u.uid, u.handle, u.rating)
# 		db.addUser(u)
# 	except sqlite3.IntegrityError as e:
# 		print(e)
# await db.updateUsers()
# db.printdb()
# db.addUser(User('219439471991586816', 'arvindpunk', 1889))
# print(db.printdb())
# print(db.dbsize())
# id = '219439471991586816'
# # db.remUser(User(id, 'arvindpunk', 1889))
# print(db.searchUsers('219439471991586816'))
# print('--------')
# print(db.printdb())

exit(0)
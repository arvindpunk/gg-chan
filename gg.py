import discord
import asyncio
from discord.ext import commands
from time import sleep
import dbhelper as db
import misc
import random

TOKEN='NDc1NTUyNzg5NTIzNTk1Mjkx.DkigGA.5Drbh4ko-qhFwqYCkXcoZcdgfsk'
bot = commands.Bot(command_prefix='!gg ', description='A bot that stores/retrieves codechef handles.')
currentHandles = []

class User:
	def __init__(self, uid, handle, rating):
		self.uid = uid
		self.handle = handle
		self.rating = rating

async def verifyUser(ctx, user, time):
	await asyncio.sleep(60.0)
	submissions = await misc.getSubmissions(user.handle)
	if len(submissions) == 0:
		print('Cannot verify user', user.handle)
		await ctx.send('Cannot verify user '+ user.handle + '.')
	elif submissions[0] <= time:
		print('Cannot verify user', user.handle)
		await ctx.send('Cannot verify user '+ user.handle + '.')
	else:
		print(user.handle, 'has been verified!')
		await ctx.send(user.handle + ' has been verified!')
		db.addUser(user)
		await changeRole(user)
	currentHandles.remove(user.handle)

async def changeRole(user):
	member = discord.utils.get(server.members, id=int(user.uid))
	if member != None:
		for role in member.roles:
			if "star" in role.name:
				print('Removed ' + role.name + ' from ' + member.name)
				await member.remove_roles(role)
		newRoleName = misc.getRoleFromRating(user.rating)
		role = discord.utils.get(server.roles, name=newRoleName)
		await member.add_roles(role)
		print('Added ' + role.name + ' to ' + member.name)

@bot.event
async def on_ready():
	global server
	server = bot.guilds[0]
	print('Logged in as')
	print(bot.user.name)
	# await db.transferDB()
	db.printdb()
	print('------')

@bot.event
async def on_member_remove(member):
	user = db.searchUsers(member.id)
	if user != None:
		db.remUser(user)

@bot.command()
@commands.has_role('moderators')
async def printdatabase(ctx):
	db.printdb()

@bot.command()
@commands.has_role('moderators')
async def removeuser(ctx, discordid: str):
	user = db.searchUsers(discordid)
	if user != None:
		db.remUser(user)
		await ctx.send(user.handle + ' has been pruned from the database!')

@bot.command()
@commands.has_role('moderators')
async def updateroles(ctx):
	await ctx.send("Alright, don't cry when you go down.")
	users = await db.updateUsers()
	for user in users:
		print(user.handle + ' - ' + str(user.rating))
		await changeRole(user)
	await ctx.send("Ratings have been updated, gg.")

@bot.command()
async def sethandle(ctx, h: str):
	rating = await misc.getRating(h)
	if rating == -1:
		await ctx.send("Handle does not exist.")
	elif h in currentHandles:
		await ctx.send("Someone else is trying to set " + h + " as their handle. Please wait.")
	else:
		user = db.searchUsers(str(ctx.message.author.id))
		if user != None:
			await ctx.send("This handle already exists in the database.")
		else:
			currentHandles.append(h)
			await ctx.send("You have 1 minute to submit a solution (doesn't have to be correct) for https://www.codechef.com/problems/FLOW006")
			l = await misc.getSubmissions()
			lastSubmitTime = l[0]
			user = User(str(ctx.message.author.id), h, str(rating))
			await verifyUser(ctx, user, lastSubmitTime)


@bot.command()
async def handle(ctx, name: str):
	user = None
	name = name.lower()		
	for m in server.members:
		if name in m.name.lower():
			user = db.searchUsers(str(m.id))
			if user != None:
				break
	if user == None:
		await ctx.send("User not found in the database.")
	else:
		await ctx.send(user.handle + ' has a rating of ' + user.rating + '.\nhttps://www.codechef.com/users/' + user.handle)

@bot.command()
@commands.has_role('moderators')
async def exit(ctx):
	quitMessage = [ "[Error 69] _commits SUDOKU_", "I'm ending my life...", "I don't feel so good...", "Alright boys, fun's over.", "Mark my words... I will come back." ]
	await ctx.send(random.choice(quitMessage))
	await bot.close()
	exit(0)

bot.run(TOKEN)
from os import environ as cred
import re

import discord
from discord import HTTPException

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
TOKEN = cred['DISCORD_TOKEN']

role_messages = []
home_server: discord.Guild

roles = {
	'he/him': 'placeholder',
	'she/her': 'placeholder',
	'they/them': 'placeholder',
	'any': 'placeholder'
}


@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, user: discord.Member):
	print(f'Reaction detected: {reaction.emoji}')
	if user.id == client.user.id:
		return
	if reaction.message in role_messages:
		if reaction.emoji == '1️⃣':
			await user.add_roles(roles['he/him'])
			print(f'Assigned "He/Him" role to {user.name}')
			return
		elif reaction.emoji == '2️⃣':
			await user.add_roles(roles['she/her'])
			print(f'Assigned "She/Her" role to {user.name}')
			return
		elif reaction.emoji == '3️⃣':
			await user.add_roles(roles['they/them'])
			print(f'Assigned "They/Them" role to {user.name}')
			return
		elif reaction.emoji == '4️⃣':
			await user.add_roles(roles['any'])
			print(f'Assigned "Any" role to {user.name}')
			return
		elif reaction.emoji == '❓':
			if not user.dm_channel:
				await user.create_dm()
			await user.send('DM me with your custom pronouns, exactly as they will appear in the role')
			return


@client.event
async def on_reaction_remove(reaction, user: discord.Member):
	print(f'Reaction removal detected: {reaction.emoji}')
	if user.id == client.user.id:
		return
	if reaction.message in role_messages:
		if reaction.emoji == '1️⃣':
			try:
				await user.remove_roles(roles['he/him'])
				print(f'Removed "He/Him" role from {user.name}')
			except HTTPException:
				pass
			return
		elif reaction.emoji == '2️⃣':
			try:
				await user.remove_roles(roles['she/her'])
				print(f'Removed "She/Her" role to {user.name}')
			except HTTPException:
				pass
			return
		elif reaction.emoji == '3️⃣':
			try:
				await user.remove_roles(roles['they/them'])
				print(f'Removed "They/Them" role to {user.name}')
			except HTTPException:
				pass
			return
		elif reaction.emoji == '4️⃣':
			try:
				await user.remove_roles(roles['any'])
				print(f'Removed "Any" role to {user.name}')
			except HTTPException:
				pass
			return


@client.event
async def on_message(message: discord.Message):
	global home_server
	channel = message.channel

	if message.author.id == client.user.id:
		return
	# await channel.send('I see your message!')
	print('message detected: ' + message.content)

	if not message.guild:
		print('private message')
		# creates a role from the DM, then assigns that role to the member
		r: discord.Role = await home_server.create_role(
			name=message.content,
			reason='Custom pronoun role'
		)
		try:
			member = home_server.get_member(message.author.id)
			await member.add_roles(r)
			print(f'Assigned role "{r}" to {member.name}')
		except AttributeError:
			print(f'User name: {message.author.name}')
			print(f'User id: {message.author.id}')
			print(f'home server member list {home_server.members}')
		return
	else:
		if re.match(r'^!here$', message.content.strip()):
			# creates a message for users to react to, adds it to role_messages, sets the message's guild as
			# home_server, and deletes the message that summons it
			m: discord.Message = await channel.send(
				'Please React to this message to pick your pronouns!\n'
				':one: is for **He/Him**\n'
				':two: is for **She/Her**\n'
				':three: is for **They/Them**\n'
				':four: is for **Any pronouns**\n'
				'❓ is for **Custom pronouns**'
			)
			await m.add_reaction('1️⃣')
			await m.add_reaction('2️⃣')
			await m.add_reaction('3️⃣')
			await m.add_reaction('4️⃣')
			await m.add_reaction('❓')
			role_messages.append(m)
			home_server = message.guild

			# pre-existing pronoun roles in the server
			roles['he/him'] = home_server.get_role(851312714269720596)
			roles['she/her'] = home_server.get_role(851312774448676874)
			roles['they/them'] = home_server.get_role(851312813368803358)
			roles['any'] = home_server.get_role(851312852438351892)

			await message.delete()
			print(f'Role message created in {message.channel.name}')
			return


client.run(TOKEN)

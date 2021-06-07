from os import environ as cred
import re

import discord

client = discord.Client
TOKEN = cred['DISCORD_TOKEN']

role_messages: list[discord.Message] = []
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
	if reaction.message in role_messages:
		if reaction.emoji == '1️':
			await user.add_roles(roles['he/him'])
			return
		elif reaction.emoji == '2️':
			await user.add_roles(roles['she/her'])
			return
		elif reaction.emoji == '3️':
			await user.add_roles(roles['they/them'])
			return
		elif reaction.emoji == '4️':
			await user.add_roles(roles['any'])
			return
		elif reaction.emoji == '❓':
			if not user.dm_channel:
				await user.create_dm()
			await user.send('DM me with your custom pronouns, exactly as they will appear in the role')


@client.event
async def on_message(message: discord.Message):
	global home_server
	channel = message.channel
	user_id: int = message.author.id
	if channel.type == 'private':
		# creates a role from the DM, then assigns that role to the member
		r: discord.Role = await home_server.create_role(
			name=message.content,
			reason='Custom pronoun role'
		)
		await home_server.get_member(user_id).add_roles([r])
		return
	elif channel.type == 'text':
		if re.match(r'!here', message.content):
			# creates a message for users to react to, adds it to role_messages, sets the message's guild as
			# home_server, and deletes the message that summons it
			m: discord.Message = await channel.send(
				'Please React to this message to pick your pronouns!\n'
				'1️ is for **He/Him**\n'
				'2️ is for **She/Her**\n'
				'3️ is for **They/Them**\n'
				'4️ is for **Any pronouns**\n'
				'❓ is for **Custom pronouns**'
			)
			await m.add_reaction('1️')
			await m.add_reaction('2️')
			await m.add_reaction('3️')
			await m.add_reaction('4️')
			await m.add_reaction('❓')
			role_messages.append(m)
			home_server = message.guild

			await message.delete()
			return


client.run(TOKEN)

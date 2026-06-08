import asyncio

import discord
from discord import guild
from discord.ext import commands # commands from discord extensions
from discord import app_commands # this and above line required to write slash commands

import logging
from dotenv import load_dotenv # this statement is used to allow to import our Discord Token (Private Key) from our .env file
import os

load_dotenv() # loads token from environment variable file (.env)
token = os.getenv('DISCORD_TOKEN') # getting out Discord Token from the .env file

logging_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # creating a file that will handle logging (name=discord.log; mode=write[w])


# setting up the intents that bot
intents = discord.Intents.none() # creates an "Intents" instance (class obj, where "Intents" is the class, "discord" is the module - "none()" is the class method for "Intents") - no intents set
# specifying manual intents; refer "https://discordpy.readthedocs.io/en/stable/api.html?highlight=intents#intents" for all Intents-class attributes (attr) and methods
intents.bans = True # allowing for Member properties (attr and methods); analogous to intents.moderation = True
intents.messages = True
intents.message_content = True # reading message content
intents.members = True
intents.reactions = True # allowing for a Bot reacting to a reaction placed on a message in that channel



# this is another way of creating a bot instance - the Bot-command creation process is a subclass of the discord.Client class
# Note: when developing slash commands, need to inherit from "discord.ext.commands.Bot" instead of "discord.Client"
class Client(commands.Bot):
# creating the discord application, by inheriting from "discord.Client" (which is the notation for inheritance)
# Regular class notation is as such: "class myClass:" with no parentheses. I.e. parentheses is only used for inheritance

  async def on_ready(self):
    print(f"Logged in as: '{self.user}'")

    # to utilize our slash commands, we have to do the "synced" line, where we force our slash commands to forcibly sync and show up
    try:
      guild = discord.Object(id=1511153803909398538)
      # synced = await self.tree.sync(guild=GUILD_ID)
      # print(f"Synced {len(synced)} commands to guild {guild.id}") # way to check if the "synced" var was successful
      # by printing a number (in the terminal) of all the possible slash commands written for the bot so the specific server being developed for

    except Exception as e:
      print(f"Whoops, error syncing commands: {e}")

  # used to receive messages from the discord server
  async def on_message(self, message : discord.Message):
    if message.author == self.user: # to avoid the case where the bot replies to itself
      return

    # if message.content.startswith('@everyone'): # hits if the message starts with "hello"
    if "@everyone" in message.content: # this does the same as the above line
      await message.channel.send(f"Hi there {message.author.mention}")

    await self.process_commands() # required! when overriding the on_message() method to process further commands

  async def detect(self, message : discord.Message):
    pass # detects all the types of content in a bot discord msg (like the product being promoted, or other common phrases)

  # the ban_kick method -> once triggered the message will be deleted (in the on_message() event) and trigger the function
  async def ban_kick_Member(self, member: discord.Member, channel):
    # catching errors
    try:
      await member.ban(reason="Bot!")  # bans said member
      await member.kick(reason="Bot!")  # kicks said member
      await channel.send(
        f"{member.mention} was a bot and was thus BANNED and KICKED by {self.user} the great! FEAR ME, RAHH!")  # sending message of the kick and ban of said member

    except Exception as e:
      await channel.send(f"The Exception captured was: {e}\n'@CompE Club Exec' for tech_Support")


# Note: if the bot stops running (after script is terminated); then rerun and then perform a reaction on a msg (which was sent before the bot was terminated), the bot will
# not respond to the reaction as described below. It will only respond to msgs that have been reacted to after the bot is run again (the script is rerun)
# most likely to do with caches etc
  async def on_reaction_add(self, reaction, user): # response if someone reacts to a msg
    # Note: "Intents.reactions = True" for ANY "Reactions" event
      await reaction.message.channel.send("You reacted")




client = Client(command_prefix="$", intents=intents) # where the command prefix represents how to interact with a bot



client.run(token, log_handler=logging_handler, log_level=logging.DEBUG)

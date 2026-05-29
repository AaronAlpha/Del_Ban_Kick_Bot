import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import webServer_keepAlive as keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

keep_alive.keep_alive() # used (in conjunction with a Flask server) to maintain the uptime of the disc bot

handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')

intents = discord.Intents.default()
intents.members = True
intents.messages= True                                                                                                  # intent enabled to detect messages in the specific channel
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents) # indicates how to 'call on'/reference the bot using which prefix - !, #, / or anything else, can also be multiple keywords


@bot.event # a python decorator
async def on_ready(): # because this uses the async/await notation, we require the async keyword!
    print(f"we are ready to go, {bot.user.name}")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return




    await bot.process_commands(message) # what is this used for?


async def ban_kick_Member(member: discord.Member, channel):

    # catching errors
    try:
        await member.ban(reason="Bot!")                                                                                 # bans said member
        await member.kick(reason="Bot!")                                                                                # kicks said member
        await channel.send(f"{member.mention} was a bot and was thus BANNED and KICKED by {bot.user.name} the great! FEAR ME, RAHH!") # sending message of the kick and ban of said member

    except Exception as e:
        await channel.send(f"The Exception captured was: {e}\n'@CompE Club Exec' for tech_Support")

bot.run(token, log_handler = handler, log_level = logging.DEBUG)



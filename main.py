import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webServer_keepAlive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')

intents = discord.Intents.default()
intents.members = True
intents.messages= True                                                                                                  # intent enabled to detect messages in the specific channel
                                                                                            # initialized to use 'on_guild_join(guild)' for when the bot has been added to a server

bot = commands.Bot(command_prefix='/', intents=intents) # indicates how to 'call on'/reference the bot using which prefix - !, #, / or anything else, can also be multiple keywords


@bot.event # a python decorator
async def on_ready(): # because this uses the async/await notation, we require the async keyword!
    print(f"we are ready to go, {bot.user.name}")

# @bot.command()
# async def assignChannel(ctx, *, channelName):
#     try:
#         await ctx.author.send(f"You sent {channelName} as the channel name")
#     except Exception as e:
#         await ctx.send(e)

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.channel.id == 1465197237092225197:
        print(message.author) # prints out the author of the message

        # catching errors
        try:
            await message.delete()                                                                                      # deleting the author's message
            # await message.channel.send(f"{message.author.mention} - The bot's message has been deleted!")             # optional statement that will be printed to the screen after deleting the message
        except Exception as e:
            print(f"Exception: {e}")

        # refers to func kick_ban_Member to carry out the ban and kick process in that order
        await ban_kick_Member(message.author, message.channel)  # listens and triggers the event kick


async def ban_kick_Member(member: discord.Member, channel):

    # catching errors
    try:
        await member.ban(reason="Bot!")                                                                               # bans said member
        await member.kick(reason="Bot!")                                                                                # kicks said member
        await channel.send(f"{member.mention} was a bot and was thus BANNED and KICKED by {bot.user.name} the great! FEAR ME, RAHH!") # sending message of the kick and ban of said member

    except Exception as e:
        await channel.send(f"The Exception captured was: {e}\n'@CompE Club Exec' for tech_Support")

bot.run(token, log_handler = handler, log_level = logging.DEBUG)

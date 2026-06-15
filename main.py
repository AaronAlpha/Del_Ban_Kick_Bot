import regex as re # used for detecting predictable phrases
import asyncio
import discord
from discord import guild
from discord.ext import commands # commands from discord extensions
from discord import app_commands # this and above line required to write slash commands

import logging
from dotenv import load_dotenv # this statement is used to allow to import our Discord Token (Private Key) from our .env file
import os

import webServer_keepAlive as keep_alive


keep_alive.keep_alive()


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


  # RegEx stuff - the pattern to look for; class-defined

  # ticket pattern (for those selling tickets) - this doesn't work
  # tickets_pattern : str = ("(@everyone|Hi @everyone|Hi everyone)?\\!\\s*(I'm|Im|im)\\s*(looking to sell my tickets to)\\s*[A-"
  #                  "Za-z]\\s*(for)\\s*([\\w+], [\\w+] [\\d+],)\\s*[A-Za-z]+\\s*(at)\\s*[A-Za-z]\\s*(,)\\s*[A-Za-z]\\s*\\.?\\s*"
  #                          "(A-Za-z)\\s*(if interested)\\s*\\.?")

  tickets_pattern : str = ("(@everyone|Hi\\s*@everyone|Hi\\s*everyone|hi\\s*@everyone|hi\\s*everyone)?\\s*([A-Za-z]|my)\\s*(looking)*\\s*(to)*\\s*(sell)\\s*[A-Za-z]*\\s*(tickets)\\s*"
                           "([A-Za-z]|to)*\\s*(taylor\\s*swift|billie\\s*eilish|dua\\s*lipa|the\\s*weekend|sabrina\\s*carpenter|[A-Za-z])+\\s*(for|[A-Za-z])\\s*(([A-Za-z]|mon(day)*|tue(sday)*|wed(nesday)*|thur(sday)*|fri(day)*|sat(urday)*|sun(day)*)*,*\\s*"
                           "([A-Za-z]|jan(uary)*|feb(ruary)*|mar(ch)*|apr(il)*|may|jun(e)*|jul(y)*|aug(ust)*|sep(tember)*|oct(ober)*|nov(ember)*|dec(ember)*)*\\s*[0-9],*)\\s*[A-Za-z0-9]*\\s*(at|[A-Za-z])\\s*[A-Za-z\\s],*\\s*(vancouver|toronto|montreal|[A-Za-z]).*\\s*"
                           "(hmu|msg\\s*(me)*|[A-Za-z])*\\s*(if|[A-Za-z])*\\s*(interested)\\s*.*")

  # gift_card pattern (for those giving out links to scam sites, dressed as gift cards) - this works
  gift_card_pattern : str = "(@everyone)?\\s*(steam|[A-Za-z])\\s*(gift\\s*card)\\s*\\$*\\s*[0-9]\\s*\\$*\\s*[-]*\\s*[A-Za-z0-9/.]\\n*(@everyone)?"

  # all forms of Products being sold (macbooks/cameras etc) - needs work
  # product_pattern : str = ("(i|[a-z])*\\s*(want|[a-z])*\\s*(to|[a-z])*\\s*(give|[a-z])*\\s*(out|[a-z])*\\s*(my|[a-z])\\s*(macbook|canon|[a-z])*\\s*(air|camera|[a-z])*\\s*(202[0-9])*\\s*((&\\s*charger\\*\\*)\\s*(for\\s*free))*,*\\s*[a-z]*\\s*(perfect\\s*health)\\s*[a-z]*(good\\s*as\\s*new)*,*(alongside\\s*a\\s*charger)*\\s*(so\\s*it’s\\s*perfect)*,*\\s*(i)*\\s*(want\\s*to)*"
  #                          "(give\\s*it\\s*out)*\\s*(because\\s*(i\\s*just\\s*got\\s*a)*\\s*new\\s*model)*\\s*[a-z]*\\s*((thought\\s*of\\s*giving)*\\s*(out\\s*the)*\\s*(old\\s*one)*\\s*(to\\s*someone)*\\s*(who can’t)*\\s*"
  #                          "(afford\\s*one)*)*\\s*[a-z]*\\s*(((dire)*\\s*need)*\\s*of\\s*it)*\\s*(…)*\\s*(strictly\\s*first\\s*come\\s*first\\s*serve\\s*!)*\\n*(dm)\\s*(if you|[a-z])*\\s*(are|[a-z])*\\s*(interested)\\s*(text)\\s*(me directly on|[a-z])*\\s*"
  #                          "(messenger|whatsapp|instagram|facebook|[a-z])*\\s*(([a-z0-9]+@(gmail|icloud)\\.com))")

  product_pattern : str = ("(i|[a-z])*\\s*(want|[a-z])*\\s*(to|[a-z])*\\s*(give|[a-z])*\\s*(out|[a-z])*\\s*(my|[a-z])\\s*(macbook|canon|[a-z])*\\s*(air|camera|[a-z])*\\s*(202[0-9])*\\s*((&\\s*charger\\*\\*)\\s*(for\\s*free))*,*\\s*[a-z]*\\s*(perfect\\s*health)\\s*[a-z]*(good\\s*as\\s*new)*,*(alongside\\s*a\\s*charger)*\\s*(so\\s*it’s\\s*perfect)*,*\\s*(i)*\\s*(want\\s*to)*\\s*"
                           "(give\\s*it\\s*out)*\\s*(because\\s*(i\\s*just\\s*got\\s*a)*\\s*new\\s*model)*\\s*[a-z]*\\s*(thought\\s*of\\s*giving)*\\s*(out\\s*the)*\\s*(old\\s*one)*\\s*(to\\s*someone)*\\s*(who\\s*can’t)*\\s*(afford\\s*one)*\\s*[a-z]*\\s*((dire)*\\s*need)*\\s*(of\\s*it)*\\s*"
                           "(…)*\\s*(strictly\\s*first\\s*come\\s*first\\s*serve\\s*(!)*)*[\\s\\n]*(dm)*\\s*(if\\s*you|[a-z])*\\s*(are|[a-z])*\\s*(interested)*\\s*(text)*\\s*(me)*\\s*(directly)*\\s*(on|[a-z])*\\s*(messenger|whatsapp|instagram|facebook|[a-z])*\\s*([a-z0-9]+@(gmail|icloud|[a-z])\\.(com|[a-z]))")



  async def on_ready(self):
    print(f"Logged in as: '{self.user}'")



  # used to receive messages from the discord server
  async def on_message(self, message : discord.Message):
    if message.author == self.user: # to avoid the case where the bot replies to itself
      return

    products_lowercase : list[str] = ["playstation", "ps5", "xbox", "nintendo", "macbook", "dell", "msi", "iphone", "samsung", "phone", "canon", "tickets", ]
    contact_lowercase : list[str] = ["msg me", "message me", "dm me", "whatsapp", "@gmail.com", "@icloud.com"]

    if re.search(pattern=self.product_pattern,string=message.content.lower()):
      await message.channel.send("Yee")
      await message.delete() # deletes the message put in the channel
    else:
      await message.channel.send("Nee")
      await message.channel.send(message.content.lower())



    await self.process_commands() # required! when overriding the on_message() method to process further commands

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




client = Client(command_prefix="$", intents=intents) # where the command prefix represents how to interact with a bot - no just use slash command



client.run(token, log_handler=logging_handler, log_level=logging.DEBUG)

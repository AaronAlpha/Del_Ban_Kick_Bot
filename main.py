from shutil import RegistryError

import regex as re # used for detecting predictable phrases
import asyncio
import discord
from discord import guild
from discord.ext import commands # commands from discord extensions
from discord import app_commands # this and above line required to write slash commands

import logging
from dotenv import load_dotenv # this statement is used to allow to import our Discord Token (Private Key) from our .env file
import os

# import webServer_keepAlive as keep_alive


# keep_alive.keep_alive()


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

  # tickets_pattern : str = ("(@everyone|Hi\\s*@everyone|Hi\\s*everyone|hi\\s*@everyone|hi\\s*everyone)?\\s*([A-Za-z]|my)\\s*(looking)*\\s*(to)*\\s*(sell)\\s*[A-Za-z]*\\s*(tickets)\\s*"
  #                          "([A-Za-z]|to)*\\s*(taylor\\s*swift|billie\\s*eilish|dua\\s*lipa|the\\s*weekend|sabrina\\s*carpenter|[A-Za-z])+\\s*(for|[A-Za-z])\\s*(([A-Za-z]|mon(day)*|tue(sday)*|wed(nesday)*|thur(sday)*|fri(day)*|sat(urday)*|sun(day)*)\\s*,*\\s*"
  #                          "([A-Za-z]|jan(uary)*|feb(ruary)*|mar(ch)*|apr(il)*|may|jun(e)*|jul(y)*|aug(ust)*|sep(tember)*|oct(ober)*|nov(ember)*|dec(ember)*)\\s*[0-9],*)\\s*[A-Za-z0-9]*\\s*(at|[A-Za-z])\\s*[A-Za-z\\s],*\\s*(vancouver|toronto|montreal|[A-Za-z]).*\\s*"
  #                          "(hmu|msg\\s*(me)*|[A-Za-z])*\\s*(if|[A-Za-z])*\\s*(interested)\\s*.*")
  #
  # # gift_card pattern (for those giving out links to scam sites, dressed as gift cards) - this works
  # gift_card_pattern : str = "(@everyone)?\\s*(steam|[A-Za-z])\\s*(gift\\s*card)\\s*\\$*\\s*[0-9]\\s*\\$*\\s*[-]*\\s*[A-Za-z0-9/.]\\n*(@everyone)?"
  #
  # # all forms of Products being sold (macbooks/cameras etc) - needs work
  # # product_pattern : str = ("(i|[a-z])*\\s*(want|[a-z])*\\s*(to|[a-z])*\\s*(give|[a-z])*\\s*(out|[a-z])*\\s*(my|[a-z])\\s*(macbook|canon|[a-z])*\\s*(air|camera|[a-z])*\\s*(202[0-9])*\\s*((&\\s*charger\\*\\*)\\s*(for\\s*free))*,*\\s*[a-z]*\\s*(perfect\\s*health)\\s*[a-z]*(good\\s*as\\s*new)*,*(alongside\\s*a\\s*charger)*\\s*(so\\s*it’s\\s*perfect)*,*\\s*(i)*\\s*(want\\s*to)*"
  # #                          "(give\\s*it\\s*out)*\\s*(because\\s*(i\\s*just\\s*got\\s*a)*\\s*new\\s*model)*\\s*[a-z]*\\s*((thought\\s*of\\s*giving)*\\s*(out\\s*the)*\\s*(old\\s*one)*\\s*(to\\s*someone)*\\s*(who can’t)*\\s*"
  # #                          "(afford\\s*one)*)*\\s*[a-z]*\\s*(((dire)*\\s*need)*\\s*of\\s*it)*\\s*(…)*\\s*(strictly\\s*first\\s*come\\s*first\\s*serve\\s*!)*\\n*(dm)\\s*(if you|[a-z])*\\s*(are|[a-z])*\\s*(interested)\\s*(text)\\s*(me directly on|[a-z])*\\s*"
  # #                          "(messenger|whatsapp|instagram|facebook|[a-z])*\\s*(([a-z0-9]+@(gmail|icloud)\\.com))")
  #
  # product_pattern : str = ("(i|[a-z])*\\s*(want|[a-z])*\\s*(to|[a-z])*\\s*(give|[a-z])*\\s*(out|[a-z])*\\s*(my|[a-z])\\s*(macbook|canon|[a-z])*\\s*(air|camera|[a-z])*\\s*(202[0-9])*\\s*((&\\s*charger\\*\\*)\\s*(for\\s*free))*,*\\s*[a-z]*\\s*(perfect\\s*health)\\s*[a-z]*(good\\s*as\\s*new)*,*(alongside\\s*a\\s*charger)*\\s*(so\\s*it’s\\s*perfect)*,*\\s*(i)*\\s*(want\\s*to)*\\s*"
  #                          "(give\\s*it\\s*out)*\\s*(because\\s*(i\\s*just\\s*got\\s*a)*\\s*new\\s*model)*\\s*[a-z]*\\s*(thought\\s*of\\s*giving)*\\s*(out\\s*the)*\\s*(old\\s*one)*\\s*(to\\s*someone)*\\s*(who\\s*can’t)*\\s*(afford\\s*one)*\\s*[a-z]*\\s*((dire)*\\s*need)*\\s*(of\\s*it)*\\s*"
  #                          "(…)*\\s*(strictly\\s*first\\s*come\\s*first\\s*serve\\s*(!)*)*[\\s\\n]*(dm)*\\s*(if\\s*you|[a-z])*\\s*(are|[a-z])*\\s*(interested)*\\s*(text)*\\s*(me)*\\s*(directly)*\\s*(on|[a-z])*\\s*(messenger|whatsapp|instagram|facebook|[a-z])*\\s*([a-z0-9]+@(gmail|icloud|[a-z])\\.(com|[a-z]))")

  tickets_pattern : str = ("(hi|hello|[a-z0-9.,/·])?\\s*(guys|(@)*everyone|anyone|[a-z0-9.,/·])*\\s*(interested|ended|[a-z0-9.,/·])\\s*(sell|buying|with)\\s*([a-z0-9.,/·]|tickets|tix|tic(s)*)\\s*[a-z0-9.,/·]*\\s*"
                           "(hmu|msg\\s*(me)*|text\\s*(me)*|[a-z0-9.,/·])*\\s*(if|[a-z0-9.,/·])*\\s*(interested|[a-z0-9.,/·])*\\s*[a-z0-9.,/·]*\\s*(messenger|whatsapp|instagram|facebook|[a-z0-9.,/·])*"
                           "\\s*(([a-z0-9]+@(gmail|icloud|[a-z])\\.(com|[a-z]))|([0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]))*")

  # gift_card pattern (for those giving out links to scam sites, dressed as gift cards) - this works
  gift_card_pattern : str = "(@everyone)?\\s*(steam|[A-Za-z])\\s*(gift\\s*card)\\s*\\$*\\s*[0-9]\\s*\\$*\\s*[-]*\\s*[A-Za-z0-9/.]\\n*(@everyone)?"

  # product_pattern : str = ("(hi|hello|[a-z0-9.,/·])?\\s*[a-z0-9.,/·]*\\s*(guys|@everyone|everyone|[a-z0-9.,/·])\\s*[a-z0-9.,/·]*\\s*(give|giving|[a-z0-9.,/·])\\s*(out|[a-z0-9.,/·])\\s*(my|[a-z0-9.,/·])\\s*"
  #                          "(macbook|canon|laptop|[a-z0-9.,/·])\\s*[a-z0-9.,/·]*\\s*(air|camera|[a-z0-9.,/·])*\\s*(202[0-9])*\\s*((&)*\\s*charger)\\s*[a-z0-9.,/]*\\s*(for\\s*free|[a-z0-9.,/])\\s*[a-z0-9.,/·]*\\s*"
  #                          "((perfect\\s*health)|[a-z0-9.,/])\\s*[a-z0-9.,/·]*\\s*((good\\s*as\\s*new)|[a-z0-9.,/·])\\s*[a-z0-9.,/·]*\\s*(alongside\\s*a\\s*charger)\\s*[a-z0-9.,/·]*\\s*((so\\s*it’s\\s*perfect)|[a-z0-9.,/·])\\s*[a-z0-9.,/·]*\\s*(i|[a-z0-9.,/·])*\\s*((want\\s*to)|[a-z0-9.,/·])\\s*"
  #                          "((give\\s*it\\s*out)|[a-z0-9.,/·])\\s*((because\\s*((i\\s*just\\s*got\\s*a)|[a-z0-9.,/·])*\\s*new\\s*model)|[a-z0-9.,/·])\\s*[a-z0-9.,/·]*\\s*((thought\\s*of)*\\s*giving)\\s*((out\\s*(the)*)|[a-z0-9.,/])*\\s*((old\\s*(one)*)|[a-z0-9.,/])\\s*"
  #                          "((to\\s*someone)|[a-z0-9.,/·])*\\s*((who\\s*can’t)|[a-z0-9.,/·])*\\s*((afford\\s*(one)*)|[a-z0-9.,/])\\s*[a-z0-9.,/·]*\\s*((dire)*\\s*need)*\\s*(of\\s*it)*\\s*(…)*\\s*((strictly\\s*first\\s*come\\s*first\\s*serve\\s*(!)*)|[a-z0-9.,/])\\s*"
  #                          "(dm)*\\s*(if\\s*you|[a-z0-9.,/·])*\\s*(are|[a-z0-9.,/·])*\\s*(interested)*\\s*(text)*\\s*(me)*\\s*(directly)*\\s*(on|[a-z0-9.,/·])*\\s*(messenger|whatsapp|instagram|facebook|[a-z0-9.,/·])\\s*([a-z0-9]+@(gmail|icloud|[a-z])\\.(com|[a-z]))")

  product_pattern : str = ("(hi|hello|hey|[a-z0-9.,/·])?\\s*[a-z0-9.,/·]*\\s*")

  
  tickets_lowercase : list[str] = ["(would)*\\s*(any(one|body))*\\s*(be)*\\s*interested\\s*in\\s*buying\\s*(my)*\\s*(tickets|tix|tics)", "won't\\s*be\\s*able\\s*to\\s*make\\s*it\\s*to\\s*the\\s*concert","(people\\s*got\\s*them\\s*for)*\\s*[a-z0-9.,/·]\\s*(look\\s*like\\s*they'll\\s*be\\s*dropping\\s*out)*"]
  products_lowercase : list[str] = ["playstation\\s*[0-9]", "ps\\s*[0-9]", "xbox(1|x|xs|360)", "nintendo", "macbook\\s*air", "dell", "msi", "iphone\\s*[0-9]*", "samsung\\s*[a-z0-9]*", "phone", "canon\\s*(camera)*", "tickets", "tics", "tix"]
  contact_lowercase : list[str] = ["msg\\s*me", "hmu\\s*(up)*\\s*if\\s*(you're)*\\s*interested", "message\\s*me", "dm\\s*(me)*", "whatsapp\\s*[0-9][0-9[0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", "[a-z0-9]+@gmail.com", "[a-z0-9]+@icloud.com"]


# [a-z0-9.,/·]*

  REGEX_patterns : list[str] = [tickets_pattern, gift_card_pattern, product_pattern]



  async def on_ready(self):
    print(f"Logged in as: '{self.user}'")



  # used to receive messages from the discord server
  async def on_message(self, message : discord.Message):
    if message.author == self.user: # to avoid the case where the bot replies to itself
      return

    for pattern in self.tickets_lowercase:
      if re.findall(pattern=pattern, string=message.content.lower()):
        if await self.detect(message):
          print("Yee tix")
          await message.delete()  # deletes the message put in the channel
          try:
            await self.ban_kick_Member(message.author, message.channel)
          except Exception as e:
            await message.channel.send(f"Error trying to ban_kick; reason: {e}")
            await self.process_commands(message)
            return

          await message.author.send( # private DMs the message.author
            f"Hi {message.author.mention}, you just got banned from the University of Alberta's \"Computer Engineering Club\" server that {self.user} is a part of.\n{self.user} exists to detect and catch certain phrases that are \"forbidden\" to be used in the server; "
            f"you typed a message that contained one or more of these such phrases and have thus been ban and kicked.\n\nThis is the message that you typed (which contains \"forbidden\" phrases) to get banned:\n\"\n{message.content}\n\""
            f"\n\nIf you feel you have been wrongly chosen to be banned and kicked, please DM \".chocolate.milk.\" with an appropriate reason; you will be judge by the Moderators/Exec Team of the club.\nThanks")

          await self.process_commands(message)

          return
        else:
          print("Nee")

    for pattern in self.products_lowercase:
      if re.findall(pattern=pattern, string=message.content.lower()):
        if await self.detect(message):
          print("Yee prods")
          await message.delete()  # deletes the message put in the channel

          try:
            await self.ban_kick_Member(message.author, message.channel)
          except Exception as e:
            await message.channel.send(f"Error, could not ban_kick {message.author}, the reason: {e}\n'@CompE Club Exec' for tech_Support")
            await self.process_commands(message)
            return

          await message.author.send( # private DMs the message.author
            f"Hi {message.author.mention}, you just got banned from the University of Alberta's \"Computer Engineering Club\" server that {self.user} is a part of.\n{self.user} exists to detect and catch certain phrases that are \"forbidden\" to be used in the server; "
            f"you typed a message that contained one or more of these such phrases and have thus been ban and kicked.\n\nThis is the message that you typed (which contains \"forbidden\" phrases) to get banned:\n\"\n{message.content}\n\""
            f"\n\nIf you feel you have been wrongly chosen to be banned and kicked, please DM \".chocolate.milk.\" with an appropriate reason; you will be judge by the Moderators/Exec Team of the club.\nThanks")

          await self.process_commands(message)

          return
        else:
          print("Nee")

    for pattern in self.contact_lowercase:
      if re.findall(pattern=pattern, string=message.content.lower()):
        if await self.detect(message):
          print("Yee contacs")
          await message.delete()  # deletes the message put in the channel

          try:
            await self.ban_kick_Member(message.author, message.channel)
          except Exception as e:
            await message.channel.send(f"Error trying to ban_kick; reason: {e}")
            await self.process_commands(message)
            return

          await message.author.send( # private DMs the message.author
            f"Hi {message.author.mention}, you just got banned from the University of Alberta's \"Computer Engineering Club\" server that {self.user} is a part of.\n{self.user} exists to detect and catch certain phrases that are \"forbidden\" to be used in the server; "
            f"you typed a message that contained one or more of these such phrases and have thus been ban and kicked.\n\nThis is the message that you typed (which contains \"forbidden\" phrases) to get banned:\n\"\n{message.content}\n\""
            f"\n\nIf you feel you have been wrongly chosen to be banned and kicked, please DM \".chocolate.milk.\" with an appropriate reason; you will be judge by the Moderators/Exec Team of the club.\nThanks")

          await self.process_commands(message)

          return
        else:
          print("Nee")


    await self.process_commands(message) # required! when overriding the on_message() method to process further commands

# contains the RegEx logic to detect the phrase patterns
  async def detect(self, message : discord.Message) -> bool:
    for pattern in self.REGEX_patterns:
      if re.search(pattern=pattern, string=message.content.lower()):
        return True
    return False # if no phrase detected

  # the ban_kick method -> once triggered the message will be deleted (in the on_message() event) and trigger the function
  async def ban_kick_Member(self, member: discord.Member, channel):
    # catching errors
    try:
      # await member.ban(reason="Bot!")  # bans said member
      # await member.kick(reason="Bot!")  # kicks said member
      await channel.send(
        f"{member.mention} was a bot and was thus BANNED and KICKED by {self.user} the great! FEAR ME, RAHH!")  # sending message of the kick and ban of said member

    except Exception as e:
      await channel.send(f"The Exception (error) captured was: {e}\n'@CompE Club Exec' for tech_Support")


# Note: if the bot stops running (after script is terminated); then rerun and then perform a reaction on a msg (which was sent before the bot was terminated), the bot will
# not respond to the reaction as described below. It will only respond to msgs that have been reacted to after the bot is run again (the script is rerun)
# most likely to do with caches etc
  async def on_reaction_add(self, reaction, user): # response if someone reacts to a msg
    # Note: "Intents.reactions = True" for ANY "Reactions" event
      await reaction.message.channel.send("You reacted")




client = Client(command_prefix="$", intents=intents) # where the command prefix represents how to interact with a bot - no just use slash command



client.run(token, log_handler=logging_handler, log_level=logging.DEBUG)

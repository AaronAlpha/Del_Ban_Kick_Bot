# from shutil import RegistryError # don't know where this piece of code came from??

import regex as re  # used for detecting predictable phrases
import discord
from discord import guild
from discord.ext import commands  # commands from discord extensions
from discord import app_commands  # this and above line required to write slash commands - not required, but kept in as reminder that this bot utilizes slash commands

import logging
from dotenv import load_dotenv  # this statement is used to allow to import our Discord Token (Private Key) from our .env file
import os


# have to test if the following will work - have been working locally on the bot - need to test integration into "render.com" and "uptimerobot.com"
import webServer_keepAlive as keep_alive
keep_alive.keep_alive()


load_dotenv()  # loads token from environment variable file (.env)
token = os.getenv('DISCORD_TOKEN')  # getting out Discord Token from the .env file

logging_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')  # creating a file that will handle logging (name=discord.log; mode=write[w])

# setting up the intents that bot
intents = discord.Intents.none()  # creates an "Intents" instance (class obj, where "Intents" is the class, "discord" is the module - "none()" is the class method for "Intents") - no intents set
# specifying manual intents; refer "https://discordpy.readthedocs.io/en/stable/api.html?highlight=intents#intents" for all Intents-class attributes (attr) and methods
intents.bans = True  # allowing for Member properties (attr and methods); analogous to intents.moderation = True
intents.messages = True
intents.message_content = True  # reading message content
intents.members = True

# unrequired for this code; kept in to remind that this bot has the "reactions" intents set in Discord Dev Portal
# intents.reactions = True  # allowing for a Bot reacting to a reaction placed on a message in that channel



# this is another way of creating a bot instance - the Bot-command creation process is a subclass of the discord.Client class
# Note: when developing slash commands, need to inherit from "discord.ext.commands.Bot" instead of "discord.Client"
class Client(commands.Bot):
    # creating the discord application, by inheriting from "discord.Client" (which is the notation for inheritance)
    # Regular class notation is as such: "class myClass:" with no parentheses. I.e. parentheses is only used for inheritance

    # RegEx stuff - the pattern to look for; class-defined


    # ---- each sub-list inside the following lists are arbitrarily been chosen to represent "phrases" (and thus known as "phrases" in this code - with regards to some vars, like the 'phrase_count' var)
    # more details in README.md

    tickets_lowercase: list[list[str]] = [
        ["[a-z0-9.,/·]*\\s*(hello|hello\\s*everyone|hello\\s*@everyone|hi|hi\\s*everyone|hi\\s*@everyone)\\s*[a-z0-9.,/·]*"],
        ["([a-z0-9.,/·]*\\s*interested\\s*in\\s*buying\\s*[a-z0-9.,/·]*|[a-z0-9.,/·]*\\s*looking\\s*to\\s*sell\\s*[a-z0-9.,/·]*|[a-z0-9.,/·]*\\s*i'm\\s*selling\\s*[a-z0-9.,/·]*|[a-z0-9.,/·]*\\s*im\\s*selling\\s*[a-z0-9.,/·]*)"],
        ["[a-z0-9.,/·]*\\s*(tickets|tix|tics)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*won't\\s*[a-z0-9.,/·]*\\s*make\\s*it\\s*[a-z0-9.,/·]*\\s*concert\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*people\\s*got\\s*them\\s*for\\s*[a-z0-9.,/·]*|[a-z0-9.,/·]*myself\\[a-z0-9.,/·]*\\s*family\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*dropping\\s*out\\s*[a-z0-9.,/·]*"],  # not an imp check
        ["[a-z0-9.,/·]*\\s*(hmu|text\\s*me|send\\s*me\\s*dm|send\\s*me\\s*a\\s*dm)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*if\\s*[a-z0-9.,/·]*\\s*interested\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(messenger|whatsapp|instagram|facebook|snapchat)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(([a-z0-9]+@(gmail|icloud|[a-z])\\.(com|[a-z]))|([0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]))\\s*[a-z0-9.,/·]*"]
    ]

    gifts_lowercase: list[list[str]] = [
        ["[a-z0-9.,/·]*\\s*(everyone|@everyone)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*steam\\s*gift\\s*card\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*gift\\s*card\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(send)\\s*(me)\\s*[a-z0-9.,/·]*\\s*(direct)\\s*(msg|message)\\s*(apply)*\\s*[a-z0-9.,/·]*"]
    ]

    products_lowercase: list[list[str]] = [
        ["[a-z0-9.,/·]*\\s*(hello|hello\\s*everyone|hello\\s*@everyone|hi|hi\\s*everyone|hi\\s*@everyone|hey|hey\\s*everyone|hey\\s*@everyone|hello\\s*@everyone\\s*@here)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(i\\s*want\\s*(to|[a-z0-9.,/·])*\\s*give\\s*out\\s*my|i'm\\s*giving\\s*out\\s*my|im\\s*giving\\s*out\\s*my)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(giving\\s*out)\\s*[a-z0-9.,/·]*\\s*(macbook|phone|camera|canon|laptop|macbook\\s*(air|pro)|ps\\s*[0-9]|iphone|iphone\\s*[0-9]*|samsung|samsung\\s*[a-z0-9]*|xbox(1|x|xs|360)|playstation\\s*[0-9]|nintendo|msi)*\\s*[a-z0-9.,/·]*\\s*(202[0-9])*\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(&)*\\s*(charger)\\s*(\\*\\*)*\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(free)\\s*[a-z0-9.,/·]*\\s*(perfect\\s*health)*\\s*[a-z0-9.,/·]*\\s*(good\\s*as\\s*new)\\s*[a-z0-9.,/·]*\\s*(charger)*\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(it's|its)*\\s*(perfect)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(i\\s*want\\s*give\\s*it\\s*out)\\s*[a-z0-9.,/·]*\\s*"],
        ["[a-z0-9.,/·]*\\s*(new\\s*model)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(giving)\\s*(out)*\\s*[a-z0-9.,/·]*\\s*(old\\s*one)\\s*[a-z0-9.,/·]*"],  # not an imp check
        ["[a-z0-9.,/·]*\\s*(someone\\s*who\\s*can't|someone\\s*who\\s*cant)\\s*(afford)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(in)\\s*(dire)*\\s*(need)\\s*[a-z0-9.,/·]*\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(college)\\s*(any\\s*other)*\\s*(important\\s*stuff)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*if\\s*[a-z0-9.,/·]*\\s*interested\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(strictly\\s*first\\s*come\\s*first\\s*serve)\\s*[a-z0-9.,/·]*"],  # imp statement catch
        ["[a-z0-9.,/·]*\\s*(text|text\\s*me|dm|dm\\s*me|hmu|hmu\\s*me)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*((dm\\s*me)\\s*[a-z0-9.,/·]*\\s*(interested)|(dm\\s*me)\\s*[a-z0-9.,/·]*\\s*(interested)\\s*[a-z0-9.,/·]*\\s*(dm\\s*me)\\s*[a-z0-9.,/·]*\\s*(more\\s*info)|interested)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(send)\\s*(me)\\s*[a-z0-9.,/·]*\\s*(direct)\\s*(msg|message)\\s*(apply)*\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(messenger|whatsapp|instagram|facebook|snapchat)\\s*[a-z0-9.,/·]*"],
        ["[a-z0-9.,/·]*\\s*(([a-z0-9]+@(gmail|icloud|[a-z])\\.(com|[a-z]))|([0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]))\\s*[a-z0-9.,/·]*"]
    ]

    # ----


    async def on_ready(self): # on_ready func; bot/discord client always hits this
        print(f"Logged in as: '{self.user}'")

  
    # used to receive messages from the discord server
    async def on_message(self, message: discord.Message):
      # all print statements within this 'on_message' func serve as debugging statments to follow the "flow" of the code when usr_input is passed
      
        phrase_count = 0 # counter used to check how many common phrases exist in the arr (tickets_lowercase; gift_lowercase; products_lowercase)

      
        if message.author == self.user:  # to avoid the case where the bot replies to itself
            return

        for tic_pattern in self.tickets_lowercase:
            for phrase in tic_pattern:
                if re.findall(pattern=phrase,string=message.content.lower()):
                    print("Yee, Tickets 1")
                    phrase_count += 1

                else:
                    print("Nee, Tickets 1")

        if phrase_count >= 0.3*len(self.tickets_lowercase): # checking to see if the number of occurrences exceed 30% of the number of phrases in a list
            print("Yee, Tickets 2")
            await self.response_action(message) # performs the response - private dm-ing the individual

        else:
            phrase_count = 0
            print("Nee, Tickets 2")

    # --------------

        for gift_pattern in self.gifts_lowercase:
            for phrase in gift_pattern:
                if re.findall(pattern=phrase, string=message.content.lower()):
                    print("Yee, Gifts 1")

                    phrase_count += 1

                else:
                    print("Nee, Gifts 1")

        if len(self.gifts_lowercase) <=3: # checking to see if the number of occurrences are less than 3, then we have to check that the
            if phrase_count >= 2:
                print("Yee, Gifts 2")
                await self.response_action(message)  # performs the response - private dm-ing the individual

            else:
                phrase_count = 0
                print("Nee, Gift 2")

        else:
            if phrase_count >= 3: # want at least 3 checks (not 30%)
                print("Yee, Gifts 3")
                await self.response_action(message) # performs the response - private dm-ing the individual

            else:
                phrase_count = 0
                print("Nee, Gift 3")

    # -------------

        for product_pattern in self.products_lowercase:
            for phrase in product_pattern:
                if re.search(pattern=phrase, string=message.content.lower()):
                    print("Yee Products 1")

                    phrase_count += 1

                else:
                    print("Nee, Products 1")
        if phrase_count >= 0.3*len(self.products_lowercase):
            print("Yee, Products 2")
            await self.response_action(message) # performs the response - private dm-ing the individual

        else:
            phrase_count = 0
            print("Nee, Products 2")
            print("Not a Bot")


        await self.process_commands(message)  # required! when overriding the on_message() method to process further commands

    # following is the "response" action if the the bot has detected 30% or more phrases in from one of the 3 main lists
    async def response_action(self, message: discord.Message):
        await message.delete()  # deletes the message put in the channel
        try:
            await self.ban_kick_Member(message.author, message.channel) # calls another class function, listed below (outside the scope of this current func)
        except Exception as e:
            await message.channel.send(f"Error trying to ban_kick; error-reason: {e}")
            await self.process_commands(message)
            return

        await message.author.send(  # private DMs the message.author
            f"Hi {message.author.mention}, you just got banned from the University of Alberta's \"Computer Engineering Club\" server that {self.user} is a part of.\nA standing rule in the server is that \"self-promotion\" is disallowed, and so {self.user} exists to detect and "
            f"catch certain phrases that are commonly found in these self-promoti\"forbidden\" to be used in the server; "
            f"you typed a message that contained one or more of these such phrases and have thus been ban and kicked.\n\nThis is the message that you typed (which contains \"forbidden\" phrases) to get banned:\n\"\n{message.content}\n\""
            f"\n\nIf you feel you have been wrongly chosen to be banned and kicked, please DM \".chocolate.milk.\" with an appropriate reason; you will be judge by the Moderators/Exec Team of the club.\nThanks")

        await self.process_commands(message)

        return



    # the ban_kick method -> once triggered the message will be deleted (in the on_message() event) and trigger the function
    async def ban_kick_Member(self, member: discord.Member, channel):
        # catching errors
        try:
            await member.ban(reason="Bot!")  # bans said member
            await member.kick(reason="Bot!")  # kicks said member
            await channel.send(f"{member.mention} was a bot and was thus BANNED and KICKED by {self.user} the great! FEAR ME, RAHH!")  # sending message of the kick and ban of said member

        except Exception as e: # exists to demonstrate if an error has occurred (also avoids breaking the program)
            await channel.send(f"The Exception (error) captured was: {e}\n'@CompE Club Exec' for tech_Support")




client = Client(command_prefix="$", intents=intents)  # where the command prefix represents how to interact with a bot - Note: just use slash command (\), the ($) wont work - idk

client.run(token, log_handler=logging_handler, log_level=logging.DEBUG)

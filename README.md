# Del_Ban_Kick_Bot \*(revised Jul 1st 2026)
## Purposes
Bot designed to delete, ban and kick a user (intentionally designed for Bot-Spammers) after a message ~~has been sent into a specific channel of choice (ban-channel for eg)~~ has been sent into a channel (that the bot may access) and contains certain keywords and/or key phrases that have been analyzed to be sent from Bot Accounts. \[Note: Self-promotional material such as advertising to sell/give away devices, charged or not, is prohibited in this club server.\]\*

Designed for UofA Computer Engineering (CompE) Club discord server (Jan ~~Feb~~Jul 2026)

~~(First-ever Discord Bot development project)~~\*

Bot uses '**Render**' as the hosting service and '**UptimeRobot**' monitoring service to allow the bot stay active indefinitely.

~~(still creating command functionality to allow for an allowable discord member [server owner, admin or other] to specify which channel to label as the 'ban-channel'; for now, because this was deisgned with the CompE Club in mind, message.channel.id has been hard-set)~~ Unrequired for this project, however certain lines of code still exist in the script... for no reason.\*
---
## Software Dev Analysis
### Previous Solutions
When this project was undertaken and started in Jan \[Jan 17th\] (thanks to a Senior Exec asking me (a Junior Exec) to accomplish the task), the initial plan was to follow an internet idea to enlist one channel (which everbody had access to) of the discord server as a catch-all "fishing net"(honeypot) where active users of the discord server were given a "final warning" to never message in this honeypot-channel. Thus, whoever would message in this channel (knowingly or not) would get a non-reviewable ban (banned by the "Del_Ban_Kick_Bot", known as "Post_Ban-ner" in the server); therefore catching bot accs who would message in the honeypot-channel, due to their automation. However, this solution was quickly made obsolete, for the curated channel was never "hit". 
Bot acc spamming continuined, but never did messages enter the intended channel. Why?

As an elected Senior Exec (continuing off my term as a Junior Exec), I was able to gain access to the "modlogs" of the server - the "modlogs" is a channel that logged the **deletion of messages**, banned members, kicked members, on-member-leaves and many more. So when a Senior Exec would delete, ban and kick a bot acc (after they spammed the server), I was able to read the logs and **see where those messages were deleted(!!)**. This provided me the insight that demonstrated that this initial solution (solutionV1 = codeV1.py) was a "hit-or-miss". 
It turned out that bot accs (normally) spam messages in the "General" (a default channel in created Discord Servers) channel (almost always, if not always) and one or multiplie other accessible channels. For example, a bot acc once spammed the CompE discord server in the "General" channel and "Q-and-A" channel; it never spammed in any other channel nor the curated channel to catch bot acc.

In desiging a new solution to this (solutionV2 = codeV2.py), I had decided to open the scope of Post_Ban-ner so that the bot can ban accs from outside of one channel to all channels Post_Ban-ner had access to - to the channels bot accs had access to. However, the banning logic had to be changed with this new solution. Whereas, in solutionV1 where we could automatically ban accs based on no criteria, due to the warning and assumption, that only bot accs would message in the curated channel, once we open the scope of Post_Ban-ner, any and everybody in the "General" channel and/or others would get banned as well for just typing/sending a message.
Upon deep inspection/analysis of the bot acc spam-messages of recent times, I noticed that the messages contained the "@everyone" discord-mention-feature. So, an initial solution was to check if an inputted message contained the phrase "@everyone" and toggling "on" a boolean-switch, which would then be expanded to other common phrases with their respective "boolean-switches". However, this failled, with no further analysis.

A third design had started to be made then, solutionV3 (= codeV3.py), which expanded the above idea and was more detailed on this "flag system". And like the solutionV2 code, we would detect to see if those certain phrases existed in a message, now with more flags, divided into "recurring" flags and "optional" flags. This too was a fail. 

The reason for the failure of solutionV2 and solutionV3 was due to the incorrect understanding of text/strings. For example, if there is a check to see if the string "everyone" is in the passed-in message, the check would "hit" if the string "everyone" is in the message (python code --> if "everyone" in message.content). But, a message that contains the phrase "@everyone" would not "hit" this check to see if string "everyone" was in the message, just because the former contains the "everyone" string along with the "@" symbol - a completely different string. This flawed understanding was the reason to the failure of solutionV3's code-solution and the aforementioned solutionV2's code-solution.
A further attempt was made to include as many "permutations and combinations" of the passed-in message, but it was tideous and half-baked (as in it could work, but not for all cases).

It was clear; that what I was trying to do in solutionV2 and solutionV3, was but escaping a python-module that was designed to do exactly what I was trying to recreate through naive solutions. To be frank, I was intimidated by its reputation, and by how long it would take to learn.


### The Solution
**RegEx** (Regular Expressions) are "\[sequences\] of characters that \[specify\] a pattern in any given text". (Not as bad as its reputation precedes it - at least in this context)
Although this notion and python-module was used to develop the current solution (main.py) being hosted by Render.com and kept running indefinitely by UpTimeRobot.com, there were 2 "phases", of which the latter phase is the solution used in "main.py".

#### Phase1: Strict Capturing of phrases
After understanding the basics of RegEx through vid-follow-through and article-follow-through, an initial solution developed was to create one long string that contained the repetitive (predicatble) patterns, phrases learnt from the modlogs, but all the cases that occurred from years before; long string as a "one size fits all" approach. 
While this was a way better solution (due to the use of RegEx) it still wasn't a viable solution; the specific arrangements of the repetitive phrases made it too strict at times to catch some bannable phrases more than others. Making the RegEx more flexible ran the risk of banning non-bannable phrases - making human user messages more susceptible to be deleted and bannable.

#### Phase2: Mathematical Capturing of phrases (the solution - main.py)

---
## References
- "discord.py API Reference" : **https://discordpy.readthedocs.io/en/stable/api.html**
- "discord.ext.commands.py API Reference" : **https://discordpy.readthedocs.io/en/stable/ext/commands/api.html***
- https://nikola.dev/posts/2021-09-25/object_oriented_discord_bot
- "Understanding Regular Expressions (Regex)" : **https://medium.com/@victoriousjvictor/understanding-regular-expressions-regex-e1c048f5aa6c***
- "Regex Tip: Use \[0-9\] Instead of \d for Digit Matching" : **https://regexforge.com/blog/regex-tip-use-0-9-instead-of-d-for-digit-matching***
### Code Tutorial Vids
(Discord)
- ["How to Build a Discord Bot With Python - Full Tutorial 2025+"-"Tech With Tim"](https://www.youtube.com/watch?v=YD_N6Ffoojw&list=PLPX8wGaTDl1bRzgQKYN6NOt-aUUhTpelc&index=2)     ~~(was OLD primary vid for setting up code)~~
- ["How to make a Discord Bot in Python! (Part 8: Kick/Ban) (2021 Update)"-"James S"](https://www.youtube.com/watch?v=AhuLLkKk-C0&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=8)
- ["Creating a Discord Bot in Python (2025) | Episode 1: Setup & Basics"-"James S"](https://www.youtube.com/watch?v=CHbN_gB30Tw&list=PL-7Dfw57ZZVQ-GCNQS4Kyz637Fffhb0Hs&index=1)      *(was revised primary vid for code setup)
- ["Creating a Discord Bot in Python (2025) | Episode 2: Events"-"Jame S"](https://www.youtube.com/watch?v=0lhYddc5M9w&list=PL-7Dfw57ZZVQ-GCNQS4Kyz637Fffhb0Hs&index=3)               *(was revised primary vid for code setup)
- ["Creating a Discord Bot in Python (2025) | Episode 3: Slash Commands"-"James S"](https://www.youtube.com/watch?v=26Sj5hJFqUs&list=PL-7Dfw57ZZVQ-GCNQS4Kyz637Fffhb0Hs&index=4)    (using to develop slash commands ~~- work in progress~~; developed, but stored in "YTber_codeTutorial_codeV4_solutionBasis.txt", but is not used in program)
(Python RegEx)
- ["\[5 Minute Tutorial\] Regular Expressions (Regex) in Python"-"Kite"](https://www.youtube.com/watch?v=UQQsYXa1EHs&list=PLPX8wGaTDl1YwTzFk27Vmx6LVBpL2xWxu&index=38)              (primary/basis vid for understanding Python RegEx - and the solution of main.py)
### Bot Hosting 
-  to run Bot 24/7 (for FREE), used 'Render' Hosting : **https://render.com/**                                                                                                                    (**hosting** service used)
-  to keep Bot running indefinetely (fixing bot downtime), used [UptimeRobot](https://uptimerobot.com/) Monitoring -  public facing status page : **https://stats.uptimerobot.com/p7rgqtuuY6**    (**monitoring** service used)
-  tutorial vids:
    1. ["Host your app 24/7 with Render (Free and Unstable)"-"Gunther"](https://www.youtube.com/watch?v=FVpEDSlGG5k)      (was primary use for setting up the hosting)
    2. ["Host Your Discord Bot For Free In 2024! (Render)"-"Max Codez"](https://www.youtube.com/watch?v=HZis54wRF98)      (was 1 of 2 used for code)
    3. ["How to Host Your Discord Bot for FREE \[Python\]"-"CreepyD"](https://www.youtube.com/watch?v=kBdDmCPcbfs)        (was 1 of 2 used for code)                                            (thingy-mah-jig)

~~### Ackowledgment of use of ChatGPT~~
~~I would like to say that I don't 'like' ChatGPT (or any other AI model) for cases of breach of Academic Inegrity or misrepresentaiton of work conducted by an individual.~~

~~However, in development of this bot, there were moments where the Documentation and Tutorial Videos were: irrelevant; not enough; vague; unclear on how to use certain code; and many other related feelings of helplessness.~~

~~Thus, to help myself **_finish_** the code rather than being with **_unfinished code_** and being zero-tolerant-to-AI-usage: there were moments where I copy-pasted MY code onto ChatGPT and asked about the correctness of the code and/or why it was incorrect, and solutions to it.~~

~~I would've used the solution ideas/code **segments** provided by ChatGPT (and Google's automatically generated AI), BUT I **did not prompt and use generated code from ChatGPT or any other AI model**~~

Thank you.

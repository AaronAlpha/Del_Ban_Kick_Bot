# Del_Ban_Kick_Bot \*(revised Jul 1st 2026)
## Purposes
Bot designed to delete, ban and kick a user (intentionally designed for Bot-Spammers) after a message ~~has been sent into a specific channel of choice (ban-channel for eg)~~ has been sent into a channel (that the bot may access) and contains certain keywords and/or key phrases that have been analyzed to be sent from Bot Accounts. \[Note: Self-promotional material such as advertising to sell/give away devices, charged or not, is prohibited in this club server.\]\*

Designed for UofA Computer Engineering (CompE) Club discord server (Jan ~~Feb~~Jul 2026)

Bot uses '**Render**' as the hosting service and '**UptimeRobot**' monitoring service to allow the bot stay active indefinitely.

---

## Software Dev Analysis

TLDR ("Previous Solutions"):
1) Solution1 attempted to designate one channel to ban all those in question (honeypot idea) --> this failed because the BotAcc messages were not sent to all channels in a server but only a few ones.
2) Solution2 and Solution3 attempted to perform string-analysis to determine if a message contained certain BotAcc phrases --> this failed because "@everyone" is not the same as "everyone" - it's just how python strings work
3) Due to the way python strings work, **RegEx** had to be used

### Previous Solutions
When this project was undertaken and started in Jan \[Jan 17th\] (thanks to a Senior Exec requesting me to accomplish a task), the initial plan was to follow an internet idea to enlist one channel (which everbody had access to) of the discord server as a catch-all "fishing net"(honeypot) where active users of the discord server were given a "final warning" to never message in this honeypot-channel. Thus, whoever would message in this channel (knowingly or not) would get a non-reviewable ban (banned by the "Del_Ban_Kick_Bot", known as "Post_Ban-ner" in the server); therefore catching bot accs who would message in the honeypot-channel, due to their automation. However, this solution was quickly made obsolete, for the curated channel was never "hit". 
Bot acc spamming continuined, but never did messages enter the intended channel. Why?

As an elected Senior Exec (now resigned), I was able to gain access to the "modlogs" of the server - a channel that logged the **deletion of messages**, banned members, kicked members, on-member-leaves and many more. 
So when a Senior Exec would delete, ban and kick a bot acc (after they spammed the server), I was able to read the logs and **see where those messages were deleted(!!)**. This provided me the insight that demonstrated that this initial solution (solutionV1 = codeV1.py) was a "hit-or-miss". 
It turned out that bot accs (normally) spam messages in the "General" (a default channel in created Discord Servers) channel (almost always, if not always) and one or multiple other accessible channels. For example, a bot acc once spammed the CompE discord server in the "General" channel and "Q-and-A" channel; it never spammed in any other channel nor the curated channel to catch bot acc.

In desiging a new solution to this (solutionV2 = codeV2.py), I had decided to open the scope of Post_Ban-ner so that the bot can ban accs from outside of one channel to all channels Post_Ban-ner had access to - to the channels bot accs had access to. However, the banning logic had to be changed with this new solution. Whereas, in _solutionV1_ where we could automatically ban accs based on no criteria - due to the warning to not message in said channel - once we open the scope of Post_Ban-ner, any and everybody in the "General" channel and/or others would get banned as well for just typing/sending a message.
Upon deep inspection/analysis of the bot acc spam-messages of recent times I noticed that the messages contained the "@everyone" discord-mention-feature. Therefore, an initial solution was to check if an inputted message contained the phrase "@everyone" and toggling "on" a boolean-switch, which would then be expanded to other common phrases with their respective "boolean-switches". However, this failled, with no further analysis.

A third design had started to be made then, solutionV3 (= codeV3.py), which expanded the above idea and was more detailed on this "flag system". And like the solutionV2 code, we would detect to see if those certain phrases existed in a message; now with more flags, divided into "recurring" flags and "optional" flags. This too was a fail. 

The reason for the **failure of solutionV2 and solutionV3** was due to the **incorrect understanding of text/strings**. For example, if there is a check to see if the string "everyone" is in the passed-in message, the check would "hit" if the string "everyone" is in the message (python code --> if "everyone" in message.content). But, a message that contains the phrase "@everyone" would not "hit" this check to see if string "everyone" was in the message; just because the former contains the "everyone" keyword along with the "@" symbol - it is not the same thing, and is a completely different string. This flawed understanding was the reason to the failure of solutionV3's code-solution and the aforementioned solutionV2's code-solution.
A further attempt was made to include as many "permutations and combinations" of the passed-in message, but it was tideous and half-baked (as in, it could work, but not for all cases).

==It was clear; that what I was trying to do in solutionV2 and solutionV3, was but escaping a python-module that was designed to do exactly what I was trying to recreate through naive solutions. To be frank, I was intimidated by its reputation, and by how long it would take to learn.==




TLDR ("The Solution"):
1) The "Phase 1" solution attempted to create a "one size fits all" string that would capture ALL BotAcc messages --> this failed because although there were repetitive/distinguishable phrases, there were also subtle differences that prevented detection
2) The "Phase 2" solution used math to check a sent discord-message contained 3 or more phrases from a predefined "list of phrases" (python list of lists of string); this was to protect human-user messages if they contained phrases that were in the "list of phrases", and to also solve the "common phrases yet subtle differences challenge from 'Phase 1'".
3) Contacting the UofA CompE Club is an added form of protection to human-users if they were wrongly banned.

### The Solution
**RegEx** (Regular Expressions) are "\[sequences\] of characters that \[specify\] a pattern in any given text". (Not as bad as its reputation precedes it - at least in this context)
Although this notion and python-module was used to develop the current solution (main.py) being hosted by Render.com and kept running indefinitely by UpTimeRobot.com, there were 2 "phases", of which the latter phase is the solution used in "main.py".

#### Phase1: Strict Capturing of phrases
After understanding the basics of RegEx through vid-follow-through and article-follow-through, an initial solution developed was to create one long string that contained the repetitive (predicatble) patterns, phrases learnt from the modlogs, and all the cases that occurred from years before. That is, the initial solution was a long string as a "one size fits all" approach. 
While this was a way better solution (due to the use of RegEx) it still wasn't a viable solution; the specific arrangements of the repetitive phrases made it too strict at times to catch some bannable phrases more than others. Making the RegEx more flexible ran the risk of banning non-bannable phrases - making human-user-messages more susceptible to be deleted and bannable.

#### Phase2: Mathematical Capturing of phrases (the solution - main.py)
And so, the actual implementation/solution (main.py) used some basic math that made the RegEx check continue to detect BotAcc messages, but more safer for human-user-messages.
Upon the analysis of the modlogs and the BotAcc messages, it obvious that certain BotAcc messages were almost copy-paste from each other, yet subtly different to appear as human (and not a copy). Thus, using a "one size fits all approach" did not work because certain BotAcc messages would get detected, but others may not get detected. Due to their subtle differences.

So, it was decided to break up the large-string RegEx implementation, and only include KEY phrases that were repetitive and BotAcc-obvious; and to include them in a python-list, of lists of strings - phraseList : list\[list\[str\]\]. The choice for this was to have this python-list resemble that of a discord message, and each sub-list (of strings) was a line that was taken from these BotAcc messages; that is, this python-list was a rudimentary "equivalent" organization of phrases that more-or-less reflected the typical structure of a BotAcc message.

We would then iterate through the 2D python-list. 
If the message contains a phrase that is RegEx-equivalent to the RegEx-phrase in the sub-list of string --> a counter (defined earlier) would be incremented by 1. At the end of this double-for-loop process, we would check to see if the collected counts of detected phrases from a message (in the discord server) was greater than 30% of the number of sub-lists in the list containing the phrases.

This decision was to take into account that a discord-message sent out wouldn't contain all the phrases from a typical BotAcc message, but if it was a BotAcc message, that it would contain **AT LEAST 3 or more phrases from this "phraseList" (list of lists of string)**. 
But seeing as how these BotAcc messages were meant to simulate human-behaviour, in communication, a normal human being may have typed something that could exist in this "list of BotAcc phrases" (phraseList), and so **to take account of this as well, we intentionally maintain a "threshold" that must be passed for a message to be deemed a BotAcc-message**.

Of course, this is not full-proof:
1) BotAcc messages may evolve to the point where the current implementation of the "phraseList" would have to change in the future (or the general solution-implementation would have to change)
2) It is possible that even with the safe procedure of 30% or more achievement to be deemed a BotAcc, a human-user may still get "caught in the crossfire"

The solution to "protect" the human-users, is to provide them a contact from within the exec-team of the UofA CompE Club (for which this bot was designed for) so that they may plead their case of a false-ban and kick, and to be allowed back into the server, for their message was incorrectly judged by the Bot (a copy of the message would be sent to the user in question). 
A copy of the message would also exist in the modlogs of the discord server, so even if a banned user pleas guilty (but tampers their message when pleading a case to the exec team), the discord server would contain the message that got the user banned.

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
(Python RegEx)
- ["\[5 Minute Tutorial\] Regular Expressions (Regex) in Python"-"Kite"](https://www.youtube.com/watch?v=UQQsYXa1EHs&list=PLPX8wGaTDl1YwTzFk27Vmx6LVBpL2xWxu&index=38)              (primary/basis vid for understanding Python RegEx - and the solution of main.py)
### Bot Hosting 
-  to run Bot 24/7 (for FREE), used 'Render' Hosting : **https://render.com/**                                                                                                                    (**hosting** service used)
-  to keep Bot running indefinetely (fixing bot downtime), used [UptimeRobot](https://uptimerobot.com/) Monitoring -  public facing status page : **https://stats.uptimerobot.com/p7rgqtuuY6**    (**monitoring** service used)
-  tutorial vids:
    1. ["Host your app 24/7 with Render (Free and Unstable)"-"Gunther"](https://www.youtube.com/watch?v=FVpEDSlGG5k)      (was primary use for setting up the hosting)
    2. ["Host Your Discord Bot For Free In 2024! (Render)"-"Max Codez"](https://www.youtube.com/watch?v=HZis54wRF98)      (was 1 of 2 used for code)
    3. ["How to Host Your Discord Bot for FREE \[Python\]"-"CreepyD"](https://www.youtube.com/watch?v=kBdDmCPcbfs)        (was 1 of 2 used for code)                                            (thingy-mah-jig)

Thank you.

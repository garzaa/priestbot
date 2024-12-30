import discord
from email.message import Message
import random
import re
from datetime import datetime
from dotenv import load_dotenv
import os
import sys
import subprocess
import uuid

load_dotenv()

TOKEN = os.getenv("TOKEN")
CONFESSION_CHANNEL_ID = 1062550292354322432
url_regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

hours_cooldown: int = 1

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

from difflib import SequenceMatcher as SM

confession_cooldowns = {}
pig_cooldowns = {}

emoji_regex = r"(?<!\<):\w+:"
emojis = {}
animated_emojis = set()

emoji_aliases = [
	{
		"triggers": ["gnash", "bite", "biting", "gnashing", "chomp"],
		"id": 992169924627812382
	},
	{
		"triggers": ["footwork", "footwerk", "work on", "this work"],
		"id": 883769522258059325
	},
	{
		"triggers": ["finger"],
		"id": 1004917222495498240
	},
	{
		"triggers": ["sussy", "throw it back"],
		"id": 1185056319779127317
	},
	{
		"triggers": ["spray", "spraybottle"],
		"id": 1185057628804628481
	},
	{
		"triggers": ["bonk", "beat"],
		"id": 1185057540178984983
	},
	{
		"triggers": ["jokr", "joke", "joker", "why so serious"],
		"id": 1185065998148186153
	},
	{
		"triggers": ["pee", "piss"],
		"id": 1185066000056586260
	},
	{
		"triggers": ["tinylmao", "tinylmfao", "tinylol", "lmao"],
		"id": 1185065026286014555
	},
	{
		"triggers": ["patheticlittleworm", "worm"],
		"id": 1185081017049030707
	},
	{
		"triggers": ["mrcum", "mr. cum", "mr.cum"],
		"id": 1185081832665006210
	},
	{
		"triggers": ["goatse", "hole"],
		"id": 1185276778969837579
	},
	{
		"triggers": ["smoothbrain", "smooth brain"],
		"id": 1185276756844892310
	},
	{
		"triggers": ["jellysad"],
		"id": 1185274212995305593
	},
	{
		"triggers": ["grinch"],
		"id": 1198372828668502037
	}
]

username_to_user = {}

@client.event
async def on_ready():
	print("starting precache...")
	forest: discord.guild = client.get_guild(372636330724950017)
	for emoji in forest.emojis:
		if emoji.animated:
			animated_emojis.add(emoji.id)
		emojis[":"+emoji.name+":"] = emoji.id

	for user in forest.members:
		username_to_user[user.name] = user
		if user.nick:
			username_to_user[user.nick] = user

	penances.append(substitute_emojis("Congrations! You've earned a single :catholic: Catholic Coin! Use :catholic: Catholic Coins as reactions to confessions to get a private DM about who sent them! Terms and conditions may apply.\n\n**Get More :catholic: Catholic Coins**\n 1:catholic: $0.99 \n5:catholic: $3.49 📈 Most Popular \n10:catholic: $8.99 💸 Best Value"))
	if len(sys.argv) > 1:
		if len(sys.argv) > 2:
			print("surround what you want to say with quotes")
			sys.exit(1)
		else:
			await confession_channel().send(substitute_emojis(sys.argv[1]))

	print("precache finished, ready for confessions")


def on_match(matchobj):
	return get_emoji(matchobj.group(0))

def get_emoji(emoji_name: str) -> str:
	if emoji_name not in emojis:
		return emoji_name

	id = emojis[emoji_name]
	if id in animated_emojis:
		return  f"<a{emoji_name}{id}>"
	return f"<{emoji_name}{id}>"

def substitute_emojis(msg: str) -> str:
	return re.sub(emoji_regex, on_match, msg)

def get_aliases(msg: str) -> list[dict]:
	aliases = []
	for x in emoji_aliases:
		for t in x["triggers"]:
			if t in msg.lower():
				# aliases.append(x)
				aliases.append({
					"x": x,
					"idx": msg.lower().index(t)
				})
	if not aliases:
		return []
	aliases.sort(key=lambda d: d["idx"])
	return map(lambda a: a["x"], aliases)

penances = [
	"say three Hail Marys and one Our Father",
	"go out there and make a real difference",
	"eat only chips for the next two weeks",
	"treat yourself to a little beverage - you've earned it",
	"say something nice to Jerry - but not _too_ nice",
	"receive the light of Islam and unhesitatingly recite the Shahāda. Truly, there is no god but Allah, and Mohammed is his messenger",
	"do a little dance and think about what you've done",
	"...hold on, that sounds bad enough that you should see a real priest",
	"etch a little cross into a saltine and eat it",
	"write 100 times on the chalkboard \"I will not do sins\"",
	"eat more fiber and think positive thoughts",
	"download a free online bible TODAY! www.godschildrenbibleschool.com/download/bible-for-beginners",
	"give me your social security number and I'll set this right with the man upstairs",
	"don't worry about it! It's Hell for you my friend",
	"sacrifice two goats and one man at the winter solstice",
	"say something nice to people in chat",
	"refrain from insulting Jerry for the next 24 hours",
	"beat your meat until it falls apart like a brisket",
	"dig out your own brain, scoop by scoop, with a little espresso spoon",
	"singe your eyebrows with a blowtorch",
	"what the fuck is wrong with you? You're a foul creature",
	"climb into a hydraulic press and stay there until you've learned your lesson",
	"edge for two hours",
	"shit your pants",
	"spend two hours in the _Wasp Room_",
	"treat yourself to a Dobby Pussy Indulgence",
	"glue two of your fingers together with Gorilla® Construction Adhesive",
	"next time you will start a petty squabble, decide not to instead",
	"enlist in the draft",
	"learn to eat a disgusting, dirty mouse",
	"you have to kill someone",
	"give me your spare change! C'mon. Just a dollar or two...cmon😃",
	"take a 200mg edible and call your parents to say hi",
	"denounce the Anglicans",
	"uhhh uhhhhhhhhhhh uhhhh … uhhhhhhhh uhhh uhhhhhh ……… uhhhh uhh.. uhhh h..",
	"interrogate and unpack the politics of desire under late capitalism",
	"listen to drum and bass",
	"GET SCARED",
	"go check your ex's social media",
	"don't ever have sex",
	"spend 20 minutes in the gorilla enclosure at the zoo",
	"let me out of this sewer, man I could be your best friend. I could be the best thing thats ever happened to you",
	"prepare for infinite agony",
	"do half a Xan and pound on your man",
	"don't worry about the thing in your house for today",
	"go outside, find a bug, and eat it",
	"try to become less racist. Just try",
	"get pig",
	"Write In Biden",
	"you must contract a rare disease",
	"gamble with borrowed money",
	"drive behind a pig trailer for at least 20 minutes next time you're on the road",
	"go out and get the worst haircut of your entire life",
	"drink more water and stop listening to fucking Bladee",
	"leave the oven on next time you go somewhere. The blessing of the Lord will protect you",
	"pay two Etsy witches to curse each other and see who dies first",
	"post a meme about **drunk driving** to your _LinkedIn_.",
    "kill craniel",
    "change your style in a way that is lovely",
    "subscribe to Twitter Blue",
    "go outside & kill people & hurt them with knives & cut them & beat them with hammers",
	"make a flop post",
	"delete your damn tiktok",
	"respect women",
	"do your best to reclaim a slur",
	"eat more corn syrup",
	"listen to Become White subliminal videos on youtube while you sleep tonight",
	"put your finger in a deli slicer but just a little",
	"learn something new",
	"jerk & pluck me",
	"cook and eat a five-course meal with all spoiled food",
	"die a painful death involving a car covered in hammers that explodes more than a few times and hammers go flying everywhere",
	"accuse someone else of submitting your confession",
	"do that thing you haven't gotten around to doing yet. YES, that one",
	"get mixed up with me and see where we match",
	"change your zodiac sign",
	"crawl",
	"punish someone else for your own sins",
	"handle raw meat with a cut on your hand",
	"identify the thing wrong with this mes‎sage",
	"collect three bags of hair (0/3)",
	"go off your meds for a month",
	"coin a new slur",
	"listen to Become White Subliminal Hypnosis videos on Youtube tonight. Unless you're already white, in which case listen to Become Latino videos instead",
	"actually drink enough water today and see if that helps",
	"try to fathom the scale of the megastructure",
	"don't have anything",
	"grieve and mourn",
	"stick your head in a drawer and slam it and open it and slam it",
	"COLLECT MY WAFERS",
	"post a credible threat and see what happens",
	"stop moralizing your hobby",
	"take the Grinchpill"
]

judgments = [
	"I don't know about this one.",
	"This one is definitely bad!",
	"This one is definitely good!",
	"This one would be good, except for the fact that the vibes are soured by the fact that it's you doing it. So, it's bad.",
	"What? Why ask me? Isn't it clear?",
	"I don't know, it could send you to heaven OR hell.",
	"This is bad, but I think you've earned it.",
	"NO",
	"CERTAIN DAMNATION",
	"I'm pretty sure you get sent to heaven immediately if you do this.",
	"You will die in seven days",
	"Maybe.",
	"Don't count on it.",
	"I don't knowwwww",
	"This is bad, but as long as you do a penance for it, it's fine.",
	"What does it matter? You won't listen to me anyway",
	"You are a deeply sick creature",
	"I did this once and it was OK.",
	"AUGHHH OW OW OW",
	"You have to do this several times for it to be worth it.",
	"You can't do it sober but otherwise it's fine.",
	"YEAH.",
	"I didn't like reading this."
]

judged_messages = set()

def is_judgment_request(msg: str) -> bool:
	return "judg" in msg


@client.event
async def on_message(message: discord.message):
	if message.author == client.user:
		return

	if message.guild:
		if was_tagged(message):
			print("was tagged in message: "+message.content)
			# if the message contains a trigger word
			aliases = get_aliases(message.content)
			if not aliases:
				print("no alias found in messages")
				# because i KNOW this will happen
				if 'cum' in message.content:
					# react with unsure
					print("someone asked for cum again")
					await message.add_reaction(client.get_emoji(819694888672296982))
					return
				elif is_judgment_request(message.content):
					if message.reference is None:
						if message.id in judged_messages:
							await message.reply("I have already passed judgment, my child.")
							return
						judged_messages.add(message.id)
						await message.reply(random.choice(judgments))
					else:
						op = await message.channel.fetch_message(message.reference.message_id)
						if op.id in judged_messages:
							await message.reply("I have already passed judgment, my child.")
							return
						judged_messages.add(op.id)
						await op.reply(random.choice(judgments))
					print(judged_messages)
				else:
					await message.reply("in DMs, my child 🙏")
				return

			for x in aliases:
				alias = x["id"]
				
				# if the message isn't a reply, emoji react on it
				if message.reference is None:
					print("adding a reaction ("+str(alias)+") to message: "+message.content)
					await message.add_reaction(client.get_emoji(alias))
				else:
					print("adding a reaction ("+str(alias)+") to OP message from reply: "+message.content)
					op = await message.channel.fetch_message(message.reference.message_id)
					await op.add_reaction(client.get_emoji(alias))
					await message.add_reaction("🙏")

			if "delete" in message.content and message.reference:
				await message.delete()
					
		return

	print("got dm: "+message.content)

	if message.content == "emojis":
		emoji_response = "I support these extra emoji, my child:\n"
		for alias in emoji_aliases:
			emoji_response += str(client.get_emoji(alias["id"])) + ": " + str(alias["triggers"]) + "\n"
		emoji_response += "\nReply to a message and tag me with one or more trigger words, and I'll put that reaction on the original message. Or tag me without replying to any message, and I'll put the react on your message instead."
		await message.reply(emoji_response)
		return
	
	space_split = message.content.split(" ")
	message_content = " ".join(space_split[2:])
	if space_split[0] == "messagepig":
		now = datetime.now()
		if message.author.id in pig_cooldowns and pig_cooldowns[message.author.id] == datetime.now().day:
			await message.reply("You may only send one message pig per day, my child.")
			return

		print(f"got message pig request from {message.author}: " + " ".join(space_split[1:]))
		if len(message_content) > 300:
			await message.reply("Message won't fit on pig, my child! try something 200 characters or less")
			return
		target = space_split[1]
		for name in username_to_user:
			similarity = SM(None, target, name).ratio()
			if similarity > 0.88:
				if name == "priestbot":
					await message.reply("Thank you for the offer, my chid. I am forbidden from receiving message pigs, as they are blasphemous.")
					return
				await message_pig(message_content, username_to_user[name])
				await message.reply(f"Message pig sent to {name}, my child.")
				pig_cooldowns[message.author.id] = datetime.now().day
				return
		await message.reply("I couldn't find a recipient for your message pig! Try their one-word username, my child.")
		return

	if message.content == "" or message.content.isspace():
		await message.reply("I need a real sin, my child.")
		return

	if len(message.content) > 600:
		await message.reply("I need a shorter sin, my child.")
		return

	if (re.search(url_regex, message.content)):
		await message.reply("Hyperlinking is a sin, my child.")
		return

	now = datetime.now()
	if message.author.id in confession_cooldowns and not past_cooldown(now, confession_cooldowns[message.author.id]):
		await message.reply("You are confessing too quickly, my child. Buy Gems To Decrease Your Cooldown Here: <http://bit.ly/4509waX>")
		return

	await message.reply(make_penance())
	await announce_sin(message.content)

	if random.randint(0, 100) == 1:
		await message.reply("Your message was passed on, but deemed not sinful enough. You may confess again this hour.")
	else:
		confession_cooldowns[message.author.id] = now


def past_cooldown(now, then) -> bool:
	diff = now - then
	# one hour, 60s/min -> 60min/hour
	cooldown_seconds: int = 60 * 60 * hours_cooldown
	return diff.total_seconds() > cooldown_seconds


def make_penance() -> str:
    if random.randint(0, 100) <= 2:
        return "I can't believe how sick you make me."
    else:
        s: str = "Thank you, my child. I will relay your message immediately. For your penance, "
        s += random.choice(penances) + "."
        return s
	

async def message_pig(message: str, target: discord.User) -> str:
	pig_id = str(uuid.uuid4())[:8]
	pigfile = f"messagePig{pig_id}.png"
	chunked_message = fit_message_to_pig(message).replace("\n", "\\n")
	subprocess.call(f"magick.exe messagepig.png -pointsize 32 -gravity North -stroke black -strokewidth 2 -annotate +90+140 \"{chunked_message}\" {pigfile}", shell=True)
	await target.send("You've recieved a daily message pig from an anonymous sender!", file=discord.File(pigfile))
	os.remove(pigfile)


def fit_message_to_pig(message: str) -> str:
	linelen = 0
	outmsg = ""
	for i, letter in enumerate(message):
		linelen += 1
		if linelen >= 40 and letter == " ":
			outmsg += "\n"
			linelen = 0
		else:
			outmsg += message[i]
	return outmsg

async def announce_sin(sin: str):
	s: str = "_One of our members has sinned. Here is their confession._\n> "
	s += substitute_emojis(sin.replace("\n", "\n> "))
	chance = random.randint(0, 100)
	if chance <= 2:
		# 1 in 50 chance, if judging, to accidentally let slip the gender
		if (random.randint(0, 50) == 1):
			if (random.randint(0, 10) == 1):
				s += "\n_Wow! It's certain damnation for him! I mean them!_"
			else:
				s += "\n_Wow! It's certain damnation for her! I mean them!_"
		else:
			s += "\n_Wow! It's certain damnation for them!_"
	elif chance <= 4:
		s += "\n_That one's good to do, actually. Everyone else, take notes._"
	await confession_channel().send(s)


def was_tagged(message: Message) -> bool:
	return client.user.mentioned_in(message)


def confession_channel():
	if os.getenv("CONFESSION_CHANNEL_OVERRIDE"):
		return client.get_channel(int(os.getenv("CONFESSION_CHANNEL_OVERRIDE")))
	return client.get_channel(CONFESSION_CHANNEL_ID)


client.run(TOKEN)

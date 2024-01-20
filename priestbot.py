import discord
from email.message import Message
import random
import re
from datetime import datetime
from dotenv import load_dotenv
import os
from operator import itemgetter

load_dotenv()

TOKEN = os.getenv("TOKEN")
CONFESSION_CHANNEL_ID = 1062550292354322432
url_regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

hours_cooldown: int = 1

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

confession_cooldowns = {}

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
		"triggers": ["sussy"],
		"id": 1185056319779127317
	},
	{
		"triggers": ["spray", "spraybottle"],
		"id": 1185057628804628481
	},
	{
		"triggers": ["bonk"],
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
		"triggers": ["tinylmao", "tinylmfao", "tinylol"],
		"id": 1185065026286014555
	},
	{
		"triggers": ["patheticlittleworm"],
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
	}
]

@client.event
async def on_ready():
	# print("priestbot online 🙏:catholic:")
	forest: discord.guild = client.get_guild(372636330724950017)
	for emoji in forest.emojis:
		if emoji.animated:
			animated_emojis.add(emoji.id)
		emojis[":"+emoji.name+":"] = emoji.id
	penances.append(substitute_emojis("Congrations! You've earned a single :catholic: Catholic Coin! Use :catholic: Catholic Coins as reactions to confessions to get a private DM about who sent them! Terms and conditions may apply.\n\n**Get More :catholic: Catholic Coins**\n 1:catholic: $0.99 \n5:catholic: $3.49 📈 Most Popular \n10:catholic: $8.99 💸 Best Value"))
	# await confession_channel().send(substitute_emojis("hi"))

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
			if t in msg:
				# aliases.append(x)
				aliases.append({
					"x": x,
					"idx": msg.index(t)
				})
	if not aliases:
		return []
	print(str(aliases))
	aliases.sort(key=lambda d: d["idx"])
	print(str(aliases))
	return map(lambda a: a["x"], aliases)

penances = [
	"say three Hail Marys and one Our Father",
	"kill yourself in public ritual suicide",
	"go out there and make a real difference",
	"eat only chips for the next two weeks",
	"treat yourself to a little beverage - you've earned it",
	"say something nice to Jerry - but not _too_ nice",
	"receive the light of Islam and unhesitatingly recite the Shahāda. Truly, there is no god but Allah, and Mohammed is his messenger",
	"do a little dance and think about what you've done",
	"...hold on, that sounds bad enough that you should see a real priest",
	"etch a little cross into a saltine and eat it",
	"write 100 times on the chalkboard \"I will not do sins\"",
	"I'd tell you to kill yourself but that's also a sin",
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
	"write in Hillary for 2024",
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
]

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


async def announce_sin(sin: str):
	s: str = "_One of our members has sinned. Here is their confession._\n> "
	s += substitute_emojis(sin.replace("\n", "\n> "))
	chance = random.randint(0, 100)
	if chance <= 2:
		# 1 in 50 chance, if judging, to accidentally let slip the gender
		if (random.randint(0, 50) == 1):
			if (random.randint(0, 1) == 1):
				s += "\n_Wow! It's certain damnation for him! I mean them!_"
			else:
				s += "\n_Wow! It's certain damnation for her! I mean them!_"
		else:
			s += "\n_Wow! It's certain damnation for them!_"
	elif chance <= 4:
		s += "\n_That one's good to do, actually. Everyone else, take notes._"
	await confession_channel().send(s)


def is_dm(message):
	return not message.guild


def was_tagged(message: Message) -> bool:
	return client.user.mentioned_in(message)


def confession_channel():
	return client.get_channel(CONFESSION_CHANNEL_ID)


client.run(TOKEN)

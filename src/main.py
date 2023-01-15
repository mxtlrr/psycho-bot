import requests, json
count = 1

import sys

# Headers sent to the API.
headers = { "accept-type": "application/json", "content-type": "application/json" }

def expand(data, unit: str):
  try:
    if "min" and "max" in data:
			# For example:
			# 20mg - 50mg
      return f"{data['min']}{unit} - {data['max']}{unit}"
  except:
    if data == None:
      return "No information"
    else:
      return data



# Send the API request
def send_request(query):
	# Formatted string for everything we need.
	payload = {
			"query": """
	{
		substances(query: "%s") {
			name
			summary
			# routes of administration
			roas {
				name
				dose {
					units
					threshold
					heavy
					common { min max }
					light { min max }
					strong { min max }
				}
				duration {
					afterglow { min max units }
					comeup { min max units }
					duration { min max units }
					offset { min max units }
					onset { min max units }
					peak { min max units }
					total { min max units }
				}
			}
		}
	}""" % query
	}
	json_payload = json.dumps(payload)

	# Send the API request
	api = requests.post("https://api.psychonautwiki.org/?",data=json_payload,headers=headers)
	if api:
		response = json.loads(api.text)
		return response

# Setting up the discord bot
import discord
from discord.ext import commands
from datetime import datetime

import downloader
import os, shutil
import wikipediaapi

prefix = ">"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents)

if len(sys.argv) != 2:
	print("You need to pass in your token file (.env)!")
	exit(9)

# Open token file and remove the "TOKEN=" part
token = open(f"{sys.argv[1]}", "r").read().replace('\n','').replace("TOKEN=", "")


@client.event
async def on_ready():
	print("I have started up!")
	# Update bot precense
	activity = discord.Activity(type=discord.ActivityType.watching,
															name="the psychonaut wiki")
	await client.change_presence(activity=activity)
	print("Status is updated")


@client.command()
async def get_info(ctx, drug):
	print(f"Recieved {prefix}{drug}!")

	async with ctx.typing():
		response = send_request(drug)
		if "data" in response:
			units = ""
			doses = [0, 0, 0]
			description = ""
			name = ""

			for subs in response["data"]["substances"]:
				#print name
				name = subs['name']
				description = subs['summary']
				_doses = subs['roas'][0]['dose']
				units: str = _doses["units"]

				doses[0] = expand(_doses['light'], units)
				doses[1] = expand(_doses['common'], units)
				doses[2] = expand(_doses['strong'], units)

				#print duration information
				duration = subs['roas'][0]['duration']

		wiki_wiki = wikipediaapi.Wikipedia('en')

		page_py = wiki_wiki.page("MDMA")
		p: str = page_py.summary
		k = p.find('.')


	embed = discord.Embed(
		title=name,
		description=f"{page_py.summary[0:k+1]}", # Required since PsychonautWIKI doesn't have the summary.
		url=f"https://psychonautwiki.org/wiki/{name}",
		color=0x5978ab
	)

	embed.set_footer(text=f"Sent at {datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')} • Pictures may not be correct")
	
	# Add field for each dosages
	embed.add_field(name="Light Doses", value=f"{doses[0]}", inline=True)
	embed.add_field(name="Common Doses", value=f"{doses[1]}", inline=True)
	embed.add_field(name="Strong Doses", value=f"{doses[2]}", inline=False)	

	# Download image
	
	# This will be renovated a shitton in the future
	downloader.DownloadImage(drug, "downloads", amount=1) # 1 image
	global count
	count += 1

	if os.path.exists(f"downloads/{drug}"):
		print("Download sucessful I think")
		try:
			f = open(f"downloads/{drug}/Image_1.png", "r")
			file = discord.File(f"downloads/{drug}/Image_1.jpg", filename="thumb.png")
			embed.set_thumbnail(url="attachment://thumb.png")
			await ctx.send(file=file, embed=embed)
		except:
			f = open(f"downloads/{drug}/Image_1.jpg", "r")
			file = discord.File(f"downloads/{drug}/Image_1.jpg", filename="thumb.jpg")
			embed.set_thumbnail(url="attachment://thumb.jpg")
			await ctx.send(file=file, embed=embed)
		print("Removing downloads directory to prevent odd conflicts")
		shutil.rmtree("downloads/")
		print("Removed!")
	else:
		print("I could not download..sending embed without file")
		await ctx.send(embed=embed)


client.run(token)
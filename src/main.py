import requests, json

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

prefix = ">"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents)

token = open(".env", "r").read().replace('\n','')

@client.event
async def on_ready():
  print("I have started up!")


@client.command()
async def get_info(ctx, drug):
	print(f"Recieved {prefix}{drug}!")

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


	embed = discord.Embed(
		title=name,
		url=f"https://psychonautwiki.org/wiki/{name}",
		color=0x5978ab
	)

	embed.set_footer(text=f"Sent at {datetime.now()} // Pictures taken from Google Images")
	
	# Add field for each dosages
	embed.add_field(name="Light Doses", value=f"{doses[0]}", inline=True)
	embed.add_field(name="Common Doses", value=f"{doses[1]}", inline=True)
	embed.add_field(name="Strong Doses", value=f"{doses[2]}", inline=False)	

	await ctx.send(embed=embed)

client.run(token)
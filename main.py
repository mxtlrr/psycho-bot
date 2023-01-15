import requests, json

# Headers sent to the API.
headers = { "accept-type": "application/json", "content-type": "application/json" }

def expand(data):
  try:
    if "min" and "max" in data:
      return f"""
Min: {data['min']}
Max: {data['max']}
        """
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
	api = requests.post("https://api.psychonautwiki.org/?",data=json_payload,headers=headers)
	if api:
		response = json.loads(api.text)
		return response

# Setting up the discord bot
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

token = open(".env", "r").read().replace('\n','')

@client.event
async def on_ready():
  print("I have started up!")


@client.command()
async def get_info(ctx, drug):
	response = send_request(drug)
	if "data" in response:
		units = ""
		doses = [0, 0, 0]
		description = ""
		name = ""

		for subs in response["data"]["substances"]:
			# nonlocal units
			# nonlocal description
			# nonlocal doses
			# nonlocal name

			#print name
			name = subs['name']
			description = subs['summary']

			_doses = subs['roas'][0]['dose']
			doses[0] = expand(_doses['light'])
			doses[1] = expand(_doses['common'])
			doses[2] = expand(_doses['strong'])
			units = _doses["units"]

			#print duration information
			duration = subs['roas'][0]['duration']
			print(f"Afterglow {expand(duration['afterglow'])}")
			print(f"Comeup {expand(duration['comeup'])}")
			print(f"Duration {expand(duration['duration'])}")
			print(f"Offset {expand(duration['offset'])}")
			print(f"Onset {expand(duration['onset'])}")
			print(f"Peak {expand(duration['peak'])}")
			print(f"Total {expand(duration['total'])}")

	embed = discord.Embed(
		title=name,
		description=f"{name}, is \"{description}\".\nDoses:\n**Light**: {doses[0]}\n\n**Common**:{doses[1]}\n\n**Strong**:{doses[2]}"
	)

	await ctx.send(embed=embed)

client.run(token)
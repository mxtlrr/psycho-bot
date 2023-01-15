import requests, json

# Default nothing
query = ""

# Headers sent to the API.
headers = { "accept-type": "application/json", "content-type": "application/json" }

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

json_payload = json.dumps(payload)


# Send the API request
def send_request():
  api = requests.post("https://api.psychonautwiki.org/?",data=json_payload,headers=headers)
  if api:
    response = json.loads(api.text)

    if "data" in response:
      return subs
    elif "error" in response:
      # I could not do the stuff!

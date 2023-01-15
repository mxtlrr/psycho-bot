# psycho-bot
Discord bot that grabs info from PsychonautWiki and formats it onto discord.

# Example Usage
![](./res/usage.gif)

# Self hosting
You will need:
- `bing_image_downloader` for the images in the embed
- `discord.py`
- `wikipedia-api` for the summary of drugs

Then, write
```
TOKEN=[Bot Token]
```
in the `.env` file, and run
```
cd src/
python3 main.py ../.env
```

To start up the bot
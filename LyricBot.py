#LyricBot.py
import os
import LyricScraper
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

client = discord.Client() # client created

sa = ScrapeArtist()

@bot.command(name='song')
async def make_song(ctx, artist: string):
    lyrics = sa.find_songs(artist)
    sa.write_file(lyrics)
    


bot.run(TOKEN)
client.run(TOKEN)
import discord
from discord.ext import commands, tasks
from datetime import time

intents = discord.intents.all()
bot = commands.Bot("!", intents=intents)

@bot.event

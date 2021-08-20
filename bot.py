from discord.ext import commands, tasks
from discord.utils import get
import discord
import re
import json
import time
import random
import asyncio
import os
import datetime

from get_yahoo_data import wrangle_data
from tokens import tickerbot_token

ticker_bot = discord.Client()

loop = asyncio.get_event_loop()

@ticker_bot.event
async def on_ready():
    print('tickerbot started')
    await called_second()


'''
@tasks.loop() can be changed to seconds, minutes, hours
https://discordpy.readthedocs.io/en/latest/ext/tasks/
'''

ticker_data = {}

@tasks.loop(seconds=60)
async def update_data():
    global ticker_data
    ticker_data = wrangle_data()
    print("updated tickers")

async def called_second():
    ## get all guild ids that the bot is joined in

    print(ticker_data)

    while True:
        for ticker in ticker_data:
            values = ticker_data[ticker]

            guild_ids = [guild.id for guild in ticker_bot.guilds]
            name = '{:20,.2f}'.format(values['last'])
            watching = values['change%']
            guild_channels = [ticker_bot.get_guild(guild_id) for guild_id in guild_ids]
            for guild_channel in guild_channels:
                try:
                    await guild_channel.me.edit(nick=f"{ticker.upper()}: {name}")
                    await ticker_bot.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                  name=f"{ticker.upper()} {watching}"))

                    red = get(guild_channel.roles, name='RED')
                    green = get(guild_channel.roles, name='GREEN')
                    if "-" in watching:
                        discord_bot = guild_channel.me
                        await discord_bot.remove_roles(green)
                        await discord_bot.add_roles(red)
                    else:
                        discord_bot = guild_channel.me
                        await discord_bot.remove_roles(red)
                        await discord_bot.add_roles(green)


                except Exception as e:
                    print(f'broke in {guild_channel}')
                    print(e)
                    pass
            await asyncio.sleep(10)



update_data.start()



async def create_bots():
    ticker_task = loop.create_task(ticker_bot.start(tickerbot_token))

    await ticker_task

loop.run_until_complete(create_bots())
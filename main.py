"""

MIT License

Copyright (c) 2021-present Punyathorn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


from discord.ext.commands.core import *
from discord.ext.commands import *
import requests
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions,cooldown, BucketType
from discord_buttons_plugin import *
from datetime import datetime
import pytz

bot_token = "" # Your Discord Token Here.
Time_Zone = "" # Your Time Zone Here. Check https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 for your time zone.
bot = commands.Bot(command_prefix = "get ")

@bot.event
async def on_ready():
  print(f"{bot.user} logged in now!")

@bot.command(brief='Invite me!', description='Link to invite me!')
@commands.cooldown(1, 10, commands.BucketType.user)
async def invite(ctx):
    embed = discord.Embed(title=f"Invite {bot.user.name}", color=0xff0000, description=f"Wanna invite {bot.user.name}, then [click here](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot)")
    await ctx.send(embed=embed)

@invite.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow Your Invite Down!",description=f"Try again in {error.retry_after:.2f}s.", color=0x5865F2)
        await ctx.send(embed=em)

@bot.command(brief='Thailand Covid Situation English Language', description='Thailand Covid Situation using Api')
@commands.cooldown(1, 10, commands.BucketType.user)
async def covid(ctx):
    response = requests.get("https://covid19.ddc.moph.go.th/api/Cases/today-cases-all")
    json = response.json()
    covid = json[0]
    Country = "Thailand"
    TotalCases = covid['total_case']
    NewCases = covid['new_case']
    NewCases_ExcludeAbroad = covid['new_case_excludeabroad']
    TotalCases_ExcludeAbroad = covid['total_case_excludeabroad']
    TotalDeaths = covid['total_death']
    NewDeaths = covid['new_death']
    TotalRecovered = covid['total_recovered']
    NewRecovered = covid['new_recovered']
    UpdateDate = covid['update_date']
    embedVar = discord.Embed(title="Covid Stats", description="Covid Stats Today from https://covid19.ddc.moph.go.th/api/Cases/today-cases-all", color=0x00ff00)
    embedVar.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embedVar.add_field(name="Country", value=Country, inline=False)
    embedVar.timestamp = datetime.now(pytz.timezone(Time_Zone))
    embedVar.add_field(name="Total Cases", value=TotalCases, inline=False)
    embedVar.add_field(name="Total Cases Exclude Abroad", value=TotalCases_ExcludeAbroad, inline=False)
    embedVar.add_field(name="New Cases", value=NewCases, inline=False)
    embedVar.add_field(name="New Cases Exclude Abroad", value=NewCases_ExcludeAbroad, inline=False)
    embedVar.add_field(name="Total Deaths", value=TotalDeaths, inline=False)
    embedVar.add_field(name="New Deaths", value=NewDeaths, inline=False)
    embedVar.add_field(name="Total Recovered", value=TotalRecovered, inline=False)
    embedVar.add_field(name="New Recovered", value=NewRecovered, inline=False)
    embedVar.add_field(name="Update Date", value=UpdateDate, inline=False)
    await ctx.send(embed=embedVar)

@covid.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow Your Covid Down!",description=f"Try again in {error.retry_after:.2f}s.", color=0x5865F2)
        em.timestamp = datetime.now(pytz.timezone(Time_Zone))
        await ctx.send(embed=em)


class TokenError(Exception):
    pass

class TimeZoneError(Exception):
    pass

if bot_token == "":
    raise TokenError("Invalid token, please fill in your token in line 38")
if Time_Zone == "":
    raise TimeZoneError("Invalid time zone, please fill in your time zone in line 39")

bot.run(bot_token)
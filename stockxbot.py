import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
from stockxsdk import Stockx
from bs4 import BeautifulSoup
import requests

client = Bot(description="Bot for retrieving product information from StockX.",
             command_prefix="!", pm_help=False)

stockxApp = Stockx()
email = ''
password = ''
stockxApp.authenticate(email, password)


def retrieveData(query):
    stock = stockxApp.search(query)

    if len(stock) == 0:
        embed = discord.Embed(colour=discord.Colour(
            0x3dae2b), description="We searched and searched but it seems no products were found matching your description.")
        embed.set_footer(
            text="StockX", icon_url="icon_url")
        return embed

    stockItem = stock[0]
    retailPrice = ""

    try:
        attribute = stockItem['searchable_traits']

        if 'Retail Price' in attribute:
            retailPrice = "$" + str(attribute['Retail Price'])
        elif 'Retail' in attribute:
            retailPrice = "$" + str(attribute['Retail'])
        else:
            retailPrice = "--"
    except KeyError:
        retailPrice = "--"

    url = "https://stockx.com/{}"
    url = url.format(stockItem['url'])

    r = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    values = soup.findAll('div', {'class': 'gauge-value'})
    premium = ""
    average = ""
    if len(values) > 0:
        premium = values[1].text
        average = values[2].text

    embed = discord.Embed(
        title=stockItem['name'], colour=discord.Colour(0x3dae2b), url=url)

    embed.set_thumbnail(url=stockItem['media']['thumbUrl'])
    embed.set_footer(
        text="StockX", icon_url="icon_url")
    embed.add_field(name="Brand", value=stockItem['brand'], inline=True)
    embed.add_field(name="Style", value=stockItem['style_id'], inline=True)
    embed.add_field(name="Retail Price", value=retailPrice, inline=True)
    embed.add_field(name="Release Date",
                    value=stockItem['release_date'], inline=True)
    embed.add_field(name="Last Sale", value="$" +
                    str(stockItem['last_sale']), inline=True)
    embed.add_field(name="Lowest Ask", value="$" +
                    str(stockItem['lowest_ask']), inline=True)
    embed.add_field(name="Highest Bid", value="$" +
                    str(stockItem['highest_bid']), inline=True)
    embed.add_field(name="Number of Sales", value=str(
        stockItem['deadstock_sold']), inline=True)
    embed.add_field(name="Price Premium", value=premium, inline=True)
    embed.add_field(name="Average Sale Price", value=average, inline=True)

    return embed


@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to ' +
          str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))


@client.command()
async def stockx(*args):
    embed = ""

    if len(args) != 0:
        query = ' '.join(map(str, args))
        embed = retrieveData(query)
    else:
        print('empty arguement')

    await client.say(embed=embed)


@client.command()
async def stockX(*args):
    embed = ""

    if len(args) != 0:
        query = ' '.join(map(str, args))
        embed = retrieveData(query)
    else:
        print('empty arguement')

    await client.say(embed=embed)


@client.command()
async def StockX(*args):
    embed = ""

    if len(args) != 0:
        query = ' '.join(map(str, args))
        embed = retrieveData(query)
    else:
        print('empty arguement')

    await client.say(embed=embed)


@client.command()
async def STOCKX(*args):
    embed = ""

    if len(args) != 0:
        query = ' '.join(map(str, args))
        embed = retrieveData(query)
    else:
        print('empty arguement')

    await client.say(embed=embed)

client.run('DISCORDBOTAPIKEY')

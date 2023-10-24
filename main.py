import discord
from discord.ext import commands
import requests, json
from bs4 import BeautifulSoup

# Own Classes
import lists
import utilities as util
import settings
import databaseManager as dbM

#BOT
token = settings.GetBotTokenKey()

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.members = False

bot = commands.Bot(command_prefix='!', description='ONLINE', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in. {bot.user.name}')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="PIRATE'S LOG: CALM WATERS", type=discord.ActivityType.playing))
    #await bot.change_presence(activity=discord.Streaming(name="PIRATE'S LOG: CALM WATERS", url='https://www.twitch.tv/randexlofi'))



# TESTING ================================================================================================

@bot.event
async def on_message(message):
    print(f'[{util.GetSysDate()} {util.GetSysTime()}] [{message.guild.name} : {message.channel.name}] - {message.author.name}: {message.content}')
    await bot.process_commands(message)



# Moderation =============================================================================================

@bot.command()
async def shutdown(ctx, title="", reason=""):
    if ctx.author.guild_permissions.administrator:
        if not title:
            title = "Shutdown"

        if not reason:
            reason = 'unknown reason'

        embed = discord.Embed(
            title=title,
            description=reason,
            color=discord.Color.blue()
        )
        
        await ctx.message.delete()
        await ctx.send(embed=embed)
        print(f"[{util.GetSysDate()} {util.GetSysTime()}] Logged OFF {bot.user.name} ({reason}). Shutdown by {ctx.author.name}")
        await bot.close()

@bot.command()
async def clearChat(ctx, amount=0):
    if amount:
        if ctx.author.guild_permissions.manage_messages:
            if amount <= 0:
                await ctx.send("You need to specify an number greater than 0.")
            elif amount <= 100:
                        await ctx.channel.purge(limit=amount + 1)  # Delete the command message as well
                        await ctx.send(f'Cleared {amount} messages!')
                        await ctx.channel.purge(limit=1)
            else:
                    await ctx.send("The maximum amount of messages that you can clear is 100.")
        else:
            await ctx.message.delete()
            await ctx.send("You don't have permission to clear messages.")
    else:
        await ctx.message.delete()
        await ctx.send("You need to specify an number.\nExample: !clearChat 10")

        



# Information ===========================================================================================

@bot.command()
async def socials(ctx):
    embed = discord.Embed(
        title='SOCIALS',
        description='socials links:',
        color=discord.Color.blue()
    )
    
    embed.add_field(name='twitch', value='https://twitch.tv/randexlofi', inline=False)
    embed.add_field(name='dev discord', value='.randex', inline=False)
    
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def commandList(ctx):
    embed = discord.Embed(
        title='SOCIALS',
        description='socials links:',
        color=discord.Color.blue()
    )
    
    embed.add_field(name='/socials', value='show the socials with links.', inline=False)
    embed.add_field(name='/dmme', value='Send you an private message.', inline=False)

    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def helpWeather(ctx):
    await ctx.send('Weather locations by country:\npt - Portugal')
    await ctx.message.delete()

@bot.command()
async def weather(ctx, city):
    key = settings.GetWeatherAPIKey()
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    output = requests.get(URL).json()
    temperature = float(output['main']['temp'])
    countryISO = (output['sys']['country'])

    embed = discord.Embed(
        title='WEATHER',
        color=discord.Color.brand_green()
    )
    
    embed.add_field(
        name=f'{city.capitalize()} - {lists.GetCountryName(countryISO)}', 
        value=f'{util.GetCelsius(temperature):.2f} Cº\n{util.GetFahrenheit(temperature):.2f} Fº', 
        inline=False)

    await ctx.message.delete()
    await ctx.send(embed=embed)



# Entertainment ========================================================================================

@bot.command()
async def dmme(ctx):
    user = ctx.message.author
    try:
        await user.send('Ahoy!')
    except discord.errors.Forbidden:
        await ctx.send("I couldn't send you a DM. Make sure your DMs are open!")
    await ctx.message.delete()

@bot.command()
async def hello(ctx):
    await ctx.send(f'Ahoy Captain, {ctx.author.mention}! How can I assist you today?')
    await ctx.message.delete()

@bot.command()
async def randQuote(ctx):
    quoteEmbed = discord.Embed(description=lists.GetRandQuote(), color=discord.Color.blue())
    quoteEmbed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    quoteEmbed.set_footer(text="generated by: Chat GPT")

    await ctx.send(embed=quoteEmbed)
    await ctx.message.delete()

@bot.command()
async def flipCoin(ctx):
    await ctx.message.delete()
    randNum = util.GetRandInt(0, 1)

    if randNum == 0:
        await ctx.send(":coin: Heads")
    elif randNum == 1:
        await ctx.send(":coin: Tails")
    else:
        await ctx.send("Contact dev team: :coin: FLIPCOIN:ERROR_01")

@bot.command()
async def gambling(ctx):
    userID = ctx.author.id
    await ctx.message.delete()

    if dbM.CheckIsUserInDB(userID):
        await ctx.send(f'{ctx.author.mention} You already have an bank account with **{dbM.GetUserFunds(userID)}**$!')
    else:
        await ctx.send(f'{ctx.author.mention} You have created your bank account with **{settings.GetDefaultBankFunds()}**$ to gamble in the tavern!')

@bot.command()
async def bet(ctx, amount, choice):
    userID = ctx.author.id

    await ctx.message.delete()
    if choice == 'red' or choice == 'black' or choice == 'white':
        if dbM.GetUserFunds(userID) >= int(amount):
            out1, out2 = dbM.StartRoulette(amount, choice).split(':')
            print(out1, out2)
            await ctx.send(f'You bet **{amount}**$ on **{choice}**')
        else:
            await ctx.send(f'You don\'t have **{amount}**$ to bet')
    else:
        await ctx.send('Please select an valid choice (white / red / black)')
        

bot.run(token)

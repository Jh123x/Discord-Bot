import os, discord, asyncio, random, praw, urllib.request, time, youtube_dl
from case import Simulator
from discord.ext import commands
from redditbot import RedditBot
from dotenv import load_dotenv

load_dotenv()
#Load the discord tokens
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Load the reddit tokens
secret = os.getenv('REDDIT_SECRET')
id = os.getenv('REDDIT_ID')
password = os.getenv('REDDIT_PASSWORD')
username = os.getenv('REDDIT_USERNAME')

#Define the client object
client = commands.Bot(command_prefix = commands.when_mentioned_or('!'), description='Jh bot')

#Define the reddit bot
rbot = RedditBot(username,password,secret,id)

@client.event
async def on_ready() -> None:
    #This command will be executed once the bot is connected to the server
    guild = discord.utils.get(client.guilds, name = GUILD)
    #Prints out the guild name that is connected to
    print(f'Client is conencted to the following server:\n{guild.name} (id : {guild.id})')

@client.event
async def on_command_error(ctx,error):
    #Send the error to the server
    await ctx.send(f"{error}")

    #Raise the error in the console
    raise error

#Commands to execute on new user join
@client.event
async def on_member_join(member) -> None:
    #Send the member a DM once they have joined the server
    await member.create_dm()
    await member.dm_channel.send(f'Hi welcome to the server!\nPlease read the rules before posting')

#Basic commands for the bot to execute
@client.command()
async def roll(ctx, *arg) -> None:
    #Rolls a dice and outputs the result to the user on the other side
    await ctx.send(f'Your dice rolled a {random.randint(1,6)}')

@client.command()
async def choose(ctx, *args) -> None:
    #Picks a choice for the user
    await ctx.send(f'The bot chooses {random.choice(args)}')

@client.command()
async def wish(ctx, *args) -> None:
    #Wish a user or multiple users happy birthday
    if not len(args):
        #If the input is empty, tell the user to choose a person
        await ctx.send(f'Please choose someone to wish')
    else:
        #Else wish them happy birthday
        msg = ', '.join(args)
        await ctx.send(f'Happy birthday {msg}')

@client.command()
async def gay(ctx, *arg) -> None:
    #Gay meter for the bot
    if(not len(arg)):
        return await ctx.send(f'Please tag someone')
    else:
        if(arg[0].upper() == 'HARMAN' or arg[0].lower() == 'hssunreal'):
            return await ctx.send(f'{arg[0]} is 100% gay')
            
        await ctx.send(f'{arg[0]} is {random.randint(0,100)}% gay')

#Meme plugins
@client.command()
async def meme(ctx) -> None:
    #Send a meme to the discord channel
    try:
        with open('temp/temp.png','rb') as f:
            await ctx.message.channel.send(file=discord.File(f, 'temp.png'))
    except:
        pass
    rbot.load_meme()
    

# @client.command()
# async def subchange(ctx, arg) -> None:
#     if(rbot.set_subreddit(arg)):
#         await ctx.send(f'Subreddit was changed to {arg}')
#     else:
#         await ctx.send(f'{arg} is not a valid subreddit')

#Economy plugins TODO

@client.command()
async def join(ctx):
    #Make the bot join the channel the user is in
    try:
        channel = ctx.author.voice.channel
        return await channel.connect()
    except:
        return await ctx.send('Please join a channel')

@client.command()
async def leave(ctx):
    #Make the bot leave the channel
    try:
        return await ctx.voice_client.disconnect()
    except:
        await ctx.send('The client is not connected')

@client.command()
async def SourceAcademy(ctx):
    '''Sends the link to source academy'''
    return await ctx.send('https://sourceacademy.nus.edu.sg/playground')

sim = Simulator()
collections = sim.get()

@client.command()
async def case(ctx, case, number = 1):
    '''Command for CSGO cases simulator'''
    if(case.lower() in sim.collections()):
        for i in range(number):
            await ctx.send(ctx.author.mention + " got " + collections[case.lower()].open())
    else:
        await ctx.send('Please choose an appropriate case')

@client.command()
async def allcases(ctx):
    await ctx.send('Cases:\n' + '\n'.join(map(lambda x: x.capitalize(),sim.collections())))

ytdl_options = {
    'format': 'bestaudio',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'quiet': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
    }

client.queue = {}
client.vc = None

@client.command()
async def play(ctx, *, url: str = None):
    if not url:
        return await ctx.send('Please specify a title or URL for me to play.')
    if ctx.voice_client is None:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            return await ctx.send('Please join a channel')
    client.vc = ctx.voice_client
    ytdl = youtube_dl.YoutubeDL(ytdl_options)
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url))
    if 'entries' in data:
        data = data['entries'][0]

    server = ctx.guild.id
    
    if server not in client.queue:
        client.queue[server] = asyncio.Queue()
    client.queue[server].put_nowait(data)

    await ctx.send(data.get('title') + ' added to the queue.')

    if not client.vc.is_playing() if client.vc else True:
        if(not client.queue[server].empty()):
            source = ytdl.prepare_filename(client.queue[server].get_nowait())
            client.vc.play(discord.FFmpegPCMAudio(source, options='-vn'))
            await ctx.send('Now playing: ' + data.get('title'))
        else:
            await ctx.voice_client.disconnect()

#Run the discord client
try:
    client.run(TOKEN)
except:
    client.close()
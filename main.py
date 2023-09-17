import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
from apis import TOKEN, channel_id


intents = discord.Intents.all()
intents.typing = False
intents.presences = False

# Initialize the bot
bot = commands.Bot(command_prefix="/", intents=intents)

# Event to run when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Function to send the current time as an embedded message every 5 minutes
@tasks.loop(minutes=5)
async def send_embedded_time():
    channel = bot.get_channel(channel_id)
    if channel:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        embed = discord.Embed(
            title="Current Time",
            description=f"The current time is: {current_time}",
            color=discord.Color.blue()  # You can change the color here
        )
        
        await channel.send(embed=embed)

@send_embedded_time.before_loop
async def before_send_embedded_time():
    await bot.wait_until_ready()

# Start the message-sending loop
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    send_embedded_time.start()

# Create and run an asyncio event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start(TOKEN))

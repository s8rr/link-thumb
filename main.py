import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

TOKEN = 'Bot_Token'
intents = discord.Intents.default()
intents.message_content = True  # Needed for accessing message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to extract video information
def get_video_info(url):
    ydl_opts = {'format': 'best'}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return {
        'title': info_dict.get('title', 'Unknown Title'),
        'url': info_dict.get('webpage_url', url),
        'thumbnail': info_dict.get('thumbnail', None),
        'description': info_dict.get('description', 'No description available.'),
    }

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages

    # Check for links in the message
    if "http" in message.content:
        # Extract the URL (assuming it's the first link in the message)
        url = next((word for word in message.content.split() if word.startswith("http")), None)

        if url:
            try:
                # Get video info from yt-dlp
                video_info = get_video_info(url)
                embed = discord.Embed(
                    title=video_info['title'],
                    url=video_info['url'],
                    description=video_info['description'],
                    color=discord.Color.blue()
                )
                if video_info['thumbnail']:
                    embed.set_thumbnail(url=video_info['thumbnail'])

                # Send the embed and delete the original message
                await message.channel.send(embed=embed)
                await message.delete()
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                await message.channel.send("Sorry, I couldn't process the link.")

# Run the bot
bot.run(TOKEN)

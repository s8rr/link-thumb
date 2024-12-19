import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio

TOKEN = 'Bot_Token'
intents = discord.Intents.default()
intents.message_content = True  # Needed for accessing message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Default settings per channel
default_settings = {
    'large_image': True,
    'description_enabled': True,
    'title_enabled': True,
    'embed_enabled': True,  # New setting for disabling embed
    'embed_color': discord.Color.blue()
}
channel_settings = {}

def get_video_info(url):
    """Extract video information using yt-dlp."""
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
        return

    # Initialize channel settings if not already done
    if message.channel.id not in channel_settings:
        channel_settings[message.channel.id] = default_settings.copy()

    # Check for links in the message
    if "http" in message.content:
        url = next((word for word in message.content.split() if word.startswith("http")), None)
        if url:
            try:
                # Get video info
                video_info = get_video_info(url)
                settings = channel_settings[message.channel.id]

                # Check if embed is enabled
                if not settings['embed_enabled']:
                    await message.channel.send(video_info['thumbnail'])
                    await message.delete()
                    return

                embed = discord.Embed(
                    color=settings['embed_color']
                )

                # Add title if enabled
                if settings['title_enabled']:
                    embed.title = video_info['title']
                    embed.url = video_info['url']

                # Add description if enabled
                if settings['description_enabled']:
                    embed.description = video_info['description']

                # Add thumbnail or large image
                if settings['large_image']:
                    embed.set_image(url=video_info['thumbnail'])
                else:
                    embed.set_thumbnail(url=video_info['thumbnail'])

                await message.channel.send(embed=embed)
                await message.delete()

            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                await message.channel.send("Sorry, I couldn't process the link.")

    # Command to open settings menu
    if message.content.lower() == "!menu":
        menu_message = await message.channel.send(
            "📷 **Settings Menu**\n"
            f"1️⃣ Toggle Thumbnail (Small/Large): {'Large' if channel_settings[message.channel.id]['large_image'] else 'Small'}\n"
            f"2️⃣ Enable/Disable Description: {'Enabled' if channel_settings[message.channel.id]['description_enabled'] else 'Disabled'}\n"
            f"3️⃣ Change Embed Color: {'Blue' if channel_settings[message.channel.id]['embed_color'] == discord.Color.blue() else 'Custom'}\n"
            f"4️⃣ Enable/Disable Title: {'Enabled' if channel_settings[message.channel.id]['title_enabled'] else 'Disabled'}\n"
            f"5️⃣ Reset to Default Settings\n"
            f"6️⃣ Disable/Enable Embed (Thumbnail Only): {'Enabled' if channel_settings[message.channel.id]['embed_enabled'] else 'Disabled'}\n"
            "❌ Close Menu"
        )
        await menu_message.add_reaction("1️⃣")
        await menu_message.add_reaction("2️⃣")
        await menu_message.add_reaction("3️⃣")
        await menu_message.add_reaction("4️⃣")
        await menu_message.add_reaction("5️⃣")
        await menu_message.add_reaction("6️⃣")
        await menu_message.add_reaction("❌")

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "❌"]

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await menu_message.edit(content="⏳ **Menu timed out.**")
                break
            else:
                settings = channel_settings[message.channel.id]

                if str(reaction.emoji) == "1️⃣":
                    settings['large_image'] = not settings['large_image']

                elif str(reaction.emoji) == "2️⃣":
                    settings['description_enabled'] = not settings['description_enabled']

                elif str(reaction.emoji) == "3️⃣":
                    color_menu = await message.channel.send(
                        "🎨 **Choose a color:**\n"
                        "🔵 Blue\n"
                        "🟢 Green\n"
                        "🔴 Red"
                    )
                    await color_menu.add_reaction("🔵")
                    await color_menu.add_reaction("🟢")
                    await color_menu.add_reaction("🔴")

                    def color_check(reaction, user):
                        return user == message.author and str(reaction.emoji) in ["🔵", "🟢", "🔴"]

                    try:
                        color_reaction, _ = await bot.wait_for("reaction_add", timeout=30.0, check=color_check)
                    except asyncio.TimeoutError:
                        await color_menu.edit(content="⏳ **Color menu timed out.**")
                    else:
                        if str(color_reaction.emoji) == "🔵":
                            settings['embed_color'] = discord.Color.blue()
                        elif str(color_reaction.emoji) == "🟢":
                            settings['embed_color'] = discord.Color.green()
                        elif str(color_reaction.emoji) == "🔴":
                            settings['embed_color'] = discord.Color.red()
                        await color_menu.edit(content="✅ **Changed Embed Color!**")

                elif str(reaction.emoji) == "4️⃣":
                    settings['title_enabled'] = not settings['title_enabled']

                elif str(reaction.emoji) == "5️⃣":
                    channel_settings[message.channel.id] = default_settings.copy()

                elif str(reaction.emoji) == "6️⃣":
                    settings['embed_enabled'] = not settings['embed_enabled']

                elif str(reaction.emoji) == "❌":
                    await menu_message.edit(content="❌ **Menu closed.**")
                    break

                # Update the menu with the new settings
                await menu_message.edit(
                    content=f"📷 **Settings Menu**\n"
                            f"1️⃣ Toggle Thumbnail (Small/Large): {'Large' if channel_settings[message.channel.id]['large_image'] else 'Small'}\n"
                            f"2️⃣ Enable/Disable Description: {'Enabled' if channel_settings[message.channel.id]['description_enabled'] else 'Disabled'}\n"
                            f"3️⃣ Change Embed Color: {'Blue' if channel_settings[message.channel.id]['embed_color'] == discord.Color.blue() else 'Custom'}\n"
                            f"4️⃣ Enable/Disable Title: {'Enabled' if channel_settings[message.channel.id]['title_enabled'] else 'Disabled'}\n"
                            f"5️⃣ Reset to Default Settings\n"
                            f"6️⃣ Disable/Enable Embed (Thumbnail Only): {'Enabled' if channel_settings[message.channel.id]['embed_enabled'] else 'Disabled'}\n"
                            "❌ Close Menu"
                )

# Run the bot
bot.run(TOKEN)

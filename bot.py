import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))  
VERIFIED_ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID', 0))    

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class WelcomeSystem:
    WELCOME_MESSAGES = [
        "Salam {mention} to {server}! Khosh Omadi .",
        "Hello {mention}! Khosh Omadi Be {server}.",
        "Welcome  {mention} To {server}!",
        "{mention} Welcome To {server}!"
    ]
    
    @staticmethod
    def generate_welcome(member):
        return random.choice(WelcomeSystem.WELCOME_MESSAGES).format(
            mention=member.mention,
            server=member.guild.name
        )

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="javadsd.ir"
    ))

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    if not welcome_channel:
        print(f"Error: Welcome channel not found (ID: {WELCOME_CHANNEL_ID})")
        return

    try:
        embed = discord.Embed(
            title="New Member Joined",
            description=WelcomeSystem.generate_welcome(member),
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(member.created_at, 'R'),
            inline=True
        )
        embed.add_field(
            name="Member Count",
            value=str(member.guild.member_count),
            inline=True
        )
        embed.set_footer(text=f"User ID: {member.id}")

        await welcome_channel.send(embed=embed)
        
        if VERIFIED_ROLE_ID:
            verified_role = member.guild.get_role(VERIFIED_ROLE_ID)
            if verified_role:
                await member.add_roles(verified_role, reason="Auto-verified new member")

    except Exception as e:
        print(f"Error welcoming {member.name}: {str(e)}")

if __name__ == "__main__":
    bot.run(TOKEN)
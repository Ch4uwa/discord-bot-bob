# bot.py
import os
import random

from bot_helper import get_quote as bh

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()


words = {
    'sad_words': ["sad", "depressed", "unhappy", "angry", "miserable"],
    'starter_encouragements': ["Cheer op!", "Hang in there.", "You are a great person!"]
}


description = '''An simple bot'''
# 4294442871
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?',
                   description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.message.reply(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a die in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.message.reply('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.message.reply(result)


@bot.command(description='For when you need help making a choice')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.message.reply(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    if abs(times) > 10:
        ctx.send('To much!')
        return
    for _ in range(abs(times)):
        await ctx.message.reply(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    try:
        member is not None
    except Exception:
        await ctx.send('Member name missing')
        return

    await ctx.message.reply(f'{member.name} joined in {member.joined_at.date()}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.message.reply(f'No, {ctx.subcommand_passed} is not cool')


@bot.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.message.reply('Yes, the bot is cool.')


@bot.command(name='quote', help='Gives you some zen.')
async def quote(ctx):
    quote = bh.get_quote()
    await ctx.message.reply(quote)


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.message.reply(response)


if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    env_file_path = os.path.join(base_path, '.env')

    if os.path.exists(env_file_path):
        # TOKEN = os.getenv('DISCORD_TOKEN')
        # bot.run(TOKEN)
        print('OK')


from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


f = open("token", "r")
token = f.read()
bot.run(token)

from discord.ext import commands
import tools

bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def monthly(ctx, *, corp_name):
    await ctx.send(tools.monthly(corp_name))


@bot.command()
async def size(ctx, *, corp_name):
    await ctx.send(tools.fleet_size(corp_name))


@bot.command()
async def comp(ctx, *, corp_name):
    await ctx.send(tools.fleet_comp(corp_name))


f = open("token", "r")
token = f.read()
bot.run(token)

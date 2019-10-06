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


@bot.command()
async def pc(ctx, *, item):
        await ctx.send(tools.pc(item, "-j"))


@bot.command()
async def pch(ctx, item, hub):
    await ctx.send(tools.pc(item, hub))


@bot.command()
async def fuel(ctx):
    await ctx.send(tools.fuel())


@bot.command()
async def rollout(ctx, *, pilot):
    await ctx.send(tools.roll(pilot))


@bot.command()
async def last_rolled(ctx):
    await ctx.send(tools.last_rolled())


f = open("token", "r")
token = f.read()
bot.run(token)

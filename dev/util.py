import re
from datetime import date, datetime

import aiohttp
import discord
from decancer_py import CuredString, parse

import vars
import views


async def send_webhook(url: str, content: str, title: str) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(url, session=session)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=content, title=title)
        time_now = datetime.now().strftime('%H:%M:%S')
        date_today = date.today().strftime('%d/%m/%Y')
        embed.set_footer(text=f'On {date_today} at {time_now}')
        await webhook.send(embed=embed)
    info(f'[{time()}] >LOG> aiohttp client session used for Webhook.')


async def check_for_roles_status(ctx: discord.Interaction):
    allowed1 = ctx.guild.get_role(vars.discordAdmin) in ctx.user.roles
    allowed2 = ctx.guild.get_role(vars.minecraftAdmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(vars.centralHosting) in ctx.user.roles
    allowed4 = ctx.guild.get_role(vars.gunjiCord) in ctx.user.roles
    return allowed1 or allowed2 or allowed3 or allowed4


async def sanitize(ctx, member):
    nick = member.display_name
    if re.match(vars.repat, nick):
        wet_name = re.sub(vars.repatce, '', nick)
        if len(wet_name) < 1:
            wet_name = 'Robin'
        clean_name_cs: CuredString = parse(wet_name, retain_capitalization=True, retain_emojis=True)
        clean_name = f'{clean_name_cs}'
        await member.edit(nick=clean_name)
        await send_webhook(vars.sanitization_webhook_url, f'Changed nick from **{nick}** to **{clean_name}**.',
                           'Nick Change:')
        if member.display_name == 'Robin':
            embed = discord.Embed(colour=discord.Colour.green(),
                                  description=f'Changed `{nick}` to placeholder `Robin`.')
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{time()}] >LOG> Member sanitized: {nick} -> {clean_name}.]')
        else:
            embed = discord.Embed(colour=discord.Colour.green(), description=f'Changed `{nick}` to `{clean_name}`.')
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{time()}] >LOG> Member sanitized: {nick} -> {clean_name}.]')
    else:
        wet_name = nick
        clean_name_cs: CuredString = parse(wet_name, retain_capitalization=True, retain_emojis=True)
        clean_name = f'{clean_name_cs}'
        if clean_name != nick:
            await member.edit(nick=clean_name)
            await send_webhook(vars.sanitization_webhook_url, f'Changed nick from **{nick}** to **{clean_name}**.',
                               'Nick Change:')
            embed = discord.Embed(colour=discord.Colour.green(), description=f'Changed `{nick}` to `{clean_name}`.')
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{time()}] >LOG> Member sanitized: {nick} -> {clean_name}.]')
        else:
            view = views.ShowDebugButton(nick=nick)
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'"`{nick}`" seems fine and is not cancerous or intentionally hoisted.\nIf you think it is, please make a [GitHub Issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and send the Debug Info.')
            await ctx.response.send_message(embed=embed, ephemeral=True, view=view)


def time():
    return datetime.now().strftime('%H:%M:%S')


def info(txt: str):
    with open(vars.log_dir_path + 'cordcrafter.log', 'a') as f:
        print(txt)
        f.write(txt + '\n')

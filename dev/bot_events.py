import re

import discord
from decancer_py import CuredString, parse
from discord.ext import commands

import rcon
import util
import vars
from util import info


# On Ready:
async def on_ready(bot: commands.Bot) -> None:
    info(f'[{util.time()}] >LOG> Setting Discord Bot Status. . .')
    await bot.change_presence(activity=discord.Game('on CordCraft Season 2.'), status=discord.Status.online)
    info(f'[{util.time()}] >LOG> Discord Bot Status Set.')
    info(f'[{util.time()}] >EVENT> Bot Ready.')


# On Member join:
async def on_member_join(member: discord.Member) -> None:
    nick = member.display_name
    if re.match(vars.repat, nick):
        wet_name = re.sub(vars.repatce, '', nick)
        if len(wet_name) < 1:
            wet_name = 'Robin'
        clean_name_cs: CuredString = parse(wet_name, retain_capitalization=True, retain_emojis=True)
        clean_name = f'{clean_name_cs}'
        await member.edit(nick=clean_name)
        await util.send_webhook(vars.sanitization_webhook_url, f'Changed nick from **{nick}** to **{clean_name}**.', 'Nick Change:')
        info(f'[{util.time()}] >EVENT> Member joined: {nick} -> {clean_name}.]')
    else:
        wet_name = nick
        clean_name_cs: CuredString = parse(wet_name, retain_capitalization=True, retain_emojis=True)
        clean_name = f'{clean_name_cs}'
        if clean_name != nick:
            await member.edit(nick=clean_name)
            await util.send_webhook(vars.sanitization_webhook_url, f'Changed nick from **{nick}** to **{clean_name}**.', 'Nick Change:')
            info(f'[{util.time()}] >EVENT> Member joined: {nick} -> {clean_name}.]')
        else:
            info(f'[{util.time()}] >EVENT> Member joined: {nick}.')
    dm = await member.create_dm()
    w_embed = discord.Embed(colour=discord.Colour.yellow(), title='Welcome!', description=f'''Welcome to GunjiCordia!
We hope you're going to have a great time here!
If you ever get stuck, feel free to use my commands that have straightforward names to get around and about to learn how things go around here.

Before you can fully Join our community, though, I am going to quickly look at your profile and make necessary changes if they're needed.

Alongside that, by joining our server you agree to MY (so the bot's) [Privacy Police](<{vars.privacy_notion}>)
''')
    e_embed = discord.Embed(colour=discord.Colour.yellow(), title='That\'s all!', description='''Have fun!

Sensing something wrong with the bot's behaviour or profile changes?
Report any issues to the [GitHub Issue Tracker](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>).
''')
    embeds = [w_embed, e_embed]
    await dm.send(embeds=embeds)


async def on_message(message: discord.Message, bot: commands.Bot) -> None:
    if not message.content.startswith('$'):
        name = message.author.display_name
        id = f'{message.author.id}'
        text = message.content
        channel = message.guild.get_channel(vars.ctd_channel)
        command = '/tellraw @a ["",{"text":"[@' + name + '] ","color":"blue","clickEvent":{"action":"suggest_command","value":"<@' + id + '>"},"hoverEvent":{"action":"show_text","contents":[{"text":"This message was sent from Discord using CordCrafter.","color":"dark_purple"}]}},{"text":"' + text + '"}]'
        if message.channel == channel and message.author != bot.user and 'CordCrafter' not in message.author.name:
            await rcon.handle_message(command, channel)
    else:
        pass

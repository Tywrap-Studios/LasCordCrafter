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


async def sanitize(interaction, member):
    await interaction.response.defer(thinking=True)
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
            await interaction.followup.send(embed=embed, ephemeral=True)
            info(f'[{time()}] >LOG> Member sanitized: {nick} -> {clean_name}.]')
        else:
            embed = discord.Embed(colour=discord.Colour.green(), description=f'Changed `{nick}` to `{clean_name}`.')
            await interaction.followup.send(embed=embed, ephemeral=True)
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
            await interaction.followup.send(embed=embed, ephemeral=True)
            info(f'[{time()}] >LOG> Member sanitized: {nick} -> {clean_name}.]')
        else:
            view = views.ShowDebugButton(nick=nick)
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'"`{nick}`" seems fine and is not cancerous or intentionally hoisted.\nIf you think it is, please make a [GitHub Issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and send the Debug Info.')
            await interaction.followup.send(embed=embed, ephemeral=True, view=view)


def format_duration(text: str) -> str:
    text = text.replace("seconds", "s")
    text = text.replace("second", "s")
    text = text.replace("minutes", "m")
    text = text.replace("minute", "m")
    text = text.replace("hours", "h")
    text = text.replace("hour", "m")
    text = text.replace("days", "d")
    text = text.replace("day", "d")
    text = text.replace("weeks", "w")
    text = text.replace("week", "w")
    text = text.replace("months", "M")
    text = text.replace("month", "M")
    text = text.replace(" ", "")
    return text


def from_formatted_get_int(formatted_string: str) -> int:
    return int(f"0{re.sub('[a-z,A-Z]', '', formatted_string)}")


def from_formatted_get_str(formatted_string: str) -> str:
    return re.sub('\d+', '', formatted_string)


def get_duration_in_days(duration_str: str, duration_int: int) -> float:
    if duration_str == 's':
        return duration_int * 0.000012
    if duration_str == 'm':
        return duration_int * 0.000694
    if duration_str == 'h':
        return duration_int * 0.041667
    if duration_str == 'd':
        return duration_int
    if duration_str == 'w':
        return duration_int * 7
    if duration_str == 'M':
        return duration_int * 30  # Approximate month length
    return 1


def time():
    return datetime.now().strftime('%H:%M:%S')


def get_log_filename():
    timestamp = datetime.now().strftime('%d-%m_%H.%M.%S')
    return f'cordcrafter-{timestamp}.log'


# Store the current log filename as a module-level variable
current_log_file = get_log_filename()


def info(txt: str):
    log_path = vars.log_dir_path + current_log_file
    with open(log_path, 'a') as f:
        print(txt)
        f.write(txt + '\n')

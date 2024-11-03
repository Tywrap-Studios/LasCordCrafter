from datetime import datetime, date

import aiohttp
import discord
from mcrcon import MCRcon

import util
import vars
from util import info

# RCON Variables needed for the client
rcon_pass = vars.rcon_pass_env
rcon_host = vars.rcon_host_env
rcon_port = int(vars.rcon_port_env)
rcon_logger_webhook_url = vars.rcon_logger_webhook_url_env

# The Raw RCON Client
mcrcon_client = MCRcon(host=rcon_host, password=rcon_pass, port=rcon_port)


# This is to send a log embed to the webhook, for debug and safety purposes.
async def send_log_webhook(command: str, response: str, source: discord.Member):
    async with aiohttp.ClientSession() as session:
        url = rcon_logger_webhook_url
        webhook = discord.Webhook.from_url(url, session=session)
        embed = discord.Embed(colour=discord.Colour.blurple(),
                              description=f':green_circle: The RCON `{rcon_host}:{rcon_port}` was sent a package.\n:package: Package: `{command}`\n:shield: Source: {source.mention}[`{source.id}`] -> [`{source.name}`].\n:information_source: Response: {response}',
                              title='RCON TRIGGER:')
        time = datetime.now().strftime('%H:%M:%S')
        datetoday = date.today().strftime('%d/%m/%Y')
        embed.set_footer(text=f'On {datetoday} at {time}')
        await webhook.send(embed=embed)


# This is what actually connects to the server, and then sends the response back to Discord.
async def send_rcon(command: str, ctx, admin_only: bool):
    allowed2 = ctx.guild.get_role(vars.minecraftAdmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(vars.centralHosting) in ctx.user.roles
    allowed = allowed2 or allowed3
    if admin_only and allowed:
        await handle_rcon(command, ctx)
    else:
        if admin_only and not allowed:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description='<:against_rules:1279142167729668096> You are not allowed to connect this Command to an RCON Client.',
                                  title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            await handle_rcon(command, ctx)


# This is an in between method to fend off code duplication.
async def handle_rcon(command, ctx):
    with mcrcon_client as mcr:
        try:
            rcon_package_resp = mcr.command(command)
            response = f'`{rcon_package_resp}`'
            if len(response) == 2:
                response = '`Response length is 0, this command likely has no console output.`'
            if '/mclogs' in command:
                response = f'\n**{rcon_package_resp}**\n'

            embed = discord.Embed(colour=discord.Colour.green(),
                                  description=f'<:con_excellent:1278830872929501286>Server successfully received package.\n<:info:1278823933717512232>Response: {response}',
                                  title='RCON: <:resources:1278835693900136532>')
            await send_log_webhook(command=command, response=response, source=ctx.user)
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{util.time()}] >RCON> Package sent: `{command}`, Source: {ctx.user.name}, Response: {response}')
        except ConnectionRefusedError as e:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'The connection could not be made as the server actively refused it.<:warn:1249069667159638206>\nPlease report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) if this seems random.\n-# {e}',
                                  title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{util.time()}] >RCON> A connection could not be made as the server actively refused it.')
        except (ConnectionResetError, ConnectionAbortedError) as e:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'The connection was terminated, the server may have been stopped.<:warn:1249069667159638206>\nPlease report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) if this seems random.\n-# {e}',
                                  title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{util.time()}] >RCON> The connection was terminated, the server may have been stopped.')
        except Exception as e:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'Something went wrong connecting to the RCON Client.<:warn:1249069667159638206>\nPlease report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) if this seems random.\n-# {e}',
                                  title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed, ephemeral=True)
            info(f'[{util.time()}] >RCON> Something went wrong connecting to the RCON Client.')


# This is for the on_message() event to send the message to the Minecraft Server.
async def handle_message(command, channel):
    with mcrcon_client as mcr:
        try:
            mcr.command(command)
        except Exception as e:
            info(f'[{util.time()}] >RCON> Something went wrong connecting to the RCON Client. {e}')

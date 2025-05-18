import re
import time
from datetime import timedelta, datetime, date
from typing import Optional, List

import discord
import psutil
from discord import app_commands
from discord.ext import commands

import bot_events
import util
import vars
import views
import database
import modals
from rcon import send_rcon
from util import info, info_time


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await bot_events.on_ready(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message):
        await bot_events.on_message(message, self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await bot_events.on_member_join(member)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await bot_events.on_member_change(before, after)


class StandaloneCog(commands.Cog):
    def __init__(self, bot: commands.Bot, start_time: float):
        self.bot = bot
        self.start_time = start_time

    @commands.command(name='debug-sync')
    async def sync(self, ctx: discord.ext.commands.Context):
        tywrap = ctx.guild.get_member(1041430503389155492)
        if ctx.author == tywrap:
            info_time(f'>LOG> Bot Tree Sync Started by {ctx.author.name}.')
            await self.bot.tree.sync()
            info_time(f'>LOG> Finished Syncing Bot Tree.')
        else:
            info_time(f'>LOG> Bot Tree Sync Failed: no permission.')

    @commands.command(name='debug-stop')
    async def exit(self, ctx: discord.ext.commands.Context):
        tywrap = ctx.guild.get_member(1041430503389155492)
        if ctx.author == tywrap:
            info_time(f'>LOG> Bot Stopped by {ctx.author.name}.')
            await self.bot.close()
        else:
            info_time(f'>LOG> Failed to stop bot.')

    @commands.command(name='debug-flush_database')
    async def flush_database(self, ctx: discord.ext.commands.Context):
        active_bans = await database.get_active_bans()
        tywrap = ctx.guild.get_member(1041430503389155492)
        if ctx.author == tywrap:
            for ban in active_bans:
                user_id, guild_id, unban_time, reason = ban
                try:
                    await database.remove_temp_ban(user_id)
                except:
                    info_time(f'>LOG> Something went wrong while Flushing a database entry.')
                    continue
        info_time(f'>LOG> {ctx.author.name} Attempted to flush database.')

    @discord.app_commands.command(name='ip-joining', description='Tells the person you specify how to join the server.')
    async def ip_joining(self, interaction, member: discord.Member) -> None:
        await interaction.response.send_message(f'''Hey, <@{member.id}>!
Are you wondering how to join? The server IP alongside the Modpack Link and the Rules are all located in
- {vars.ipChannel}.
And hey, if you're there already, why not read the rules?

> ## For the future: Please use your eyes, not your mouth.
> ~ Sincerely, the entire admin team cuz this question was asked by too many people already. /hj''')
        info_time(f'>LOG> {interaction.user.name} ran /ip-joining for {member.name}.')

    @discord.app_commands.command(name='ping', description='See how slow/fast the Bot\'s reaction time (ping) is.')
    async def ping(self, interaction) -> None:
        latency = round(self.bot.latency * 1000)
        latency_str = f'`{latency}ms`'
        if latency >= 400:
            latency_str = f'`{latency}ms` <:con_bad:1278830871532802089>'
        else:
            if latency >= 200:
                latency_str = f'`{latency}ms` <:con_mediocre:1278830874074546199>'
            else:
                if latency <= 199:
                    latency_str = f'`{latency}ms` <:con_excellent:1278830872929501286>'
        embed = discord.Embed(description=f'## Pong! {latency_str}', colour=discord.Colour.from_rgb(70, 230, 210))
        embed.set_footer(text='Want to see more? Use /stats!', )
        await interaction.response.send_message(embed=embed)
        info_time(f'>LOG> {interaction.user.name} ran /ping -> {latency}.')

    @discord.app_commands.command(name="bean", description="Beans the member. Yep. That's all it does.")
    async def bean(self, interaction, member: discord.Member):
        embed = discord.Embed(title='Member Beaned',
                              description=f'Member: {member.mention},\nResponsible "moderator": {interaction.user.mention}',
                              colour=discord.Colour.og_blurple())
        await interaction.response.send_message(embed=embed)
        info_time(f'>LOG> {interaction.user.name} ran /bean for {member.name}.')

    # TODO>GOAL: Fix whatever the hell happens here
    @discord.app_commands.command(name='stats', description='Displays the Bot\'s statistics.')
    async def stats(self, interaction) -> None:
        await interaction.response.defer(thinking=True)
        # Stats
        cpu_stat = psutil.cpu_percent(5)
        actual_ram = psutil.virtual_memory()[3] / 1000000
        rounded_ram = round(actual_ram)
        if actual_ram == 0 or actual_ram < 0:
            ram = 'Stat fetched under or is 0. Error 1.'
        else:
            ram = f'{rounded_ram}MB'
        uptime = str(timedelta(seconds=int(round(time.time() - self.start_time))))
        latency = round(self.bot.latency * 1000)
        latency_str = f'`{latency}ms`'
        if latency >= 400:
            latency_str = f'`{latency}ms`<:con_bad:1278830871532802089>'
        else:
            if latency >= 200:
                latency_str = f'`{latency}ms`<:con_mediocre:1278830874074546199>'
            else:
                if latency <= 199:
                    latency_str = f'`{latency}ms`<:con_excellent:1278830872929501286>'
        member_count = len([m for m in interaction.guild.members if not m.bot])
        bot_count = len([m for m in interaction.guild.members if m.bot])
        guild_age_secs = time.time() - interaction.guild.created_at.timestamp()
        guild_age = round(guild_age_secs / 86400)
        bot_member = self.bot
        bot_status_game = bot_member.activity.name
        bot_status_raw = bot_member.activity
        if 'on CordCraft' in bot_status_game:
            bot_status = f'**The server is online and stable.** <a:stable:1278830944932855911>'
        else:
            if '; DOWN' in bot_status_raw.state:
                message = bot_status_raw.state.replace('; DOWN', '')
                bot_status = f'**The server might currently be __down__.** <a:down:1278830877396172840>\n<:arrow_under:1278834153655107646>**Message:** {message}'
            else:
                bot_status = f'**There might be a slight complication.** <a:unstable:1278830948120789064>\n<:arrow_under:1278834153655107646>**Message:** {bot_status_raw.state}'
        status_embed = discord.Embed(colour=discord.Colour.og_blurple(), title='CordCrafter Status.',
                                     description=f'''----------------------------
<:space:1251655233919123628><:speed:1251649973418983565> **Latency:** {latency_str}
<:space:1251655233919123628><:uptime:1251648456301346946> **Uptime:** `{uptime}`
<:space:1251655233919123628><:info:1278823933717512232> **Bot Ver:** `{vars.botVersion}`
<:space:1251655233919123628><:resources:1278835693900136532> **Resource Usage:**
<:space:1251655233919123628><:arrow_under:1278834153655107646><:ram:1251659281384738857> RAM: `{ram}`
<:space:1251655233919123628><:arrow_under:1278834153655107646><:cpu_load:1251684895038902324> CPU: `{cpu_stat}%`
<:space:1251655233919123628><:servericon:1251671285277130753> **Server:**
<:space:1251655233919123628><:space:1251655233919123628><:party:1278816948846596157> Members:
<:space:1251655233919123628><:space:1251655233919123628><:arrow_under:1278834153655107646><:member:1278834558485397624>`{member_count}`;
<:space:1251655233919123628><:space:1251655233919123628><:arrow_under:1278834153655107646><:bot:1278833876961198120>`{bot_count}`
<:space:1251655233919123628><:space:1251655233919123628>⏰ Age: `{guild_age}`
----------------------------
**<:minecraft_logo:1278852452396826634> MC-Server Status:**
<:arrow_under:1278834153655107646>{bot_status}''')
        await interaction.followup.send(embed=status_embed)
        info_time(f'>LOG> {interaction.user.name} ran /stats -> {latency_str}.')

    @discord.app_commands.command(name='resign', description='Resigns the Minecraft admin you chose.')
    async def resign(self, interaction, admin: discord.Member):
        tywrap = interaction.guild.get_member(1041430503389155492)
        old_role = interaction.guild.get_role(vars.minecraftAdmin)
        new_role = interaction.guild.get_role(vars.resigned)
        if interaction.user == tywrap:
            if old_role in admin.roles and new_role not in admin.roles:
                await admin.remove_roles(old_role, reason='Resigning Minecraft Admin...')
                await admin.add_roles(new_role, reason='Resigning Minecraft Admin...')
                await interaction.response.send_message(
                    f'Successfully resigned {admin.mention} from the Admin team.\nDon\'t forget to /deop them!',
                    ephemeral=True)
            else:
                if old_role not in admin.roles and new_role not in admin.roles:
                    await interaction.response.send_message(
                        f'Could not resign Admin {admin.mention}. \nReason: Could not find {old_role.mention} role in User roles.',
                        ephemeral=True)
                if old_role not in admin.roles and new_role in admin.roles:
                    await interaction.response.send_message(
                        f'Could not resign Admin {admin.mention}. \nReason: User is already resigned.', ephemeral=True)
                if old_role in admin.roles and new_role in admin.roles:
                    await interaction.response.send_message(
                        f'Something went wrong while assigning and resigning roles.\nPlease manually re-check {admin.mention}\'s roles',
                        ephemeral=True)
        else:
            await interaction.response.send_message('You do not have the permission to send this command.',
                                                    ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} ran /resign for {admin.name}.')

    @discord.app_commands.command(name='say', description='Says stuff as the bot')
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def say(self, interaction, text: str, reference: Optional[str]):
        if reference is not None:
            reference_int = int(reference)
            reference_m = await interaction.channel.fetch_message(reference_int)
            await reference_m.reply(text)
            await interaction.response.send_message(content=f'Sent {text}', ephemeral=True)
        else:
            await interaction.channel.send(content=text)
            await interaction.response.send_message(content=f'Sent {text}', ephemeral=True)
        info_time(f'>LOG> {text}.')

    # noinspection SpellCheckingInspection
    @discord.app_commands.command(name='credits', description='Displays Credits for the bot.')
    async def credits(self, interaction):
        description = f'''<:resources:1278835693900136532> **Coding:**
<:arrow_under:1278834153655107646> Tiazzz -- On [GitHub](<https://github.com/TywrapStudios>)

<:asterix:1279190506777088000> **Emojis:**
<:arrow_under:1278834153655107646> Tiazzz -- On [GitHub](<https://github.com/TywrapStudios>)
<:arrow_under:1278834153655107646> NEVER -- On [Emoji.gg](<https://emoji.gg/user/never_see>)

<:con_excellent:1278830872929501286> **Server Provider:**
<:arrow_under:1278834153655107646> Tiazzz' Dad -- Private

<:pluse:1279147951519825931> **Special Thanks:**
<:arrow_under:1278834153655107646> Richard Schwabe -- On [YouTube](<https://www.youtube.com/@richardschwabe>) for discord.py tutors.
<:arrow_under:1278834153655107646> Tiazzz' Dad -- Private, for explaining some Python stuff.
<:arrow_under:1278834153655107646> Discord Developers Server -- Hidden as per rules.

<:config:1278820765797580921> **Libraries Used:**
<:arrow_under:1278834153655107646> discord.py
<:arrow_under:1278834153655107646> psutil
<:arrow_under:1278834153655107646> decancer_py
<:arrow_under:1278834153655107646> dotenv
<:arrow_under:1278834153655107646> aiohttp
<:arrow_under:1278834153655107646> mcrcon

<:search:1279151128466165911> **Extra:**
<:arrow_under:1278834153655107646> <:githubblack:1279105948908130404> The Tywrap Studios Org on [GitHub](<https://github.com/orgs/Tywrap-Studios/repositories>)
<:arrow_under:1278834153655107646> <:githubblack:1279105948908130404> The project on [GitHub](<https://github.com/Tywrap-Studios/LasCordCrafter>)
<:arrow_under:1278834153655107646> <:mail:1279219863654629426> Want to get in contact and contribute? info.tywrap.studio@gmail.com

-# MIT; Copyright (c) 2024 Tywrap Studios. -- info.tywrap.studio@gmail.com -- {vars.botVersion}
    '''
        embed = discord.Embed(colour=discord.Colour.teal(), title='<:list:1279213268082229381> Credits:',
                              description=description)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} ran /credits.')

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nStandaloneCogError: {error}',
                ephemeral=True)
            raise error


class AppealServiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name='setup', description='Sets up the Bot\'s Ban Appeal Function.')
    @discord.app_commands.checks.has_permissions(administrator=True)
    @discord.app_commands.describe(channel='The channel to set the appeal service up in.')
    async def setup(self, interaction, channel: discord.TextChannel):
        embed = discord.Embed(colour=discord.Colour.from_rgb(230, 230, 60), title='**Appeal a Minecraft Unban.**',
                              description='By using the command **/appeal**, a Private Channel can be made for your Appeal.')
        await channel.send(embed=embed,
                           content='Opening a ban appeal or ticket will ping the `@Minecraft Admin` role, so please do NOT ping them again in the ticket yourself!\nThanks in advance!')
        await interaction.response.send_message(
            content=f'Setup Completed in {channel.mention}.\nMake sure to delete any leftovers.', ephemeral=True)
        info_time(f'>LOG> Setup Completed in #{channel.name} by {interaction.user.name}.')

    @discord.app_commands.command(name='appeal', description='Manually appeals a Minecraft Ban Appeal ticket.')
    async def appeal(self, interaction):
        view = views.ManualAppealButton()
        embed = discord.Embed(colour=discord.Colour.from_rgb(230, 230, 60), title='**Appeal a Minecraft Unban.**',
                              description='By clicking the button below, a Private Channel will be made for your Appeal.')
        await interaction.response.send_message(view=view, embed=embed, ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} ran /appeal.')

    @discord.app_commands.command(name='add', description='Adds a user to the current ticket.')
    @discord.app_commands.describe(member='The member to add to the ticket.')
    async def add(self, interaction, member: discord.Member):
        if "ban-appeal-" in interaction.channel.name and member != interaction.user:
            await interaction.channel.set_permissions(member, view_channel=True, send_messages=True, attach_files=True,
                                                      embed_links=True)
            view = views.RemoveButton(member=member)
            ping = await interaction.channel.send(f'{member.mention}')
            await ping.delete()
            embed = discord.Embed(title='Member Add',
                                  description=f"{member.mention} has been added to the ticket by {interaction.user.mention}.",
                                  colour=discord.Colour.dark_gray())
            await interaction.response.send_message(embed=embed, view=view)
            info_time(f'>LOG> {interaction.user.name} added {member.name} to {interaction.channel.name}.')
        else:
            if "ban-appeal-" not in interaction.channel.name:
                await interaction.response.send_message("This isn't a ticket!", ephemeral=True)
            else:
                if member == interaction.user:
                    await interaction.response.send_message("You can't add or remove yourself!", ephemeral=True)

    @discord.app_commands.command(name='remove', description='Removes a user from the current ticket.')
    @discord.app_commands.describe(member='The member to remove from the ticket.')
    async def remove(self, interaction, member: discord.Member):
        if "ban-appeal-" in interaction.channel.name and member != interaction.user:
            await interaction.channel.set_permissions(member, overwrite=None)
            embed = discord.Embed(title='Member Remove',
                                  description=f"{member.mention} has been removed from the ticket by {interaction.user.mention}.",
                                  colour=discord.Colour.dark_gray())
            await interaction.response.send_message(embed=embed)
            info_time(f'>LOG> {interaction.user.name} removed {member.name} from {interaction.channel.name}.')
        else:
            if "ban-appeal-" not in interaction.channel.name:
                await interaction.response.send_message("This isn't a ticket!", ephemeral=True)
            else:
                if member == interaction.user:
                    await interaction.response.send_message("You can't add or remove yourself!", ephemeral=True)

    @discord.app_commands.command(name='close', description='Closes the ticket.')
    async def close(self, interaction):
        embed = discord.Embed(title='Confirm',
                              description='Please confirm that you want to close your Ban Appeal Ticket.',
                              colour=discord.Colour.green())
        view = views.ConfirmButton()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} closed {interaction.channel.name}.')

    @discord.app_commands.command(name='forceclose', description='Forcefully closes the selected ticket.')
    @discord.app_commands.describe(ticket='The ticket channel to close.')
    async def forceclose(self, interaction, ticket: discord.TextChannel):
        allowedrole1 = interaction.guild.get_role(vars.discordAdmin)
        allowedrole2 = interaction.guild.get_role(vars.minecraftAdmin)
        if allowedrole1 in interaction.user.roles or allowedrole2 in interaction.user.roles:
            if "ban-appeal-" in ticket.name:
                ticket_log_channel = interaction.guild.get_channel(1164581289022722148)
                opname = ticket.name.replace('ban-appeal-', '')
                op = interaction.guild.get_member_named(opname)
                closer = interaction.user
                embed = discord.Embed(title='Ban Appeal Closed', description=f'''
<:id:1279190510027800709> **Ticket Opened by:**
<:asterix:1279190506777088000> {op.mention}

<:leave:1279190513190178826> **Ticket Closed by:**
<:asterix:1279190506777088000> {closer.mention}
<:arrow_under:1278834153655107646> **__This ticket was Force Closed__**''', colour=discord.Colour.green())
                time = datetime.now().strftime('%H:%M')
                datetoday = date.today().strftime('%d/%m/%Y')
                embed.set_footer(text=f'{datetoday} {time}')
                await ticket.delete(reason=f'{interaction.user} wanted to force close {ticket}')
                await ticket_log_channel.send(embed=embed)
                await interaction.response.send_message(f'Force closed {ticket.mention}', ephemeral=True)
                info_time(f'>LOG> {interaction.user.name} force closed {interaction.channel.name}.')
            else:
                if "ban-appeal-" not in ticket.name:
                    await interaction.response.send_message("That TextChannel isn't a ticket!", ephemeral=True)
        else:
            await interaction.response.send_message(f'You do not have the permissions to send this command.',
                                                    ephemeral=True)

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nAppealServiceCogError: {error}',
                ephemeral=True)
            raise error


class SanitizeServiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.interaction_menu = discord.app_commands.ContextMenu(
            name='Sanitize & Dehoist',
            callback=self.sanitize_interaction_menu_callback
        )
        self.bot.tree.add_command(self.interaction_menu)

    @discord.app_commands.checks.has_permissions(manage_nicknames=True)
    async def sanitize_interaction_menu_callback(self, interaction: discord.Interaction, member: discord.Member):
        await util.sanitize(interaction, member)
        info_time(f'>LOG> {interaction.user.name} sanitized {member.name} using a Context Menu.')

    @discord.app_commands.command(name='sanitize',
                                  description='Sanitizes and Dehoists the member\'s Nick using Regex Patterns.')
    @discord.app_commands.checks.has_permissions(manage_nicknames=True)
    async def sanitize(self, interaction, member: discord.Member):
        await util.sanitize(interaction, member)
        info_time(f'>LOG> {interaction.user.name} sanitized {member.name} using a command.]')

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nSanitizeServiceCogError: {error}',
                ephemeral=True)
            raise error


class ClaimCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    claim = app_commands.Group(name='claims', description='Info about the claim system.')

    @claim.command(name='claiming', description='How to claim a piece of land.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''
 1. Press "`M`" (Might need to rebind: Press "esc">Options>Control>Keybinds>"open world map") to open the world map
2. Right-click-drag over the area You want to claim. 
3. In the popup: Click "Claim selected"
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:claim:1278815499349786704> Claiming Chunks:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims claiming for {mention.name}.')

    @claim.command(name='party', description='What are Parties?')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''In your claim config (use my **/claims perms** or **/claims config** command for info) you can set perms for your party.
This means that anyone in a party you're in, has those perms.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party:1278816948846596157> Parties:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims party for {mention.name}.')

    @claim.command(name='party-creation', description='How to create a Party and add people to it.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''- How to create a party: Run in game `/openpac-parties create`
- Does it error? You are likely already in one, or messed something else up.
- How to leave a party: Run in game `/openpac-parties leave`

**How to...**
> - ...*Invite* people to your party: Run in game `openpac-parties member invite <username>`
> - ...*Kick* people from your party: Run in game `openpac-parties member kick <username>`
> - ...*Delete* your party: Run in game `openpac-parties destroy confirm`.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party:1278816948846596157> Party Creation:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims party-creation for {mention.name}.')

    @claim.command(name='party-misc', description='Misc in Parties.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''There is some Misc stuff to having a Party.

**How to...**
> - ...*Give people perms* in terms of party management: Run in game `/openpac-parties member rank <ADMIN|MODERATOR|MEMBER> <username>`
>  - <:info:1278823933717512232> Giving people perms for parties for instance makes them able to send invites or kick people from the party.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party:1278816948846596157> Party Misc:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims party-misc for {mention.name}.')

    @claim.command(name='party-ally', description='How Allies work.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''Alongside giving Party members perms in your claims, you can also Ally another party to get specific claim perms for them as well!

**How to...**
> - ...*Ally* parties: Run in game `/openpac-parties ally add <username of party owner>`.
> - ...*Unally* parties: Run in game `/openpac-parties ally remove <username of party owner>`.

> <:info:1278823933717512232> **NOTES:**
> Allying a party does not give you perms to their claims, they need to ally you on their own as well!
> -> This can mean you have them allied, but they don't, and vice versa.
> Allies have separate perms to Party members.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:ally:1278823662589313045> Allies:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims party-ally for {mention.name}.')

    @claim.command(name='party-ownership', description='How Ownership works.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''The player who ran the `/openpac-parties create` command "owns" said party.

**How to...**
> - ...*Transfer* party ownership: Run in game `/openpac-parties transfer <username> confirm`
> - <:info:1278823933717512232> The user has to be in the party for this to work.
> - <:warn:1249069667159638206> This action is irreversible unless the new owner re-transfers back to you.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party_owner:1278830882828062802> Allies:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims party-ownership for {mention.name}.')

    @claim.command(name='config', description='How to use the config.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''To specify how your (sub)claims work, you are provided an in game config screen.
1. Press "`'`" (Might need to rebind: Press "esc">Options>Controls>Keybinds>"Open Parties and Claims Menu")
2. In the Menu: Player Config menu > My Player Config.
> <:info:1278823933717512232> In here you can now set all sorts of settings related to your (sub)claims.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:config:1278820765797580921> Config:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims config for {mention.name}.')

    @claim.command(name='perms', description='How do I give players perms on my claim?')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''To specify which perms are given to whom, you are provided an in game config screen.
1. Press "`'`" (Might need to rebind: Press "esc">Options>Controls>Keybinds>"Open Parties and Claims Menu")
2. In the Menu: Player Config menu > My Player Config.
3. Set the perms you want your friend to have to something related to "party" or "party only", etc.
> <:info:1278823933717512232> Have you not made a Party yet? Run my command **/claims party-creation** for info on how to do that!
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:perms:1278838464456032388> Perms:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /claims perms for {mention.name}.')

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nClaimCogError: {error}',
                ephemeral=True)
            raise error


class NotesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    notes = app_commands.Group(name='notes', description='Notes about random stuff.')

    @notes.command(name='schematics', description='Explains the fuzz about schematics.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''We've disabled Create's Schematic feature because of the following reasons:
> - It's a little too OP. We'd love you to actually play the game instead of downloading a file and just watching it build. 
> - They cause a ton of strain on the server because of the way they're rendered and loaded. Plus your schematic file gets uploaded to the physical server, and this can unnecessarily take up storage space.
> - We believe that in general that having something just build stuff for you seems unethical and uncreative.


> <:info:1278823933717512232> We understand that you'd still want a way to transfer over builds you made in creative, and this basically blew that opportunity away.
> If you want a way to port over Creative builds: We suggest [Litematica](<https://www.curseforge.com/minecraft/mc-mods/litematica/files/4626718>).'''

        embed = discord.Embed(colour=discord.Colour.blurple(),
                              title='<:list:1279213268082229381> Create\'s Schematics', description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes schematics for {mention}.')

    @notes.command(name='cracked', description='Explains the fuzz about Cracked accounts.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''> Sorry but we do not allow cracked or unofficial accounts to join our server.
> This is because it can get both the Discord and Minecraft server in a lot of trouble.

> Furthermore it is illegal to Pirate games. We can report your message to Discord, and it can in turn get *you* in trouble.

<:info:1278823933717512232> You can buy the official game [here](<https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc>)
<:warn:1249069667159638206> **ALSO PLEASE, PLEASE NOTE THAT MOST CRACKED/ILLEGAL LAUNCHERS __VERY__ OFTEN DUB AS [SPYWARE, ADWARE, DISCOVERERS, PERSISTS, STEALERS AND PRIVILEGE ESCALATORS.](<https://tria.ge/241021-n5b91ssgpf>)**
**WE SUGGEST CLEANSING THEM! NOT JUST FOR YOUR OWN (ONLINE) SAFETY, BUT ALSO FOR OTHERS WHO USE THE SAME DEVICE.**'''
        embed = discord.Embed(colour=discord.Colour.blurple(),
                              title='<:against_rules:1279142167729668096> Cracked Instances:', description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes cracked for {mention}.')

    @notes.command(name='bedrock', description='Explains the fuzz about Bedrock accounts.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''> Our server sadly isn't available for Bedrock users.
> Since we are a modded server you require [Minecraft Java Edition](<https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc>) and [The CurseForge app](<https://www.curseforge.com/download/app>) to play.

<:info:1278823933717512232> **Note you can get [Java for free if you own a (PC) Bedrock license.](<https://help.minecraft.net/hc/en-us/articles/6657208607501-I-Own-Minecraft-Java-or-Bedrock-Edition-for-PC-How-Do-I-Get-the-Other>)**
<:arrow_under:1278834153655107646> This does not count for Console Versions and PE. Using PC Game Pass Bedrock, however, should work.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(),
                              title='<:bedrock:1279144625168191598> Bedrock Instances:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes bedrock for {mention}.')

    @notes.command(name='zip-import', description='How to manually import modpacks using Zip-Files.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''1. Open the <:minecraft_logo:1278852452396826634>Minecraft section of the app.
2. Click <:pluse:1279147951519825931>Create Custom Profile
3. Click the Import option.
4. Find the zip-file you downloaded and select it.
5. CurseForge will now attempt to download and unpack the modpack. If it fails, try steps 2-4 again.
6. Once finished, click Play!
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:download:1279148597094514698> Zip-Importing:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes zip-import for {mention}.')

    @notes.command(name='modlist', description='How to make a modlist.txt file using command prompt.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''To make a modlist.txt file for your modpack, go to the `mods` folder in cmd and run the following command:
```cmd
dir /b "*.jar" >modlist.txt
```
if done correctly a `modlist.txt` file should show up in your `mods` folder.
Please note that some knowledge about the `cd` command, and cmd in general, is to be known for this to properly work.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:perms:1278838464456032388> Modlist:',
                              description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes modlist for {mention}.')

    @notes.command(name='binary-search', description='How to perform a binary-search instead of a sequential-search')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''The binary search is a way of finding a faulty thing amongst a lot of other things, without having to remove the things one-by-one. This is useful for finding a broken mod amongst hundreds of mods, without having to spend time testing the mods one-by-one.

> **This is how it goes:**
> 1. Remove half of the existing things, and put them aside somewhere where they are not affected by or affecting anything.
> 2. Run the program.
> 3. Does the issue persist?
> <:arrow_under:1278834153655107646> If YES: Repeat from step 1 with the current things.
> <:arrow_under:1278834153655107646> IF NO: Swap out the current things with the ones set aside, and repeat from step 1.
> 4. Repeat this process until you are left with only the faulty thing(s).

<:info:1278823933717512232> Why is this beneficial and better? See the GIF attached!
    '''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:search:1279151128466165911> Binary Search:',
                              description=description)
        embed.set_image(
            url='https://media.discordapp.net/attachments/1249069998148812930/1279156096103354448/binary_search.gif?ex=66d36a72&is=66d218f2&hm=b7dd480dfb0d4da00a1359d15ca47a0540a8de18bbe6ff8d8baf1bf0a5301788&=&width=480&height=319')
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes binary-search for {mention}.')

    @notes.command(name='provider', description='What server provider do we use?')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''Our main server provider and sponsor is <#1272562565985206325>,

All of their servers run 24/7, on real hardware (none of that vCPU/threads nonsense), and are actively maintained by them. 
They have plans accommodating budgets of all sizes: big and small, so *your* plan can grow along with your server.
Alongside that, you're free to trial a server for up to a week, or just hang around after.

Again, huge thanks to Central Hosting for Sponsoring our beautiful server;
Without them we would now be nothing :purple_heart:
'''
        embed = discord.Embed(colour=discord.Colour.blurple(),
                              title='<:central_hosting_au:1279161169747116064> Provider:',
                              description=description)
        embed.set_footer(text='https://centralhosting.au/central-hosting/',
                         icon_url='https://media.discordapp.net/attachments/1249069998148812930/1279200313345310741/central_hosting_au.png?ex=66d393a1&is=66d24221&hm=0c085589b8c90653db1aca21932b391e33d68330adc9c44de889a21dc60a029b&=&format=webp&quality=lossless&width=450&height=450')
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes provider for {mention}.')

    @notes.command(name='dontasktoask', description='Don\'t ask to ask. Just ask.')
    async def sub_command(self, interaction, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''**How not to ask a question:**
> I have a question...; 
> Can somebody help me with something?; 
> Is anyone here that can help me?; 
> Is there someone here that knows about <topic/profession/skill>?

**None of those** state what or why you are asking for help, and are more likely to **be ignored** even by someone that can help you. 
Remember, **be clear** about what you need **as soon as possible.**
```ansi
[4;2m[0m[2;31m[4;31mPeople are busy.[0m[2;31m[0m[4;2m[0m
[2;31m[4;31mAttention spans are short.[0m[2;31m[0m[4;2m[0m
[2;31m[4;31mTime is precious.[0m[2;31m[0m[4;2m[0m
```
**How to properly ask a question:**
> Can somebody help me with how to learn how to make a map?
> Is anyone here that can point me towards a tutorial on how to edit an NPC file?

-# Credits to [jkhub.org's "Don't Ask to ask, just Ask." page](https://jkhub.org/dontasktoask/)
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), description=description)
        await interaction.response.send_message(embed=embed, content=mention_text)
        info_time(f'>LOG> {interaction.user.name} sent /notes dontasktoask for {mention}.')

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nNotesCogError: {error}',
                ephemeral=True)
            raise error


class CmdCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd = app_commands.Group(name='cmd', description='Send commands to the Minecraft server.')

    @cmd.command(name='tellraw', description='Says something in the MC Server.')
    @discord.app_commands.describe(content='The String to send.')
    async def sub_command(self, interaction, content: str) -> None:
        command = f'/tellraw @a "{content}"'
        await send_rcon(command, interaction, True)

    @cmd.command(name='log', description='Logs your phrase to the Console.')
    @discord.app_commands.describe(info='The String to send.')
    async def sub_command(self, interaction, info: str):
        command = f'/logtellraw targetless "{info}"'
        await send_rcon(command, interaction, True)

    @cmd.command(name='mclogs', description='Sends a request to mclo.gs for the latest.log, or a log you specify.')
    @discord.app_commands.describe(log='The specific log to send. File name.')
    async def sub_command(self, interaction, log: Optional[str]):
        if log is None:
            file = ''
        else:
            file = f' share {log}'
        command = f'/mclogs{file}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='maintenance', description='Allows you to Toggle Maintenance.')
    @discord.app_commands.describe(enabled='Whether to enable or disable maintenance.')
    async def sub_command(self, interaction, enabled: bool):
        if enabled is True:
            arg = ' on'
        else:
            arg = ' off'
        command = f'/maintenance{arg}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='ban', description='Bans the selected player from the server.')
    @discord.app_commands.describe(player_user='The player to ban.',
                                   reason='The reason for the ban.')
    async def sub_command(self, interaction, player_user: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/ban {player_user}{reason1}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='tempban', description='Temporarily Bans the selected player from the server.')
    @discord.app_commands.describe(player_user='The player to ban.',
                                   duration='The duration of the ban.',
                                   reason='The reason for the ban.')
    async def sub_command(self, interaction, player_user: str, duration: str, reason: Optional[str]):
        duration_v2 = util.format_duration(duration)
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        if re.match(vars.duregex, duration_v2):
            command = f'/tempban {player_user} {duration_v2}{reason1}'
            await send_rcon(command, interaction, True)
        else:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'<:warn:1249069667159638206> `{duration}` does not seem like a valid duration type even when corrected to `{duration_v2}` by our system!\n\n> <:info:1278823933717512232> A correct syntax would be: <number><either s, m, d or w> (e.g. 1w for 1 week.)\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed in e.g. a screenshot.\n-# {vars.botVersion}',
                                  title='RCON: <:resources:1278835693900136532>')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @cmd.command(name='ban-ip', description='IP Bans the selected player from the server.')
    async def sub_command(self, interaction):
        embed = discord.Embed(colour=discord.Colour.red(),
                              description='<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in game.',
                              title='RCON: <:resources:1278835693900136532>')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} sent /ban-ip.')

    @cmd.command(name='tempban-ip', description='IP Bans the selected player from the server.')
    async def sub_command(self, interaction):
        embed = discord.Embed(colour=discord.Colour.red(),
                              description='<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in game.',
                              title='RCON: <:resources:1278835693900136532>')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} sent /tempban-ip.')

    @cmd.command(name='unban', description='Unbans the selected player from the server.')
    @discord.app_commands.describe(player_user='The player to unban.',
                                   reason='The reason for the unban.')
    async def sub_command(self, interaction, player_user: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/unban {player_user}{reason1}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='pardon', description='Pardons the selected player. THIS IS DIFFERENT FROM /UNBAN!')
    @discord.app_commands.describe(player_user='The player to pardon.',
                                   reason='The reason for the pardon.')
    async def sub_command(self, interaction, player_user: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/pardon {player_user}{reason1}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='run', description='Runs any command you provide, given that it has correct syntax.')
    @discord.app_commands.describe(command='The command to run.')
    async def sub_command(self, interaction, command: str):
        mod_chat = interaction.guild.get_channel(vars.logChannel)
        if interaction.channel == mod_chat:
            await send_rcon(command, interaction, True)
        else:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in {mod_chat.mention}.\n-# `Error Code 421`',
                                  title='RCON: <:resources:1278835693900136532>')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @cmd.command(name='clear', description='Clears the selected player\'s inventory.')
    @discord.app_commands.describe(player='The player to clear.',
                                   item='The specific item to clear. This needs a namespace if it isn\'t vanilla.')
    async def sub_command(self, interaction, player: str, item: Optional[str]):
        if item is None:
            items = ''
        else:
            items = f' {item}'
        command = f'/clear {player}{items}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='list', description='Lists all the players online.')
    async def sub_command(self, interaction):
        command = '/list'
        await send_rcon(command, interaction, False)

    @cmd.command(name='restore', description='Restores the grave of a player\'s last death.')
    @discord.app_commands.describe(player='The player to restore for.')
    async def sub_command(self, interaction, player: str):
        command = f'/yigd restore {player}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='view-balance', description='Allows you to see someone\'s Nm. Balance.')
    @discord.app_commands.describe(player='The player to view the balance from.')
    async def sub_command(self, interaction, player: str):
        command = f'/nm view {player}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='tp-offline', description='Allows you to TP Someone who\'s offline.')
    @discord.app_commands.describe(player='The player to teleport.',
                                   pos='The position to teleport to.')
    async def sub_command(self, interaction, player: str, pos: str):
        command = f'/tp_offline {player} {pos}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='heal', description='Heals the selected player.')
    @discord.app_commands.describe(player='The player to heal.')
    async def sub_command(self, interaction, player: str):
        command = f'/heal {player}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='whitelist-toggle', description='Toggle the whitelist on or off.')
    @discord.app_commands.describe(enable='Whether to enable or disable the whitelist.')
    async def sub_command(self, interaction, enable: bool):
        if enable:
            command = f'/whitelist on'
        else:
            command = f'/whitelist off'
        await send_rcon(command, interaction, True)

    @cmd.command(name='whitelist-entry', description='Adds or removes a user to the whitelist.')
    @discord.app_commands.describe(player='The player to add or remove.',
                                   can_enter='Whether to allow the player to enter the server.')
    async def sub_command(self, interaction, player: str, can_enter: bool):
        if can_enter:
            command = f'/whitelist add {player}'
        else:
            command = f'/whitelist remove {player}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='whitelist', description='Lists the Whitelist')
    async def sub_command(self, interaction):
        command = f'/whitelist list'
        await send_rcon(command, interaction, True)

    @cmd.command(name='damage', description='Damages the selected player.')
    @discord.app_commands.describe(player='The player to damage.',
                                   amount='The amount of damage to apply. Remember that 1 damage is 0.5 hearts.')
    async def sub_command(self, interaction, player: str, amount: float):
        command = f'/damage {player} {amount}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='ban-legacy', description='Uses Minecraft\'s ban system.')
    @discord.app_commands.describe(player='The player to ban.',
                                   reason='The reason for the ban.')
    async def sub_command(self, interaction, player: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/minecraft:ban {player}{reason1}'
        await send_rcon(command, interaction, True)

    @cmd.command(name='unban-legacy', description='Uses Minecraft\'s ban system.')
    @discord.app_commands.describe(player='The player to unban.',
                                   reason='The reason for the unban.')
    async def sub_command(self, interaction, player: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/minecraft:pardon {player}{reason1}'
        await send_rcon(command, interaction, True)

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nCmdCogError: {error}',
                ephemeral=True)
            raise error


class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_downtime = None

    async def title_autocomplete(self, interaction, current) -> List[app_commands.Choice[str]]:
        choice = self.current_downtime
        return [app_commands.Choice(name=choice, value=choice)]

    status = app_commands.Group(name='status', description='Commands to send pregen embeds about stati.')

    @status.command(name='downtime', description='Pregen a Downtime Embed, should be used when the server is down.')
    @discord.app_commands.checks.has_any_role(vars.discordAdmin, vars.minecraftAdmin, vars.centralHosting, vars.gunjiCord)
    @discord.app_commands.describe(title='The title of the downtime.')
    @discord.app_commands.autocomplete(title=title_autocomplete)
    async def sub_command(self, interaction, title: str, channel: Optional[discord.TextChannel], ping: Optional[discord.Role]):
        self.current_downtime = title
        modal = modals.DowntimeModal(bot=self.bot, status_title=title, channel=channel, ping=ping)
        await interaction.response.send_modal(modal)

    @status.command(name='update',
                    description='Pregen a Downtime Update Embed, should be used when an update about a downtime can be given.')
    @discord.app_commands.checks.has_any_role(vars.discordAdmin, vars.minecraftAdmin, vars.centralHosting, vars.gunjiCord)
    @discord.app_commands.describe(title='The title of the downtime.')
    @discord.app_commands.autocomplete(title=title_autocomplete)
    async def sub_command(self, interaction, title: str, channel: Optional[discord.TextChannel], ping: Optional[discord.Role]):
        self.current_downtime = title
        modal = modals.DowntimeUpdateModal(bot=self.bot, status_title=title, channel=channel, ping=ping)
        await interaction.response.send_modal(modal)

    @status.command(name='uptime',
                    description='Pregen a Downtime Update Embed, that\'s specifically for the service being back up.')
    @discord.app_commands.checks.has_any_role(vars.discordAdmin, vars.minecraftAdmin, vars.centralHosting, vars.gunjiCord)
    @discord.app_commands.describe(title='The title of the downtime.')
    @discord.app_commands.autocomplete(title=title_autocomplete)
    async def sub_command(self, interaction, title: str, channel: Optional[discord.TextChannel], ping: Optional[discord.Role]):
        self.current_downtime = None
        modal = modals.UptimeModal(bot=self.bot, status_title=title, channel=channel, ping=ping)
        await interaction.response.send_modal(modal)

    @status.command(name='notice',
                    description='Pregen a Notice Embed.')
    @discord.app_commands.checks.has_any_role(vars.discordAdmin, vars.minecraftAdmin, vars.centralHosting, vars.gunjiCord)
    async def sub_command(self, interaction, channel: Optional[discord.TextChannel], ping: Optional[discord.Role]):
        modal = modals.NoticeModal(bot=self.bot, channel=channel, ping=ping)
        await interaction.response.send_modal(modal)

    @status.command(name='bot-status', description='Change the Bot\'s status to say Minecraft Server Stati.')
    @discord.app_commands.checks.has_any_role(vars.discordAdmin, vars.minecraftAdmin, vars.centralHosting,
                                              vars.gunjiCord)
    @discord.app_commands.describe(status='The status to change to. Put nothing to reset',
                                   down='Whether the server is down.')
    async def slash_command(self, interaction, status: Optional[str], down: Optional[bool] = False):
        if down:
            status = f'{status}; DOWN'
        if status is not None:
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.custom, state=status, name='CustomStatus'),
                status=discord.Status.online)
            await interaction.response.send_message('Attempted to change status.', ephemeral=True)
            info_time(f'>STATUS> {interaction.user.name} changed bot status: {status}.')
        else:
            await self.bot.change_presence(activity=discord.Game('on CordCraft Season 2'),
                                           status=discord.Status.online)
            await interaction.response.send_message('Attempted to reset status.', ephemeral=True)
            info_time(f'>STATUS> {interaction.user.name} reset the bot status.')

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nStatusCogError: {error}',
                ephemeral=True)
            raise error


class ThreadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    thread = app_commands.Group(name='thread', description='Commands for managing your thread.')

    @thread.command(name='pin', description='Pin or unpin a message in your thread, given you have permission.')
    @discord.app_commands.describe(message_id='The ID of the message you want to pin or unpin.')
    async def sub_command(self, interaction, message_id: str):
        message = await interaction.channel.fetch_message(int(message_id))
        channel = interaction.channel
        perms = channel.permissions_for(interaction.user)
        if channel.owner is not interaction.user and not perms.manage_messages:
            await interaction.response.send_message(content='You do not have the permissions to send this command.',
                                                    ephemeral=True)
        else:
            if not message.pinned:
                await message.pin(
                    reason=f'{interaction.user.mention} pinned a message in their thread, {interaction.channel.mention}.')
                info_time(f'>LOG> {interaction.user.name} pinned a message in their thread.')
            else:
                await message.unpin(
                    reason=f'{interaction.user.mention} unpinned a message in their thread, {interaction.channel.mention}.')
                info_time(f'>LOG> {interaction.user.name} unpinned a message in their thread.')

    @thread.command(name='lock', description='Lock or unlock your thread, given you have permission.')
    @discord.app_commands.describe(thread='The thread to lock or unlock.')
    async def sub_command(self, interaction, thread: Optional[discord.Thread]):
        if thread is None:
            thread = interaction.channel
        perms = thread.permissions_for(interaction.user)
        if thread.owner is not interaction.user and not perms.manage_threads:
            await interaction.response.send_message(content='You do not have the permissions to send this command.',
                                                    ephemeral=True)
        else:
            if not thread.locked:
                await thread.edit(locked=True,
                                  reason=f'{interaction.user.mention} locked their thread, {thread.mention}.')
                info_time(f'>LOG> {interaction.user.name} locked their thread.')
            else:
                await thread.edit(locked=True,
                                  reason=f'{interaction.user.mention} unlocked their thread, {thread.mention}.')
                info_time(f'>LOG> {interaction.user.name} unlocked their thread.')

    @thread.command(name='delete', description='Deletes your thread, given you have permission.')
    @discord.app_commands.describe(thread='The thread to delete.')
    async def sub_command(self, interaction, thread: Optional[discord.Thread]):
        if thread is None:
            thread = interaction.channel
        perms = thread.permissions_for(interaction.user)
        if thread.owner is not interaction.user and not perms.manage_threads:
            await interaction.response.send_message(content='You do not have the permissions to send this command.',
                                                    ephemeral=True)
        else:
            embed = discord.Embed(title='Warning:', colour=discord.Colour.brand_red(),
                                  description=f'You are about to fully delete {thread.mention}, are you sure?\nNote that this action is IRREVERSIBLE!')
            view = views.ConfirmDeleteThreadButton(thread=thread)
            await interaction.response.send_message(embed=embed, view=view)

    @thread.command(name='info', description='Displays info about the Thread.')
    @discord.app_commands.describe(thread='The thread to get info about.')
    async def sub_command(self, interaction, thread: Optional[discord.Thread]):
        if thread is None:
            thread = interaction.channel

        last_message = thread.last_message
        if last_message is None:
            last_message = 'No message could be found.'

        starter_message = thread.starter_message
        jump_to_top = ''
        if starter_message is not None:
            jump_to_top = f'\n-# [Jump to top]({starter_message.jump_url})'

        description = f'''<:party_owner:1278830882828062802> Owner: {thread.owner.mention}
<:config:1278820765797580921> Locked: {thread.locked}
<:id:1279190510027800709> Thread Type: {thread.type}
<:asterix:1279190506777088000> Stats:
<:arrow_under:1278834153655107646> Member Count: {thread.member_count}
<:arrow_under:1278834153655107646> Message Count: {thread.message_count}
<:arrow_under:1278834153655107646> Last Message: {last_message}{jump_to_top}
'''
        embed = discord.Embed(title=f'Info about {thread.mention}', description=description)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        info_time(f'>LOG> {interaction.user.name} viewed info about {thread.name}.')

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nThreadCogError: {error}',
                ephemeral=True)
            raise error


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moderation = app_commands.Group(name='moderation', description='Moderation commands.')

    @moderation.command(name='ban', description='Bans a user.')
    @discord.app_commands.checks.has_permissions(ban_members=True)
    @discord.app_commands.describe(offender='The user to ban.',
                                   reason='The reason for the ban.',
                                   time='The length of this ban, if any.',
                                   delete_messages='Whether to delete the messages of the user. (7 days)',
                                   silent='Whether to notify the channel of this action.')
    async def sub_command(self, interaction, offender: discord.Member, reason: Optional[str] = 'No reason given',
                          time: Optional[str] = 'infinite', delete_messages: Optional[bool] = False,
                          silent: Optional[bool] = False):
        offender_dm = await offender.create_dm()
        reason_for_audit = f'{interaction.user.mention}: {reason}.'
        if delete_messages:
            del_days = 7
        else:
            del_days = 0

        if time.lower() != 'infinite':
            dur = util.format_duration(time)
            dur_int = util.from_formatted_get_int(dur)
            dur_str = util.from_formatted_get_str(dur)

            unban_time = datetime.now()
            if dur_str == 's':
                unban_time = unban_time + timedelta(seconds=dur_int)
            elif dur_str == 'm':
                unban_time = unban_time + timedelta(minutes=dur_int)
            elif dur_str == 'h':
                unban_time = unban_time + timedelta(hours=dur_int)
            elif dur_str == 'd':
                unban_time = unban_time + timedelta(days=dur_int)
            elif dur_str == 'w':
                unban_time = unban_time + timedelta(weeks=dur_int)
            elif dur_str == 'M':
                unban_time = unban_time + timedelta(days=dur_int * 30)  # Approximate month length

            await database.add_temp_ban(offender.id, interaction.guild.id, unban_time.isoformat(), reason)
            time_str = f"until {unban_time.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            time_str = "indefinitely"

        await offender_dm.send(content=f'''Hi. Unfortunately I am here to inform you that you have been banned from GunjiCordia.
The reason for your ban was: **{reason}**.
You are banned **{time_str}**.
The moderator responsible for your ban was {interaction.user.mention}.

If you think this ban was not rightful, or an actual accident feel free to contact said, or a different moderator.
I wish you a great day further!''')

        await offender.ban(reason=reason_for_audit, delete_message_days=del_days)
        embed = discord.Embed(
            description=f'{offender.mention} was banned from the server {time_str}. <:red:1301608135370473532>',
            colour=discord.Colour.red())
        await interaction.response.send_message(embed=embed, ephemeral=silent)
        info_time(f'>LOG> {interaction.user.name} Banned {offender.name} from {interaction.guild.name} for {reason} {time_str}.')

    @moderation.command(name='unban', description='Unbans the user.')
    @discord.app_commands.checks.has_permissions(ban_members=True)
    @discord.app_commands.describe(offender='The user to unban.',
                                   reason='The reason for the unban.',
                                   silent='Whether to notify the channel of this action.')
    async def unban(self, interaction, offender: discord.User, reason: Optional[str] = 'No reason given',
                    silent: Optional[bool] = False):
        reason_for_audit = f'{interaction.user.mention}: {reason}.'
        active_bans = await database.get_active_bans()

        for ban in active_bans:
            user_id, guild_id, unban_time, reason = ban

            if offender.id == user_id:
                try:
                    await database.remove_temp_ban(user_id)
                    info_time(f'>LOG> Unbanned a Tempban.')
                except discord.HTTPException:
                    info_time(f'>LOG> Something went wrong while Unbanning a Tempban.')
                    continue
        interaction.guild.unban(user=offender, reason=reason_for_audit)
        embed = discord.Embed(
            description=f'{offender.mention} was unbanned from the server. <:green:1301608134011256852>',
            colour=discord.Colour.green())
        await interaction.response.send_message(embed=embed, ephemeral=silent)
        info_time(f'>LOG> {interaction.user.name} Unbanned {offender.name} from {interaction.guild.name} for {reason}.')

    @moderation.command(name='kick', description='Kicks a user.')
    @discord.app_commands.checks.has_permissions(kick_members=True)
    @discord.app_commands.describe(offender='The user to kick.',
                                   reason='The reason for the kick.',
                                   silent='Whether to notify the channel of this action.')
    async def sub_command(self, interaction, offender: discord.Member, reason: Optional[str] = 'No reason given',
                          silent: Optional[bool] = False):
        offender_dm = await offender.create_dm()
        reason_for_audit = f'{interaction.user.mention}: {reason}.'
        await offender_dm.send(f'''Hi. I am here to inform you that you have been kicked from GunjiCordia.
The reason for your kick was: `{reason}`.
The moderator responsible for your kick was {interaction.user.mention}.

If you wish to join back, here is the Discord Invite Link: {vars.guildInviteLink}
I wish you a great day further!''')
        await offender.kick(reason=reason_for_audit)
        embed = discord.Embed(description=f'{offender.mention} was kicked from the server. <:red:1301608135370473532>',
                              colour=discord.Colour.red())
        await interaction.response.send_message(embed=embed, ephemeral=silent)
        info(f'>LOG> {interaction.user.name} Kicked {offender.name} from {interaction.guild.name} for {reason}.')

    @moderation.command(name='timeout', description='Times out a user.')
    @discord.app_commands.checks.has_permissions(moderate_members=True)
    @discord.app_commands.describe(offender='The user to timeout.',
                                   duration='The duration of the timeout. Maximum 28 days.',
                                   reason='The reason for the timeout.',
                                   silent='Whether to notify the channel of this action.')
    async def sub_command(self, interaction, offender: discord.Member, duration: str,
                          reason: Optional[str] = 'No reason given', silent: Optional[bool] = False):
        dur = util.format_duration(duration)
        dur_int = util.from_formatted_get_int(dur)
        dur_str = util.from_formatted_get_str(dur)
        dur_days = util.get_duration_in_days(dur_str, dur_int)
        reason = f'{interaction.user.mention}: {reason}.'
        invalid = False
        handled = False

        if dur_days > 28 or dur_days == 0 and not invalid:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> `{duration}`, even when automatically corrected to `{dur}` by our system, is an invalid duration length!\n\n> <:info:1278823933717512232> Note: The technical limit is 28 days.\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed.\n-# {vars.botVersion} | {dur}:{dur_int}:{dur_str}:{dur_days}',
                colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            invalid = True
            handled = True
        if dur_str != 's' and dur_str != 'm' and dur_str != 'h' and dur_str != 'd' and dur_str != 'w' and not invalid:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> `{duration}` does not seem like a valid duration even when automatically corrected to `{dur}` by our system!\n\n> <:info:1278823933717512232> A correct format would be: e.g. 1w, 1 week, 6 days, 2h.\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed.\n-# {vars.botVersion} | {dur}:{dur_int}:{dur_str}:{dur_days}',
                colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            invalid = True
            handled = True

        if 's' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} second(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(seconds=dur_int), reason=reason)
            await interaction.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'm' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} minutes(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(minutes=dur_int), reason=reason)
            await interaction.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'h' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} hours(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(hours=dur_int), reason=reason)
            await interaction.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'd' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} days(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(days=dur_int), reason=reason)
            await interaction.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'w' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} week(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(weeks=dur_int), reason=reason)
            await interaction.response.send_message(embed=embed, ephemeral=silent)

    @moderation.command(name='lock', description='Lock or unlock the channel.')
    @discord.app_commands.checks.has_permissions(moderate_members=True)
    @discord.app_commands.describe(silent='Whether to notify the channel of this action.')
    async def sub_command(self, interaction, silent: Optional[bool] = False):
        channel = interaction.channel
        if channel.type != discord.ChannelType.text:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> {channel.mention} is not a valid text channel!',
                colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif channel.overwrites_for(interaction.guild.default_role).send_messages is False:
            embed = discord.Embed(
                description=f'{channel.mention} was unlocked by {interaction.user.mention}. <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await channel.set_permissions(interaction.guild.default_role,
                                          overwrite=discord.PermissionOverwrite(send_messages=True))
            await interaction.response.send_message(embed=embed, ephemeral=silent)
        else:
            embed = discord.Embed(
                description=f'{channel.mention} was locked by {interaction.user.mention}. <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await channel.set_permissions(interaction.guild.default_role,
                                          overwrite=discord.PermissionOverwrite(send_messages=False))
            await interaction.response.send_message(embed=embed, ephemeral=silent)

    @moderation.command(name='slowmode', description='Set a slowmode for the channel.')
    @discord.app_commands.checks.has_permissions(moderate_members=True)
    @discord.app_commands.describe(channel='The channel to set the slowmode for.',
                                   duration='The duration of the slowmode. Maximum 6 hours.')
    async def sub_command(self, interaction, channel: Optional[discord.TextChannel], duration: str,
                          silent: Optional[bool] = False):
        dur = util.format_duration(duration)
        dur_int = util.from_formatted_get_int(dur)
        dur_str = util.from_formatted_get_str(dur)
        dur_seconds = round(util.get_duration_in_days(dur_str, dur_int) * 86400)

        if channel is None:
            channel = interaction.channel
        if channel.type != discord.ChannelType.text:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> {channel.mention} is not a valid text channel!',
                colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif dur_seconds > 21600:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> {dur} is too long of a duration!\nThe maximum is 6 hours.',
                colour=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif dur_seconds != 0:
            await channel.edit(slowmode_delay=dur_seconds)
            embed = discord.Embed(
                description=f'{channel.mention} was set on a slowmode of {dur} seconds by {interaction.user.mention}. <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await interaction.response.send_message(embed=embed, ephemeral=silent)
        else:
            await channel.edit(slowmode_delay=dur_seconds)
            embed = discord.Embed(
                description=f'{channel.mention}\'s slowmode was disabled by {interaction.user.mention}. <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await interaction.response.send_message(embed=embed, ephemeral=silent)

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f'You are on cooldown. Please wait {error.retry_after:.2f} seconds.', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(
                f'I do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                f'You do not have the required permissions to run this command.\nMissing Permissions: {error.missing_permissions}',
                ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.HTTPException):
            await interaction.response.send_message(
                f'An HTTPException was raised while executing this command.\nError: {error}', ephemeral=True)
            raise error
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(
                f'Something went wrong while invoking this command.\nError: {error}', ephemeral=True)
            raise error
        else:
            await interaction.response.send_message(
                f'Something unexpected happened while handling this command.\nModCogError: {error}',
                ephemeral=True)
            raise error

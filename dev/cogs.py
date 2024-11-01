import re
import time
from datetime import timedelta, datetime, date
from typing import Optional, Union

import discord
import psutil
from discord import app_commands
from discord.ext import commands

import bot_events
import util
import vars
import views
import database
from rcon import send_rcon
from util import info


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


class StandaloneCog(commands.Cog):
    def __init__(self, bot: commands.Bot, start_time: float):
        self.bot = bot
        self.start_time = start_time

    @commands.command(name='debug-sync')
    async def sync(self, ctx):
        tywrap = ctx.guild.get_member(1041430503389155492)
        if ctx.author == tywrap:
            info(f'[{util.time()}] >LOG> Bot Tree Sync Started by {ctx.author.name}.')
            await self.bot.tree.sync()
            info(f'[{util.time()}] >LOG> Finished Syncing Bot Tree.')
        else:
            info(f'[{util.time()}] >LOG> Bot Tree Sync Failed: no permission.')

    @commands.command(name='debug-stop')
    async def exit(self, ctx):
        tywrap = ctx.guild.get_member(1041430503389155492)
        if ctx.author == tywrap:
            info(f'[{util.time()}] >LOG> Bot Stopped by {ctx.author.name}.')
            await self.bot.close()
        else:
            info(f'[{util.time()}] >LOG> Failed to stop bot.')

    @commands.command(name='debug-flush_database')
    async def flush_database(self, ctx):
        active_bans = database.get_active_bans()
        tywrap = ctx.guild.get_member(1041430503389155492)
        if ctx.author == tywrap:
            for ban in active_bans:
                user_id, guild_id, unban_time, reason = ban
                try:
                    database.remove_temp_ban(user_id)
                except:
                    info(f'[{util.time()}] >LOG> Something went wrong while Flushing a database entry.')
                    continue
        info(f'[{util.time()}] >LOG> {ctx.author.name} Attempted to flush database.')

    @app_commands.command(name='ip-joining', description='Tells the person you specify how to join the server.')
    async def slash_command(self, ctx, member: discord.Member) -> None:
        await ctx.response.send_message(f'''Hey, <@{member.id}>!
Are you wondering how to join? The server IP alongside the Modpack Link and the Rules are all located in
- {vars.ipChannel}.
And hey, if you're there already, why not read the rules?

> ## For the future: Please use your eyes, not your mouth.
> ~ Sincerely, the entire admin team cuz this question is asked too much. /hj''')
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /ip-joining for {member.name}.')

    @app_commands.command(name='ping', description='See how slow/fast the Bot\'s reaction time (ping) is.')
    async def slash_command(self, ctx) -> None:
        global latency_val
        latency = round(self.bot.latency * 1000)
        if latency > 200 or latency == 200:
            latency_val = f'`{latency}ms` <:con_bad:1278830871532802089>'
        else:
            if latency > 100 or latency == 100:
                latency_val = f'`{latency}ms` <:con_mediocre:1278830874074546199>'
            else:
                if latency < 100:
                    latency_val = f'`{latency}ms` <:con_excellent:1278830872929501286>'
        embed = discord.Embed(description=f'## Pong! {latency_val}', colour=discord.Colour.from_rgb(70, 230, 210))
        embed.set_footer(text='Want to see more? Use /stats!', )
        await ctx.response.send_message(embed=embed)
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /ping -> {latency_val}.')

    @app_commands.command(name="bean", description="Beans the member. Yep. That's all it does.")
    async def slash_command(self, ctx, member: discord.Member):
        embed = discord.Embed(title='Member Beaned',
                              description=f'Member: {member.mention},\nResponsible "moderator": {ctx.user.mention}',
                              colour=discord.Colour.og_blurple())
        await ctx.response.send_message(embed=embed)
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /bean for {member.name}.')

    # noinspection SpellCheckingInspection
    @app_commands.command(name='stats', description='Displays the Bot\'s statistics.')
    async def slash_command(self, ctx) -> None:
        # Stats
        global latency_val
        cpu_stat = psutil.cpu_percent(5)
        actual_ram = psutil.virtual_memory()[3] / 1000000
        rounded_ram = round(actual_ram)
        if actual_ram == 0 or actual_ram < 0:
            ram = 'Stat fetched under or is 0. Error 1.'
        else:
            ram = f'{rounded_ram}MB'
        uptime = str(timedelta(seconds=int(round(time.time() - self.start_time))))
        latency = round(self.bot.latency * 1000)
        if latency > 200 or latency == 200:
            latency_val = f'`{latency}ms`<:con_bad:1278830871532802089>'
        else:
            if latency > 100 or latency == 100:
                latency_val = f'`{latency}ms`<:con_mediocre:1278830874074546199>'
            else:
                if latency < 100:
                    latency_val = f'`{latency}ms`<:con_excellent:1278830872929501286>'
        member_count = len([m for m in ctx.guild.members if not m.bot])
        bot_count = len([m for m in ctx.guild.members if m.bot])
        guild_age_secs = time.time() - ctx.guild.created_at.timestamp()
        guild_age = round(guild_age_secs / 86400)
        bot_member = ctx.guild.get_member_named(vars.botName)
        bot_status_game = bot_member.activity.name
        bot_status_raw = bot_member.activity
        if 'on CordCraft' in bot_status_game:
            bot_status = f'**The server is online and stable.** <a:stable:1278830944932855911>'
        else:
            if '; DOWN' in bot_status_raw.state:
                message = bot_status_raw.state.replace('; DOWN', '')
                bot_status = f'**The server is currently __down__.** <a:down:1278830877396172840>\n<:arrow_under:1278834153655107646>**Message:** {message}'
            else:
                bot_status = f'**There might be a slight complication.** <a:unstable:1278830948120789064>\n<:arrow_under:1278834153655107646>**Message:** {bot_status_raw.state}'
        status_embed = discord.Embed(colour=discord.Colour.from_rgb(70, 230, 210), title='CordCrafter Status.',
                                     description=f'''----------------------------
<:space:1251655233919123628><:speed:1251649973418983565> **Latency:** {latency_val}
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
        await ctx.response.send_message(embed=status_embed)
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /stats -> {latency_val}.')

    @app_commands.command(name='resign', description='Resigns the Minecraft member you chose.')
    async def slash_command(self, ctx, admin: discord.Member):
        tywrap = ctx.guild.get_member(1041430503389155492)
        old_role = ctx.guild.get_role(vars.minecraftAdmin)
        new_role = ctx.guild.get_role(vars.resigned)
        if ctx.user == tywrap:
            if old_role in admin.roles and new_role not in admin.roles:
                await admin.remove_roles(old_role, reason='Resigning Minecraft Admin...')
                await admin.add_roles(new_role, reason='Resigning Minecraft Admin...')
                await ctx.response.send_message(
                    f'Successfully resigned {admin.mention} from the Admin team.\nDon\'t forget to /deop them!',
                    ephemeral=True)
            else:
                if old_role not in admin.roles and new_role not in admin.roles:
                    await ctx.response.send_message(
                        f'Could not resign Admin {admin.mention}. \nReason: Could not find {old_role.mention} role in User roles.',
                        ephemeral=True)
                if old_role not in admin.roles and new_role in admin.roles:
                    await ctx.response.send_message(
                        f'Could not resign Admin {admin.mention}. \nReason: User is already resigned.', ephemeral=True)
                if old_role in admin.roles and new_role in admin.roles:
                    await ctx.response.send_message(
                        f'Something went wrong while assigning and resigning roles.\nPlease manually re-check {admin.mention}\'s roles',
                        ephemeral=True)
        else:
            await ctx.response.send_message('You do not have the permission to send this command.', ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /resign for {admin.name}.')

    @app_commands.command(name='say', description='Says stuff as the bot')
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def slash_command(self, ctx, text: str, reference: Optional[str]):
        if reference is not None:
            reference_int = int(reference)
            reference_m = await ctx.channel.fetch_message(reference_int)
            await reference_m.reply(text)
            await ctx.response.send_message(content=f'Sent {text}', ephemeral=True)
        else:
            await ctx.channel.send(content=text)
            await ctx.response.send_message(content=f'Sent {text}', ephemeral=True)
        info(f'[{util.time()}] >LOG> {text}.')

    # noinspection SpellCheckingInspection
    @app_commands.command(name='credits', description='Displays Credits for the bot.')
    async def slash_command(self, ctx):
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
<:arrow_under:1278834153655107646> datetime
<:arrow_under:1278834153655107646> psutil
<:arrow_under:1278834153655107646> decancer_py
<:arrow_under:1278834153655107646> dotenv
<:arrow_under:1278834153655107646> typing
<:arrow_under:1278834153655107646> aiohttp
<:arrow_under:1278834153655107646> mcrcon
<:arrow_under:1278834153655107646> logging

<:search:1279151128466165911> **Extra:**
<:arrow_under:1278834153655107646> <:githubblack:1279105948908130404> The Tywrap Studios Org on [GitHub](<https://github.com/orgs/Tywrap-Studios/repositories>)
<:arrow_under:1278834153655107646> <:githubblack:1279105948908130404> The project on [GitHub](<https://github.com/Tywrap-Studios/LasCordCrafter>)
<:arrow_under:1278834153655107646> <:mail:1279219863654629426> Want to get in contact and contribute? info.tywrap.studio@gmail.com

-# MIT; Copyright 2024 Tywrap Studios. -- info.tywrap.studio@gmail.com -- {vars.botVersion}
    '''
        embed = discord.Embed(colour=discord.Colour.teal(), title='<:list:1279213268082229381> Credits:',
                              description=description)
        await ctx.response.send_message(embed=embed, ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /credits.')


class AppealServiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='setup', description='Sets up the Bot\'s Ban Appeal Function.')
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def slash_command(self, ctx, channel: discord.TextChannel):
        embed = discord.Embed(colour=discord.Colour.from_rgb(230, 230, 60), title='**Appeal a Minecraft Unban.**',
                              description='By using the command **/appeal**, a Private Channel can be made for your Appeal.')
        await channel.send(embed=embed,
                           content='Opening a ban appeal or ticket will ping the `@Minecraft Admin` role, so please do NOT ping them again in the ticket yourself!\nThanks in advance!')
        await ctx.response.send_message(
            content=f'Setup Completed in {channel.mention}.\nMake sure to delete any leftovers.', ephemeral=True)
        info(f'[{util.time()}] >LOG> Setup Completed in #{channel.name} by {ctx.user.name}.')

    @app_commands.command(name='appeal', description='Manually appeals a Minecraft Ban Appeal ticket.')
    async def slash_command(self, ctx):
        view = views.ManualAppealButton()
        embed = discord.Embed(colour=discord.Colour.from_rgb(230, 230, 60), title='**Appeal a Minecraft Unban.**',
                              description='By clicking the button below, a Private Channel will be made for your Appeal.')
        await ctx.response.send_message(view=view, embed=embed, ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} ran /appeal.')

    @app_commands.command(name='add', description='Adds a user to the current ticket.')
    async def slash_command(self, ctx, member: discord.Member):
        if "ban-appeal-" in ctx.channel.name and member != ctx.user:
            await ctx.channel.set_permissions(member, view_channel=True, send_messages=True, attach_files=True,
                                              embed_links=True)
            view = views.RemoveButton(member=member)
            ping = await ctx.channel.send(f'{member.mention}')
            await ping.delete()
            embed = discord.Embed(title='Member Add',
                                  description=f"{member.mention} has been added to the ticket by {ctx.user.mention}.",
                                  colour=discord.Colour.dark_gray())
            await ctx.response.send_message(embed=embed, view=view)
            info(f'[{util.time()}] >LOG> {ctx.user.name} added {member.name} to {ctx.channel.name}.')
        else:
            if "ban-appeal-" not in ctx.channel.name:
                await ctx.response.send_message("This isn't a ticket!", ephemeral=True)
            else:
                if member == ctx.user:
                    await ctx.response.send_message("You can't add or remove yourself!", ephemeral=True)

    @app_commands.command(name='remove', description='Removes a user from the current ticket.')
    async def slash_command(self, ctx, member: discord.Member):
        if "ban-appeal-" in ctx.channel.name and member != ctx.user:
            await ctx.channel.set_permissions(member, overwrite=None)
            embed = discord.Embed(title='Member Remove',
                                  description=f"{member.mention} has been removed from the ticket by {ctx.user.mention}.",
                                  colour=discord.Colour.dark_gray())
            await ctx.response.send_message(embed=embed)
            info(f'[{util.time()}] >LOG> {ctx.user.name} removed {member.name} from {ctx.channel.name}.')
        else:
            if "ban-appeal-" not in ctx.channel.name:
                await ctx.response.send_message("This isn't a ticket!", ephemeral=True)
            else:
                if member == ctx.user:
                    await ctx.response.send_message("You can't add or remove yourself!", ephemeral=True)

    @app_commands.command(name='close', description='Closes the ticket.')
    async def slash_command(self, ctx):
        embed = discord.Embed(title='Confirm',
                              description='Please confirm that you want to close your Ban Appeal Ticket.',
                              colour=discord.Colour.green())
        view = views.ConfirmButton()
        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} closed {ctx.channel.name}.')

    @app_commands.command(name='forceclose', description='Forcefully closes the selected ticket.')
    async def slash_command(self, ctx, ticket: discord.TextChannel):
        allowedrole1 = ctx.guild.get_role(vars.discordAdmin)
        allowedrole2 = ctx.guild.get_role(vars.minecraftAdmin)
        if allowedrole1 in ctx.user.roles or allowedrole2 in ctx.user.roles:
            if "ban-appeal-" in ticket.name:
                ticket_log_channel = ctx.guild.get_channel(1164581289022722148)
                opname = ticket.name.replace('ban-appeal-', '')
                op = ctx.guild.get_member_named(opname)
                closer = ctx.user
                embed = discord.Embed(title='Ban Appeal Closed', description=f'''
    <:id:1279190510027800709> **Ticket Opened by:**
    <:asterix:1279190506777088000> {op.mention}

    <:leave:1279190513190178826> **Ticket Closed by:**
    <:asterix:1279190506777088000> {closer.mention}
    <:arrow_under:1278834153655107646> **__This ticket was Force Closed__**
    ''', colour=discord.Colour.green())
                time = datetime.now().strftime('%H:%M')
                datetoday = date.today().strftime('%d/%m/%Y')
                embed.set_footer(text=f'{datetoday} {time}')
                await ticket.delete(reason=f'{ctx.user} wanted to force close {ticket}')
                await ticket_log_channel.send(embed=embed)
                await ctx.response.send_message(f'Force closed {ticket.mention}', ephemeral=True)
                info(f'[{util.time()}] >LOG> {ctx.user.name} force closed {ctx.channel.name}.')
            else:
                if "ban-appeal-" not in ticket.name:
                    await ctx.response.send_message("That TextChannel isn't a ticket!", ephemeral=True)
        else:
            await ctx.response.send_message(f'You do not have the permissions to send this command.', ephemeral=True)


class SanitizeServiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # TODO>WIP[4]: Make a Context Menu work for this Cog.

    @app_commands.command(name='sanitize',
                          description='Sanitizes and Dehoists the member\'s Nick using Regex Patterns.')
    @discord.app_commands.checks.has_permissions(manage_nicknames=True)
    async def context(self, ctx, member: discord.Member):
        await util.sanitize(ctx, member)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sanitized {member.name} using a command.]')


class ClaimCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    claim = app_commands.Group(name='claims', description='Info about the claim system.')

    @claim.command(name='claiming', description='How to claim a piece of land.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''
 1. Press "`M`" (Might need to rebind: Press "esc">Options>Control>Keybinds>"open world map") to open up the world map
2. Right-click-drag over the area You want to claim. 
3. In the popup: Click "Claim selected"
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:claim:1278815499349786704> Claiming Chunks:',
                              description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims claiming for {mention.name}.')

    @claim.command(name='party', description='What are Parties?')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''In your claim config (use my **/claims perms** or **/claims config** command for info) you can set perms for your party.
This means that anyone in a party you're in, has those perms.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party:1278816948846596157> Parties:',
                              description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims party for {mention.name}.')

    @claim.command(name='party-creation', description='How to create a Party and add people to it.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
> - ...*Delete* your party: Run in game `openpac-parties destroy confirm`
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party:1278816948846596157> Party Creation:',
                              description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims party-creation for {mention.name}.')

    @claim.command(name='party-misc', description='Misc in Parties.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims party-misc for {mention.name}.')

    @claim.command(name='party-ally', description='How Allies work.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''Alongside giving Party members perms in your claims, you can also Ally another party to get specific claim perms for them as well!

**How to...**
> - ...*Ally* parties: Run in game `/openpac-parties ally add <username of party owner>`
> - ...*Unally* parties: Run in game `/openpac-parties ally remove <username of party owner>`

> <:info:1278823933717512232> **NOTES:**
> Allying a party does not give you perms to their claims, they need to ally you on their own as well!
> -> This can mean you have them allied, but they don't, and vice versa.
> Allies have separate perms to Party members.
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:ally:1278823662589313045> Allies:',
                              description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims party-ally for {mention.name}.')

    @claim.command(name='party-ownership', description='How Ownership works.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''The player who ran the `/openpac-parties create` command "owns" said party.

**How to...**
> - ...*Transfer* party ownership: Run in game `/openpac-parties transfer <username> confirm`
> - <:info:1278823933717512232> The user has to be in the party for this to work.
> - <:warn:1249069667159638206> This action is irreversible unless the new owner re-transfers back to you
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:party_owner:1278830882828062802> Allies:',
                              description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims party-ownership for {mention.name}.')

    @claim.command(name='config', description='How to use the config.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims config for {mention.name}.')

    @claim.command(name='perms', description='How do I give players perms on my claim?')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''To specify which perms are given to who, you are provided an in game config screen.
1. Press "`'`" (Might need to rebind: Press "esc">Options>Controls>Keybinds>"Open Parties and Claims Menu")
2. In the Menu: Player Config menu > My Player Config.
3. Set the perms you want your friend to have to something related to "party" or "party only", etc.
> <:info:1278823933717512232> Have you not made a Party yet? Run my command **/claims party-creation** for info on how to do that!
'''
        embed = discord.Embed(colour=discord.Colour.blurple(), title='<:perms:1278838464456032388> Perms:',
                              description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /claims perms for {mention.name}.')


class NotesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    notes = app_commands.Group(name='notes', description='Notes about random stuff.')

    @notes.command(name='cracked', description='Explains the fuzz about Cracked accounts.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''> Sorry but we do not allow cracked or unofficial accounts to join our server.
> This is because it can get both the Discord and Minecraft server in a lot of trouble.

> Furthermore it is illegal to Pirate games. We can report your message to Discord and it can in turn get *you* in trouble.

<:info:1278823933717512232> You can buy the official game [here](<https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc>)
<:warn:1249069667159638206> **ALSO PLEASE, PLEASE NOTE THAT MOST CRACKED/ILLEGAL LAUNCHERS __VERY__ OFTEN DUB AS [SPYWARE, ADWARE, DISCOVERERS, PERSISTS, STEALERS AND PRIVILEGE ESCALATORS.](<https://tria.ge/241021-n5b91ssgpf>)**
**WE SUGGEST CLEANSING THEM! NOT JUST FOR YOUR OWN (ONLINE) SAFETY, BUT ALSO FOR OTHERS WHO USE THE SAME DEVICE.**'''
        embed = discord.Embed(colour=discord.Colour.blurple(),
                              title='<:against_rules:1279142167729668096> Cracked Instances:', description=description)
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes cracked for {mention.name}.')

    @notes.command(name='bedrock', description='Explains the fuzz about Bedrock accounts.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes bedrock for {mention.name}.')

    @notes.command(name='zip-import', description='How to manually import modpacks using Zip-Files.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes zip-import for {mention.name}.')

    @notes.command(name='modlist', description='How to make a modlist.txt file using command prompt.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes modlist for {mention.name}.')

    @notes.command(name='binary-search', description='How to perform a binary-search instead of a sequential-search')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
        if mention is None:
            mention_text = ''
        else:
            mention_text = mention.mention
        description = '''The binary search is a way of finding a faulty thing amongst a lot of other things, without having to remove the things one-by-one. This is useful for finding a broken mod among hundreds of mods, without having to spend time testing the mods one-by-one.

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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes binary-search for {mention.name}.')

    @notes.command(name='provider', description='What server provider do we use?')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes provider for {mention.name}.')

    @notes.command(name='dontasktoask', description='Don\'t ask to ask. Just ask.')
    async def sub_command(self, ctx, mention: Optional[discord.Member]):
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
        await ctx.response.send_message(embed=embed, content=mention_text)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /notes dontasktoask for {mention.name}.')


class CmdCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    cmd = app_commands.Group(name='cmd', description='Send commands to the Minecraft server.')

    @cmd.command(name='tellraw', description='Says something in the MC Server.')
    async def sub_command(self, ctx, content: str) -> None:
        command = f'/tellraw @a "{content}"'
        await send_rcon(command, ctx, True)

    @cmd.command(name='log', description='Logs your phrase to the Console.')
    async def sub_command(self, ctx, info: str):
        command = f'/logtellraw targetless "{info}"'
        await send_rcon(command, ctx, True)

    @cmd.command(name='mclogs', description='Sends a request to mclo.gs for the latest.log or a log you specify.')
    async def sub_command(self, ctx, log: Optional[str]):
        if log is None:
            file = ''
        else:
            file = f' share {log}'
        command = f'/mclogs{file}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='maintenance', description='Allows you to Toggle Maintenance.')
    async def sub_command(self, ctx, enabled: bool):
        if enabled is True:
            arg = ' on'
        else:
            arg = ' off'
        command = f'/maintenance{arg}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='ban', description='Bans the selected player from the server.')
    async def sub_command(self, ctx, player_user: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/ban {player_user}{reason1}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='tempban', description='Temporarily Bans the selected player from the server.')
    async def sub_command(self, ctx, player_user: str, duration: str, reason: Optional[str]):
        d_short_s = duration.replace("seconds", "s")
        d_short_m = d_short_s.replace("minutes", "m")
        d_short_d = d_short_m.replace("days", "d")
        d_short_w = d_short_d.replace("weeks", "w")
        d_short_ws = d_short_w.replace(" ", "")
        duration_v2 = d_short_ws
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        if re.match(vars.duregex, duration_v2):
            command = f'/tempban {player_user} {duration_v2}{reason1}'
            await send_rcon(command, ctx, True)
        else:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'<:warn:1249069667159638206> `{duration}` does not seem like a valid duration type even when corrected to `{duration_v2}` by our system!\n\n> <:info:1278823933717512232> A correct syntax would be: <number><either s, m, d or w> (e.g. 1w for 1 week.)\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed in e.g. a screenshot.\n-# {vars.botVersion}',
                                  title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed, ephemeral=True)

    @cmd.command(name='ban-ip', description='IP Bans the selected player from the server.')
    async def sub_command(self, ctx):
        embed = discord.Embed(colour=discord.Colour.red(),
                              description='<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in game.\n-# `Error Code 423`',
                              title='RCON: <:resources:1278835693900136532>')
        await ctx.response.send_message(embed=embed, ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /ban-ip.')

    @cmd.command(name='tempban-ip', description='IP Bans the selected player from the server.')
    async def sub_command(self, ctx):
        embed = discord.Embed(colour=discord.Colour.red(),
                              description='<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in game.\n-# `Error Code 423`',
                              title='RCON: <:resources:1278835693900136532>')
        await ctx.response.send_message(embed=embed, ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} sent /tempban-ip.')

    @cmd.command(name='unban', description='Unbans the selected player from the server.')
    async def sub_command(self, ctx, player_user: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/unban {player_user}{reason1}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='pardon', description='Pardons the selected player. THIS IS DIFFERENT FROM /UNBAN!')
    async def sub_command(self, ctx, player_user: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/pardon {player_user}{reason1}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='run', description='Runs any command you provide, given that it has correct syntax.')
    async def sub_command(self, ctx, command: str):
        mod_chat = ctx.guild.get_channel(vars.logChannel)
        if ctx.channel == mod_chat:
            await send_rcon(command, ctx, True)
        else:
            embed = discord.Embed(colour=discord.Colour.red(),
                                  description=f'<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in {mod_chat.mention}.\n-# `Error Code 421`',
                                  title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed, ephemeral=True)

    @cmd.command(name='clear', description='Clears the selected player\'s inventory.')
    async def sub_command(self, ctx, player: str, item: Optional[str]):
        if item is None:
            items = ''
        else:
            items = f' {item}'
        command = f'/clear {player}{items}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='list', description='Lists all the players online.')
    async def sub_command(self, ctx):
        command = '/list'
        await send_rcon(command, ctx, False)

    @cmd.command(name='restore', description='Restores the grave of a player\'s last death.')
    async def sub_command(self, ctx, player: str):
        command = f'/yigd restore {player}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='view-balance', description='Allows you to see someone\'s Nm. Balance.')
    async def sub_command(self, ctx, player: str):
        command = f'/nm view {player}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='tp-offline', description='Allows you to TP Someone who\'s offline.')
    async def sub_command(self, ctx, player: str, pos: str):
        command = f'/tp_offline {player} {pos}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='heal', description='Heals the selected player.')
    async def sub_command(self, ctx, player: str):
        command = f'/heal {player}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='whitelist-toggle', description='Toggle the whitelist on or off.')
    async def sub_command(self, ctx, enable: bool):
        if enable:
            command = f'/whitelist on'
        else:
            command = f'/whitelist off'
        await send_rcon(command, ctx, True)

    @cmd.command(name='whitelist-entry', description='Adds or removes a user to the whitelist.')
    async def sub_command(self, ctx, player: str, can_enter: bool):
        if can_enter:
            command = f'/whitelist add {player}'
        else:
            command = f'/whitelist remove {player}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='whitelist', description='Lists the Whitelist')
    async def sub_command(self, ctx):
        command = f'/whitelist list'
        await send_rcon(command, ctx, True)

    @cmd.command(name='damage', description='Damages the selected player.')
    async def sub_command(self, ctx, player: str, amount: float):
        command = f'/damage {player} {amount}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='ban-legacy', description='Uses Minecraft\'s ban system.')
    async def sub_command(self, ctx, player: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/minecraft:ban {player}{reason1}'
        await send_rcon(command, ctx, True)

    @cmd.command(name='unban-legacy', description='Uses Minecraft\'s ban system.')
    async def sub_command(self, ctx, player: str, reason: Optional[str]):
        if reason is None:
            reason1 = ''
        else:
            reason1 = f' {reason}'
        command = f'/minecraft:pardon {player}{reason1}'
        await send_rcon(command, ctx, True)


class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    status = app_commands.Group(name='status', description='Commands to send pregen embeds about stati.')

    @status.command(name='downtime', description='Pregen a Downtime Embed, should be used when the server is down.')
    async def sub_command(self, ctx, title: str, summary: Optional[str], impact: Optional[str],
                          channel: Optional[discord.TextChannel], ping: Optional[Union[discord.Member, discord.Role]]):
        status = f'{title}; DOWN'
        if await util.check_for_roles_status(ctx):
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.custom, state=status, name='CustomStatus'),
                status=discord.Status.online)
            if channel is None:
                channel = ctx.channel
            if summary is None:
                summary = 'No summary was provided.'
            if impact is None:
                impact = 'No impact.'
            if ping is None:
                ping = ' '
            else:
                ping = ping.mention
            description = f"""**Summary:**
{summary}

**Impact:**
{impact}"""
            embed = discord.Embed(title=f'Downtime - {title}', description=description,
                                  colour=discord.Colour.from_str('#fd5151'), timestamp=datetime.now())
            embed.set_footer(text='CordCraft',
                             icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
            message = await channel.send(embed=embed, content=ping)
            view = views.DeleteEmbed(message=message)
            await ctx.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                            view=view)
            info(f'[{util.time()}] >STATUS> {ctx.user.name} stated the server as DOWNTIME: {title}.')
        else:
            await ctx.response.send_message(f'You do not have the permissions to send this command.', ephemeral=True)

    @status.command(name='update',
                    description='Pregen a Downtime Update Embed, should be used when an update about a downtime can be given.')
    async def sub_command(self, ctx, title: str, summary: Optional[str], channel: Optional[discord.TextChannel],
                          ping: Optional[Union[discord.Member, discord.Role]]):
        status = f'{title}'
        if await util.check_for_roles_status(ctx):
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.custom, state=status, name='CustomStatus'),
                status=discord.Status.online)
            if channel is None:
                channel = ctx.channel
            if summary is None:
                summary = 'No summary was provided.'
            if ping is None:
                ping = ' '
            else:
                ping = ping.mention
            description = f"""**Summary:**
{summary}"""
            embed = discord.Embed(title=f'Downtime Update - {title}', description=description,
                                  colour=discord.Colour.from_str('#e2a915'), timestamp=datetime.now())
            embed.set_footer(text='CordCraft',
                             icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
            message = await channel.send(embed=embed, content=ping)
            view = views.DeleteEmbed(message=message)
            await ctx.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                            view=view)
            info(f'[{util.time()}] >STATUS> {ctx.user.name} stated a status update: {title}.')
        else:
            await ctx.response.send_message(f'You do not have the permissions to send this command.', ephemeral=True)

    @status.command(name='uptime',
                    description='Pregen a Downtime Update Embed, that\'s specifically for the service being back up.')
    async def sub_command(self, ctx, title: str, note: Optional[str], channel: Optional[discord.TextChannel],
                          ping: Optional[Union[discord.Member, discord.Role]]):
        if await util.check_for_roles_status(ctx):
            await self.bot.change_presence(activity=discord.Game('on CordCraft Season 2'), status=discord.Status.online)
            if channel is None:
                channel = ctx.channel
            if note is None:
                note = 'No extra note was provided.'
            if ping is None:
                ping = ' '
            else:
                ping = ping.mention
            description = f"""**Extra note:**
{note}"""
            embed = discord.Embed(title=f'Downtime Update - {title}', description=description,
                                  colour=discord.Colour.from_str('#2dc79c'), timestamp=datetime.now())
            embed.set_footer(text='CordCraft',
                             icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
            message = await channel.send(embed=embed, content=ping)
            view = views.DeleteEmbed(message=message)
            await ctx.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                            view=view)
            info(f'[{util.time()}] >STATUS> {ctx.user.name} stated the server as UP: {title}.')
        else:
            await ctx.response.send_message(f'You do not have the permissions to send this command.', ephemeral=True)

    @status.command(name='notice',
                    description='Pregen a Notice Embed.')
    async def sub_command(self, ctx, note: str, channel: Optional[discord.TextChannel],
                          ping: Optional[Union[discord.Member, discord.Role]]):
        if await util.check_for_roles_status(ctx):
            if channel is None:
                channel = ctx.channel
            if ping is None:
                ping = ' '
            else:
                ping = ping.mention
            description = f"""{note}"""
            embed = discord.Embed(title=f'Notice:', description=description, colour=discord.Colour.dark_gold(),
                                  timestamp=datetime.now())
            embed.set_footer(text='CordCraft',
                             icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
            message = await channel.send(embed=embed, content=ping)
            view = views.DeleteEmbed(message=message)
            await ctx.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                            view=view)
            info(f'[{util.time()}] >STATUS> {ctx.user.name} stated a NOTICE: {note}.')
        else:
            await ctx.response.send_message(f'You do not have the permissions to send this command.', ephemeral=True)

    @status.command(name='status', description='Change the Bot\'s status to say Minecraft Server Stati.')
    async def slash_command(self, ctx, status: str, reset: Optional[bool] = False, down: Optional[bool] = False):
        if down:
            status = f'{status}; DOWN'
        else:
            status = status
        if await util.check_for_roles_status(ctx):
            if reset is False:
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.custom, state=status, name='CustomStatus'),
                    status=discord.Status.online)
                await ctx.response.send_message('Attempted to change status.', ephemeral=True)
                info(f'[{util.time()}] >STATUS> {ctx.user.name} changed bot status: {status}.')
            else:
                await self.bot.change_presence(activity=discord.Game('on CordCraft Season 2'),
                                               status=discord.Status.online)
                await ctx.response.send_message('Attempted to reset status.', ephemeral=True)
                info(f'[{util.time()}] >STATUS> {ctx.user.name} reset the bot status.')
        else:
            await ctx.response.send_message(f'You do not have the permissions to send this command.', ephemeral=True)


class ThreadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    thread = app_commands.Group(name='thread', description='Commands for managing your thread.')

    @thread.command(name='pin', description='Pin or unpin a message in your thread, given you have permission.')
    async def sub_command(self, ctx, message_id: str):
        message = await ctx.channel.fetch_message(int(message_id))
        channel = ctx.channel
        perms = channel.permissions_for(ctx.user)
        if channel.owner is not ctx.user and not perms.manage_messages:
            await ctx.response.send_message(content='You do not have the permissions to send this command.',
                                            ephemeral=True)
        else:
            if not message.pinned:
                await message.pin(reason=f'{ctx.user.mention} pinned a message in their thread, {ctx.channel.mention}.')
                info(f'[{util.time()}] >LOG> {ctx.user.name} pinned a message in their thread.')
            else:
                await message.unpin(
                    reason=f'{ctx.user.mention} unpinned a message in their thread, {ctx.channel.mention}.')
                info(f'[{util.time()}] >LOG> {ctx.user.name} unpinned a message in their thread.')

    @thread.command(name='lock', description='Lock or unlock your thread, given you have permission.')
    async def sub_command(self, ctx, thread: Optional[discord.Thread]):
        if thread is None:
            thread = ctx.channel
        perms = thread.permissions_for(ctx.user)
        if thread.owner is not ctx.user and not perms.manage_threads:
            await ctx.response.send_message(content='You do not have the permissions to send this command.',
                                            ephemeral=True)
        else:
            if not thread.locked:
                await thread.edit(locked=True, reason=f'{ctx.user.mention} locked their thread, {thread.mention}.')
                info(f'[{util.time()}] >LOG> {ctx.user.name} locked their thread.')
            else:
                await thread.edit(locked=True, reason=f'{ctx.user.mention} unlocked their thread, {thread.mention}.')
                info(f'[{util.time()}] >LOG> {ctx.user.name} unlocked their thread.')

    @thread.command(name='delete', description='Deletes your thread, given you have permission.')
    async def sub_command(self, ctx, thread: Optional[discord.Thread]):
        if thread is None:
            thread = ctx.channel
        perms = thread.permissions_for(ctx.user)
        if thread.owner is not ctx.user and not perms.manage_threads:
            await ctx.response.send_message(content='You do not have the permissions to send this command.',
                                            ephemeral=True)
        else:
            embed = discord.Embed(title='Warning:', colour=discord.Colour.brand_red(),
                                  description=f'You are about to fully delete {thread.mention}, are you sure?\nNote that this action is IRREVERSIBLE!')
            view = views.ConfirmDeleteThreadButton(thread=thread)
            await ctx.response.send_message(embed=embed, view=view)

    @thread.command(name='info', description='Displays info about the Thread.')
    async def sub_command(self, ctx, thread: Optional[discord.Thread]):
        if thread is None:
            thread = ctx.channel

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
        await ctx.response.send_message(embed=embed, ephemeral=True)
        info(f'[{util.time()}] >LOG> {ctx.user.name} viewed info about {thread.name}.')


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moderation = app_commands.Group(name='moderation', description='Moderation commands.')

    @moderation.command(name='ban', description='Bans a user.')
    @discord.app_commands.checks.has_permissions(ban_members=True)
    async def sub_command(self, ctx, offender: discord.Member, reason: Optional[str] = 'No reason given',
                          time: Optional[str] = 'infinite', delete_messages: Optional[bool] = False,
                          silent: Optional[bool] = False):
        offender_dm = await offender.create_dm()
        reason_for_audit = f'{ctx.user.mention}: {reason}.'
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

            database.add_temp_ban(offender.id, ctx.guild.id, unban_time.isoformat(), reason)
            time_str = f"until {unban_time.strftime('%Y-%m-%d %H:%M%S')}"
        else:
            time_str = "indefinitely"

        await offender_dm.send(content=f'''Hi. Unfortunately I am here to inform you that you have been banned from GunjiCordia.
The reason for your ban was: **{reason}**.
You are banned **{time_str}**.
The moderator responsible for your ban was {ctx.user.mention}.

If you think this ban was not rightful, or an actual accident feel free to contact said, or a different moderator.
I wish you a great day further!''')

        await offender.ban(reason=reason_for_audit, delete_message_days=del_days)
        embed = discord.Embed(
            description=f'{offender.mention} was banned from the server {time_str}. <:red:1301608135370473532>',
            colour=discord.Colour.red())
        await ctx.response.send_message(embed=embed, ephemeral=silent)

    @moderation.command(name='kick', description='Kicks a user.')
    @discord.app_commands.checks.has_permissions(kick_members=True)
    async def sub_command(self, ctx, offender: discord.Member, reason: Optional[str] = 'No reason given',
                          silent: Optional[bool] = False):
        offender_dm = await offender.create_dm()
        reason_for_audit = f'{ctx.user.mention}: {reason}.'
        await offender_dm.send(f'''Hi. I am here to inform you that you have been kicked from GunjiCordia.
The reason for your kick was: `{reason}`.
The moderator responsible for your kick was {ctx.user.mention}.

If you wish to join back, here is the Discord Invite Link: {vars.guildInviteLink}
I wish you a great day further!''')
        await offender.kick(reason=reason_for_audit)
        embed = discord.Embed(description=f'{offender.mention} was kicked from the server. <:red:1301608135370473532>',
                              colour=discord.Colour.red())
        await ctx.response.send_message(embed=embed, ephemeral=silent)

    @moderation.command(name='timeout', description='Times out a user.')
    @discord.app_commands.checks.has_permissions(mute_members=True)
    async def sub_command(self, ctx, offender: discord.Member, duration: str,
                          reason: Optional[str] = 'No reason given', silent: Optional[bool] = False):
        dur = util.format_duration(duration)
        dur_int = util.from_formatted_get_int(dur)
        dur_str = util.from_formatted_get_str(dur)
        dur_days = util.get_duration_in_days(dur_str, dur_int)
        reason = f'{ctx.user.mention}: {reason}.'
        invalid = False
        handled = False

        if dur_days > 28 or dur_days == 0 and not invalid:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> `{duration}`, even when automatically corrected to `{dur}` by our system, is an invalid duration length!\n\n> <:info:1278823933717512232> Note: The technical limit is 28 days.\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed.\n-# {vars.botVersion} | {dur}:{dur_int}:{dur_str}:{dur_days}',
                colour=discord.Colour.red())
            await ctx.response.send_message(embed=embed, ephemeral=True)
            invalid = True
            handled = True
        if dur_str != 's' and dur_str != 'm' and dur_str != 'h' and dur_str != 'd' and dur_str != 'w' and not invalid:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> `{duration}` does not seem like a valid duration even when automatically corrected to `{dur}` by our system!\n\n> <:info:1278823933717512232> A correct format would be: e.g. 1w, 1 week, 6 days, 2h.\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed.\n-# {vars.botVersion} | {dur}:{dur_int}:{dur_str}:{dur_days}',
                colour=discord.Colour.red())
            await ctx.response.send_message(embed=embed, ephemeral=True)
            invalid = True
            handled = True

        if 's' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} second(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(seconds=dur_int), reason=reason)
            await ctx.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'm' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} minutes(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(minutes=dur_int), reason=reason)
            await ctx.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'h' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} hours(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(hours=dur_int), reason=reason)
            await ctx.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'd' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} days(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(days=dur_int), reason=reason)
            await ctx.response.send_message(embed=embed, ephemeral=silent)
            invalid = False
            handled = True
        if 'w' == dur_str and not invalid and not handled:
            embed = discord.Embed(
                description=f'{offender.mention} was timed out for {dur_int} week(s). <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await offender.timeout(timedelta(weeks=dur_int), reason=reason)
            await ctx.response.send_message(embed=embed, ephemeral=silent)

    @moderation.command(name='lock', description='Lock or unlock the channel.')
    @discord.app_commands.checks.has_permissions(mute_members=True)
    async def sub_command(self, ctx, silent: Optional[bool] = False):
        channel = ctx.channel
        if channel.type != discord.ChannelType.text:
            embed = discord.Embed(
                description=f'<:warn:1249069667159638206> {channel.mention} is not a valid text channel!',
                colour=discord.Colour.red())
            await ctx.response.send_message(embed=embed, ephemeral=True)
        if channel.overwrites_for(ctx.guild.default_role).send_messages is False:
            embed = discord.Embed(
                description=f'{channel.mention} was unlocked by {ctx.user.mention}. <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await channel.set_permissions(ctx.guild.default_role,
                                          overwrite=discord.PermissionOverwrite(send_messages=True))
            await ctx.response.send_message(embed=embed, ephemeral=silent)
        else:
            embed = discord.Embed(
                description=f'{channel.mention} was locked by {ctx.user.mention}. <:blue:1301608132195258368>',
                colour=discord.Colour.blue())
            await channel.set_permissions(ctx.guild.default_role,
                                          overwrite=discord.PermissionOverwrite(send_messages=False))
            await ctx.response.send_message(embed=embed, ephemeral=silent)

import discord
import datetime
import time
import os
import psutil
import re
import aiohttp
import logging
from mcrcon import MCRcon
from decancer_py import parse, CuredString
from datetime import date
from datetime import timedelta
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
from typing import Optional, Union

load_dotenv()
description1 = '''This is a Bot made by Tywrap Studios for the GunjiCordia Discord server to help people and others 
in the wonderful server that is Gunji's that he crafted back in july of 2023'''
# Intents Configurment
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
intents.auto_moderation = True
intents.auto_moderation_configuration = True
intents.auto_moderation_execution = True
# Minecraft server RCON
rcon_pass = os.getenv('RCONPASSWORD')
rcon_host = os.getenv('RCONHOST')
rcon_port = int(os.getenv('RCONPORT'))
rcon_logger_webhook_url = os.getenv('RCONLOGGERWEBHOOK')
mcrcon_client = MCRcon(host=rcon_host,password=rcon_pass,port=rcon_port)
# Webhooks
sanitization_webhook_url = os.getenv('SANLOGGERWEBHOOK')
# Clients
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='??', description=description1, intents=intents)
# Logger
log_filepath = os.getenv('WINDOWSLOGFILEPATH')
log_handler = logging.FileHandler(filename=log_filepath,encoding='utf-8',mode='w')
log_level = logging.DEBUG
# Bot Stuff
bottoken = os.getenv("EXHOTOKENS")
botid = '1213859965836595260'
botping = f'<@{botid}>'
botversion = 'CordCrafter 1.6.0 [EXPERIMENTAL]'
botname = 'CordTester'
# Links
guildinvitelink = os.getenv("CORDINVITELINK")
privacy_notion = 'https://trusted-substance-f20.notion.site/CordCrafter-bot-Privacy-Notice-7d02fae4b3d64db4b90206b3d92fd9de'
# Regex Patterns
repat = '(^!|^\.|^\?)'
repatce = '(!|\.|\?)'
duregex = '^\d+\w*[smdw]$'
# Tags
trusted_team_tag_id = 1287526517248622592 #1287179981843206144
# Channels
roleschannel = '<#1189339256016093345>'
ipchannel = '<#1238669922641510502>'
techsupportchannel = '<#1188157890117242952>'
logchannel = 1248374509778632744 #1191085319102140528
ticketcategory = 1256762776035000401 #1165265825196945449
ticketlog = 1248374509778632744 #1164581289022722148
spam = 1273087934198976592 #1139925935093727292
team_forum = 1287526462215426170 #1287178984530120715
ctd_channel = 1273087934198976592 #1219383524289941505
# Roles
resigned = 1268338910300475393 #1265790384336801964
discordadmin = 1248639531318513835 #1160004558609731644
minecraftadmin = 1248646236475625535 #1191088046695792720
centralhosting = 1300072430341197955 #1272562661451632702
gunjicord = 1300072489489268747 #1139926170905886853
# Stats
cpustat = psutil.cpu_percent(5)
actualram = psutil.virtual_memory()[3]/1000000
roundedram = round(actualram)
if actualram == 0 or actualram < 0:
    ram = 'Stat fetched under or is 0. Error 1.'
else:
    ram = f'{roundedram}MB'
# File Paths
red_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078349477838899/red_mod_badge.png?ex=6665fe5d&is=6664acdd&hm=832fb33a6ed5fe76ecc7539e56842a526cf3309fc189e59e73b6bb78400eb441&'
green_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078327872852071/green_mod_badge.png?ex=6665fe58&is=6664acd8&hm=d0713da6a04831a28b89db4cfba93cd21a196fe9716dafeb0daa367fb4603d6d&'
blue_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078338484568124/Ongetiteld.png?ex=6665fe5a&is=6664acda&hm=157173744c4ec4e8075d2386b3543419319bda26ae8f21bbdffa60c4d63cae2e&'
red_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085071508639894/red_mc_mod_badge.png?ex=6666049f&is=6664b31f&hm=d9c745c2bf2f872df1cd1b977b42f3408ed46d262e00e5dc58aa9fb7c2a7e54d&'
green_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085058682458173/green_mc_mod_badge.png?ex=6666049c&is=6664b31c&hm=f8767eed24c7c5565014dd8930141c0b3061611bf63a7a727ba5b4d6938540f9&'

# TRY TO ONLY COMMIT THESE UNDERNEATH CHANGES:
@bot.event
async def on_ready():
    print('----------------------------------------------------------------------------')
    print(f'Logged in as {bot.user} (ID: {botid})')
    print('----------------------------------------------------------------------------')
    print('''   ____              _  ____            __ _                _        __          ___  
  / ___|___  _ __ __| |/ ___|_ __ __ _ / _| |_ ___ _ __    / |      / /_        / _ \ 
 | |   / _ \| '__/ _` | |   | '__/ _` | |_| __/ _ \ '__|   | |     | '_ \      | | | |
 | |__| (_) | | | (_| | |___| | | (_| |  _| ||  __/ |      | |  _  | (_) |  _  | |_| |
  \____\___/|_|  \__,_|\____|_|  \__,_|_|  \__\___|_|      |_| (_)  \___/  (_)  \___/ ''')
    print('----------------------------------------------------------------------------')
    print('Setting Discord Bot Status. . .')
    await bot.change_presence(activity=discord.Game('on CordCraft Season 2.'), status=discord.Status.online)
    print(f'Set Discord Bot Status.')
    print(f'Starting Tasks. . .')
    task_loop.start()
    print(f'Tasks Started.')
    print('Starting Uptime Timer. . .')
    global startTime
    startTime = time.time()
    print('Timer Started.')
    print('Adding onto Bot Tree. . .')
    bot.tree.add_command(claim)
    print('Added claim')
    bot.tree.add_command(notes)
    print('Added notes')
    bot.tree.add_command(cmd)
    print('Added cmd')
    bot.tree.add_command(status)
    print('Added status')
    bot.tree.add_command(thread)
    print('Added thread')
    print(f'Added everything to Bot Tree.')
    print('----------------------------------------------------------------------------')
    print('''Intents set:
    intents.auto_moderation✅
    intents.auto_moderation_configuration✅
    intents.auto_moderation_execution✅
    intents.dm_messages❌
    intents.dm_reactions❌
    intents.dm_typing✅
    intents.emojis_and_stickers❌
    intents.guild_messages❌
    intents.guild_reactions❌
    intents.guild_scheduled_events❌
    intents.guild_typing❌
    intents.guilds❌
    intents.integrations❌
    intents.invites❌
    intents.members✅
    intents.message_content✅
    intents.moderation❌
    intents.presences❌
    intents.voice_states❌
    intents.webhooks❌''')
    print('----------------------------------------------------------------------------')
    print('')
    print('')
        
@bot.command()
async def sync(ctx:commands.Context):
    tywrap = ctx.guild.get_member(1041430503389155492)
    try:
        if ctx.author == tywrap:
            print('Syncing Bot Tree')
            await bot.tree.sync()
            print('Synced Bot Tree')
        else:
            print('No perm to sync Bot Tree')
    except:
        print('someting wen wron')

@bot.tree.command(name='ip-joining', description='Tells the person you specify how to join the server.')
async def slash_command(ctx: discord.Interaction, member: discord.Member) -> None:
    await ctx.response.send_message(f'''Hey, <@{member.id}>!
Are you wondering how to join? The server IP alongside the Modpack Link and the Rules are all located in
- {ipchannel}.
And hey, if you're there already, why not read the rules?

> ## For the future: Please use your eyes, not your mouth.
> ~ Sincerely, the entire admin team cuz this question is asked too much. /hj''')

@bot.tree.command(name='ping', description='See how slow/fast the Bot\'s reaction time (ping) is.')
async def slash_command(ctx: discord.Interaction) -> None:
    latency = round(bot.latency * 1000)
    if latency > 200 or latency == 200:
        latency_val = f'`{latency}ms` <:con_bad:1278830871532802089>'
    else:
        if latency > 100 or latency == 100:
            latency_val = f'`{latency}ms` <:con_mediocre:1278830874074546199>'
        else: 
            if latency < 100:
                latency_val = f'`{latency}ms` <:con_excellent:1278830872929501286>'
    embed = discord.Embed(description=f'## Pong! {latency_val}',colour=discord.Colour.from_rgb(70,230,210))
    embed.set_footer(text='Want to see more? Use /stats!',)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="bean",description="Beans the member. Yep. That's all it does.")
async def slash_command(ctx:discord.Interaction, member: discord.Member):
    embed = discord.Embed(title='Member Beaned',description=f'Member: {member.mention},\nResponsible "moderator": {ctx.user.mention}',colour=discord.Colour.og_blurple())
    await ctx.response.send_message(embed=embed)

class FormButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(discord.ui.Button(label='Form',url='https://forms.gle/dLYLvfWkZXh5JLQM7',style=discord.ButtonStyle.gray))

@bot.tree.command(name='stats', description='Displays the Bot\'s statistics.')
async def slash_command(ctx: discord.Interaction) -> None:
    uptime = str(timedelta(seconds=int(round(time.time()-startTime))))
    latency = round(bot.latency * 1000)
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
    guild_age_secs = time.time()-ctx.guild.created_at.timestamp()
    guild_age = round(guild_age_secs/86400)
    bot_member = ctx.guild.get_member_named(botname)
    bot_status_game = bot_member.activity.name
    bot_status_raw = bot_member.activity
    if 'on CordCraft' in bot_status_game:
        bot_status = f'**The server is online and stable.** <a:stable:1278830944932855911>'
    else:
        if '; DOWN' in bot_status_raw.state:
            message = bot_status_raw.state.replace('; DOWN','')
            bot_status = f'**The server is currently __down__.** <a:down:1278830877396172840>\n<:arrow_under:1278834153655107646>**Message:** {message}'
        else:
            bot_status = f'**There might be a slight complication.** <a:unstable:1278830948120789064>\n<:arrow_under:1278834153655107646>**Message:** {bot_status_raw.state}'
    statusembed = discord.Embed(colour=discord.Colour.from_rgb(70,230,210),title='CordCrafter Status.',description=f'''----------------------------
<:space:1251655233919123628><:speed:1251649973418983565> **Latency:** {latency_val}
<:space:1251655233919123628><:uptime:1251648456301346946> **Uptime:** `{uptime}`
<:space:1251655233919123628><:info:1278823933717512232> **Bot Ver:** `{botversion}`
<:space:1251655233919123628><:resources:1278835693900136532> **Resource Usage:**
<:space:1251655233919123628><:arrow_under:1278834153655107646><:ram:1251659281384738857> RAM: `{ram}`
<:space:1251655233919123628><:arrow_under:1278834153655107646><:cpu_load:1251684895038902324> CPU: `{cpustat}%`
<:space:1251655233919123628><:servericon:1251671285277130753> **Server:**
<:space:1251655233919123628><:space:1251655233919123628><:party:1278816948846596157> Members:
<:space:1251655233919123628><:space:1251655233919123628><:arrow_under:1278834153655107646><:member:1278834558485397624>`{member_count}`;
<:space:1251655233919123628><:space:1251655233919123628><:arrow_under:1278834153655107646><:bot:1278833876961198120>`{bot_count}`
<:space:1251655233919123628><:space:1251655233919123628>⏰ Age: `{guild_age}`
----------------------------
**<:minecraft_logo:1278852452396826634> MC-Server Status:**
<:arrow_under:1278834153655107646>{bot_status}
''')
    await ctx.response.send_message(embed=statusembed)

class ConfirmButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Confirm',style=discord.ButtonStyle.green,emoji='✅')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        ticketlogchannel = ctx.guild.get_channel(ticketlog)
        mcadminrole = ctx.guild.get_role(minecraftadmin)
        if mcadminrole in ctx.user.roles:
            isadmin = '<:arrow_under:1278834153655107646> **__This User is a Minecraft Admin.__**'
        else:
            isadmin = ''
        opname = ctx.channel.name.replace('ban-appeal-','')
        op = ctx.guild.get_member_named(opname)
        closer = ctx.user
        embed = discord.Embed(title='Ban Appeal Closed',description=f'''
<:id:1279190510027800709> **Ticket Opened by:**
<:asterix:1279190506777088000> {op.mention}

<:leave:1279190513190178826> **Ticket Closed by:**
<:asterix:1279190506777088000> {closer.mention}
{isadmin}
''',colour=discord.Colour.green())
        time = datetime.now().strftime('%H:%M')
        datetoday = date.today().strftime('%d/%m/%Y')
        embed.set_footer(text=f'{datetoday} {time}')
        await ctx.channel.delete(reason=f'Closed ticket {ctx.channel.mention}')
        await ticketlogchannel.send(embed=embed)

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Close',style=discord.ButtonStyle.danger,emoji='🔒')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        embed = discord.Embed(title='Confirm',description='Please confirm that you want to close your Ban Appeal Ticket.',colour=discord.Colour.green())
        view = ConfirmButton()
        await ctx.response.send_message(embed=embed,view=view,ephemeral=True)
        
class ManualAppealButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Open MC Ban Appeal',style=discord.ButtonStyle.blurple,emoji='📫')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                ctx.user: discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True,attach_files=True,embed_links=True),
                ctx.guild.me: discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True)
        }
        allowedrole = ctx.guild.get_role(minecraftadmin)
        category = ctx.guild.get_channel(ticketcategory)
        view = CloseTicketButton()
        channel = await ctx.guild.create_text_channel(name=f'ban-appeal-{ctx.user.name}',overwrites=overwrites,reason=f'Made Ban appeal ticket for {ctx.user}',category=category,topic=f'{ctx.user.id}')
        await channel.set_permissions(target=allowedrole,view_channel=True,send_messages=True,read_message_history=True,attach_files=True,embed_links=True)
        embed = discord.Embed(description='Thanks for opening a ban appeal ticket.\nPlease stay calm and civil while discussing your ban with our admin staff.',colour=discord.Colour.green())
        embed.set_footer(text=f'*This appeal was manually triggered using the command!*')
        ping = await channel.send(f'<@&{minecraftadmin}>')
        await ping.delete()
        await channel.send(embed=embed,view=view)
        await ctx.response.send_message(content=f'Thanks {ctx.user.mention}, I made {channel.mention} for you!',ephemeral=True)

class RemoveButton(discord.ui.View):        
    def __init__(
        self,
        *,
        member: discord.Member
    ): 
        self.member: discord.Member = member
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Remove User.',style=discord.ButtonStyle.danger)
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        if "ban-appeal-" in ctx.channel.name:
            emember = self.member
            await ctx.channel.set_permissions(emember, overwrite = None)
            embed = discord.Embed(title='Member Remove',description=f"{emember.mention} has been removed from the ticket by {ctx.user.mention}.",colour=discord.Colour.dark_gray())
            await ctx.response.send_message(embed=embed)
        else: await ctx.response.send_message("This isn't a ticket!", ephemeral = True)
            

@bot.tree.command(name='setup',description='Sets up the Bot\'s Ban Appeal Function.')
@discord.app_commands.checks.has_permissions(administrator=True)
async def slash_command(ctx:discord.Interaction,channel:discord.TextChannel):
    embed = discord.Embed(colour=discord.Colour.from_rgb(230,230,60),title='**Appeal a Minecraft Unban.**',description='By using the command **/appeal**, a Private Channel can be made for your Appeal.')
    await channel.send(embed=embed,content='Opening a ban appeal or ticket will ping the `@Minecraft Admin` role, so please do NOT ping them again in the ticket yourself!\nThanks in advance!')
    await ctx.response.send_message(content=f'Setup Completed in {channel.mention}.\nMake sure to delete any leftovers.',ephemeral=True)
    
@bot.tree.command(name='appeal',description='Manually appeals a Minecraft Ban Appeal ticket.')
async def slash_command(ctx:discord.Interaction):
    view = ManualAppealButton()
    embed = discord.Embed(colour=discord.Colour.from_rgb(230,230,60),title='**Appeal a Minecraft Unban.**',description='By clicking the button below, a Private Channel will be made for your Appeal.')
    await ctx.response.send_message(view=view,embed=embed,ephemeral=True)
    
@bot.tree.command(name='add',description='Adds a user to the current ticket.')
async def slash_command(ctx:discord.Interaction,member:discord.Member):
    if "ban-appeal-" in ctx.channel.name and member != ctx.user:
        await ctx.channel.set_permissions(member, view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        view = RemoveButton(member=member)
        ping = await ctx.channel.send(f'{member.mention}')
        await ping.delete()
        embed = discord.Embed(title='Member Add',description=f"{member.mention} has been added to the ticket by {ctx.user.mention}.",colour=discord.Colour.dark_gray())
        await ctx.response.send_message(embed=embed,view=view)
    else: 
        if "ban-appeal-" not in ctx.channel.name:
            await ctx.response.send_message("This isn't a ticket!", ephemeral = True)
        else: 
            if member == ctx.user:
                await ctx.response.send_message("You can't add or remove yourself!", ephemeral = True)
    
@bot.tree.command(name='remove',description='Removes a user from the current ticket.')
async def slash_command(ctx:discord.Interaction,member:discord.Member):
    if "ban-appeal-" in ctx.channel.name and member != ctx.user:
        await ctx.channel.set_permissions(member, overwrite = None)
        embed = discord.Embed(title='Member Remove',description=f"{member.mention} has been removed from the ticket by {ctx.user.mention}.",colour=discord.Colour.dark_gray())
        await ctx.response.send_message(embed=embed)
    else: 
        if "ban-appeal-" not in ctx.channel.name:
            await ctx.response.send_message("This isn't a ticket!", ephemeral = True)
        else: 
            if member == ctx.user:
                await ctx.response.send_message("You can't add or remove yourself!", ephemeral = True)
                
@bot.tree.command(name='close',description='Closes the ticket.')
async def slash_command(ctx:discord.Interaction):
    embed = discord.Embed(title='Confirm',description='Please confirm that you want to close your Ban Appeal Ticket.',colour=discord.Colour.green())
    view = ConfirmButton()
    await ctx.response.send_message(embed=embed,view=view,ephemeral=True)
                
@bot.tree.command(name='forceclose',description='Forcefully closes the selected ticket.')
async def slash_command(ctx:discord.Interaction,ticket:discord.TextChannel):
    allowedrole1 = ctx.guild.get_role(discordadmin)
    allowedrole2 = ctx.guild.get_role(minecraftadmin)
    if allowedrole1 in ctx.user.roles or allowedrole2 in ctx.user.roles:
        if "ban-appeal-" in ticket.name:
            ticketlogchannel = ctx.guild.get_channel(1164581289022722148)
            opname = ticket.name.replace('ban-appeal-','')
            op = ctx.guild.get_member_named(opname)
            closer = ctx.user
            embed = discord.Embed(title='Ban Appeal Closed',description=f'''
<:id:1279190510027800709> **Ticket Opened by:**
<:asterix:1279190506777088000> {op.mention}

<:leave:1279190513190178826> **Ticket Closed by:**
<:asterix:1279190506777088000> {closer.mention}
<:arrow_under:1278834153655107646> **__This ticket was Force Closed__**
''',colour=discord.Colour.green())
            time = datetime.now().strftime('%H:%M')
            datetoday = date.today().strftime('%d/%m/%Y')
            embed.set_footer(text=f'{datetoday} {time}')
            await ticket.delete(reason=f'{ctx.user} wanted to force close {ticket}')
            await ticketlogchannel.send(embed=embed)
            await ctx.response.send_message(f'Force closed {ticket.mention}',ephemeral=True)
        else: 
            if "ban-appeal-" not in ticket.name:
                await ctx.response.send_message("That TextChannel isn't a ticket!", ephemeral = True)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)
        
@bot.tree.command(name='resign',description='Resigns the Minecraft member you chose.')
async def slash_command(ctx:discord.Interaction,admin:discord.Member):
    tywrap = ctx.guild.get_member(1041430503389155492)
    oldrole = ctx.guild.get_role(minecraftadmin)
    newrole = ctx.guild.get_role(resigned)
    if ctx.user == tywrap:
        if oldrole in admin.roles and newrole not in admin.roles:
            await admin.remove_roles(oldrole, reason='Resigning Minecraft Admin...')
            await admin.add_roles(newrole, reason='Resigning Minecraft Admin...')
            await ctx.response.send_message(f'Successfully resigned {admin.mention} from the Admin team.\nDon\'t forget to /deop them!',ephemeral=True)
        else: 
            if oldrole not in admin.roles and newrole not in admin.roles:
                await ctx.response.send_message(f'Could not resign Admin {admin.mention}. \nReason: Could not find {oldrole.mention} role in User roles.',ephemeral=True)
            if oldrole not in admin.roles and newrole in admin.roles:
                await ctx.response.send_message(f'Could not resign Admin {admin.mention}. \nReason: User is already resigned.',ephemeral=True)
            if oldrole in admin.roles and newrole in admin.roles:
                await ctx.response.send_message(f'Something went wrong while assigning and resigning roles.\nPlease manually re-check {admin.mention}\'s roles',ephemeral=True)
    else:
        await ctx.response.send_message('You do not have the permission to send this command.',ephemeral=True)

@bot.tree.command(name='say',description='Says stuff as the bot')
@discord.app_commands.checks.has_permissions(administrator=True)
async def slash_command(ctx:discord.Interaction,text:str,reference:Optional[str]):
    if reference is not None:
        referenceint = int(reference)
        referencem = await ctx.channel.fetch_message(referenceint)
        await referencem.reply(text)
        await ctx.response.send_message(content=f'Sent {text}',ephemeral=True)
    else:
        await ctx.channel.send(content=text)
        await ctx.response.send_message(content=f'Sent {text}',ephemeral=True)

@bot.tree.context_menu(name='Sanitize & Dehoist')
@discord.app_commands.checks.has_permissions(manage_nicknames=True)
async def context(ctx:discord.Interaction,member:discord.Member):
    nick = member.display_name
    if re.match(repat,nick):
        wetname = re.sub(repatce,'',nick)
        if len(wetname) < 1:
            wetname = 'Robin'
        cleanname_cs: CuredString = parse(wetname,retain_capitalization=True,retain_emojis=True)
        cleanname = f'{cleanname_cs}'
        await member.edit(nick=cleanname)
        await send_webhook(sanitization_webhook_url,f'Changed nick from **{nick}** to **{cleanname}**.','Nick Change:')
        if member.display_name == 'Robin':
            embed = discord.Embed(colour=discord.Colour.green(),description=f'Changed `{nick}` to placeholder `Robin`.')
            await ctx.response.send_message(embed=embed,ephemeral=True)
        else:
            embed = discord.Embed(colour=discord.Colour.green(),description=f'Changed `{nick}` to `{cleanname}`.')
            await ctx.response.send_message(embed=embed,ephemeral=True)
    else:
        wetname = nick
        cleanname_cs: CuredString = parse(wetname,retain_capitalization=True,retain_emojis=True)
        cleanname = f'{cleanname_cs}'
        if cleanname != nick:
            await member.edit(nick=cleanname)
            await send_webhook(sanitization_webhook_url,f'Changed nick from **{nick}** to **{cleanname}**.','Nick Change:')
            embed = discord.Embed(colour=discord.Colour.green(),description=f'Changed `{nick}` to `{cleanname}`.')
            await ctx.response.send_message(embed=embed,ephemeral=True)
        else:
            view = ShowDebugButton(nick=nick)
            embed = discord.Embed(colour=discord.Colour.red(),description=f'"`{nick}`" seems fine and is not cancerous or intentionally hoisted.\nIf you think it is, please make a [GitHub Issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and send the Debug Info.')
            await ctx.response.send_message(embed=embed,ephemeral=True,view=view)
        
@bot.tree.command(name='sanitize',description='Sanitizes and Dehoists the member\'s Nick using Regex Patterns.')
@discord.app_commands.checks.has_permissions(manage_nicknames=True)
async def context(ctx:discord.Interaction,member:discord.Member):
    nick = member.display_name
    if re.match(repat,nick):
        wetname = re.sub(repatce,'',nick)
        if len(wetname) < 1:
            wetname = 'Robin'
        cleanname_cs: CuredString = parse(wetname,retain_capitalization=True,retain_emojis=True)
        cleanname = f'{cleanname_cs}'
        await member.edit(nick=cleanname)
        await send_webhook(sanitization_webhook_url,f'Changed nick from **{nick}** to **{cleanname}**.','Nick Change:')
        if member.display_name == 'Robin':
            embed = discord.Embed(colour=discord.Colour.green(),description=f'Changed `{nick}` to placeholder `Robin`.',ephemeral=True)
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.green(),description=f'Changed `{nick}` to `{cleanname}`.',ephemeral=True)
            await ctx.response.send_message(embed=embed)
    else:
        wetname = nick
        cleanname_cs: CuredString = parse(wetname,retain_capitalization=True,retain_emojis=True)
        cleanname = f'{cleanname_cs}'
        if cleanname != nick:
            await member.edit(nick=cleanname)
            await send_webhook(sanitization_webhook_url,f'Changed nick from **{nick}** to **{cleanname}**.','Nick Change:')
            embed = discord.Embed(colour=discord.Colour.green(),description=f'Changed `{nick}` to `{cleanname}`.',ephemeral=True)
            await ctx.response.send_message(embed=embed)
        else:
            view = ShowDebugButton(nick=nick)
            embed = discord.Embed(colour=discord.Colour.red(),description=f'"`{nick}`" seems fine and is not cancerous or intentionally hoisted.\nIf you think it is, please make a [GitHub Issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and send the Debug Info.')
            await ctx.response.send_message(embed=embed,ephemeral=True,view=view)

class ShowDebugButton(discord.ui.View):
    def __init__(
        self,
        *,
        nick: str
    ):
        self.nick: str = nick
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Show Debug Info',style=discord.ButtonStyle.gray,emoji='☑️')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        attempted_nick = self.nick
        embed = discord.Embed(colour=discord.Colour.dark_embed(),title='__Debug Info__',description=f'''
```
Current Regex Pattern:
{repat}
```
```
Current Decancering Software:
decancer-py 0.4.0
```
```
Nick trying to Sanitize:
{attempted_nick}
```
```
Patch:
{botversion}
```
''')
        await ctx.response.send_message(embed=embed,ephemeral=True)

@bot.event
async def on_member_join(member:discord.Member):
    nick = member.display_name
    if re.match(repat,nick):
        wetname = re.sub(repatce,'',nick)
        if len(wetname) < 1:
            wetname = 'Robin'
        cleanname_cs: CuredString = parse(wetname,retain_capitalization=True,retain_emojis=True)
        cleanname = f'{cleanname_cs}'
        await member.edit(nick=cleanname)
        await send_webhook(sanitization_webhook_url,f'Changed nick from **{nick}** to **{cleanname}**.','Nick Change:')
    else:
        wetname = nick
        cleanname_cs: CuredString = parse(wetname,retain_capitalization=True,retain_emojis=True)
        cleanname = f'{cleanname_cs}'
        if cleanname != nick:
            await member.edit(nick=cleanname)
            await send_webhook(sanitization_webhook_url,f'Changed nick from **{nick}** to **{cleanname}**.','Nick Change:')
    dm = await member.create_dm()
    
    wembed = discord.Embed(colour=discord.Colour.yellow(),title='Welcome!',description=f'''Welcome to GunjiCordia!
We hope you're going to have a great time here!
If you ever get stuck, feel free to use my commands that have straightforward names to get around and about to learn how things go around here.

Before you can fully Join our community, though, I am going to quickly look at your profile and make necessary changes if they're needed.
                           
Alongside that, by joining our server you agree to MY (so the bot's) [Privacy Police](<{privacy_notion}>)
''')
    await dm.send(embed=wembed)
    endbed = discord.Embed(colour=discord.Colour.yellow(),title='That\'s all!',description='''Have fun!
                           
Something wrong with the bot's behaviour or profile changes?
Report any issues to the [GitHub Issue Tracker](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>).
''')
    await dm.send(embed=endbed)

async def send_webhook(url: str, content: str, title: str) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(url, session=session)
        embed = discord.Embed(colour=discord.Colour.blurple(),description=content,title=title)
        time = datetime.now().strftime('%H:%M:%S')
        datetoday = date.today().strftime('%d/%m/%Y')
        embed.set_footer(text=f'On {datetoday} at {time}')
        await webhook.send(embed=embed)

@bot.tree.command(name='credits',description='Displays Credits for the bot.')
async def slash_command(ctx:discord.Interaction):
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

-# MIT; Copyright 2024 Tywrap Studios. -- info.tywrap.studio@gmail.com -- {botversion}
'''
    embed = discord.Embed(colour=discord.Colour.teal(),title='<:list:1279213268082229381> Credits:',description=description)
    await ctx.response.send_message(embed=embed,ephemeral=True)
    
class Claim(discord.app_commands.Group):
    ...
claim = Claim(name='claims',description='Root for the Claim notes commands.')

@claim.command(name='claiming',description='How to claim a piece of land.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''
1. Press "`M`" (Might need to rebind: Press "esc">Options>Control>Keybinds>"open world map") to open up the world map
2. Right-click-drag over the area You want to claim. 
3. In the popup: Click "Claim selected"
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:claim:1278815499349786704> Claiming Chunks:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)

@claim.command(name='party',description='What are Parties?')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''In your claim config (use my **/claims perms** or **/claims config** command for info) you can set perms for your party.
This means that anyone in a party you're in, has those perms.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:party:1278816948846596157> Parties:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@claim.command(name='party-creation',description='How to create a Party and add people to it.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''- How to create a party: Run in game `/openpac-parties create`
 - Does it error? You are likely already in one.
- How to leave a party: Run in game `/openpac-parties leave`

**How to...**
> - ...*Invite* people to your party: Run in game `openpac-parties member invite <username>`
> - ...*Kick* people from your party: Run in game `openpac-parties member kick <username>`
> - ...*Delete* your party: Run in game `openpac-parties destroy confirm`
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:party:1278816948846596157> Party Creation:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@claim.command(name='party-misc',description='Misc in Parties.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''There is some Misc stuff to having a Party.
    
**How to...**
> - ...*Give people perms* in terms of party management: Run in game `/openpac-parties member rank <ADMIN|MODERATOR|MEMBER> <username>`
>  - <:info:1278823933717512232> Giving people perms for parties for instance makes them able to send invites or kick people from the party.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:party:1278816948846596157> Party Misc:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@claim.command(name='party-ally',description='How Allies work.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''Alongside giving Party members perms in your claims, you can also Ally another party to get specific claim perms for them as well!
    
**How to...**
> - ...*Ally* parties: Run in game `/openpac-parties ally add <username of party owner>`
> - ...*Unally* parties: Run in game `/openpac-parties ally remove <username of party owner>`

> <:info:1278823933717512232> **NOTES:**
> Allying a party does not give you perms to their claims, they need to ally you on their own as well!
> -> This can mean you have them allied, but they don't, and vice versa.
> Allies have separate perms to Party members.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:ally:1278823662589313045> Allies:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@claim.command(name='party-ownership',description='How Ownership works.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''The player who ran the `/openpac-parties create` command "owns" said party.
    
**How to...**
> - ...*Transfer* party ownership: Run in game `/openpac-parties transfer <username> confirm`
> - <:info:1278823933717512232> The user has to be in the party for this to work.
> - <:warn:1249069667159638206> This action is irreversible unless the new owner re-transfers back to you
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:party_owner:1278830882828062802> Allies:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@claim.command(name='config',description='How to use the config.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''To specify how your (sub)claims work, you are provided an in game config screen.
1. Press "`'`" (Might need to rebind: Press "esc">Options>Controls>Keybinds>"Open Parties and Claims Menu")
2. In the Menu: Player Config menu > My Player Config.
> <:info:1278823933717512232> In here you can now set all sorts of settings related to your (sub)claims.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:config:1278820765797580921> Config:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@claim.command(name='perms',description='How do I give players perms on my claim?')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''To specify which perms are given to who, you are provided an in game config screen.
1. Press "`'`" (Might need to rebind: Press "esc">Options>Controls>Keybinds>"Open Parties and Claims Menu")
2. In the Menu: Player Config menu > My Player Config.
3. Set the perms you want your friend to have to something related to "party" or "party only", etc.
> <:info:1278823933717512232> Have you not made a Party yet? Run my command **/claims party-creation** for info on how to do that!
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:perms:1278838464456032388> Perms:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)

@claim.command(name='mod',description='Info about the mod.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''The mod we use for the claiming system is Open Parties and Claims.
Xaero's Mini- and World map have also been added to make that experience nicer!

> <:curseforge:1279105910945480797> [CurseForge Page](<https://www.curseforge.com/minecraft/mc-mods/open-parties-and-claims>)
> <:modrinth:1279105929421258872> [Modrinth Page](<https://modrinth.com/mod/open-parties-and-claims>)
> <:githubblack:1279105948908130404> [GitHub repo](<https://github.com/thexaero/open-parties-and-claims>)
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:claim:1278815499349786704> Open Parties and Claims:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)

class Notes(discord.app_commands.Group):
    ...
notes = Notes(name='notes',description='Root for the Notes commands.')

@notes.command(name='cracked',description='Explains the fuzz about Cracked accounts.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''> Sorry but we do not allow cracked or unofficial accounts to join our server.
> This is because it can get both the Discord and Minecraft server in a lot of trouble.

> Furthermore it is illegal to Pirate games. We can report your message to Discord and it can get you in trouble.

<:info:1278823933717512232> You can buy the official game [here](<https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc>)
<:warn:1249069667159638206> **NOTE:** Most Cracked Launchers actually dub as spyware, we suggest cleansing them immediately anyways.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:against_rules:1279142167729668096> Cracked Instances:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@notes.command(name='bedrock',description='Explains the fuzz about Bedrock accounts.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''> Our server sadly isn't available for Bedrock users.
> Since we are a modded server you require [Minecraft Java Edition](<https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc>) and [The CurseForge app](<https://www.curseforge.com/download/app>) to play.

<:info:1278823933717512232> **Note you can get [Java for free if you own a (PC) Bedrock license.](<https://help.minecraft.net/hc/en-us/articles/6657208607501-I-Own-Minecraft-Java-or-Bedrock-Edition-for-PC-How-Do-I-Get-the-Other>)**
<:arrow_under:1278834153655107646> This does not count for Console Verions and PE. Using PC Game Pass Bedrock, however, should work.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:bedrock:1279144625168191598> Bedrock Instances:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)

@notes.command(name='zip-import',description='How to manually import modpacks using Zip-Files.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''1. Open the <:minecraft_logo:1278852452396826634>Minecraft section of the app.
2. Click <:pluse:1279147951519825931>Create Custom Profile
3. Click the Import option.
4. Find the zip-file you downloaded and select it.
5. CurseForge will now attempt to download and unpack the modpack. If it fails, try steps 2-4 again.
6. Once finished, click Play!
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:download:1279148597094514698> Zip-Importing:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@notes.command(name='modlist',description='How to make a modlist.txt file using command prompt.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''To make a modlist.txt file for your modpack, go to the `mods` folder in cmd and run the following command:
```cmd
dir /b "*.jar" >modlist.txt
```
if done correctly a `modlist.txt` file should show up in your `mods` folder.
Please note that some knowledge about the `cd` command, and cmd in general, is to be known for this to properly work.
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:perms:1278838464456032388> Modlist:',description=description)
    await ctx.response.send_message(embed=embed,content=mention)
    
@notes.command(name='binary-search',description='How to perform a binary-search instead of a sequential-search')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
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
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:search:1279151128466165911> Binary Search:',description=description)
    embed.set_image(url='https://media.discordapp.net/attachments/1249069998148812930/1279156096103354448/binary_search.gif?ex=66d36a72&is=66d218f2&hm=b7dd480dfb0d4da00a1359d15ca47a0540a8de18bbe6ff8d8baf1bf0a5301788&=&width=480&height=319')
    await ctx.response.send_message(embed=embed,content=mention)

@notes.command(name='provider',description='What server provider do we use?')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
    description = '''Our main server provider and sponsor is <#1272562565985206325>,
    
All of their servers run 24/7, on real hardware (none of that vCPU/threads nonsense), and are actively maintained by them. 
They have plans accommodating budgets of all sizes: big and small, so *your* plan can grow along with your server.
Alongside that, you're free to trial a server for up to a week, or just hang around after.

Again, huge thanks to Central Hosting for Sponsoring our beautiful server;
Without them we would now be nothing :purple_heart:
'''
    embed = discord.Embed(colour=discord.Colour.blurple(),title='<:central_hosting_au:1279161169747116064> Provider:',description=description)
    embed.set_footer(text='https://centralhosting.au/central-hosting/',icon_url='https://media.discordapp.net/attachments/1249069998148812930/1279200313345310741/central_hosting_au.png?ex=66d393a1&is=66d24221&hm=0c085589b8c90653db1aca21932b391e33d68330adc9c44de889a21dc60a029b&=&format=webp&quality=lossless&width=450&height=450')
    await ctx.response.send_message(embed=embed,content=mention)

@notes.command(name='dontasktoask',description='Don\'t ask to ask. Just ask.')
async def sub_command(ctx:discord.Interaction,mention:Optional[discord.Member]):
    if mention == None:
        mention = ''
    else:
        mention = mention.mention
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
    embed = discord.Embed(colour=discord.Colour.blurple(),description=description)
    await ctx.response.send_message(embed=embed,content=mention)

class Rcon(discord.app_commands.Group):
    ...
cmd = Rcon(name='cmd',description='Root for the Cmd commands.')

async def send_log_webhook(command:str,response:str,source:discord.Member):
    async with aiohttp.ClientSession() as session:
        url = rcon_logger_webhook_url
        webhook = discord.Webhook.from_url(url, session=session)
        embed = discord.Embed(colour=discord.Colour.blurple(),description=f':green_circle: The RCON `{rcon_host}:{rcon_port}` was sent a package.\n:package: Package: `{command}`\n:shield: Source: {source.mention}[`{source.id}`] -> [`{source.name}`].\n:information_source: Response: {response}',title='RCON TRIGGER:')
        time = datetime.now().strftime('%H:%M:%S')
        datetoday = date.today().strftime('%d/%m/%Y')
        embed.set_footer(text=f'On {datetoday} at {time}')
        await webhook.send(embed=embed)

async def send_rcon(command:str,ctx:discord.Interaction,adminOnly:bool):
    allowed2 = ctx.guild.get_role(minecraftadmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(centralhosting) in ctx.user.roles
    allowed = allowed2 or allowed3
    if adminOnly and allowed:
        with mcrcon_client as mcr:
            try:
                rcon_package_resp = mcr.command(command)
                response = f'`{rcon_package_resp}`'
                if len(response) == 2:
                    response = '`Response length is 0, this command likely has no console output.`'
                if '/mclogs' in command:
                    response = f'\n**{rcon_package_resp}**\n'
                
                embed = discord.Embed(colour=discord.Colour.green(),description=f'<:con_excellent:1278830872929501286>Server successfully recieved package.\n<:info:1278823933717512232>Response: {response}',title='RCON: <:resources:1278835693900136532>')
                await send_log_webhook(command=command,response=response,source=ctx.user)
                await ctx.response.send_message(embed=embed,ephemeral=True)
            except:
                embed = discord.Embed(colour=discord.Colour.red(),description='Something went wrong connecting to the RCON Client.<:warn:1249069667159638206>\nPlease report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) if this seems random.\n-# `Error Code 500`',title='RCON: <:resources:1278835693900136532>')
                await ctx.response.send_message(embed=embed,ephemeral=True)
    else:
        if adminOnly and not allowed:
            embed = discord.Embed(colour=discord.Colour.red(),description='<:against_rules:1279142167729668096> You are not allowed to connect this Command to an RCON Client.\n-# `Error Code 403`',title='RCON: <:resources:1278835693900136532>')
            await ctx.response.send_message(embed=embed,ephemeral=True)
        else:
            with mcrcon_client as mcr:
                try:
                    rcon_package_resp = mcr.command(command)
                    response = f'`{rcon_package_resp}`'
                    if len(response) == 2:
                        response = '`Response length is 0, this command likely has no console output.`'
                    if '/mclogs' in command:
                        response = f'\n**{rcon_package_resp}**\n'
                    embed = discord.Embed(colour=discord.Colour.green(),description=f'<:con_excellent:1278830872929501286>Server successfully recieved package.\n<:info:1278823933717512232>Response: {response}',title='RCON: <:resources:1278835693900136532>')
                    await send_log_webhook(command=command,response=response,source=ctx.user)
                    await ctx.response.send_message(embed=embed,ephemeral=True)
                except:
                    embed = discord.Embed(colour=discord.Colour.red(),description='Something went wrong connecting to the RCON Client.<:warn:1249069667159638206>\nPlease report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) if this seems random.\n-# `Error Code 500`',title='RCON: <:resources:1278835693900136532>')
                    await ctx.response.send_message(embed=embed,ephemeral=True) 
            

@cmd.command(name='tellraw', description='Says something in the MC Server.')
async def sub_command(ctx: discord.Interaction, content: str) -> None:
    command = f'/tellraw @a "{content}"'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='log',description='Logs your phrase to the Console.')
async def sub_command(ctx:discord.Interaction,info:str):
    command = f'/logtellraw targetless "{info}"'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='mclogs',description='Sends a request to mclo.gs for the latest.log or a log you specify.')
async def sub_command(ctx:discord.Interaction,log:Optional[str]):
    if log == None:
        file = ''
    else:
        file = f' share {log}'
    command = f'/mclogs{file}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='maintenance',description='Allows you to Toggle Maintenance.')
async def sub_command(ctx:discord.Interaction,enabled:bool):
    if enabled == True:
        arg = ' on'
    else:
        arg = ' off'
    command = f'/maintenance{arg}'
    await send_rcon(command,ctx,True)

@cmd.command(name='ban',description='Bans the selected player from the server.')
async def sub_command(ctx:discord.Interaction,player_user:str,reason:Optional[str]):
    if reason == None:
        reason1 = ''
    else:
        reason1 = f' {reason}'
    command = f'/ban {player_user}{reason1}'
    await send_rcon(command,ctx,True)

@cmd.command(name='tempban',description='Temporarily Bans the selected player from the server.')
async def sub_command(ctx:discord.Interaction,player_user:str,duration:str,reason:Optional[str]):
    dshort_s = duration.replace("seconds","s")
    dshort_m = dshort_s.replace("minutes","m")
    dshort_d = dshort_m.replace("days","d")
    dshort_w = dshort_d.replace("weeks","w")
    dshortws = dshort_w.replace(" ","")
    duration_v2 = dshortws
    if reason == None:
            reason1 = ''
    else:
        reason1 = f' {reason}'
    if re.match(duregex, duration_v2):
        command = f'/tempban {player_user} {duration_v2}{reason1}'
        await send_rcon(command,ctx,True)
    else:
        embed = discord.Embed(colour=discord.Colour.red(),description=f'<:warn:1249069667159638206> `{duration}` does not seem like a valid duration type even when corrected to `{duration_v2}` by our system!\n\n> <:info:1278823933717512232> A correct one would be: <number><either s, m, d or w> (e.g. 1w for 1 week.)\n> If you think it should actually be correct, please report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) and show this Embed.\n-# {botversion}',title='RCON: <:resources:1278835693900136532>')
        await ctx.response.send_message(embed=embed,ephemeral=True)

@cmd.command(name='ban-ip',description='IP Bans the selected player from the server.')    
async def sub_command(ctx:discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.red(),description='<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in game.\n-# `Error Code 423`',title='RCON: <:resources:1278835693900136532>')
    await ctx.response.send_message(embed=embed,ephemeral=True)

@cmd.command(name='tempban-ip',description='IP Bans the selected player from the server.')    
async def sub_command(ctx:discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.red(),description='<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in game.\n-# `Error Code 423`',title='RCON: <:resources:1278835693900136532>')
    await ctx.response.send_message(embed=embed,ephemeral=True)

@cmd.command(name='unban',description='Unbans the selected player from the server.')
async def sub_command(ctx:discord.Interaction,player_user:str,reason:Optional[str]):
    if reason == None:
        reason1 = ''
    else:
        reason1 = f' {reason}'
    command = f'/unban {player_user}{reason1}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='pardon',description='Pardons the selected player. THIS IS DIFFERENT FROM /UNBAN!')
async def sub_command(ctx:discord.Interaction,player_user:str,reason:Optional[str]):
    if reason == None:
        reason1 = ''
    else:
        reason1 = f' {reason}'
    command = f'/pardon {player_user}{reason1}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='run',description='Runs any command you provide, given that it has correct syntax.')
async def sub_command(ctx:discord.Interaction,command:str):
    mod_chat = ctx.guild.get_channel(logchannel)
    if ctx.channel == mod_chat:
        await send_rcon(command,ctx,True)
    else:
        embed = discord.Embed(colour=discord.Colour.red(),description=f'<:against_rules:1279142167729668096> Due to security concerns and issues, please run this command in {mod_chat.mention}.\n-# `Error Code 421`',title='RCON: <:resources:1278835693900136532>')
        await ctx.response.send_message(embed=embed,ephemeral=True)
        
@cmd.command(name='clear',description='Clears the selected player\'s inventory.')
async def sub_command(ctx:discord.Interaction,player:str,item:Optional[str]):
    if item == None:
        items = ''
    else:
        items = f' {item}'
    command = f'/clear {player}{items}'
    send_rcon(command,ctx,True)
    
@cmd.command(name='list',description='Lists all the players online.')
async def sub_command(ctx:discord.Interaction):
    command = '/list'
    await send_rcon(command,ctx,False)

@bot.event
async def on_message(message:discord.Message):
    name = message.author.display_name
    id = f'{message.author.id}'
    text = message.content
    channel = bot.get_channel(ctd_channel)
    command = '/tellraw @a ["",{"text":"[@'+name+'] ","color":"blue","clickEvent":{"action":"suggest_command","value":"<@'+id+'>"},"hoverEvent":{"action":"show_text","contents":[{"text":"This message was sent from Discord using CordCrafter.","color":"dark_purple"}]}},{"text":"'+text+'"}]'
    if message.channel == channel and message.author != client.user and 'CordCrafter' not in message.author.name:
        with mcrcon_client as mcr:
            try:
                rcon_package = mcr.command(command)
            except:
                    embed = discord.Embed(colour=discord.Colour.red(),description='Something went wrong connecting to the RCON Client.<:warn:1249069667159638206>\nPlease report this on a [GitHub issue](<https://github.com/Tywrap-Studios/LasCordCrafter/issues>) if this seems random.\n-# `Error Code 500`',title='RCON: <:resources:1278835693900136532>')
                    await channel.send(embed=embed)

@cmd.command(name='restore',description='Restores the grave of a player\'s last death.')
async def sub_command(ctx:discord.Interaction,player:str):
    command = f'/yigd restore {player}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='view-balance',description='Allows you to see someone\'s Nm. Balance.')
async def sub_command(ctx:discord.Interaction,player:str):
    command = f'/nm view {player}'
    await send_rcon(command,ctx,True)

@cmd.command(name='tp-offline',description='Allows you to TP Someone who\'s offline.')
async def sub_command(ctx:discord.Interaction,player:str,pos:str):
    command = f'/tp_offline {player} {pos}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='heal',description='Heals the selected player.')
async def sub_command(ctx:discord.Interaction,player:str):
    command = f'/heal {player}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='whitelist-toggle',description='Toggle the whitelist on or off.')
async def sub_command(ctx:discord.Interaction,enable:bool):
    if enable:
        command = f'/whitelist on'
    else:
        command = f'/whitelist off'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='whitelist-entry',description='Adds or removes a user to the whitelist.')
async def sub_command(ctx:discord.Interaction,player:str,can_enter:bool):
    if can_enter:
        command = f'/whitelist add {player}'
    else:
        command = f'/whitelist remove {player}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='whitelist',description='Lists the Whitelist')
async def sub_command(ctx:discord.Interaction):
    command = f'/whitelist list'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='damage',description='Damages the selected player.')
async def sub_command(ctx:discord.Interaction,player:str,amount:float):
    command = f'/damage {player} {amount}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='ban-legacy',description='Uses Minecraft\'s ban system.')
async def sub_command(ctx:discord.Interaction,player:str,reason:Optional[str]):
    if reason == None:
        reason1 = ''
    else:
        reason1 = f' {reason}'
    command = f'/minecraft:ban {player}{reason1}'
    await send_rcon(command,ctx,True)
    
@cmd.command(name='unban-legacy',description='Uses Minecraft\'s ban system.')
async def sub_command(ctx:discord.Interaction,player:str,reason:Optional[str]):
    if reason == None:
        reason1 = ''
    else:
        reason1 = f' {reason}'
    command = f'/minecraft:pardon {player}{reason1}'
    await send_rcon(command,ctx,True)
    
class Status(discord.app_commands.Group):
    ...
status = Status(name='status',description='Root for the Status commands.')

@status.command(name='downtime',description='Pregen a Downtime Embed, should be used when the server is down.')
async def sub_command(ctx:discord.Interaction,title:str,summary:Optional[str],impact:Optional[str],channel:Optional[discord.TextChannel],ping:Optional[Union[discord.Member,discord.Role]]):
    allowed1 = ctx.guild.get_role(discordadmin) in ctx.user.roles
    allowed2 = ctx.guild.get_role(minecraftadmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(centralhosting) in ctx.user.roles
    allowed4 = ctx.guild.get_role(gunjicord) in ctx.user.roles
    allowed = allowed1 or allowed2 or allowed3 or allowed4
    status = f'{title}; DOWN'
    if allowed:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,state=status,name='CustomStatus'), status=discord.Status.online)
        if channel == None:
            channel = ctx.channel
        if summary == None:
            summary = 'No summary was provided.'
        if impact == None:
            impact = 'No impact.'
        if ping == None:
            ping = ''
        description = f"""**Summary:**
{summary}

**Impact:**
{impact}"""
        embed = discord.Embed(title=f'Downtime - {title}',description=description,colour=discord.Colour.from_str('#fd5151'),timestamp=datetime.now())
        embed.set_footer(text='CordCraft',icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed,content=ping.mention)
        view = DeleteEmbed(message=message)
        await ctx.response.send_message(embed=embed,ephemeral=True,content='The following Embed was sent:',view=view)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)
    
@status.command(name='update',description='Pregen a Downtime Update Embed, should be used when an update about a downtime can be given.')
async def sub_command(ctx:discord.Interaction,title:str,summary:Optional[str],channel:Optional[discord.TextChannel],ping:Optional[Union[discord.Member,discord.Role]]):
    allowed1 = ctx.guild.get_role(discordadmin) in ctx.user.roles
    allowed2 = ctx.guild.get_role(minecraftadmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(centralhosting) in ctx.user.roles
    allowed4 = ctx.guild.get_role(gunjicord) in ctx.user.roles
    allowed = allowed1 or allowed2 or allowed3 or allowed4
    status = f'{title}'
    if allowed:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,state=status,name='CustomStatus'), status=discord.Status.online)
        if channel == None:
            channel = ctx.channel
        if summary == None:
            summary = 'No summary was provided.'
        if ping == None:
            ping = ''
        description = f"""**Summary:**
{summary}"""
        embed = discord.Embed(title=f'Downtime Update - {title}',description=description,colour=discord.Colour.from_str('#e2a915'),timestamp=datetime.now())
        embed.set_footer(text='CordCraft',icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed,content=ping.mention)
        view = DeleteEmbed(message=message)
        await ctx.response.send_message(embed=embed,ephemeral=True,content='The following Embed was sent:',view=view)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)
    
@status.command(name='uptime',description='Pregen a Downtime Update Embed, that\'s specifically for the service being back up.')
async def sub_command(ctx:discord.Interaction,title:str,note:Optional[str],channel:Optional[discord.TextChannel],ping:Optional[Union[discord.Member,discord.Role]]):
    allowed1 = ctx.guild.get_role(discordadmin) in ctx.user.roles
    allowed2 = ctx.guild.get_role(minecraftadmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(centralhosting) in ctx.user.roles
    allowed4 = ctx.guild.get_role(gunjicord) in ctx.user.roles
    allowed = allowed1 or allowed2 or allowed3 or allowed4
    if allowed:
        await bot.change_presence(activity=discord.Game('on CordCraft Season 2'), status=discord.Status.online)
        if channel == None:
            channel = ctx.channel
        if note == None:
            note = 'No extra note was provided.'
        if ping == None:
            ping = ''
        description = f"""**Extra note:**
{note}"""
        embed = discord.Embed(title=f'Downtime Update - {title}',description=description,colour=discord.Colour.from_str('#2dc79c'),timestamp=datetime.now())
        embed.set_footer(text='CordCraft',icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed,content=ping.mention)
        view = DeleteEmbed(message=message)
        await ctx.response.send_message(embed=embed,ephemeral=True,content='The following Embed was sent:',view=view)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)
        
@status.command(name='notice',description='Pregen a Notice Embed, which is just a simple way to point something out that doesn\'t have big impact.')
async def sub_command(ctx:discord.Interaction,note:str,channel:Optional[discord.TextChannel],ping:Optional[Union[discord.Member,discord.Role]]):
    allowed1 = ctx.guild.get_role(discordadmin) in ctx.user.roles
    allowed2 = ctx.guild.get_role(minecraftadmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(centralhosting) in ctx.user.roles
    allowed4 = ctx.guild.get_role(gunjicord) in ctx.user.roles
    allowed = allowed1 or allowed2 or allowed3 or allowed4
    if allowed:
        if channel == None:
            channel = ctx.channel
        if ping == None:
            ping = ''
        description = f"""{note}"""
        embed = discord.Embed(title=f'Notice:',description=description,colour=discord.Colour.dark_gold,timestamp=datetime.now())
        embed.set_footer(text='CordCraft',icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed,content=ping.mention)
        view = DeleteEmbed(message=message)
        await ctx.response.send_message(embed=embed,ephemeral=True,content='The following Embed was sent:',view=view)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)

@status.command(name='status',description='Change the Bot\'s status to say Minecraft Server Stati.')
async def slash_command(ctx:discord.Interaction,status:str,reset:bool,down:Optional[bool]):
    allowed1 = ctx.guild.get_role(discordadmin) in ctx.user.roles
    allowed2 = ctx.guild.get_role(minecraftadmin) in ctx.user.roles
    allowed3 = ctx.guild.get_role(centralhosting) in ctx.user.roles
    allowed4 = ctx.guild.get_role(gunjicord) in ctx.user.roles
    allowed = allowed1 or allowed2 or allowed3 or allowed4
    if down:
        status = f'{status}; DOWN'
    else:
        status = status
    if allowed:
        if reset == False:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,state=status,name='CustomStatus'), status=discord.Status.online)
            await ctx.response.send_message('Attempted to change status.',ephemeral=True)
        else: 
            await bot.change_presence(activity=discord.Game('on CordCraft Season 2'), status=discord.Status.online)
            await ctx.response.send_message('Attempted to reset status.',ephemeral=True)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)

class DeleteEmbed(discord.ui.View):
    def __init__(
        self,
        *,
        message: discord.Message
    ):
        self.message: discord.Message = message
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Delete Embed',style=discord.ButtonStyle.danger,emoji='🗑️')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        message = self.message
        await message.delete()
        await ctx.response.send_message('Message Deleted.',ephemeral=True)

class Thread(discord.app_commands.Group):
    ...
thread = Thread(name='thread',description='Root for the Thread commands.')

@thread.command(name='pin',description='Pin or unpin a message in your thread, given you have permission.')
async def sub_command(ctx:discord.Interaction,message_id:str):
    message = await ctx.channel.fetch_message(int(message_id))
    channel = ctx.channel
    perms = channel.permissions_for(ctx.user)
    perms.manage_messages
    if channel.owner is not ctx.user or not perms.manage_messages:
        await ctx.response.send_message(content='You do not have the permissions to send this command.',ephemeral=True)
    else:
        if not message.pinned:
            await message.pin(reason=f'{ctx.user.mention} pinned a message in thier thread, {ctx.channel.mention}.')
        else:
            await message.unpin(reason=f'{ctx.user.mention} unpinned a message in thier thread, {ctx.channel.mention}.')
    
@thread.command(name='lock',description='Lock or unlock your thread, given you have permission.')
async def sub_command(ctx:discord.Interaction,thread:Optional[discord.Thread]):
    if thread == None:
        thread = ctx.channel
    perms = thread.permissions_for(ctx.user)
    if thread.owner is not ctx.user or not perms.manage_threads:
        await ctx.response.send_message(content='You do not have the permissions to send this command.',ephemeral=True)
    else:
        if not thread.locked:
            await thread.edit(locked=True,reason=f'{ctx.user.mention} locked thier thread, {thread.mention}.')
        else:
            await thread.edit(locked=True,reason=f'{ctx.user.mention} unlocked thier thread, {thread.mention}.')
            
@thread.command(name='delete',description='Deletes your thread, given you have permission.')
async def sub_command(ctx:discord.Interaction,thread:Optional[discord.Thread]):
    if thread == None:
        thread = ctx.channel
    perms = thread.permissions_for(ctx.user)
    if thread.owner is not ctx.user or not perms.manage_threads:
        await ctx.response.send_message(content='You do not have the permissions to send this command.',ephemeral=True)
    else:
        embed = discord.Embed(title='Warning:',colour=discord.Colour.brand_red(),description=f'You are about to fully delete {thread.mention}, are you sure?\nNote that this action is IRREVERSIBLE!')
        view = ConfirmDeleteThreadButton(thread=thread)
        await ctx.response.send_message(embed=embed,view=view)
        
class ConfirmDeleteThreadButton(discord.ui.View):        
    def __init__(
        self,
        *,
        thread: discord.Thread
    ): 
        self.thread: discord.Thread = thread
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Confirm Deletion.',style=discord.ButtonStyle.danger)
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        thread = self.thread
        await thread.delete()
        
@thread.command(name='info',description='Displays info about the Thread.')
async def sub_command(ctx:discord.Interaction,thread:Optional[discord.Thread]):
    if thread == None:
        thread = ctx.channel
        
    tags = thread.applied_tags
    if tags.count == 0:
        tags = 'This thread has no tags.'
        
    last_message = thread.last_message
    if last_message == None:
        last_message = 'No message could be found.'
        
    starter_message = thread.starter_message
    jump_to_top = ''
    if starter_message is not None:
        jump_to_top = f'\n-# [Jump to top]({starter_message.jump_url})'
    
    description = f'''<:party_owner:1278830882828062802> Owner: {thread.owner.mention}
<:search:1279151128466165911> Tags: {tags}
<:config:1278820765797580921> Locked: {thread.locked}
<:id:1279190510027800709> Thread Type: {thread.type}
<:asterix:1279190506777088000> Stats:
<:arrow_under:1278834153655107646> Member Count: {thread.member_count}
<:arrow_under:1278834153655107646> Message Count: {thread.message_count}
<:arrow_under:1278834153655107646> Last Message: {last_message}{jump_to_top}
'''
    embed = discord.Embed(title=f'Info about {thread.mention}',description=description)
    await ctx.response.send_message(embed=embed,ephemeral=True)

@tasks.loop(hours=4)
async def task_loop() -> None:
    forum = bot.get_channel(team_forum)
    forum_posts = forum.threads
    trusted_tag = forum.get_tag(trusted_team_tag_id)
    for post in forum_posts:
        if trusted_tag in post.applied_tags:
            msg = await post.send(content='Auto-Bump.')
            await msg.delete()

bot.run(bottoken,log_handler=log_handler,log_level=log_level)
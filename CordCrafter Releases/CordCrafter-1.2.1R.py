import discord
import datetime, time
import os
from dotenv import load_dotenv
from discord.ext import commands
import psutil
from discord import ui
from typing import Any, Optional


load_dotenv()
description1 = '''This is a Bot made by Tywrap Studios for the GunjiCordia Discord server to help people and others 
in the wonderful server that is Gunji's that he crafted back in july of 2023'''
# Intents Configurement
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
intents.auto_moderation = True
intents.auto_moderation_configuration = True
intents.auto_moderation_execution = True
# Other Definements
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='??', description=description1, intents=intents)
bottoken = os.getenv("CORDTOKENS")
botid = '1248280095013998633'
botping = f'<@{botid}>'
guildinvitelink = os.getenv("CORDINVITELINK")
# Channels
roleschannel = '<#1189339256016093345>'
ipchannel = '<#1238669922641510502>'
techsupportchannel = '<#1188157890117242952>'
logchannel = 1191085319102140528
ticketcategory = 1165265825196945449
# Roles
discordadmin = 1160004558609731644
minecraftadmin = 1191088046695792720
# Stats
cpustat = psutil.cpu_percent(5)
ramstat  = round(psutil.virtual_memory()[3]/1000000000)
# Badge Stuff
red_badge = discord.File('discord-bot\mfiles\mred_mod_badge.png', filename='image.png')
green_badge = discord.File('discord-bot\mfiles\mgreen_mod_badge.png', filename='image.png')
blue_badge = discord.File('discord-bot\mfiles\mblue_mod_badge.png', filename='image.png')
red_mc_badgee = discord.File('discord-bot\mfiles\mred_mc_mod_badge.png', filename="image.png")
green_mc_badgee = discord.File('discord-bot\mfiles\mgreen_mc_mod_badge.png', filename='image.png')
red_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078349477838899/red_mod_badge.png?ex=6665fe5d&is=6664acdd&hm=832fb33a6ed5fe76ecc7539e56842a526cf3309fc189e59e73b6bb78400eb441&'
green_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078327872852071/green_mod_badge.png?ex=6665fe58&is=6664acd8&hm=d0713da6a04831a28b89db4cfba93cd21a196fe9716dafeb0daa367fb4603d6d&'
blue_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078338484568124/Ongetiteld.png?ex=6665fe5a&is=6664acda&hm=157173744c4ec4e8075d2386b3543419319bda26ae8f21bbdffa60c4d63cae2e&'
red_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085071508639894/red_mc_mod_badge.png?ex=6666049f&is=6664b31f&hm=d9c745c2bf2f872df1cd1b977b42f3408ed46d262e00e5dc58aa9fb7c2a7e54d&'
green_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085058682458173/green_mc_mod_badge.png?ex=6666049c&is=6664b31c&hm=f8767eed24c7c5565014dd8930141c0b3061611bf63a7a727ba5b4d6938540f9&'

# ONLY COMMIT THESE UNDERNEATH CHANGES:
@bot.event
async def on_ready():
    print('----------------------------------------------------------------------------')
    print(f'Logged in as {bot.user} (ID: {botid})')
    print('----------------------------------------------------------------------------')
    print('Setting Discord Bot Status. . .')
    await bot.change_presence(activity=discord.Game('on CordCraft Season 1'), status=discord.Status.online)
    print(f'Set Discord Bot Status.')
    print('Syncing Bot Tree. . .')
    await bot.tree.sync()
    print(f'Synced Bot Tree.')
    print('Starting Uptime Timer. . .')
    global startTime
    startTime = time.time()
    print('Started Timer.')
    print('----------------------------------------------------------------------------')
    print('Intents set:')
    print('''
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
    intents.webhooks❌
''')
    print('----------------------------------------------------------------------------')
    print('')
    print('')


@bot.tree.command(name='ip-joining',description='Tells the person you specify how to join the server.')
async def slash_command(ctx:discord.Interaction, member: discord.Member):
    await ctx.response.send_message(f'''Hey, <@{member.id}>!
Are you wondering how to join? The server IP alongside the Modpack Link and the Rules are all located in
- {ipchannel}.
And hey, if you're there already, why not read the rules?

> ## For the future: Please use your eyes, not your mouth.
> ~ Sincerely, the entire admin team cuz this question is asked too much. /hj''')

@bot.tree.command(name='fixing',description='Tells the person you specify where to find support channels.')
async def slash_command(ctx:discord.Interaction,member:discord.Member):
    await ctx.response.send_message(f'''Hey, {member.mention}!
Are you crashing or having issues? Instead of posting random stuff in <#1133093959959326722>. (Or wherever ya freak put it. 😜)
We suggest you carefully read <#1237949192526233660> before you post anything in {techsupportchannel}, as it already has a lot of fixes for a lot of common issues.

Is your issue not listed in there? Feel free to then make a post in {techsupportchannel} and we will try to look into it!
''')

@bot.tree.command(name='roles',description='Tells the person you specify where to find the obtainable roles')
async def slash_command(ctx:discord.Interaction, member: discord.Member):
    await ctx.response.send_message(f'''Hey, <@{member.id}>!
You can get some roles to be pinged or for other purposes in {roleschannel}!
An example of this is the Minecraft Server Pings to get pinged for server related stuff!''')

@bot.tree.command(name='ping',description='See how slow/fast the Bot\'s reaction time (ping) is.')
async def slash_command(ctx:discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(description=f'## Pong! `{latency}ms`',colour=discord.Colour.from_rgb(70,230,210))
    embed.set_footer(text='Want to see more? Use /stats!',)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="bean",description="Beans the member")
async def slash_command(ctx:discord.Interaction, member: discord.Member):
    embed = discord.Embed(title='Member Beaned',description=f'Member: {member.mention},\nResponsible "moderator": {ctx.user.mention}',colour=discord.Colour.og_blurple())
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name='discord-ban',description='Bans a member from the server.')
@discord.app_commands.checks.has_permissions(ban_members=True)
async def slash_command(ctx:discord.Interaction,offender:discord.Member,reason:str,bantime:str):
    bannedoffenderdm = await offender.create_dm()
    banlog = bot.get_channel(logchannel)
    view = FormButton()
    logembed = discord.Embed(colour=discord.Colour.from_rgb(220,90,90),title='Discord Server Ban:',description=f'''Offender: {offender.mention}.
Reason: `{reason}`.
Length: `{bantime} days`.
''')
    logembed.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {offender.id}.')
    logembed.set_thumbnail(url=red_badge_image)
    await banlog.send(embed=logembed)
    await bannedoffenderdm.send(content=f'''Hi. Unfortunately I am here to inform you you have been banned from GunjiCordia.
The reason for your ban has been: `{reason}`.
The length of your ban is: `{bantime} days`.
The moderator responsible for your ban was {ctx.user.mention}.

If you think this ban was unrightful, feel free to contact said, or a different moderator.
This ban will not be removed automatically. If the time is over and you have not been unbanned yet. Please contact a moderator.
I wish you a great day further.
~Tywrap Studios, your Head Minecraft Admin.

Preferably also fill in the post-ban-form using the below button.
''',view=view)
    await offender.ban(reason=reason)
    embed = discord.Embed(description=f'{offender.mention} was banned from the server. <:red:1249075916907348068>',colour=discord.Colour.from_rgb(220,90,90))
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name='discord-kick',description='Kicks a member from the server.')
@discord.app_commands.checks.has_permissions(kick_members=True)
async def slash_command(ctx:discord.Interaction,offender:discord.Member,reason:str):
    kickedoffenderdm = await offender.create_dm()
    kicklog = bot.get_channel(logchannel)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(220,90,90),title='Discord Server Kick:',description=f'''Offender: {offender.mention}.
Reason: `{reason}`.
''')
    logembed.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {offender.id}.')
    logembed.set_thumbnail(url=red_badge_image)
    await kicklog.send(file=file,embed=logembed)
    await kickedoffenderdm.send(f'''Hi. I am here to inform you you have been kicked from GunjiCordia.
The reason for your kick has been: `{reason}`.
The moderator responsible for your kick was <@{ctx.user.id}>.

If you wish to join back, here is the Discord Invite Link: {guildinvitelink}
I wish you a great day further!
~Tywrap Studios
''')
    await offender.kick(reason=reason)
    embed = discord.Embed(description=f'{offender.mention} was kicked from the server. <:red:1249075916907348068>',colour=discord.Colour.from_rgb(220,90,90))
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name='time-out',description='Times out a member. Timetype: s for seconds, m for minutes, h for hours, d for days.')
@discord.app_commands.checks.has_permissions(mute_members=True)
async def slash_command(ctx:discord.Interaction,offender:discord.Member,length:int,timetype:str,reason:str):
    mutelog = bot.get_channel(logchannel)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(90,200,220),title='Time-out:',description=f'''Offender: {offender.mention}.
Reason: `{reason}`.
Length: `{length}{timetype}`
''')
    logembed.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {offender.id}.')
    logembed.set_thumbnail(url=blue_badge_image)
    if timetype == 's':
        embed = discord.Embed(description=f'{offender.mention} was timed out for {length} second(s). <:blue:1249075855204810762>',colour=discord.Colour.from_rgb(90,200,220))
        await offender.timeout(datetime.timedelta(seconds=length),reason=reason)
        await ctx.response.send_message(embed=embed)
        await mutelog.send(embed=logembed)
    else:
        if timetype == 'm':
            embed = discord.Embed(description=f'{offender.mention} was timed out for {length} minutes(s). <:blue:1249075855204810762>',colour=discord.Colour.from_rgb(90,200,220))
            await offender.timeout(datetime.timedelta(minutes=length),reason=reason)
            await ctx.response.send_message(embed=embed)
            await mutelog.send(embed=logembed)
        else:
            if timetype == 'h':
                embed = discord.Embed(description=f'{offender.mention} was timed out for {length} hours(s). <:blue:1249075855204810762>',colour=discord.Colour.from_rgb(90,200,220))
                await offender.timeout(datetime.timedelta(hours=length),reason=reason)
                await ctx.response.send_message(embed=embed)
                await mutelog.send(embed=logembed)
            else:
                if timetype == 'd':
                    embed = discord.Embed(description=f'{offender.mention} was timed out for {length} days(s). <:blue:1249075855204810762>',colour=discord.Colour.from_rgb(90,200,220))
                    await offender.timeout(datetime.timedelta(days=length),reason=reason)
                    await ctx.response.send_message(embed=embed)
                    await mutelog.send(embed=logembed)
                else:
                    await ctx.response.send_message(f'''`{timetype}` is not a valid timetype.
Timetype must be either `s` for seconds, `m` for minutes, `h` for hours or `d` for days.''',ephemeral=True)
    
@bot.tree.command(name='discord-unban',description='Unbans a member from the Discord Server.')
@discord.app_commands.checks.has_permissions(ban_members=True)
async def slash_command(ctx:discord.Interaction,id:discord.User,reason:str):
    banlog = bot.get_channel(logchannel)
    embed = discord.Embed(colour=discord.Colour.from_rgb(90,220,125),description=f'{id.mention} was unbanned from the server. <:green:1249075836196360204>')
    await ctx.response.send_message(embed=embed)
    embed2 = discord.Embed(colour=discord.Colour.from_rgb(90,220,125),description=f'Offender: {id.mention}\nReason: `{reason}`',title='Discord Server Unban:')
    embed2.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {id.id}.')
    embed2.set_thumbnail(url=green_badge_image)
    await ctx.guild.unban(id,reason=reason)
    await banlog.send(embed=embed2)

@bot.tree.command(name='mcban',description='Logs a Minecraft Ban to the Admin Channel.')
async def slash_command(ctx:discord.Interaction,ign:str,reason:str,length:str,responsiblemoderator:discord.Member):
    allowedrole1 = ctx.guild.get_role(discordadmin)
    allowedrole2 = ctx.guild.get_role(minecraftadmin)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(220,90,90),title='Minecraft Server Ban:',description=f'''Who: `{ign}`
Reason: **{reason}**
Length: `{length}`
Responsible Moderator: {responsiblemoderator.mention}
''')
    logembed.set_footer(text=f'Logged By: {ctx.user.display_name}')
    logembed.set_thumbnail(url=red_mc_badge)
    recievechannel = bot.get_channel(logchannel)
    if allowedrole1 in ctx.user.roles or allowedrole2 in ctx.user.roles:
        await recievechannel.send(embed=logembed)
        await ctx.response.send_message(f'Minecraft Ban Log Succesfully sent.')
        await ctx.delete_original_response()
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)

@bot.tree.command(name='mcpardon',description='Logs a Minecraft Pardon to the Admin Channel.')
async def slash_command(ctx:discord.Interaction,ign:str,responsiblemoderator:discord.Member):
    allowedrole1 = ctx.guild.get_role(discordadmin)
    allowedrole2 = ctx.guild.get_role(minecraftadmin)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(90,220,125),title='Minecraft Server Unban:',description=f'''Who: `{ign}`
Responsible Moderator: {responsiblemoderator.mention}''')
    logembed.set_footer(text=f'Logged By: {ctx.user.display_name}.')
    logembed.set_thumbnail(url=green_mc_badge)
    recievechannel = bot.get_channel(logchannel)
    if allowedrole1 in ctx.user.roles or allowedrole2 in ctx.user.roles:
        await recievechannel.send(embed=logembed)
        await ctx.response.send_message(f'Minecraft Ban Log Succesfully sent.')
        await ctx.delete_original_response()
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)

          

class FormButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Form',url='https://forms.gle/dLYLvfWkZXh5JLQM7',style=discord.ButtonStyle.gray))

@bot.tree.command(name='stats',description='Displays the Bot\'s statistics.')
async def slash_command(ctx:discord.Interaction):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    latency = round(bot.latency * 1000)
    member_count = len([m for m in ctx.guild.members if not m.bot])
    bot_count = len([m for m in ctx.guild.members if m.bot])
    guild_age_secs = time.time()-ctx.guild.created_at.timestamp()
    guild_age = round(guild_age_secs/86400)
    statusembed = discord.Embed(colour=discord.Colour.from_rgb(70,230,210),title='CordCrafter Status.',description=f'''<:space:1251655233919123628><:speed:1251649973418983565> **Latency:** `{latency}ms`
<:space:1251655233919123628><:uptime:1251648456301346946> **Uptime:** `{uptime}`
<:space:1251655233919123628><:resources:1251658404372414586> **Resource Usage:**
<:space:1251655233919123628><:arrowunder:1257526524274278431><:ram:1251659281384738857> RAM: `{ramstat}GB`
<:space:1251655233919123628><:arrowunder:1257526524274278431><:cpu_load:1251684895038902324> CPU: `{cpustat}%`
<:space:1251655233919123628><:servericon:1251671285277130753> **Server:**
<:space:1251655233919123628><:space:1251655233919123628>🫂 Members:
<:space:1251655233919123628><:space:1251655233919123628><:arrowunder:1257526524274278431>🧑‍🤝‍🧑`{member_count}`;
<:space:1251655233919123628><:space:1251655233919123628><:arrowunder:1257526524274278431>🤖`{bot_count}`
<:space:1251655233919123628><:space:1251655233919123628>⏰ Age: {guild_age}
''')
    await ctx.response.send_message(embed=statusembed)
    
class ConfirmButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Confirm',style=discord.ButtonStyle.green,emoji='✅')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        await ctx.channel.delete(reason=f'Closed ticket {ctx.channel.mention}')

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Close',style=discord.ButtonStyle.danger,emoji='🔒')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        embed = discord.Embed(title='Confirm',description='Please confirm that you want to close your Ban Appeal Ticket.',colour=discord.Colour.green())
        view = ConfirmButton()
        await ctx.response.send_message(embed=embed,view=view,ephemeral=True)
    
    
class AppealButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label='Open MC Ban Appeal',style=discord.ButtonStyle.blurple,emoji='📫')
    async def onclick(self,ctx:discord.Interaction,button:discord.Button):
        overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                ctx.user: discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True,attach_files=True,embed_links=True),
                ctx.guild.me: discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True)
        }
        category = ctx.guild.get_channel(ticketcategory)
        view = CloseTicketButton()
        channel = await ctx.guild.create_text_channel(name=f'ban-appeal-{ctx.user.name}',overwrites=overwrites,reason=f'Made Ban appeal ticket for {ctx.user}',category=category)
        embed = discord.Embed(description='Thanks for opening a ban appeal ticket.\nPlease stay calm and civil while discussing your ban with our admin staff.',colour=discord.Colour.green())
        ping = await channel.send(f'<@&{discordadmin}>')
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
    view = AppealButton()
    embed = discord.Embed(colour=discord.Colour.from_rgb(230,230,60),title='**Appeal a Minecraft Unban.**',description='By clicking the button below, a Private Channel will be made for your Appeal.')
    await channel.send(embed=embed,view=view)
    await ctx.response.send_message(content=f'Setup Completed in {channel.mention}.',ephemeral=True)
    
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
            await ticket.delete(reason=f'{ctx.user} wanted to force close {ticket}')
            await ctx.response.send_message(f'Force closed {ticket.mention}',ephemeral=True)
        else: 
            if "ban-appeal-" not in ticket.name:
                await ctx.response.send_message("That TextChannel isn't a ticket!", ephemeral = True)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)
                   
@bot.tree.command(name='server-status',description='Change the Bot\'s status to say Minecraft Server Stati.')
async def slash_command(ctx:discord.Interaction,status:str,reset:Optional[bool]):
    allowedrole1 = ctx.guild.get_role(discordadmin)
    allowedrole2 = ctx.guild.get_role(minecraftadmin)
    if allowedrole1 in ctx.user.roles or allowedrole2 in ctx.user.roles:
        if reset == False:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,state=status,name='CustomStatus'), status=discord.Status.online)
            await ctx.response.send_message('Attempted to change status.',ephemeral=True)
        else: 
            await bot.change_presence(activity=discord.Game('on CordCraft Season 1'), status=discord.Status.online)
            await ctx.response.send_message('Attempted to reset status.',ephemeral=True)
    else:
        await ctx.response.send_message(f'You do not have the permissions to send this command.',ephemeral=True)

bot.run(bottoken)

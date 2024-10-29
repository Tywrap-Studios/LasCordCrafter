import discord
import datetime, time
import os
from dotenv import load_dotenv
from discord.ext import commands
import psutil
from discord import ui


load_dotenv()
description1 = '''This is a Bot made by Tywrap Studios for the GunjiCordia Discord server to help people and others in the wonderful server that is Gunji's that he crafted back in july of 2023'''
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
red_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078349477838899/red_mod_badge.png?ex=6665fe5d&is=6664acdd&hm=832fb33a6ed5fe76ecc7539e56842a526cf3309fc189e59e73b6bb78400eb441&'
green_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078327872852071/green_mod_badge.png?ex=6665fe58&is=6664acd8&hm=d0713da6a04831a28b89db4cfba93cd21a196fe9716dafeb0daa367fb4603d6d&'
blue_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078338484568124/Ongetiteld.png?ex=6665fe5a&is=6664acda&hm=157173744c4ec4e8075d2386b3543419319bda26ae8f21bbdffa60c4d63cae2e&'
red_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085071508639894/red_mc_mod_badge.png?ex=6666049f&is=6664b31f&hm=d9c745c2bf2f872df1cd1b977b42f3408ed46d262e00e5dc58aa9fb7c2a7e54d&'
green_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085058682458173/green_mc_mod_badge.png?ex=6666049c&is=6664b31c&hm=f8767eed24c7c5565014dd8930141c0b3061611bf63a7a727ba5b4d6938540f9&'
# Channels
roleschannel = '<#1189339256016093345>'
ipchannel = '<#1238669922641510502>'
techsupportchannel = '<#1188157890117242952>'
logchannel = 1191085319102140528
# Roles
discordadmin = 1160004558609731644
minecraftadmin = 1191088046695792720
# Stats
cpustat = psutil.cpu_percent(5)
ramstat  = round(psutil.virtual_memory()[3]/1000000000)

# ONLY COMMIT THESE UNDERNEATH CHANGES:
@bot.event
async def on_ready():
    print('----------------------------------------------------------------------------')
    print(f'Logged in as {bot.user} (ID: {botid})')
    print('----------------------------------------------------------------------------')
    print('Setting Discord Bot Status. . .')
    await bot.change_presence(activity=discord.Game("on CordCraft Season 1."), status=discord.Status.online)
    print(f'Set Discord Bot Status to ONLINE, Playing on CordCraft Season 1.')
    print('Syncing Bot Tree. . .')
    await bot.tree.sync()
    print(f'Synced Bot Tree.')
    global startTime
    startTime = time.time()
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


@bot.tree.command(name='ip',description='Tells the person you specify where to find the IP-Address of the server.')
async def slash_command(ctx:discord.Interaction, member: discord.Member):
    print(f'{ctx.user.display_name} ran /ip? for member \"NAME:{member.name},ID:{member.id}\"')
    await ctx.response.send_message(f'''Hey, <@{member.id}>!
Are you looking for the server IP? The server IP alongside the Modpack Link and the Rules are all located in
## {ipchannel}.
And hey, if you're there already, why not read the rules?

# For the future: Use your eyes, not your mouth.
~ Sincerely, the entire motherfucking admin team cuz this question is asked too much. /hj''')

@bot.tree.command(name='fixing',description='Tells the person you specify where to find support channels.')
async def slash_command(ctx:discord.Interaction,member:discord.Member):
    await ctx.response.send_message(f'''Hey, {member.mention}!
Are you crashing or having issues? Instead of posting random stuff in <#1133093959959326722>. (Or wherever ya freak put it. 😜)
We suggest you carefully read <#1237949192526233660> before you post anything in {techsupportchannel}, as it already has a lot of fixes for a lot of common issues.

Is your issue not listed in there? Feel free to then make a post in {techsupportchannel} and we will try to look into it!
''')

@bot.tree.command(name='roles',description='Tells the person you specify where to find the obtainable roles')
async def slash_command(ctx:discord.Interaction, member: discord.Member):
    print(f'{ctx.user.display_name} ran /getroles for member \"NAME:{member.name},ID:{member.id}\"')
    await ctx.response.send_message(f'''Hey, <@{member.id}>!
You can get some roles to be pinged or for other purposes in {roleschannel}!''')

@bot.tree.command(name='ping',description='See how slow/fast the Bot\'s reaction time (ping) is.')
async def slash_command(ctx:discord.Interaction):
    latency = round(bot.latency * 1000)
    print(f'Pong! {latency}ms')
    await ctx.response.send_message(f'Pong! `{latency}ms`.\nWant to see more? Use /stats!')

@bot.tree.command(name="bean",description="Beans the member")
async def slash_command(interaction:discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"Member beaned: {member.display_name}, responsible \"moderator\": {interaction.user.display_name}")

@bot.tree.command(name='discord-ban',description='Bans a member from the server.')
@discord.app_commands.checks.has_permissions(ban_members=True)
async def slash_command(ctx:discord.Interaction,offender:discord.Member,reason:str,bantime:str):
    print(f'{ctx.user.name} banned {offender.name} from the server. Reason: {reason}. Length: {bantime} days.')
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
The moderator responsible for your ban was <@{ctx.user.id}>.

If you think this ban was unrightful, feel free to contact said, or a different moderator.
This ban will not be removed automatically. If the time is over and you have not been unbanned yet. Please contact a moderator.
I wish you a great day further.
~Tywrap Studios

Preferably also fill in the post-ban-form using the below button.
''',view=view)
    await offender.ban()
    await ctx.response.send_message(f'<@{offender.id}> was banned from the server. <:red:1249075916907348068>')

@bot.tree.command(name='discord-kick',description='Kicks a member from the server.')
@discord.app_commands.checks.has_permissions(kick_members=True)
async def slash_command(ctx:discord.Interaction,offender:discord.Member,reason:str):
    print(f'{ctx.user.name} kicked {offender.name} from the server. Reason: {reason}')
    kickedoffenderdm = await offender.create_dm()
    kicklog = bot.get_channel(logchannel)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(220,90,90),title='Discord Server Kick:',description=f'''Offender: <@{offender.id}>.
Reason: `{reason}`.
''')
    logembed.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {offender.id}.')
    logembed.set_thumbnail(url=red_badge_image)
    await kicklog.send(embed=logembed)
    await kickedoffenderdm.send(f'''Hi. I am here to inform you you have been kicked from GunjiCordia.
The reason for your kick has been: `{reason}`.
The moderator responsible for your kick was <@{ctx.user.id}>.

If you wish to join back, here is the Discord Invite Link: {guildinvitelink}
I wish you a great day further!
~Tywrap Studios

```
Note: Please send the command "??ign <Minecraft In Game Name>" before or after rejoining the server.
```
''')
    await offender.kick()
    await ctx.response.send_message(f'<@{offender.id}> was kicked from the server. 👋')

@bot.tree.command(name='time-out',description='Times out a member. Timetype: s for seconds, m for minutes, h for hours, d for days.')
@discord.app_commands.checks.has_permissions(mute_members=True)
async def slash_command(ctx:discord.Interaction,offender:discord.Member,length:int,timetype:str,reason:str):
    print(f'{ctx.user.name} timed {offender.name} out for {length}{timetype}. Reason: {reason}')
    mutelog = bot.get_channel(logchannel)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(90,200,220),title='Time-out:',description=f'''Offender: {offender.mention}.
Reason: `{reason}`.
Length: `{length}{timetype}`
''')
    logembed.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {offender.id}.')
    logembed.set_thumbnail(url=blue_badge_image)
    if timetype == 's':
        await offender.timeout(datetime.timedelta(seconds=length))
        await ctx.response.send_message(f'<:blue:1249075855204810762> <@{offender.id}> was timed out for {length} second(s). ⏲️')
        await mutelog.send(embed=logembed)
    else:
        if timetype == 'm':
            await offender.timeout(datetime.timedelta(minutes=length))
            await ctx.response.send_message(f'<:blue:1249075855204810762> <@{offender.id}> was timed out for {length} minute(s). ⏲️')
            await mutelog.send(embed=logembed)
        else:
            if timetype == 'h':
                await offender.timeout(datetime.timedelta(hours=length))
                await ctx.response.send_message(f'<:blue:1249075855204810762> <@{offender.id}> was timed out for {length} hour(s). ⏲️')
                await mutelog.send(embed=logembed)
            else:
                if timetype == 'd':
                    await offender.timeout(datetime.timedelta(days=length))
                    await ctx.response.send_message(f'<:blue:1249075855204810762> <@{offender.id}> was timed out for {length} day(s). ⏲️')
                    await mutelog.send(embed=logembed)
                else:
                    await ctx.response.send_message(f'''`{timetype}` is not a valid timetype.
Timetype must be either `s` for seconds, `m` for minutes, `h` for hours or `d` for days.''')

@bot.tree.command(name='restart',description='Explains to members why and how the server restarts.')
async def slash_command(ctx:discord.Interaction,member:discord.Member):
    await ctx.response.send_message(f'''> "Crash? Close? Why did I get kicked?"
## That. Was probably you ({member.mention}) just now. 
The reason you were kicked from the server was likely a perfectly normal **server restart**.
## What is that you may ask. 
Well, every 3 hours the server is restarted to keep it fresh and get rid of unwanted entities, so to remove any lag that might occur if the server were to keep going.
It announces this restart in the Minecraft Chat AND in your kick message.
''')
    
@bot.tree.command(name='discord-unban',description='Unbans a member from the Discord Server.')
@discord.app_commands.checks.has_permissions(ban_members=True)
async def slash_command(ctx:discord.Interaction,id:discord.User):
    banlog = bot.get_channel(logchannel)
    logembed = discord.Embed(colour=discord.Colour.from_rgb(90,220,125),title=f'✅ {id.name} was unbanned.')
    await ctx.response.send_message(embed=logembed)
    logembed.set_footer(text=f'Responsible Moderator: {ctx.user.display_name}. Offender ID: {id.id}.')
    logembed.set_thumbnail(url=green_badge_image)
    await ctx.guild.unban(id)
    await banlog.send(embed=logembed)

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
        await ctx.response.send_message(f'You do not have the permissions to send this command.')

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
        await ctx.response.send_message(f'You do not have the permissions to send this command.')

class AppealModal(ui.Modal, title='Ban Appeal'):
    name = ui.TextInput(label='Minecraft In Game Name.')
    answer = ui.TextInput(label='Ban Reason')
    appeal = ui.TextInput(label='Why should you be unbanned?',style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction:discord.Interaction):
        submitchannel = interaction.client.get_channel(logchannel)
        logembed = discord.Embed(colour=discord.Colour.from_rgb(220,90,90),title=f'"{self.name}" Minecraft Ban Appeal:',description=f'**Minecraft In Game Name**: `{self.name}`. \n\n**Appeal:**\n> *{self.appeal}*')
        logembed.set_thumbnail(url=red_mc_badge)
        await submitchannel.send(embed=logembed)
        await interaction.response.send_message(f'Thanks for your appeal, {self.name}! You\'ll soon hear from us.',ephemeral=True)

class FormButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Form',url='https://forms.gle/dLYLvfWkZXh5JLQM7',style=discord.ButtonStyle.gray))
        
class AppealModalButton(discord.ui.View):
        @discord.ui.button(label='Open MC Ban Appeal',style=discord.ButtonStyle.blurple,emoji='📫')
        async def onclick(self, interaction:discord.Interaction,button:discord.Button):
            modal = AppealModal()
            await interaction.response.send_modal(modal)

@bot.tree.command(name='stats',description='Displays the Bot\'s statistics.')
async def slash_command(ctx:discord.Interaction):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    latency = round(bot.latency * 1000)
    statusembed = discord.Embed(colour=discord.Colour.from_rgb(70,230,210),title='CordCrafter Status.',description=f'''<:space:1251655233919123628><:speed:1251649973418983565> **Latency:** `{latency}ms`
<:space:1251655233919123628><:uptime:1251648456301346946> **Uptime:** `{uptime}`
<:space:1251655233919123628><:resources:1251658404372414586> **Resource Usage:**
<:space:1251655233919123628><:space:1251655233919123628><:ram:1251659281384738857> RAM: `{ramstat}GB`
<:space:1251655233919123628><:space:1251655233919123628><:cpu_load:1251684895038902324> CPU: `{cpustat}%`
<:space:1251655233919123628><:servericon:1251671285277130753> **Server:**
<:space:1251655233919123628><:space:1251655233919123628>🫂 Members: `{ctx.guild.member_count}`
''')
    await ctx.response.send_message(embed=statusembed)
    
@bot.tree.command(name='setup',description='Sets up the Bot\'s Form Function.')
@discord.app_commands.checks.has_permissions(administrator=True)
async def slash_command(ctx:discord.Interaction,channel:discord.TextChannel):
    view = AppealModalButton()
    embed = discord.Embed(colour=discord.Colour.from_rgb(230,230,60),title='**Appeal a Minecraft Unban.**',description='By clicking the button below, a Modal will pop up for your Appeal.')
    await channel.send(embed=embed,view=view)
    await ctx.response.send_message(content='Setup Completed.',ephemeral=True)

bot.run(bottoken)

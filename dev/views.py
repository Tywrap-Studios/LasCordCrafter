from datetime import date
from datetime import datetime

import discord
from discord.ext import commands

import util
import vars


class ConfirmButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
    async def onclick(self, ctx: discord.Interaction):
        ticket_log_channel = ctx.guild.get_channel(vars.ticketLog)
        mc_admin_role = ctx.guild.get_role(vars.minecraftAdmin)
        if mc_admin_role in ctx.user.roles:
            is_admin = '<:arrow_under:1278834153655107646> **__This User is a Minecraft Admin.__**'
        else:
            is_admin = ''
        opname = ctx.channel.name.replace('ban-appeal-', '')
        op = ctx.guild.get_member_named(opname)
        closer = ctx.user
        embed = discord.Embed(title='Ban Appeal Closed', description=f'''
<:id:1279190510027800709> **Ticket Opened by:**
<:asterix:1279190506777088000> {op.mention}

<:leave:1279190513190178826> **Ticket Closed by:**
<:asterix:1279190506777088000> {closer.mention}
{is_admin}
''', colour=discord.Colour.green())
        time = datetime.now().strftime('%H:%M')
        datetoday = date.today().strftime('%d/%m/%Y')
        embed.set_footer(text=f'{datetoday} {time}')
        await ctx.channel.delete(reason=f'Closed ticket {ctx.channel.mention}')
        await ticket_log_channel.send(embed=embed)
        util.info(f'[{util.time()}] >LOG> {closer.name} Closed ticket by {op.name}.]')


class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close', style=discord.ButtonStyle.danger, emoji='🔒')
    async def onclick(self, ctx):
        embed = discord.Embed(title='Confirm',
                              description='Please confirm that you want to close your Ban Appeal Ticket.',
                              colour=discord.Colour.green())
        view = ConfirmButton()
        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)


class ManualAppealButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Open MC Ban Appeal', style=discord.ButtonStyle.blurple, emoji='📫')
    async def onclick(self, ctx):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True,
                                                  attach_files=True, embed_links=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }
        allowedrole = ctx.guild.get_role(vars.minecraftAdmin)
        category = ctx.guild.get_channel(vars.ticketCategory)
        view = CloseTicketButton()
        channel = await ctx.guild.create_text_channel(name=f'ban-appeal-{ctx.user.name}', overwrites=overwrites,
                                                      reason=f'Made Ban appeal ticket for {ctx.user}',
                                                      category=category, topic=f'{ctx.user.id}')
        await channel.set_permissions(target=allowedrole, view_channel=True, send_messages=True,
                                      read_message_history=True, attach_files=True, embed_links=True)
        embed = discord.Embed(
            description='Thanks for opening a ban appeal ticket.\nPlease stay calm and civil while discussing your ban with our admin staff.',
            colour=discord.Colour.green())
        embed.set_footer(text=f'*This appeal was manually triggered using the command!*')
        ping = await channel.send(f'<@&{vars.minecraftAdmin}>')
        await ping.delete()
        await channel.send(embed=embed, view=view)
        await ctx.response.send_message(content=f'Thanks {ctx.user.mention}, I made {channel.mention} for you!',
                                        ephemeral=True)
        util.info(f'[{util.time()}] >LOG> {ctx.user.name} Opened ticket.]')


class RemoveButton(discord.ui.View):
    def __init__(
            self,
            *,
            member: discord.Member
    ):
        self.member: discord.Member = member
        super().__init__(timeout=None)

    @discord.ui.button(label='Remove User.', style=discord.ButtonStyle.danger)
    async def onclick(self, ctx):
        if "ban-appeal-" in ctx.channel.name:
            member = self.member
            await ctx.channel.set_permissions(member, overwrite=None)
            embed = discord.Embed(title='Member Remove',
                                  description=f"{member.mention} has been removed from the ticket by {ctx.user.mention}.",
                                  colour=discord.Colour.dark_gray())
            await ctx.response.send_message(embed=embed)
            util.info(f'[{util.time()}] >LOG> {ctx.author.name} removed {member.name} from {ctx.channel.name}.')
        else:
            await ctx.response.send_message("This isn't a ticket!", ephemeral=True)


class ShowDebugButton(discord.ui.View):
    def __init__(
            self,
            *,
            nick: str
    ):
        self.nick: str = nick
        super().__init__(timeout=None)

    @discord.ui.button(label='Show Debug util.info', style=discord.ButtonStyle.gray, emoji='☑️')
    async def onclick(self, ctx):
        attempted_nick = self.nick
        embed = discord.Embed(colour=discord.Colour.dark_embed(), title='__Debug util.info__', description=f'''
```
Current Regex Pattern:
{vars.repat}
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
Version:
{vars.botVersion}
```
''')
        await ctx.response.send_message(embed=embed, ephemeral=True)


class DeleteEmbed(discord.ui.View):
    def __init__(
            self,
            *,
            message: discord.Message
    ):
        self.message: discord.Message = message
        super().__init__(timeout=None)

    @discord.ui.button(label='Delete Embed', style=discord.ButtonStyle.danger, emoji='🗑️')
    async def onclick(self, ctx):
        message = self.message
        await message.delete()
        await ctx.response.send_message('Message Deleted.', ephemeral=True)
        util.info(f'[{util.time()}] >LOG> {ctx.author.name} deleted an Embed they sent.')


class ConfirmDeleteThreadButton(discord.ui.View):
    def __init__(
            self,
            *,
            thread: discord.Thread,
            ctx: commands.Context
    ):
        self.thread: discord.Thread = thread
        self.ctx: commands.Context = ctx
        super().__init__(timeout=None)

    @discord.ui.button(label='Confirm Deletion.', style=discord.ButtonStyle.danger)
    async def onclick(self):
        thread = self.thread
        ctx = self.ctx
        await thread.delete()
        util.info(f'[{util.time()}] >LOG> {ctx.author.name} deleted their thread.')

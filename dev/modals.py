from datetime import datetime

import discord.ui
from discord import Interaction
from discord.ext import commands

import views
from util import info_time


class DowntimeModal(discord.ui.Modal, title='Status Info'):
    def __init__(self, bot: commands.bot, title: str):
        self.title = title
        self.bot = bot
        super().__init__()

    summary = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Summary',
        required=True,
        max_length=600,
        placeholder='Summary of the downtime.'
    )

    impact = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Impact',
        default='No impact provided.',
        required=False,
        max_length=600,
        placeholder='Impact of the downtime.'
    )

    channel = discord.ui.ChannelSelect(
        min_values=1,
        max_values=1,
        placeholder='Select a channel to send the downtime notice to.',
        channel_types=[discord.ChannelType.text]
    )

    ping = discord.ui.RoleSelect(
        min_values=0,
        max_values=1,
        placeholder='Select a role to ping.',
    )

    async def on_submit(self, interaction: Interaction) -> None:
        title = self.title
        channel = self.bot.get_channel(self.channel.values[0].id)
        summary = self.summary.value
        impact = self.impact.value
        if len(self.ping.values) == 0:
            ping = ''
        else:
            ping = self.ping.values[0].mention

        status = f'{title}; DOWN'
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.custom, state=status, name='CustomStatus'),
            status=discord.Status.online)
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
        await interaction.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                                view=view)
        info_time(f'>STATUS> {interaction.user.name} stated the server as DOWNTIME: {title}.')

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        await interaction.response.send_message(
            f'Something unexpected happened while handling this command.\nDowntimeModalException: {error}',
            ephemeral=True)
        raise error


class DowntimeUpdateModal(discord.ui.Modal, title='Status Info'):
    def __init__(self, bot: commands.bot, title: str):
        self.title = title
        self.bot = bot
        super().__init__()

    summary = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Summary',
        required=True,
        max_length=600,
        placeholder='Summary of the downtime.'
    )

    channel = discord.ui.ChannelSelect(
        min_values=1,
        max_values=1,
        placeholder='Select a channel to send the downtime notice to.',
        channel_types=[discord.ChannelType.text]
    )

    ping = discord.ui.RoleSelect(
        min_values=0,
        max_values=1,
        placeholder='Select a role to ping.',
    )

    async def on_submit(self, interaction: Interaction) -> None:
        title = self.title
        channel = self.bot.get_channel(self.channel.values[0].id)
        summary = self.summary.value
        if len(self.ping.values) == 0:
            ping = ''
        else:
            ping = self.ping.values[0].mention

        status = f'{title}'
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.custom, state=status, name='CustomStatus'),
            status=discord.Status.online)
        description = f"""**Summary:**
{summary}"""
        embed = discord.Embed(title=f'Downtime Update - {title}', description=description,
                              colour=discord.Colour.from_str('#e2a915'), timestamp=datetime.now())
        embed.set_footer(text='CordCraft',
                         icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed, content=ping)
        view = views.DeleteEmbed(message=message)
        await interaction.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                                view=view)
        info_time(f'>STATUS> {interaction.user.name} stated a status update: {title}.')

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        await interaction.response.send_message(
            f'Something unexpected happened while handling this command.\nDowntimeUpdateModalException: {error}',
            ephemeral=True)
        raise error


class UptimeModal(discord.ui.Modal, title='Status Info'):
    def __init__(self, bot: commands.bot, title: str):
        self.title = title
        self.bot = bot
        super().__init__()

    note = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Note',
        required=False,
        default='No extra notes given.',
        max_length=600,
        placeholder='Extra notes for after the downtime.'
    )

    channel = discord.ui.ChannelSelect(
        min_values=1,
        max_values=1,
        placeholder='Select a channel to send the downtime notice to.',
        channel_types=[discord.ChannelType.text]
    )

    ping = discord.ui.RoleSelect(
        min_values=0,
        max_values=1,
        placeholder='Select a role to ping.',
    )

    async def on_submit(self, interaction: Interaction) -> None:
        title = self.title
        channel = self.bot.get_channel(self.channel.values[0].id)
        note = self.note.value
        if len(self.ping.values) == 0:
            ping = ''
        else:
            ping = self.ping.values[0].mention

        await self.bot.change_presence(activity=discord.Game('on CordCraft Season 2'), status=discord.Status.online)
        description = f"""**Extra note:**
{note}"""
        embed = discord.Embed(title=f'Uptime - {title}', description=description,
                              colour=discord.Colour.from_str('#2dc79c'), timestamp=datetime.now())
        embed.set_footer(text='CordCraft',
                         icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed, content=ping)
        view = views.DeleteEmbed(message=message)
        await interaction.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                                view=view)
        info_time(f'>STATUS> {interaction.user.name} stated the server as UP: {title}.')

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        await interaction.response.send_message(
            f'Something unexpected happened while handling this command.\nUptimeModalException: {error}',
            ephemeral=True)
        raise error


class NoticeModal(discord.ui.Modal, title='Status Info'):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    notice = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Notice',
        required=True,
        max_length=600,
        placeholder='The notice.'
    )

    channel = discord.ui.ChannelSelect(
        min_values=1,
        max_values=1,
        placeholder='Select a channel to send the downtime notice to.',
        channel_types=[discord.ChannelType.text]
    )

    ping = discord.ui.RoleSelect(
        min_values=0,
        max_values=1,
        placeholder='Select a role to ping.',
    )

    async def on_submit(self, interaction: Interaction) -> None:
        channel = self.bot.get_channel(self.channel.values[0].id)
        note = self.notice.value
        if len(self.ping.values) == 0:
            ping = ''
        else:
            ping = self.ping.values[0].mention

        description = note
        embed = discord.Embed(title=f'Notice:', description=description, colour=discord.Colour.dark_gold(),
                              timestamp=datetime.now())
        embed.set_footer(text='CordCraft',
                         icon_url='https://media.discordapp.net/attachments/1249069998148812930/1296890029368545332/GunjiCord.png?ex=6713ee76&is=67129cf6&hm=d7787038b655a669e758ccfda1258a217280ec6667b8a341f694134f024e94e9&=&format=webp&quality=lossless&width=384&height=384')
        message = await channel.send(embed=embed, content=ping)
        view = views.DeleteEmbed(message=message)
        await interaction.response.send_message(embed=embed, ephemeral=True, content='The following Embed was sent:',
                                                view=view)
        info_time(f'>STATUS> {interaction.user.name} stated a NOTICE: {note}.')

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        await interaction.response.send_message(
            f'Something unexpected happened while handling this command.\nNoticeModalException: {error}',
            ephemeral=True)
        raise error

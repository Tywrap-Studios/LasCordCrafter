import asyncio
import logging
import time
from typing import Optional

import discord
from aiohttp import ClientSession
from discord.ext import commands

import tasks
import vars
import cogs
import util
from util import info


# Clients
class CordBot(commands.Bot):
    def __init__(
            self,
            *args,
            web_client: ClientSession,
            testing_guild_id: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self._start_time = None

    async def setup_hook(self) -> None:
        info('------------------------------------------Login-------------------------------------------')
        info(f'Logged in as {self.user} (ID: {self.user.id})')
        info('-----------------------------------------Software-----------------------------------------')
        info('''   ____              _  ____            __ _                _        __          ___  
  / ___|___  _ __ __| |/ ___|_ __ __ _ / _| |_ ___ _ __    / |      / /_        / _ \ 
 | |   / _ \| '__/ _` | |   | '__/ _` | |_| __/ _ \ '__|   | |     | '_ \      | | | |
 | |__| (_) | | | (_| | |___| | | (_| |  _| ||  __/ |      | |  _  | (_) |  _  | |_| |
  \____\___/|_|  \__,_|\____|_|  \__,_|_|  \__\___|_|      |_| (_)  \___/  (_)  \___/ ''')
        info('-------------------------------------------Init-------------------------------------------')
        info('Setting Discord Bot Status. . .')
        await self.change_presence(activity=discord.Game('on CordCraft Season 2.'), status=discord.Status.online)
        info(f'Discord Bot Status Set.')
        info(f'Starting Tasks. . .')
        tasks.task_loop.start()
        info(f'Tasks Started.')
        info('Starting Uptime Timer. . .')
        self._start_time = time.time()
        info('Timer Started.')
        info('Registering Cogs. . .')
        await self.add_cog(cogs.CmdCog(self))
        await self.add_cog(cogs.ClaimCog(self))
        await self.add_cog(cogs.NotesCog(self))
        await self.add_cog(cogs.StatusCog(self))
        await self.add_cog(cogs.ThreadCog(self))
        await self.add_cog(cogs.AppealServiceCog(self))
        await self.add_cog(cogs.SanitizeServiceCog(self))
        await self.add_cog(cogs.StandaloneCog(self, self._start_time))
        await self.add_cog(cogs.EventCog(self))
        info('Cogs Registered.')
        info('Syncing Bot Tree. . .')
        await self.tree.sync()
        info('Bot Tree Synced.')
        info('-----------------------------------------Intents------------------------------------------')
        info('''Intents set:
    [X] intents.auto_moderation
    [X] intents.auto_moderation_configuration
    [X] intents.auto_moderation_execution
    [ ] intents.dm_messages
    [ ] intents.dm_reactions
    [X] intents.dm_typing
    [ ] intents.emojis_and_stickers
    [ ] intents.guild_messages
    [ ] intents.guild_reactions
    [ ] intents.guild_scheduled_events
    [ ] intents.guild_typing
    [ ] intents.guilds
    [ ] intents.integrations
    [ ] intents.invites
    [X] intents.members
    [X] intents.message_content
    [ ] intents.moderation
    [ ] intents.presences
    [ ] intents.voice_states
    [ ] intents.webhooks''')
        info('------------------------------Thanks for using CordCrafter!-------------------------------')
        info('')
        info('>> The following messages are messages that are colloquially perceived as "random".')
        info('-------------------------------------CordCrafter Log--------------------------------------')

    def get_start_time(self):
        return self._start_time

    def get_bot(self):
        return self


async def bot_run():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(filename=vars.log_dir_path + 'discord-bot.log', encoding='utf-8', mode='w')
    dt_fmt = '%H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with open(vars.log_dir_path + 'cordcrafter.log', 'w') as file:
        file.write(f'// Log file init at {util.time()}\n\n')

    async with ClientSession() as our_client:
        # Intents
        intents = discord.Intents.default()
        intents.members = True
        intents.dm_messages = True
        intents.message_content = True
        intents.auto_moderation = True
        intents.auto_moderation_configuration = True
        intents.auto_moderation_execution = True
        intents.message_content = True
        async with CordBot(
                '>>',
                web_client=our_client,
                intents=intents
        ) as bot:
            await bot.start(vars.botToken)


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(bot_run())

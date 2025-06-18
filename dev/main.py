import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Optional

import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord.ext import tasks

import database
import vars
import cogs
import util
from util import info, info_time


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
        info('''   _____              _  _____            __ _                __         __        __ 
  / ____|            | |/ ____|          / _| |              /_ |       / /       /_ |
 | |     ___  _ __ __| | |     _ __ __ _| |_| |_ ___ _ __     | |      / /_        | |
 | |    / _ \| '__/ _` | |    | '__/ _` |  _| __/ _ \ '__|    | |     | '_ \       | |
 | |___| (_) | | | (_| | |____| | | (_| | | | ||  __/ |       | |  _  | (_) |  _   | |
  \_____\___/|_|  \__,_|\_____|_|  \__,_|_|  \__\___|_|       |_| (_)  \___/  (_)  |_|''')
        info('-------------------------------------------Init-------------------------------------------')
        info('Checking for old log files. . .')
        log_files = [f for f in os.listdir(vars.log_dir_path) if f.startswith('cordcrafter-')]
        if len(log_files) > vars.max_log_files:
            log_files.sort()
            oldest_log = vars.log_dir_path + log_files[0]
            os.remove(oldest_log)
            info(f'Removed old log file: {log_files[0]}')
        info('All files checked and potentially cleaned.')
        info('Starting Uptime Timer. . .')
        self._start_time = time.time()
        info('Timer Started.')
        info('Starting Background Tasks. . .')
        
        #self.post_bump.start() Tasks are started before boat loads, so stuff like get_channel() may not work because it requires bot to be loaded. Instead, it would be better to start task fter setup hook awaiting on_ready()
        self.check_temp_bans.start()
        info('Background Tasks Started.')
        info('Registering Cogs. . .')
        await self.add_cog(cogs.EventCog(self))
        await self.add_cog(cogs.StandaloneCog(self, self._start_time))
        await self.add_cog(cogs.AppealServiceCog(self))
        await self.add_cog(cogs.SanitizeServiceCog(self))
        await self.add_cog(cogs.ClaimCog(self))
        await self.add_cog(cogs.NotesCog(self))
        await self.add_cog(cogs.CmdCog(self))
        await self.add_cog(cogs.StatusCog(self))
        await self.add_cog(cogs.ThreadCog(self))
        await self.add_cog(cogs.ModCog(self))
        info('Cogs Registered.')
        info('Syncing Bot Tree. . .')
        await self.tree.sync()
        info('Bot Tree Synced.')
        info('-----------------------------------------Database-----------------------------------------')
        info('INFO: Utilizing sqlite3.')
        info('Initializing databases Directory. . .')
        os.makedirs('databases', exist_ok=True)
        info('Directory Initialized.')
        info('Initializing Database(s). . .')
        await database.init_db()
        info('Database(s) Initialized.')
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
        info('---------------------------------------Runtime Log----------------------------------------')
    
    @tasks.loop(hours=4)
    async def post_bump(self):
        forum = self.get_channel(vars.team_forum)
        forum_posts = forum.threads
        trusted_tag = forum.get_tag(vars.trusted_team_tag_id)
        for post in forum_posts:
            if trusted_tag in post.applied_tags:
                msg = await post.send(content='Auto-Bump.')
                await msg.delete()
        info_time(f'>LOG> #{forum.name} posts bumped.')
    
    @tasks.loop(minutes=1)
    async def check_temp_bans(self):
        active_bans = await database.get_active_bans()
        current_time = datetime.now()

        for ban in active_bans:
            user_id, guild_id, unban_time, reason = ban
            unban_datetime = datetime.fromisoformat(unban_time)

            if current_time >= unban_datetime:
                guild = self.get_guild(guild_id)
                try:
                    await guild.unban(discord.Object(id=user_id), reason="A temporary ban expired")
                    await database.remove_temp_ban(user_id)
                    info_time(f'>LOG> Unbanned a Tempban.')
                except discord.HTTPException:
                    info_time(f'>LOG> Something went wrong while Unbanning a Tempban.')
                    continue


async def bot_run():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(filename=vars.log_dir_path + 'discord-bot.log', encoding='utf-8', mode='w')
    dt_fmt = '%H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with open(vars.log_dir_path + util.current_log_file, 'w') as file:
        file.write(f'// Log file init at {util.time()}\n\n')

    async with ClientSession() as client:
        # Intents, do we need all em? NAHHHHH
        intents = discord.Intents.default()
        intents.members = True
        intents.dm_messages = True
        intents.message_content = True
        intents.auto_moderation = True
        intents.auto_moderation_configuration = True
        intents.auto_moderation_execution = True
        intents.message_content = True
        async with CordBot(
                vars.botCommandPrefix,
                web_client=client,
                intents=intents
        ) as bot:
            await bot.start(vars.botToken)


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(bot_run())

from discord.ext import tasks, commands

import util
import vars
from util import info


@tasks.loop(hours=4)
async def task_loop(bot: commands.Bot):
    forum = bot.get_channel(vars.team_forum)
    forum_posts = forum.threads
    trusted_tag = forum.get_tag(vars.trusted_team_tag_id)
    for post in forum_posts:
        if trusted_tag in post.applied_tags:
            msg = await post.send(content='Auto-Bump.')
            await msg.delete()
    info(f'[{util.time()}] >LOG> #{forum.name} posts bumped.')

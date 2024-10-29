from datetime import datetime

with open('C:\\Anaconda\\envs\\LasCordCrafter\\discord-bots\\dev\\logs\\' + 'cordcrafter.log', 'w') as file:
    file.write(f'// Log file init at {datetime.now().strftime("%H:%M:%S")}\n\n')


def info(txt: str):
    with open('C:\\Anaconda\\envs\\LasCordCrafter\\discord-bots\\dev\\logs\\' + 'cordcrafter.log', 'a') as f:
        print(txt)
        f.write(txt + '\n')


info('------------------------------------------Login-------------------------------------------')
info(f'Logged in as User (ID: id)')
info('-----------------------------------------Software-----------------------------------------')
# noinspection PyPep8
info('''   ____              _  ____            __ _                _        __          ___  
  / ___|___  _ __ __| |/ ___|_ __ __ _ / _| |_ ___ _ __    / |      / /_        / _ \ 
 | |   / _ \| '__/ _` | |   | '__/ _` | |_| __/ _ \ '__|   | |     | '_ \      | | | |
 | |__| (_) | | | (_| | |___| | | (_| |  _| ||  __/ |      | |  _  | (_) |  _  | |_| |
  \____\___/|_|  \__,_|\____|_|  \__,_|_|  \__\___|_|      |_| (_)  \___/  (_)  \___/ ''')
info('-------------------------------------------Init-------------------------------------------')
info('Setting Discord Bot Status. . .')
info(f'Discord Bot Status Set.')
info(f'Starting Tasks. . .')
info(f'Tasks Started.')
info('Starting Uptime Timer. . .')
info('Timer Started.')
info('Registering Cogs. . .')
info('Cogs Registered.')
info('Syncing Bot Tree. . .')
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

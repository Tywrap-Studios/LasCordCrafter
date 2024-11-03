import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(verbose=True)
# .env Variables
rcon_pass_env = os.getenv('RCON_PASSWORD')
rcon_host_env = os.getenv('RCON_HOST')
rcon_port_env = os.getenv('RCON_PORT')
rcon_logger_webhook_url_env = os.getenv('RCON_LOGGER_WEBHOOK')
sanitization_webhook_url_env = os.getenv('SAN_LOGGER_WEBHOOK')
botToken_env = os.getenv("CORD_TOKEN")  # Interchangeable, please change for final release. For other devs: Use your own token.
guildInviteLink_env = os.getenv("CORD_INVITE_LINK")
log_filepath_w_env = os.getenv('WINDOWS_LOG_FILE_PATH')
log_filepath_l_env = os.getenv('LINUX_LOG_FILE_PATH')

# File Stuff
log_dir_path = log_filepath_l_env  # Interchangeable

# Webhooks
sanitization_webhook_url = sanitization_webhook_url_env

# Bot Stuff
botToken = botToken_env
botId = '1248280095013998633'  # Interchangeable, please change for final release.
botPing = f'<@{botId}>'
botVersion = 'CordCrafter 1.6.0 [BETA]'  # Interchangeable, please change for final release.
botName = 'CordCrafter'  # Interchangeable, please change for final release.
botDescription = '''This is a Bot made by Tywrap Studios for the GunjiCordia Discord server to help people and others in the wonderful server that is Gunji's that he crafted back in july of 2023'''
botCommandPrefix = '>>'

# Links
guildInviteLink = guildInviteLink_env
privacy_notion = 'https://trusted-substance-f20.notion.site/CordCrafter-bot-Privacy-Notice-7d02fae4b3d64db4b90206b3d92fd9de'

# Regex Patterns
# noinspection SpellCheckingInspection,PyPep8
repat = '(^!|^\.|^\?)'
# noinspection SpellCheckingInspection,PyPep8
repatce = '(!|\.|\?)'
# noinspection SpellCheckingInspection,PyPep8
duregex = '^\d+\w*[smdw]$'


# NOTE THAT CONSTS WITH A COMMENT BEHIND IT SHOULD HAVE THE COMMENTED VALUE ON-RELEASE!
# THE CURRENT VALUES ARE MERELY TEST VALUES!

# Tags
trusted_team_tag_id = 1287179981843206144

# Channels
ipChannel = '<#1238669922641510502>'
techSupportChannel = '<#1188157890117242952>'
logChannel = 1191085319102140528
ticketCategory = 1165265825196945449
ticketLog = 1164581289022722148
spam = 1139925935093727292
team_forum = 1287178984530120715
ctd_channel = 1219383524289941505

# Roles
resigned = 1265790384336801964
discordAdmin = 1160004558609731644
minecraftAdmin = 1191088046695792720
centralHosting = 1272562661451632702
gunjiCord = 1139926170905886853

# Image Links
red_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078349477838899/red_mod_badge.png?ex=6665fe5d&is=6664acdd&hm=832fb33a6ed5fe76ecc7539e56842a526cf3309fc189e59e73b6bb78400eb441&'
green_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078327872852071/green_mod_badge.png?ex=6665fe58&is=6664acd8&hm=d0713da6a04831a28b89db4cfba93cd21a196fe9716dafeb0daa367fb4603d6d&'
blue_badge_image = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249078338484568124/Ongetiteld.png?ex=6665fe5a&is=6664acda&hm=157173744c4ec4e8075d2386b3543419319bda26ae8f21bbdffa60c4d63cae2e&'
red_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085071508639894/red_mc_mod_badge.png?ex=6666049f&is=6664b31f&hm=d9c745c2bf2f872df1cd1b977b42f3408ed46d262e00e5dc58aa9fb7c2a7e54d&'
green_mc_badge = 'https://cdn.discordapp.com/attachments/1249069998148812930/1249085058682458173/green_mc_mod_badge.png?ex=6666049c&is=6664b31c&hm=f8767eed24c7c5565014dd8930141c0b3061611bf63a7a727ba5b4d6938540f9&'

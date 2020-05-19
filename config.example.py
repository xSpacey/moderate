"""
GLOBAL
Global configuration settings.
"""
TOKEN = ""
PREFIX = "!"

"""
COGS
Here, you can specify which cogs should be loaded upon startup. I don't recommend changing these.
"""
COGS = ['cogs.error_handler',
        'cogs.punishment_handler',
        'cogs.history',
        'cogs.ban',
        'cogs.mute',
        'cogs.logs',
        'cogs.automod']

"""
LOGGING
Here, you can specify which events and commands you would like to be logged to a specified logs channel.
"""
LOGGING_CHANNEL = 1234
LOG_JOIN = True
LOG_LEAVE = True
LOG_MUTES = True
LOG_BANS = True
LOG_UNMUTES = True
LOG_UNBANS = True
LOG_AUTOMOD = True

"""
PERMISSIONS
Set roles that can execute commands here. Note that roles aren't hierarchical so all roles need to be specified.
"""
HISTORY_ROLES = ['Staff', 'Admin', 'Owner']
MUTE_ROLES = ['Staff', 'Admin', 'Owner']
BAN_ROLES = ['Admin', 'Owner']

"""
AUTO-MOD
Settings for auto moderation.
"""
LIMITED_URLS = ['discord.gg']
LIMITED_URLS_CHANNELS_ALLOWED = [1234]
BLACKLISTED_URLS = ['bing.com']

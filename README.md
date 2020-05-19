# moderate

moderate is a Discord moderation bot designed to be simple, lightweight and configurable.

Built using Discord.py. Uses SQLite3 for simple database storage.

## Installation
**Requires Python 3.6+, tested with 3.7**

Install dependencies:

`pip install -r requirements.txt`

If you want mutes to be functional, you'll need to create a role called 'Muted' and manually disable 'Send Messages' in each channel.


## Configuration
Edit the values in `config.example.py` and rename to `config.py`:

**Global**
* `TOKEN` - Discord bot token
* `PREFIX` - Bot prefix

**Cogs**
* `COGS` - Edit which cogs or 'modules' are loaded on startup.

**LOGGING**
* `LOGGING_CHANNEL` - ID of the Discord channel where log messages should be sent.
* `LOG_JOIN` - Toggle logging for when a user joins the guild.
* `LOG_LEAVE` - Toggle logging for when a user leaves a guild.
* `LOG_MUTES` - Toggle logging for when a guild member is muted.
* `LOG_BANS` - Toggle logging for when a guild member is banned.
* `LOG_UNMUTES` - Toggle logging for when a guild member is unmuted.
* `LOG_UNBANS` - Toggle logging for when a user is unbanned.
* `LOG_AUTOMOD` - Toggles logging for auto moderation events like editing messages etc.

**PERMISSIONS**

Note: Role permissions aren't hierarchical, so you'll need to specify all roles individually that will need permission. 
* `HISTORY_ROLES` - A list of roles that are allowed to use the history command.
* `MUTE_ROLES` - A list of roles that are allowed to use the mute command.
* `BAN_ROLES` - A list of roles that are allowed to use the ban command.

**AUTO-MOD**
* `LIMITED_URLS` - A list of urls (or strings) that will be deleted unless they are sent in the below channel.
* `LIMITED_URLS_CHANNELS_ALLOWED` - Channels where `LIMITED_URLS` can be sent. Common use case is to only allow people to advertise invite links in certain channels.
* `BLACKLISTED_URLS` - A list of URLs (or strings) that will be deleted if found in a sent message.

## Commands

Note: Time is specified in m/h/d or anything else for a permanent ban. E.g. 1m = 1 minute, 2d = 2 days, perm = perm.
> ban <@member> <time - 1m/1h/1d/perm> \<reason>

Bans the tagged member for the specified amount of time.

> mute <@member> <time - 1m/1h/1d/perm> \<reason>

Mutes the tagged member for the specified amount of time.

> history \<member id>

Gets a users punishment history and displays this as an embed.

## Development

This is an early stage of the bot, I plan on giving it some future updates including support for regex in auto-mod, support for other databases etc. If you'd like to contribute feel free to make a PR or issue.
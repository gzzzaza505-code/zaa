# Drac Bot

A powerful Discord bot with server management, ticket systems, IP-logging verification, and destructive nuke capabilities.

## Features
- **Verification System**: IP-logging verification with automated channel locking.
- **Ticket System**: Private support tickets for users.
- **Nuke Commands**: Various destructive commands (Nuke, Glitch, Ghost, Own, Drain, Freeze, Strip Roles).
- **Protection**: Whitelisted server ID (`1453064260555903225`) cannot be nuked.

## Commands
### Regular
- `/nuke`: Nuke the server.
- `/ticket`: Open a support ticket.
- `/verify`: Verify your identity.

### Premium
- `/glitch`: Role & Channel flood.
- `/ghost`: Silent wipe (Bans + Deletes).
- `/own`: Takeover nicknames and nuke.
- `/drain`: Wipe with data scraping tags.
- `/freeze`: Server-wide lockdown.
- `/strip_roles`: Delete all roles.
- `/premiumnuke`: Wipe with custom messages.

### Owner
- `/setup`: Main configuration panel.
- `/leave_all`: Leave all unauthorized servers.
- `/spam`: Spam a channel.
- `/massdm`: DM everyone in the server.
- `/announce`: Send global or local announcements.
- `/add_premium`: Grant premium to a user.
- `/remove_premium`: Remove premium from a user.

## Configuration
- **Owner IDs**: `1443051529190772768`, `980129921596788736`
- **Whitelisted ID**: `1453064260555903225`
- **Verification Server**: Flask app running on port 5000.

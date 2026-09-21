import discord
from discord.ext import commands
from discord.ui import View, Select, Button
import json
import os
import re
import asyncio
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

# ============================================================
# STEAL A BRAINROT — Full Merged Ticket + Moderation Bot
# Theme matches the banner (gold + neon purple/cyan)
# ============================================================

TOKEN = os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("TOKEN")
PREFIX = "+"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANNERS_DIR = os.path.join(BASE_DIR, "banners")

THEME_COLOR = 0xFFD700
FOOTER_TEXT = "STEAL A BRAINROT • Server Services"
BRAND_NAME = "STEAL A BRAINROT"

# ==================== CHANNELS ====================
LOG_CHANNEL_ID = 1550996038159179898
WELCOME_CHANNEL_ID = 1551280369771225101
INVITE_TRACKER_ID = 1550995989714698451
BOOST_CHANNEL_ID = 1551280619240034314
LEAVES_CHANNEL_ID = 1551280673619443754

# Panel channels (auto-posted on startup)
PANEL_CHANNEL_SUPPORT = 1550996022979858515   # support / scammer / reward / ads / rolls
PANEL_CHANNEL_INDEX = 1550996020572323931     # index panel
PANEL_CHANNEL_MM = 1550996014419288065        # middleman panel
PANEL_CHANNEL_STAFF = 1550996017720074374     # staff applications panel
PANEL_CHANNEL_REACTION = 1551270491665338399  # reaction roles panel

# ==================== REACTION ROLES ====================
REACTION_ROLES = [
    {
        "id": 1550995943028166747,
        "label": "Important Ping",
        "emoji": "🚨",
        "gif": "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif",
    },
    {
        "id": 1550995945640951831,
        "label": "Shop Ping",
        "emoji": "🛒",
        "gif": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
    },
    {
        "id": 1550995948589551746,
        "label": "Poll Ping",
        "emoji": "📊",
        "gif": "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
    },
    {
        "id": 1550995950997348396,
        "label": "Announcement Ping",
        "emoji": "📢",
        "gif": "https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif",
    },
    {
        "id": 1550995954415444068,
        "label": "Dead Chat Ping",
        "emoji": "💤",
        "gif": "https://media.giphy.com/media/3o7aCTPPm4OHfRLSH6/giphy.gif",
    },
    {
        "id": 1551571055129268244,
        "label": "Trade Ping",
        "emoji": "💱",
        "gif": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
    },
    {
        "id": 1551571055166885948,
        "label": "Leaks Ping",
        "emoji": "🔓",
        "gif": "https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif",
    },
    {
        "id": 1551571546789781594,
        "label": "SAB",
        "emoji": "🧠",
        "gif": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    },
]
REACTION_PANEL_GIF = "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif"

# ==================== CATEGORIES ====================
SUPPORT_CATEGORY_ID = 1551278227417202790
SCAMMER_CATEGORY_ID = 1551278311811063908
REWARD_CATEGORY_ID = 1551278391867478027
MM_CATEGORY_ID = 1551278466090139728
INDEX_CATEGORY_ID = 1551278551989489764
RECRUITMENT_CATEGORY_ID = 1551278227417202790
PAY_ROLES_CATEGORY_ID = 1551278772244979763
INDEX_APP_CATEGORY_ID = 1551278848166076508
MM_APP_CATEGORY_ID = 1551278466090139728
INVITE_REWARDS_CHANNEL_ID = 1550995989714698451

# ==================== SPECIAL USERS ====================
SPECIAL_USERS = [
    "1536409975008657500",
    "1532561566271017009",
    "1391635894045380619",
    "1540025216657526796",
]
# Full power (ban / unban / kick / bl / unbl)
BAN_COMMAND_USERS = SPECIAL_USERS[:]          # + the limited user below
KICK_COMMAND_USERS = SPECIAL_USERS[:]
BL_COMMAND_USERS = SPECIAL_USERS[:]           # only full special users

# Limited user: can only ban, unban, kick (no blacklist)
BAN_COMMAND_USERS.append("1495975678863085670")
KICK_COMMAND_USERS.append("1495975678863085670")

# ==================== ROLE HIERARCHY ====================
ROLES = {
    1: {"slots": [{"ids": [1550995784483479606], "names": ["Test Mod", "Test Moderator"]}]},
    2: {"slots": [
        {"ids": [1550995776199589910], "names": ["Moderator"]},
        {"ids": [1550995773481554000], "names": ["Senior Mod", "Senior Moderator"]},
    ]},
    3: {"slots": [
        {"ids": [1550995770931675376], "names": ["Head Staff"]},
        {"ids": [1550995767525769296], "names": ["Head Moderator"]},
    ]},
    4: {"slots": [
        {"ids": [1550995764635902032], "names": ["Admin", "Administrator"]},
        {"ids": [1550995740149555322], "names": ["Vice Manager"]},
        {"ids": [1550995737398083645], "names": ["Server Manager"]},
    ]},
    5: {"slots": [
        {"ids": [1550995734281588776], "names": ["Supervisor"]},
        {"ids": [1550995730053996718], "names": ["Co Owner", "Co-Owner"]},
        {"ids": [1550995725746438254], "names": ["Owners", "Owner"]},
    ]},
    6: {"slots": [
        {"ids": [1550995714828406824], "names": ["Guardian"]},
        {"ids": [1550995712496631818], "names": ["Founder"]},
        {"ids": [1550995708793065563], "names": ["Creator"]},
    ]},
}
ROLE_MANAGE_EXTRA_IDS = [1550995745958658088, 1550995750824050831]

TICKET_TEAM_T1 = "1550995871179735192"
TICKET_TEAM = "1550995873880870962"

MM_ROLES = {
    "cross": "1550995798060433599",
    "og": "1550995795216699543",
    "1b": "1550995800186683464",
    "500m": "1550995803277893642",
    "0-250m": "1550995805479895103",
}
MM_DISPLAY = {
    "cross": "Cross Trades", "og": "OG Trades", "1b": "1B+ Trades",
    "500m": "500M Trades", "0-250m": "0-250M Trades",
}
MM_EMOJIS = {"cross": "🟡", "og": "🥇", "1b": "🥈", "500m": "🥉", "0-250m": "✅"}
ALL_MM_ROLES = list(MM_ROLES.values())

INDEX_ROLES = {
    "crystal": "1550995810752143382", "phantom": "1550995823528247391",
    "cyber": "1550995826417991713", "divine": "1550995830092070992",
    "cursed": "1550995832466047008", "radioactive": "1550995835121311796",
    "yingyang": "1550995837549551830", "galaxy": "1550995840372445215",
    "lava": "1550995843191017513", "candy": "1550995845954928701",
    "rainbow": "1550995848626700438", "diamond": "1550995853651738777",
    "gold": "1550995857023963177",
}
INDEX_PRICES = {
    "crystal": "1x Base Drag (or equivalent value ; collat will be needed)",
    "phantom": "9 garam (or equivalent value ; collat will be needed)",
    "cyber": "9 garam (or equivalent value ; collat will be needed)",
    "divine": "Ask staff for current price (or equivalent value ; collat will be needed)",
    "cursed": "7+ garams (or equivalent value ; collat will be needed)",
    "radioactive": "6+ garams (or equivalent value ; collat will be needed)",
    "yingyang": "5+ garams (or equivalent value ; collat will be needed)",
    "galaxy": "3+ garams (or equivalent value ; collat will be needed)",
    "lava": "3+ garams (or equivalent value ; collat will be needed)",
    "candy": "2+ garams (or equivalent value ; collat will be needed)",
    "rainbow": "5 garams (or equivalent value ; collat will be needed)",
    "diamond": "4 garams (or equivalent value ; collat will be needed)",
    "gold": "3 garams (or equivalent value ; collat will be needed)",
}
INDEX_DISPLAY = {
    "crystal": "Crystal Base", "phantom": "Phantom Base", "cyber": "Cyber Base",
    "divine": "Divine Base", "cursed": "Cursed Base", "radioactive": "Radioactive Base",
    "yingyang": "Yin Yang Base", "galaxy": "Galaxy Base", "lava": "Lava Base",
    "candy": "Candy Base", "rainbow": "Rainbow Base", "diamond": "Diamond Base", "gold": "Gold Base",
}
INDEX_EMOJIS = {
    "crystal": "💎", "phantom": "👻", "cyber": "🤖", "divine": "✨", "cursed": "☠️",
    "radioactive": "☢️", "yingyang": "☯️", "galaxy": "🌌", "lava": "🌋", "candy": "🍬",
    "rainbow": "🌈", "diamond": "💠", "gold": "🟡",
}
ALL_INDEX_ROLES = list(INDEX_ROLES.values())

BOOST_ROLE_ID = 1550995890485985281

STAFF_PANEL_ROLES = [
    "1550995708793065563", "1550995712496631818", "1550995714828406824",
    "1550995725746438254", "1550995730053996718", "1550995734281588776",
    "1550995737398083645", "1550995740149555322", "1550995745958658088", "1550995750824050831",
]
STAFF_CATEGORY_IDS = {
    "recruitment": RECRUITMENT_CATEGORY_ID,
    "payrolls": PAY_ROLES_CATEGORY_ID,
    "indexprovider": INDEX_APP_CATEGORY_ID,
    "mmapplication": MM_APP_CATEGORY_ID,
}

HIGH_STAFF_ROLES = [
    "1550995708793065563", "1550995712496631818", "1550995714828406824",
    "1550995725746438254", "1550995730053996718", "1550995734281588776",
    "1550995737398083645", "1550995740149555322", "1550995764635902032",
]
ADMIN_AND_ABOVE_ROLES = HIGH_STAFF_ROLES[:]
REWARD_STAFF_ROLES = HIGH_STAFF_ROLES[:]
ADS_STAFF_ROLES = [
    "1550995708793065563", "1550995725746438254", "1550995734281588776",
    "1550995737398083645", "1550995740149555322",
]
ROLLS_STAFF_ROLES = ADS_STAFF_ROLES[:]
ALL_STAFF_ROLES = [
    "1550995708793065563", "1550995712496631818", "1550995714828406824",
    "1550995725746438254", "1550995730053996718", "1550995734281588776",
    "1550995737398083645", "1550995740149555322", "1550995764635902032",
    "1550995767525769296", "1550995770931675376", "1550995773481554000",
    "1550995776199589910", "1550995784483479606",
    TICKET_TEAM, TICKET_TEAM_T1,
]

# ==================== ANTI-RAID / ANTI-NUKE ====================
ANTI_NUKE_ENABLED = True
# Max actions of each type in the time window before punishment
ANTI_NUKE_WINDOW = 12          # seconds
ANTI_NUKE_THRESHOLDS = {
    "ban": 3,                  # 3+ bans in window
    "kick": 4,                 # 4+ kicks
    "channel_delete": 2,       # 2+ channel deletes
    "role_delete": 2,          # 2+ role deletes
    "channel_create": 5,       # spam channel create
    "role_create": 5,
    "webhook": 3,
}
# Users/roles immune to anti-nuke (special users + creator always immune)
ANTI_NUKE_IMMUNE_ROLES = [
    "1550995708793065563",  # creator
    "1550995712496631818",  # founder
    "1550995714828406824",  # guardian
    "1550995725746438254",  # owners
]

BLACKLISTED_WORDS = [
    "nigger", "nigga", "faggot", "fag", "tranny", "retard", "retarded",
    "nazi", "hitler", "kike", "chink", "spic", "coon", "beaner",
    "femboy", "d*ck", "dick", "cock", "pussy", "whore", "slut", "hoe",
    "porn", "nudes", "onlyfans",
    "kys", "kill yourself", "kill urself", "hang yourself", "go die",
    "neck yourself", "end yourself",
]
SCAM_WORDS = [
    "free nitro", "discord.gift", "steamcommunity.com/gift",
    "free nitro giveaway", "nitro gift", "claim nitro",
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None, case_insensitive=True)

# ==================== DATA ====================
os.makedirs("data", exist_ok=True)
SANCTIONS_FILE = "data/sanctions.json"
BLACKLIST_FILE = "data/blacklist.json"
SNIPE_FILE = "data/snipe.json"
ROLE_PERMS_FILE = "data/role_perms.json"
TEMPROLES_FILE = "data/temproles.json"
COMMAND_PERMS_FILE = "data/command_perms.json"
LINKED_ALTS_FILE = "data/linked_alts.json"
CONFIG_FILE = "config.json"

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

sanctions_data = load_json(SANCTIONS_FILE, {})
blacklist = load_json(BLACKLIST_FILE, [])
snipe_data = load_json(SNIPE_FILE, {})
clearing_channels = set()
role_perms = load_json(ROLE_PERMS_FILE, {})
temproles_data = load_json(TEMPROLES_FILE, [])
_temprole_tasks = {}
command_overrides = load_json(COMMAND_PERMS_FILE, {})
linked_alts = load_json(LINKED_ALTS_FILE, {})
config = load_json(CONFIG_FILE, {"ticketCounter": 0})

# Anti-nuke action tracker: {guild_id: {user_id: {action: [timestamps...]}}}
_antinuke_actions = {}
_antinuke_punished = set()  # user ids currently being punished (avoid loops)

def save_config():
    save_json(CONFIG_FILE, config)

BAN_FILE = "data/banned_ips.txt"
def load_banned_ips():
    if not os.path.exists(BAN_FILE):
        return set()
    with open(BAN_FILE, "r") as f:
        return {line.strip() for line in f if line.strip()}
def save_banned_ips(ips):
    with open(BAN_FILE, "w") as f:
        for ip in sorted(ips):
            f.write(ip + "\n")
BANNED_IPS = load_banned_ips()

def ban_ip(ip: str) -> str:
    ip = ip.strip()
    if not re.match(r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$", ip):
        return f"Invalid IP: {ip}"
    if ip in BANNED_IPS:
        return f"{ip} is already banned"
    BANNED_IPS.add(ip)
    save_banned_ips(BANNED_IPS)
    return f"Banned {ip} (total: {len(BANNED_IPS)})"

def unban_ip(ip: str) -> str:
    ip = ip.strip()
    if ip not in BANNED_IPS:
        return f"{ip} was not banned"
    BANNED_IPS.discard(ip)
    save_banned_ips(BANNED_IPS)
    return f"Unbanned IP {ip}"

DEFAULT_COMMAND_PERMS = {
    "warn": 1, "tempmute": 1, "unmute": 1, "mutelist": 1, "sanctions": 1, "perms": 1,
    "del": 2, "rolemembers": 2, "clearwarns": 3,
    "derank": 4, "addrole": 4, "delrole": 4, "clear": 4, "lock": 4, "unlock": 4,
    "banlist": 5, "baninfo": 5, "blist": 5, "linkalt": 5,
    "create": 6, "temprole": 6, "syncroles": 6, "modstats": 6, "changeperm": 6,
    "ban": 99, "unban": 99, "kick": 99, "bl": 99, "unbl": 99,
}

def save_sanctions(): save_json(SANCTIONS_FILE, sanctions_data)
def save_blacklist(): save_json(BLACKLIST_FILE, blacklist)
def save_snipe(): save_json(SNIPE_FILE, snipe_data)
def save_role_perms(): save_json(ROLE_PERMS_FILE, role_perms)
def save_temproles(): save_json(TEMPROLES_FILE, temproles_data)
def save_command_perms(): save_json(COMMAND_PERMS_FILE, command_overrides)
def save_linked_alts(): save_json(LINKED_ALTS_FILE, linked_alts)

def get_cmd_perm(name: str) -> int:
    key = name.lower().strip()
    if key in command_overrides:
        val = command_overrides[key]
        if val is None or str(val).lower() == "none":
            return 99
        try:
            return int(val)
        except Exception:
            return DEFAULT_COMMAND_PERMS.get(key, 5)
    return DEFAULT_COMMAND_PERMS.get(key, 5)

# ==================== PERM HELPERS ====================
def _match_role_exact(guild, name):
    name = name.strip()
    if not name:
        return None
    role = discord.utils.find(lambda r, n=name: r.name == n, guild.roles)
    if role:
        return role
    role = discord.utils.find(lambda r, n=name: r.name.lower() == n.lower(), guild.roles)
    if role:
        return role
    return None

def resolve_role_ids(guild, force=False):
    gid = str(guild.id)
    mapping = {}
    used_ids = set()
    for level in sorted(ROLES.keys(), reverse=True):
        entry = ROLES[level]
        found = []
        for slot in entry.get("slots", []):
            picked = None
            for rid in slot.get("ids", []):
                if rid in used_ids:
                    continue
                role = guild.get_role(rid)
                if role is not None:
                    picked = rid
                    break
            if picked is None:
                for name in slot.get("names", []):
                    role = _match_role_exact(guild, name)
                    if role and role.id not in used_ids:
                        picked = role.id
                        break
            if picked is not None:
                found.append(picked)
                used_ids.add(picked)
        mapping[level] = found
    role_perms[gid] = {str(k): v for k, v in mapping.items()}
    save_role_perms()
    return mapping

def get_perm_level(member):
    if str(member.id) in SPECIAL_USERS:
        return 99
    if not member.guild:
        return 0
    cache = resolve_role_ids(member.guild)
    member_ids = {r.id for r in member.roles}
    highest = 0
    for level, role_ids in cache.items():
        if member_ids & set(role_ids):
            highest = max(highest, level)
    return highest

def has_perm(member, level):
    return get_perm_level(member) >= level

def can_moderate(moderator, target):
    if moderator is None or target is None or moderator.id == target.id:
        return False
    if str(moderator.id) in SPECIAL_USERS or moderator.id == moderator.guild.owner_id:
        return True
    if target.id == target.guild.owner_id or str(target.id) in SPECIAL_USERS:
        return False
    mod_level = get_perm_level(moderator)
    target_level = get_perm_level(target)
    if target_level == 0:
        return mod_level >= 1
    return mod_level > target_level

def has_role_manage_extra(member):
    if not member or not getattr(member, "roles", None):
        return False
    return any(r.id in ROLE_MANAGE_EXTRA_IDS for r in member.roles)

def has_staff_permission(member):
    try:
        all_roles = ALL_STAFF_ROLES + ALL_INDEX_ROLES + ALL_MM_ROLES + [str(x) for x in ROLE_MANAGE_EXTRA_IDS]
        return any(str(role.id) in all_roles for role in member.roles) or str(member.id) in SPECIAL_USERS
    except Exception:
        return False

def has_high_staff_permission(member):
    try:
        return any(str(role.id) in HIGH_STAFF_ROLES for role in member.roles) or str(member.id) in SPECIAL_USERS
    except Exception:
        return False

def member_has_any_role(member, role_ids):
    try:
        return any(str(role.id) in [str(r) for r in role_ids] for role in member.roles)
    except Exception:
        return False

# ==================== TICKET HELPERS ====================
def get_ticket_kind(channel):
    if not channel or not channel.category_id:
        return "unknown"
    cat = channel.category_id
    if cat == INDEX_CATEGORY_ID: return "index"
    if cat == MM_CATEGORY_ID: return "mm"
    if cat == SCAMMER_CATEGORY_ID: return "scammer"
    if cat == REWARD_CATEGORY_ID: return "reward"
    if cat == SUPPORT_CATEGORY_ID: return "support"
    if cat in STAFF_CATEGORY_IDS.values(): return "staff"
    return "unknown"

def can_add_or_remove(member, channel):
    kind = get_ticket_kind(channel)
    if kind == "index":
        return False
    if kind == "mm":
        return member_has_any_role(member, ALL_MM_ROLES) or member_has_any_role(member, HIGH_STAFF_ROLES)
    if kind in ("support", "scammer"):
        return (member_has_any_role(member, [TICKET_TEAM, TICKET_TEAM_T1])
                or member_has_any_role(member, ADMIN_AND_ABOVE_ROLES)
                or str(member.id) in SPECIAL_USERS)
    return member_has_any_role(member, ADMIN_AND_ABOVE_ROLES) or str(member.id) in SPECIAL_USERS

def is_ticket_opener(channel, user):
    if not channel.topic or not str(channel.topic).startswith("ticket-"):
        return False
    return str(user.id) == str(channel.topic).replace("ticket-", "")

def clean_channel_name(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9\-]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name[:90] if name else "ticket"

def get_staff_mentions(ticket_type="support"):
    """Who gets pinged when a ticket opens."""
    # Creator, Server Manager, Supervisor, Ticket Team
    CREATOR = "1550995708793065563"
    SERVER_MANAGER = "1550995737398083645"
    SUPERVISOR = "1550995734281588776"
    core = [CREATOR, SERVER_MANAGER, SUPERVISOR, TICKET_TEAM]
    if ticket_type in ("support", "scammer", "reward"):
        return " ".join(f"<@&{r}>" for r in dict.fromkeys(core))
    if ticket_type in ("ads", "rolls"):
        roles = [CREATOR, "1550995725746438254", SUPERVISOR]  # creator, owners, supervisor
        return " ".join(f"<@&{r}>" for r in dict.fromkeys(roles))
    return ""

async def resolve_member(ctx, user_input):
    if ctx.message.mentions:
        return ctx.message.mentions[0]
    user_input = user_input.strip()
    if user_input.isdigit():
        member = ctx.guild.get_member(int(user_input))
        if member:
            return member
        try:
            return await bot.fetch_user(int(user_input))
        except Exception:
            pass
    lower = user_input.lower()
    for m in ctx.guild.members:
        if m.name.lower() == lower or m.display_name.lower() == lower:
            return m
    return None

# ==================== TICKET UI ====================
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Contact Staff", description="Need help? Open a support ticket.", value="support", emoji="🛡️"),
            discord.SelectOption(label="Scammer Report", description="Report a scammer with evidence.", value="scammer", emoji="🚨"),
            discord.SelectOption(label="Claim Reward", description="Won a giveaway? Claim here.", value="reward", emoji="🎁"),
            discord.SelectOption(label="Promote / Ads", description="Advertise your server or content.", value="ads", emoji="📢"),
            discord.SelectOption(label="Pay for Rolls", description="Purchase secure rolls.", value="rolls", emoji="💰"),
        ]
        super().__init__(placeholder="✦ Select a service…", min_values=1, max_values=1, options=options, custom_id="ticket_select")

    async def callback(self, interaction):
        await interaction.response.defer(ephemeral=True)
        await create_ticket(interaction, self.values[0])

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class IndexSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Gold Base", description=INDEX_PRICES["gold"], value="gold", emoji="🟡"),
            discord.SelectOption(label="Diamond Base", description=INDEX_PRICES["diamond"], value="diamond", emoji="💠"),
            discord.SelectOption(label="Rainbow Base", description=INDEX_PRICES["rainbow"], value="rainbow", emoji="🌈"),
            discord.SelectOption(label="Galaxy Base", description=INDEX_PRICES["galaxy"], value="galaxy", emoji="🌌"),
            discord.SelectOption(label="Candy Base", description=INDEX_PRICES["candy"], value="candy", emoji="🍬"),
            discord.SelectOption(label="Lava Base", description=INDEX_PRICES["lava"], value="lava", emoji="🌋"),
            discord.SelectOption(label="Radioactive Base", description=INDEX_PRICES["radioactive"], value="radioactive", emoji="☢️"),
            discord.SelectOption(label="Yin Yang Base", description=INDEX_PRICES["yingyang"], value="yingyang", emoji="☯️"),
            discord.SelectOption(label="Cursed Base", description=INDEX_PRICES["cursed"], value="cursed", emoji="☠️"),
            discord.SelectOption(label="Divine Base", description=INDEX_PRICES["divine"], value="divine", emoji="✨"),
            discord.SelectOption(label="Cyber Base", description=INDEX_PRICES["cyber"], value="cyber", emoji="🤖"),
            discord.SelectOption(label="Phantom Base", description=INDEX_PRICES["phantom"], value="phantom", emoji="👻"),
            discord.SelectOption(label="Crystal Base", description=INDEX_PRICES["crystal"], value="crystal", emoji="💎"),
        ]
        super().__init__(placeholder="✦ Select a base to index…", min_values=1, max_values=1, options=options, custom_id="index_select")

    async def callback(self, interaction):
        await interaction.response.defer(ephemeral=True)
        await create_index_ticket(interaction, self.values[0])

class IndexView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(IndexSelect())

class MiddlemanModal(discord.ui.Modal, title="MiddleMan Request"):
    def __init__(self, trade_type):
        super().__init__()
        self.trade_type = trade_type
        self.trade_with = discord.ui.TextInput(label="Who is the trade with?", placeholder="Ex: @user", required=True, max_length=100)
        self.trade_details = discord.ui.TextInput(label="What is the trade?", placeholder="Ex: Dragon for garamas", required=True, max_length=200)
        self.tip = discord.ui.TextInput(label="What is the tip?", placeholder="Please tip 10% or ticket may be closed.", required=True, max_length=100)
        self.add_item(self.trade_with)
        self.add_item(self.trade_details)
        self.add_item(self.tip)

    async def on_submit(self, interaction):
        await interaction.response.defer(ephemeral=True)
        await create_middleman_ticket(interaction, self.trade_type, self.trade_with.value, self.trade_details.value, self.tip.value)

class MiddlemanSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Cross Trades", description="Cross trade middleman", value="cross", emoji="🟡"),
            discord.SelectOption(label="OG Trades", description="OG trade middleman", value="og", emoji="🥇"),
            discord.SelectOption(label="1B+ Trades", description="1B+ value middleman", value="1b", emoji="🥈"),
            discord.SelectOption(label="500M Trades", description="500M middleman", value="500m", emoji="🥉"),
            discord.SelectOption(label="0-250M Trades", description="0 to 250M middleman", value="0-250m", emoji="✅"),
        ]
        super().__init__(placeholder="✦ Select a trade service…", min_values=1, max_values=1, options=options, custom_id="middleman_select")

    async def callback(self, interaction):
        await interaction.response.send_modal(MiddlemanModal(self.values[0]))

class MiddlemanView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MiddlemanSelect())

class StaffPanelSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Staff Application", description="Apply for a staff position", value="recruitment", emoji="📝"),
            discord.SelectOption(label="Pay for Rolls", description="Purchase secure staff rolls", value="payrolls", emoji="🎟️"),
            discord.SelectOption(label="Index Provider", description="Apply to become an index provider", value="indexprovider", emoji="📦"),
            discord.SelectOption(label="Middleman Application", description="Apply to become a middleman", value="mmapplication", emoji="🤝"),
        ]
        super().__init__(placeholder="✦ Choose a staff option…", min_values=1, max_values=1, options=options, custom_id="staff_panel_select")

    async def callback(self, interaction):
        await interaction.response.defer(ephemeral=True)
        await create_staff_ticket(interaction, self.values[0])

class StaffPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(StaffPanelSelect())

class ReactionRoleButton(Button):
    def __init__(self, role_id: int, label: str, emoji: str, gif: str = None):
        super().__init__(
            label=label,
            emoji=emoji,
            style=discord.ButtonStyle.secondary,
            custom_id=f"rr_{role_id}",
        )
        self.role_id = role_id
        self.gif = gif

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id) if interaction.guild else None
        if role is None:
            return await interaction.response.send_message("Role not found on this server.", ephemeral=True)
        member = interaction.user
        try:
            if role in member.roles:
                await member.remove_roles(role, reason="Reaction role toggle")
                text = f"✅ Removed **{role.name}**"
            else:
                await member.add_roles(role, reason="Reaction role toggle")
                text = f"✅ Added **{role.name}**"

            if self.gif:
                emb = discord.Embed(description=text, color=THEME_COLOR)
                emb.set_image(url=self.gif)
                emb.set_footer(text=FOOTER_TEXT)
                await interaction.response.send_message(embed=emb, ephemeral=True)
            else:
                await interaction.response.send_message(text, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to manage that role.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed: {e}", ephemeral=True)

class ReactionRoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for r in REACTION_ROLES:
            self.add_item(ReactionRoleButton(r["id"], r["label"], r["emoji"], r.get("gif")))

class TicketButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary, emoji="👤", custom_id="ticket_claim")
    async def claim_button(self, interaction, button):
        if is_ticket_opener(interaction.channel, interaction.user):
            return await interaction.response.send_message("You cannot claim your own ticket.", ephemeral=True)
        if not has_staff_permission(interaction.user):
            return await interaction.response.send_message("Only staff can claim tickets.", ephemeral=True)
        embed = interaction.message.embeds[0]
        for field in embed.fields:
            if field.name.lower() == "claimed by":
                return await interaction.response.send_message("This ticket is already claimed.", ephemeral=True)
        embed.add_field(name="Claimed by", value=interaction.user.mention, inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(f"Ticket claimed by {interaction.user.mention}")

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="ticket_close")
    async def close_button(self, interaction, button):
        if not (is_ticket_opener(interaction.channel, interaction.user) or has_staff_permission(interaction.user)):
            return await interaction.response.send_message("Only staff or the ticket owner can close tickets.", ephemeral=True)
        await interaction.response.defer()
        deleted = await close_ticket(interaction.channel, interaction.user)
        if not deleted:
            try:
                await interaction.followup.send("❌ Could not delete channel. Bot needs Manage Channels.", ephemeral=True)
            except Exception:
                pass

# ==================== CREATE TICKETS ====================
async def create_ticket(interaction, ticket_type):
    guild = interaction.guild
    member = interaction.user
    for channel in guild.text_channels:
        if channel.topic == f"ticket-{member.id}":
            return await interaction.followup.send(f"You already have an open ticket: {channel.mention}", ephemeral=True)

    config["ticketCounter"] = config.get("ticketCounter", 0) + 1
    save_config()
    channel_name = clean_channel_name(member.name)

    if ticket_type == "support":
        category_id = SUPPORT_CATEGORY_ID
    elif ticket_type == "scammer":
        category_id = SCAMMER_CATEGORY_ID
    elif ticket_type == "reward":
        category_id = REWARD_CATEGORY_ID
    else:
        category_id = SUPPORT_CATEGORY_ID

    if ticket_type in ("support", "scammer"):
        allowed_roles = [TICKET_TEAM, TICKET_TEAM_T1] + HIGH_STAFF_ROLES
    elif ticket_type == "reward":
        allowed_roles = REWARD_STAFF_ROLES
    elif ticket_type == "ads":
        allowed_roles = ADS_STAFF_ROLES
    else:
        allowed_roles = ROLLS_STAFF_ROLES

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, manage_messages=True),
    }
    for rid in allowed_roles:
        role = guild.get_role(int(rid))
        if role:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True, manage_messages=True)

    category = guild.get_channel(category_id)
    channel = await guild.create_text_channel(name=channel_name, category=category, topic=f"ticket-{member.id}", overwrites=overwrites)

    if ticket_type == "support":
        embed = discord.Embed(title=f"✦ Ticket opened by {member.name}", description="Thank you for contacting **STEAL A BRAINROT** support.\nPlease describe your issue and wait for a response.", color=THEME_COLOR)
    elif ticket_type == "scammer":
        embed = discord.Embed(title=f"✦ Scammer Report — {member.name}", description="**SCAMMER REPORT SERVICE**\n\nPlease follow the format:\n\n`DISCORDIDOFSCAMMER - ID`\n`DISCORDIDOFVICTIM - ID`\n`ROBLOXUSEROFSCAMMER - USER`\n`ROBLOXUSEROFVICTIM - USER`\n\n**Deal:** (ex: Robux for Brainrots)\n**Evidences:** Screens / Records only", color=THEME_COLOR)
    elif ticket_type == "reward":
        embed = discord.Embed(title=f"✦ Reward Claim — {member.name}", description="**REWARD CLAIMING SERVICE**\n\n`DISCORDIDOFWINNER - ID`\n`ROBLOXUSEROFWINNER - USER`\n\n**Prize:**\n**Evidences:**", color=THEME_COLOR)
    elif ticket_type == "ads":
        embed = discord.Embed(title=f"✦ Promote Your Server — {member.name}", description="**📢 Promote Your Server!**\n\n**Package 1:** 2 Days | 1 Ping\n**Package 2:** 3 Days | 2 Pings\n**Package 3:** 7 Days | 4 Pings\n**Package 4:** 12 Days | 6 Pings\n\nTell us which package you want.", color=THEME_COLOR)
    else:
        embed = discord.Embed(title=f"✦ Pay for Rolls — {member.name}", description="**💰 Pay for Rolls**\n\nTell us how many rolls and what you are offering.", color=THEME_COLOR)

    embed.set_footer(text=FOOTER_TEXT)
    await channel.send(content=get_staff_mentions(ticket_type), embed=embed, view=TicketButtons())
    await interaction.followup.send(f"Ticket created: {channel.mention}", ephemeral=True)

async def create_index_ticket(interaction, base_key):
    guild = interaction.guild
    member = interaction.user
    for channel in guild.text_channels:
        if channel.topic == f"ticket-{member.id}":
            return await interaction.followup.send(f"You already have an open ticket: {channel.mention}", ephemeral=True)
    if base_key not in INDEX_ROLES:
        return await interaction.followup.send("Invalid base.", ephemeral=True)

    config["ticketCounter"] = config.get("ticketCounter", 0) + 1
    save_config()
    display_name = INDEX_DISPLAY.get(base_key, base_key.title())
    price = INDEX_PRICES.get(base_key, "Ask staff")
    role_id = INDEX_ROLES[base_key]
    emoji = INDEX_EMOJIS.get(base_key, "📦")
    channel_name = clean_channel_name(display_name)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, manage_messages=True),
    }
    role = guild.get_role(int(role_id))
    if role:
        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True, manage_messages=True)

    category = guild.get_channel(INDEX_CATEGORY_ID)
    if category is None or not isinstance(category, discord.CategoryChannel):
        return await interaction.followup.send(
            f"❌ Index category not found (ID: `{INDEX_CATEGORY_ID}`). Check the category ID and bot permissions.",
            ephemeral=True
        )

    channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        topic=f"ticket-{member.id}",
        overwrites=overwrites
    )

    embed = discord.Embed(
        title=f"{emoji} Index Request: {display_name}",
        description=f"**Ticket opened by {member.mention}**\n\n**Base:** {display_name}\n**Price:** {price}\n\n**Index Base Rules**\n1. PLEASE HAVE AN EMPTY BASE\n2. IF YOU FAIL TO RETURN A BRAINROT THE INDEX WILL BE CANCELED\n3. HIGH VALUE BRAINROTS WILL BE GIVEN ONE AT A TIME\n\nWe only take Garam's+.",
        color=THEME_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    # Ping the specific index role for this base
    await channel.send(content=f"<@&{role_id}>", embed=embed, view=TicketButtons())
    await interaction.followup.send(f"Index ticket created: {channel.mention}", ephemeral=True)

async def create_middleman_ticket(interaction, trade_type, trade_with, trade_details, tip):
    guild = interaction.guild
    member = interaction.user
    for channel in guild.text_channels:
        if channel.topic == f"ticket-{member.id}":
            return await interaction.followup.send(f"You already have an open ticket: {channel.mention}", ephemeral=True)
    if trade_type not in MM_ROLES:
        return await interaction.followup.send("Invalid trade type.", ephemeral=True)

    config["ticketCounter"] = config.get("ticketCounter", 0) + 1
    save_config()
    display_name = MM_DISPLAY.get(trade_type, trade_type)
    role_id = MM_ROLES[trade_type]
    emoji = MM_EMOJIS.get(trade_type, "🤝")
    channel_name = clean_channel_name(display_name)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, manage_messages=True),
    }
    role = guild.get_role(int(role_id))
    if role:
        overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True, manage_messages=True)

    category = guild.get_channel(MM_CATEGORY_ID)
    if category is None or not isinstance(category, discord.CategoryChannel):
        return await interaction.followup.send(
            f"❌ Middleman category not found (ID: `{MM_CATEGORY_ID}`). Check the category ID and bot permissions.",
            ephemeral=True
        )

    channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        topic=f"ticket-{member.id}",
        overwrites=overwrites
    )

    embed = discord.Embed(
        title=f"{emoji} MiddleMan Request: {display_name}",
        description=f"**Ticket opened by {member.mention}**\n\n**Service:** {display_name}\n**Trade with:** {trade_with}\n**Trade:** {trade_details}\n**Tip:** {tip}\n\nA middleman will assist you shortly.",
        color=THEME_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    # Ping the specific middleman role for this trade type
    await channel.send(content=f"<@&{role_id}>", embed=embed, view=TicketButtons())
    await interaction.followup.send(f"MiddleMan ticket created: {channel.mention}", ephemeral=True)

async def create_staff_ticket(interaction, ticket_type):
    guild = interaction.guild
    member = interaction.user
    for channel in guild.text_channels:
        if channel.topic == f"ticket-{member.id}":
            return await interaction.followup.send(f"You already have an open ticket: {channel.mention}", ephemeral=True)

    category_id = STAFF_CATEGORY_IDS.get(ticket_type)
    if not category_id:
        return await interaction.followup.send("Staff category not set.", ephemeral=True)

    config["ticketCounter"] = config.get("ticketCounter", 0) + 1
    save_config()
    channel_name = clean_channel_name(member.name)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, manage_messages=True),
    }
    for rid in STAFF_PANEL_ROLES:
        role = guild.get_role(int(rid))
        if role:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True, manage_messages=True)

    category = guild.get_channel(category_id)
    channel = await guild.create_text_channel(name=channel_name, category=category, topic=f"ticket-{member.id}", overwrites=overwrites)

    recruitment_ping = "<@&1550995750824050831> <@&1550995745958658088>"
    high_staff_ping = "<@&1550995708793065563> <@&1550995712496631818> <@&1550995725746438254> <@&1550995730053996718>"
    ping = recruitment_ping if ticket_type == "recruitment" else high_staff_ping

    if ticket_type == "recruitment":
        embed = discord.Embed(title="📝 Staff Application", description=f"Welcome {member.mention}! Thanks for applying to **STEAL A BRAINROT**.\n\n**Application Form**\n```\n1. Discord Username:\n2. Age:\n3. Fluent in English?\n4. Days active per week:\n5. Hours online per day:\n6. How would you handle a toxic member?\n7. Previous staff experience?\n8. Why do you want to join staff?\n9. Anything else?\n```\nCopy, fill, and send.", color=THEME_COLOR)
        embed.set_footer(text="Staff Recruitment • STEAL A BRAINROT")
    elif ticket_type == "payrolls":
        embed = discord.Embed(title="🎟️ Pay for Rolls", description=f"Ticket opened by {member.mention}\n\n**Staff Pay Rates**\n```\nTest Mod — 2 Garams\nModerator — 3 Garams\nSenior Mod — 4 Garams\nHead Staff — 5 Garams\nAdmin — 7 Garams / 1 Colored Garam\n```\nTell us which role and what you offer.", color=THEME_COLOR)
        embed.set_footer(text="Pay for Rolls • STEAL A BRAINROT")
    elif ticket_type == "indexprovider":
        embed = discord.Embed(title="📦 Index Provider Application", description=f"Welcome {member.mention}!\n\n**Payment & Collat:** 1+ Drag\n\nTell us why you want to be an index provider, how active you are, and any experience.", color=THEME_COLOR)
        embed.set_footer(text="Index Provider • STEAL A BRAINROT")
    else:
        embed = discord.Embed(title="🤝 Middleman Application", description=f"Welcome {member.mention}!\n\n**Payment & Collat:** 1+ Drag\n\nTell us why you want to middleman, how often you can be online, and past experience.", color=THEME_COLOR)
        embed.set_footer(text="Middleman Application • STEAL A BRAINROT")

    await channel.send(content=ping, embed=embed, view=TicketButtons())
    await interaction.followup.send(f"Ticket created: {channel.mention}", ephemeral=True)

async def close_ticket(channel, closer):
    channel_name = channel.name
    channel_id = channel.id
    guild = channel.guild
    try:
        await channel.edit(topic="closed", reason="Ticket closing")
    except Exception:
        pass
    try:
        messages = [msg async for msg in channel.history(limit=50, oldest_first=True)]
        transcript = "---- TICKET LOGS ----\n\n"
        for msg in messages:
            time = msg.created_at.strftime("%d/%m/%Y %H:%M")
            transcript += f"{time} - {msg.author}: {msg.content}\n"
        log_path = f"log_{channel_id}.txt"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(content=f"Ticket closed by {closer.mention}\nChannel: `{channel_name}`", file=discord.File(log_path, filename="log.txt"))
            except Exception:
                pass
        if os.path.exists(log_path):
            os.remove(log_path)
    except Exception as e:
        print(f"Transcript error: {e}")

    for _ in range(5):
        try:
            ch = guild.get_channel(channel_id)
            if ch is None:
                return True
            await ch.delete(reason=f"Ticket closed by {closer}")
            return True
        except discord.NotFound:
            return True
        except discord.Forbidden:
            return False
        except Exception:
            await asyncio.sleep(0.8)
    return False

# ==================== MOD HELPERS ====================
def _blacklist_pattern(word):
    parts = [re.escape(p) for p in word.split() if p] or [re.escape(word)]
    body = r"\s+".join(parts)
    return re.compile(rf"(?<![A-Za-z0-9_]){body}(?![A-Za-z0-9_])", re.IGNORECASE)

def _find_blacklisted(text):
    if not text:
        return []
    hits = []
    for word in sorted(BLACKLISTED_WORDS, key=len, reverse=True):
        if not word:
            continue
        for m in _blacklist_pattern(word).finditer(text):
            hits.append((m.group(0), word))
    return hits

def censor_blacklisted(text):
    if not text:
        return text
    out = text
    for word in sorted(BLACKLISTED_WORDS, key=len, reverse=True):
        if not word:
            continue
        out = _blacklist_pattern(word).sub(lambda m: "•" * len(m.group(0)), out)
    return out

def parse_duration(text):
    match = re.match(r"^(\d+)([smhd])$", text.lower())
    if not match:
        return None
    num, unit = int(match.group(1)), match.group(2)
    if unit == "s": return timedelta(seconds=num)
    if unit == "m": return timedelta(minutes=num)
    if unit == "h": return timedelta(hours=num)
    if unit == "d": return timedelta(days=num)
    return None

def _sort_sanctions_newest_first(lst):
    def _key(s):
        ts = s.get("timestamp")
        if ts:
            try:
                return datetime.fromisoformat(ts)
            except Exception:
                pass
        return datetime.min.replace(tzinfo=timezone.utc)
    return sorted(lst, key=_key, reverse=True)

def add_sanction(user_id, reason, mod_id):
    uid = str(user_id)
    if uid not in sanctions_data:
        sanctions_data[uid] = []
    now = datetime.now(timezone.utc)
    entry = {"id": len(sanctions_data[uid]) + 1, "reason": reason, "date": now.strftime("%d/%m/%Y %H:%M"), "timestamp": now.isoformat(), "moderator": str(mod_id)}
    sanctions_data[uid].append(entry)
    save_sanctions()
    return entry

async def get_target(ctx, arg=None):
    if ctx.message.mentions:
        return ctx.message.mentions[0]
    if ctx.message.reference:
        ref = ctx.message.reference
        if ref.resolved and hasattr(ref.resolved, "author"):
            return ref.resolved.author
        if ref.message_id:
            try:
                msg = await ctx.channel.fetch_message(ref.message_id)
                return msg.author
            except Exception:
                pass
    if arg:
        arg = arg.strip()
        if arg.isdigit():
            try:
                return await bot.fetch_user(int(arg))
            except Exception:
                pass
        if ctx.guild:
            lower = arg.lower()
            for m in ctx.guild.members:
                if m.name.lower() == lower or (m.display_name and m.display_name.lower() == lower):
                    return m
    return None

async def get_member(guild, user):
    if user is None or guild is None:
        return None
    uid = getattr(user, "id", user)
    try:
        uid = int(uid)
    except Exception:
        return None
    member = guild.get_member(uid)
    if member:
        return member
    try:
        return await guild.fetch_member(uid)
    except Exception:
        return None

def find_role(guild, query):
    """Find role by ID, exact name, partial name, or common short forms."""
    if not query or not guild:
        return None
    query = query.strip()
    # Strip role mention
    if query.startswith("<@&") and query.endswith(">"):
        query = query[3:-1]
    if query.isdigit():
        role = guild.get_role(int(query))
        if role:
            return role
    q = query.lower()
    # 1) Exact name
    role = discord.utils.find(lambda r: r.name.lower() == q, guild.roles)
    if role:
        return role
    # 2) Exact after stripping brackets/prefixes like "[ H ] • "
    def clean(n):
        n = n.lower()
        if "•" in n:
            n = n.split("•")[-1].strip()
        n = n.replace("[", " ").replace("]", " ")
        return " ".join(n.split())
    role = discord.utils.find(lambda r: clean(r.name) == q, guild.roles)
    if role:
        return role
    # 3) Substring match (prefer shortest role name = best match)
    matches = [r for r in guild.roles if q in r.name.lower() or q in clean(r.name)]
    if matches:
        matches.sort(key=lambda r: len(r.name))
        return matches[0]
    # 4) All words present (order independent) e.g. "head recruitment" -> "Head of Recruitment"
    words = [w for w in q.replace("-", " ").split() if w and w not in ("of", "the", "and")]
    if words:
        candidates = []
        for r in guild.roles:
            rn = clean(r.name)
            if all(w in rn for w in words):
                candidates.append(r)
        if candidates:
            candidates.sort(key=lambda r: len(r.name))
            return candidates[0]
    return None

CMD_FAIL_MSG = "I'm sorry this command you tried to use is not going to work with your perm or u just did the command wrong — STEAL A BRAINROT"

async def cmd_fail(ctx):
    try:
        await ctx.send(CMD_FAIL_MSG)
    except Exception:
        pass

async def cmd_usage(ctx, text):
    try:
        await ctx.send(f"Usage: {text}")
    except Exception:
        pass

async def empty_result(ctx, text):
    try:
        emb = discord.Embed(description=text, color=THEME_COLOR, timestamp=datetime.now(timezone.utc))
        emb.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=emb)
    except Exception:
        pass

async def send_log(embed):
    ch = bot.get_channel(LOG_CHANNEL_ID)
    if ch is None:
        try:
            ch = await bot.fetch_channel(LOG_CHANNEL_ID)
        except Exception:
            return
    try:
        await ch.send(embed=embed)
    except Exception:
        pass

def _temprole_key(gid, uid, rid):
    return f"{gid}:{uid}:{rid}"

async def _remove_temprole(gid, uid, rid):
    key = _temprole_key(gid, uid, rid)
    _temprole_tasks.pop(key, None)
    global temproles_data
    temproles_data = [e for e in temproles_data if not (e.get("guild_id") == gid and e.get("user_id") == uid and e.get("role_id") == rid)]
    save_temproles()
    guild = bot.get_guild(gid)
    if not guild:
        return
    member = guild.get_member(uid)
    if not member:
        try:
            member = await guild.fetch_member(uid)
        except Exception:
            return
    role = guild.get_role(rid)
    if not role or role not in member.roles:
        return
    try:
        await member.remove_roles(role, reason="Temporary role expired")
    except Exception:
        pass

def schedule_temprole(gid, uid, rid, ends_at):
    key = _temprole_key(gid, uid, rid)
    old = _temprole_tasks.pop(key, None)
    if old and not old.done():
        old.cancel()
    now = datetime.now(timezone.utc)
    if ends_at.tzinfo is None:
        ends_at = ends_at.replace(tzinfo=timezone.utc)
    delay = max(0, (ends_at - now).total_seconds())
    async def _runner():
        try:
            await asyncio.sleep(delay)
            await _remove_temprole(gid, uid, rid)
        except asyncio.CancelledError:
            return
    _temprole_tasks[key] = asyncio.create_task(_runner())
    global temproles_data
    temproles_data = [e for e in temproles_data if not (e.get("guild_id") == gid and e.get("user_id") == uid and e.get("role_id") == rid)]
    temproles_data.append({"guild_id": gid, "user_id": uid, "role_id": rid, "ends_at": ends_at.isoformat()})
    save_temproles()

async def restore_temproles():
    now = datetime.now(timezone.utc)
    for entry in list(temproles_data):
        try:
            gid, uid, rid = int(entry["guild_id"]), int(entry["user_id"]), int(entry["role_id"])
            ends = datetime.fromisoformat(entry["ends_at"])
            if ends.tzinfo is None:
                ends = ends.replace(tzinfo=timezone.utc)
            if ends <= now:
                await _remove_temprole(gid, uid, rid)
            else:
                schedule_temprole(gid, uid, rid, ends)
        except Exception as e:
            print(f"temprole restore error: {e}")

async def filter_bad_content(message):
    if not message.guild or message.author.bot:
        return False
    content = message.content or ""
    if not content:
        return False
    content_lower = content.lower()
    member = message.guild.get_member(message.author.id)
    if member and has_perm(member, 5):
        return False
    async def _warn(text):
        try:
            m = await message.channel.send(text)
            await m.delete(delay=3)
        except Exception:
            pass
    for word in SCAM_WORDS:
        if word in content_lower:
            try:
                await message.delete()
            except Exception:
                pass
            add_sanction(message.author.id, "link", bot.user.id if bot.user else 0)
            await _warn(f"{message.author.mention} this a some bad things you got going")
            return True
    hits = _find_blacklisted(content)
    if hits:
        try:
            await message.delete()
        except Exception:
            pass
        add_sanction(message.author.id, "bad word", bot.user.id if bot.user else 0)
        await _warn(f"{message.author.mention} you said a blacklisted word")
        return True
    return False

# ==================== AUTO PANEL POSTER ====================
async def _clear_bot_messages(channel, limit=15):
    """Remove previous panel messages from this bot so panels reset cleanly."""
    try:
        def is_me(m):
            return m.author.id == bot.user.id
        await channel.purge(limit=limit, check=is_me)
    except Exception as e:
        print(f"Could not clear old panels in {getattr(channel, 'id', '?')}: {e}")

async def post_panels():
    """Post / refresh all service panels on startup (clears old ones first)."""
    # Support panel
    try:
        ch = bot.get_channel(PANEL_CHANNEL_SUPPORT) or await bot.fetch_channel(PANEL_CHANNEL_SUPPORT)
        await _clear_bot_messages(ch)
        embed = discord.Embed(
            title="✦ Server Services — STEAL A BRAINROT",
            description=(
                "**SERVICES**\n"
                "Use the menu below to open a private ticket.\n\n"
                "🛡️ **Contact Staff** — General support\n"
                "🚨 **Scammer Report** — Report scammers\n"
                "🎁 **Claim Reward** — Claim giveaway prizes\n"
                "📢 **Promote / Ads** — Paid ads / promotions\n"
                "💰 **Pay for Rolls** — Purchase rolls\n\n"
                "*STEAL A BRAINROT*"
            ),
            color=THEME_COLOR
        )
        embed.set_image(url="attachment://server_services.jpg")
        embed.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "server_services.jpg"), filename="server_services.jpg")
        await ch.send(embed=embed, view=TicketView(), file=file)
        print(f"Support panel posted in {PANEL_CHANNEL_SUPPORT}")
    except Exception as e:
        print(f"Failed to post support panel: {e}")

    # Index panel
    try:
        ch = bot.get_channel(PANEL_CHANNEL_INDEX) or await bot.fetch_channel(PANEL_CHANNEL_INDEX)
        await _clear_bot_messages(ch)
        embed = discord.Embed(
            title="✦ Index Department — STEAL A BRAINROT",
            description=(
                "Request an indexing service by selecting a base below.\n\n"
                "🟡 Gold  💠 Diamond  🌈 Rainbow  🌌 Galaxy\n"
                "🍬 Candy  🌋 Lava  ☢️ Radioactive  ☯️ Yin Yang\n"
                "☠️ Cursed  ✨ Divine  🤖 Cyber  👻 Phantom  💎 Crystal\n\n"
                "**Rules**\n"
                "1. PLEASE HAVE AN EMPTY BASE\n"
                "2. FAIL TO RETURN A BRAINROT = INDEX CANCELED\n"
                "3. HIGH VALUE ITEMS ONE AT A TIME\n\n"
                "We only take Garam's+ — no lowballs."
            ),
            color=THEME_COLOR
        )
        embed.set_image(url="attachment://index_department.jpg")
        embed.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "index_department.jpg"), filename="index_department.jpg")
        await ch.send(embed=embed, view=IndexView(), file=file)
        print(f"Index panel posted in {PANEL_CHANNEL_INDEX}")
    except Exception as e:
        print(f"Failed to post index panel: {e}")

    # Middleman panel
    try:
        ch = bot.get_channel(PANEL_CHANNEL_MM) or await bot.fetch_channel(PANEL_CHANNEL_MM)
        await _clear_bot_messages(ch)
        embed = discord.Embed(
            title="✦ Middleman (MM) — STEAL A BRAINROT",
            description=(
                "**SERVICES**\n"
                "Middleman (MM) — secure trade service\n\n"
                "• **Cross Trades** 🟡\n"
                "• **OG Trades** 🥇\n"
                "• **1B+ Trades** 🥈\n"
                "• **500M Trades** 🥉\n"
                "• **0-250M Trades** ✅\n\n"
                "*STEAL A BRAINROT*"
            ),
            color=THEME_COLOR
        )
        embed.set_image(url="attachment://middleman.jpg")
        embed.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "middleman.jpg"), filename="middleman.jpg")
        await ch.send(embed=embed, view=MiddlemanView(), file=file)
        print(f"Middleman panel posted in {PANEL_CHANNEL_MM}")
    except Exception as e:
        print(f"Failed to post middleman panel: {e}")

    # Staff / Applications panel
    try:
        ch = bot.get_channel(PANEL_CHANNEL_STAFF) or await bot.fetch_channel(PANEL_CHANNEL_STAFF)
        await _clear_bot_messages(ch)
        embed = discord.Embed(
            title="✦ Staff & Team Opportunities — STEAL A BRAINROT",
            description=(
                "Interested in joining the team?\n"
                "Pick an option below to open a private ticket.\n\n"
                "📝 **Staff Application** — Apply for a staff position\n"
                "🎟️ **Pay for Rolls** — Purchase secure staff rolls\n"
                "📦 **Index Provider** — Apply to become an index provider\n"
                "🤝 **Middleman Application** — Apply to become a middleman\n\n"
                "Our team will review every request carefully."
            ),
            color=THEME_COLOR
        )
        embed.set_image(url="attachment://staff_applications.jpg")
        embed.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "staff_applications.jpg"), filename="staff_applications.jpg")
        await ch.send(embed=embed, view=StaffPanelView(), file=file)
        print(f"Staff panel posted in {PANEL_CHANNEL_STAFF}")
    except Exception as e:
        print(f"Failed to post staff panel: {e}")

    # Reaction roles panel
    try:
        ch = bot.get_channel(PANEL_CHANNEL_REACTION) or await bot.fetch_channel(PANEL_CHANNEL_REACTION)
        await _clear_bot_messages(ch)
        embed = discord.Embed(
            title="✦ Reaction Roles — STEAL A BRAINROT",
            description=(
                "Click the buttons below to **toggle** notification roles.\n\n"
                "Get pinged only for the things you care about!\n\n"
                "🚨 **Important**  ·  🛒 **Shop**  ·  📊 **Poll**  ·  📢 **Announcement**\n"
                "💤 **Dead Chat**  ·  💱 **Trade**  ·  🔓 **Leaks**  ·  🧠 **SAB**"
            ),
            color=THEME_COLOR
        )
        embed.set_image(url="attachment://reaction_roles.jpg")
        embed.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "reaction_roles.jpg"), filename="reaction_roles.jpg")
        await ch.send(embed=embed, view=ReactionRoleView(), file=file)
        print(f"Reaction roles panel posted in {PANEL_CHANNEL_REACTION}")
    except Exception as e:
        print(f"Failed to post reaction roles panel: {e}")


# ==================== ANTI-NUKE HELPERS ====================
def _antinuke_is_immune(member) -> bool:
    if not member:
        return True
    if str(member.id) in SPECIAL_USERS:
        return True
    if getattr(member, "bot", False):
        return True
    if member.guild and member.id == member.guild.owner_id:
        return True
    try:
        if any(str(r.id) in ANTI_NUKE_IMMUNE_ROLES for r in member.roles):
            return True
    except Exception:
        pass
    return False

def _antinuke_record(guild_id: int, user_id: int, action: str) -> int:
    """Record an action and return count in the current window."""
    now = datetime.now(timezone.utc).timestamp()
    g = _antinuke_actions.setdefault(guild_id, {})
    u = g.setdefault(user_id, {})
    times = u.setdefault(action, [])
    # Drop old timestamps
    cutoff = now - ANTI_NUKE_WINDOW
    times[:] = [t for t in times if t >= cutoff]
    times.append(now)
    return len(times)

async def _antinuke_punish(guild: discord.Guild, member: discord.Member, action: str, count: int):
    """Strip dangerous roles and log. Tries timeout + remove all roles above everyone."""
    if not ANTI_NUKE_ENABLED or not member or not guild:
        return
    key = f"{guild.id}:{member.id}"
    if key in _antinuke_punished:
        return
    _antinuke_punished.add(key)
    try:
        # Timeout 1 hour if possible
        try:
            await member.timeout(datetime.now(timezone.utc) + timedelta(hours=1), reason=f"Anti-nuke: mass {action}")
        except Exception:
            pass
        # Remove all roles the bot can remove (except @everyone)
        removable = [
            r for r in member.roles
            if r != guild.default_role
            and not r.managed
            and r < guild.me.top_role
        ]
        if removable:
            try:
                await member.remove_roles(*removable, reason=f"Anti-nuke: mass {action} ({count} in {ANTI_NUKE_WINDOW}s)")
            except Exception:
                for r in removable:
                    try:
                        await member.remove_roles(r, reason=f"Anti-nuke: mass {action}")
                    except Exception:
                        pass
        # Log
        emb = discord.Embed(
            title="🚨 ANTI-NUKE TRIGGERED — STEAL A BRAINROT",
            description=(
                f"**User:** {member.mention} (`{member.id}`)\n"
                f"**Action:** mass `{action}`\n"
                f"**Count:** `{count}` in `{ANTI_NUKE_WINDOW}s`\n"
                f"**Response:** roles stripped + 1h timeout\n\n"
                f"Review this account immediately."
            ),
            color=0xFF0000,
            timestamp=datetime.now(timezone.utc),
        )
        emb.set_footer(text=FOOTER_TEXT)
        # Ping creators / owners
        ping = " ".join(f"<@&{r}>" for r in ["1550995708793065563", "1550995725746438254"])
        ch = bot.get_channel(LOG_CHANNEL_ID)
        if ch:
            try:
                await ch.send(content=ping, embed=emb)
            except Exception:
                pass
        print(f"[ANTI-NUKE] Punished {member} for mass {action} ({count})")
    finally:
        # Allow future triggers after a short delay
        await asyncio.sleep(5)
        _antinuke_punished.discard(key)

async def _antinuke_check(guild: discord.Guild, user: discord.abc.User, action: str):
    if not ANTI_NUKE_ENABLED or not guild or not user:
        return
    threshold = ANTI_NUKE_THRESHOLDS.get(action)
    if not threshold:
        return
    member = guild.get_member(user.id)
    if member is None:
        try:
            member = await guild.fetch_member(user.id)
        except Exception:
            return
    if _antinuke_is_immune(member):
        return
    count = _antinuke_record(guild.id, user.id, action)
    if count >= threshold:
        await _antinuke_punish(guild, member, action, count)

# ==================== EVENTS ====================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("STEAL A BRAINROT bot is ready!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name="STEAL A BRAINROT", url="https://www.twitch.tv/discord"))
    for guild in bot.guilds:
        try:
            resolve_role_ids(guild)
        except Exception as e:
            print(f"Role resolve failed: {e}")
    try:
        await restore_temproles()
    except Exception as e:
        print(f"Temp role restore failed: {e}")

    bot.add_view(TicketView())
    bot.add_view(TicketButtons())
    bot.add_view(IndexView())
    bot.add_view(MiddlemanView())
    bot.add_view(StaffPanelView())
    bot.add_view(ReactionRoleView())

    # Auto-post all panels
    await post_panels()

@bot.event
async def on_member_ban(guild, user):
    try:
        # Find who banned via audit log
        await asyncio.sleep(0.6)
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.ban):
            if entry.target and entry.target.id == user.id:
                await _antinuke_check(guild, entry.user, "ban")
                break
    except Exception as e:
        print(f"anti-nuke ban track error: {e}")

@bot.event
async def on_guild_channel_delete(channel):
    try:
        guild = channel.guild
        await asyncio.sleep(0.6)
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.channel_delete):
            if entry.target and getattr(entry.target, "id", None) == channel.id:
                await _antinuke_check(guild, entry.user, "channel_delete")
                break
    except Exception as e:
        print(f"anti-nuke channel_delete error: {e}")

@bot.event
async def on_guild_channel_create(channel):
    try:
        guild = channel.guild
        await asyncio.sleep(0.6)
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.channel_create):
            if entry.target and getattr(entry.target, "id", None) == channel.id:
                await _antinuke_check(guild, entry.user, "channel_create")
                break
    except Exception as e:
        print(f"anti-nuke channel_create error: {e}")

@bot.event
async def on_guild_role_delete(role):
    try:
        guild = role.guild
        await asyncio.sleep(0.6)
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.role_delete):
            if entry.target and getattr(entry.target, "id", None) == role.id:
                await _antinuke_check(guild, entry.user, "role_delete")
                break
    except Exception as e:
        print(f"anti-nuke role_delete error: {e}")

@bot.event
async def on_guild_role_create(role):
    try:
        guild = role.guild
        await asyncio.sleep(0.6)
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.role_create):
            if entry.target and getattr(entry.target, "id", None) == role.id:
                await _antinuke_check(guild, entry.user, "role_create")
                break
    except Exception as e:
        print(f"anti-nuke role_create error: {e}")

@bot.event
async def on_webhooks_update(channel):
    try:
        guild = channel.guild
        await asyncio.sleep(0.6)
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.webhook_create):
            await _antinuke_check(guild, entry.user, "webhook")
            break
    except Exception as e:
        print(f"anti-nuke webhook error: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        content = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
        if len(content) < 3:
            await message.channel.send(f"My prefix on this server is: `{PREFIX}`")
            return
    if await filter_bad_content(message):
        return
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.author.bot or not message.guild or message.channel.id in clearing_channels:
        return
    content = message.content or "*no text*"
    snipe_data[str(message.channel.id)] = {
        "content": content,
        "author": str(message.author),
        "author_id": message.author.id,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    save_snipe()

@bot.event
async def on_member_join(member):
    if str(member.id) in blacklist:
        try:
            await member.ban(reason="Blacklisted (auto on join)")
        except Exception:
            pass
        return
    try:
        ch = bot.get_channel(WELCOME_CHANNEL_ID) or await bot.fetch_channel(WELCOME_CHANNEL_ID)
        emb = discord.Embed(
            title="✦ New Member Joined!",
            description=f"👏 Welcome {member.mention} to **{BRAND_NAME}**!",
            color=THEME_COLOR,
            timestamp=datetime.now(timezone.utc)
        )
        emb.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, "R"), inline=True)
        emb.set_thumbnail(url=member.display_avatar.url)
        emb.set_image(url="attachment://welcome.jpg")
        emb.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "welcome.jpg"), filename="welcome.jpg")
        await ch.send(embed=emb, file=file)
    except Exception as e:
        print(f"Welcome failed: {e}")

@bot.event
async def on_member_remove(member):
    # Anti-nuke: detect kicks via audit log
    try:
        await asyncio.sleep(0.6)
        async for entry in member.guild.audit_logs(limit=3, action=discord.AuditLogAction.kick):
            if entry.target and entry.target.id == member.id:
                await _antinuke_check(member.guild, entry.user, "kick")
                break
    except Exception as e:
        print(f"anti-nuke kick track error: {e}")
    # Leave log
    try:
        ch = bot.get_channel(LEAVES_CHANNEL_ID) or await bot.fetch_channel(LEAVES_CHANNEL_ID)
        emb = discord.Embed(
            title="✦ Member Left",
            description=f"👋 **{member}** has left **{BRAND_NAME}**.",
            color=THEME_COLOR,
            timestamp=datetime.now(timezone.utc)
        )
        emb.set_thumbnail(url=member.display_avatar.url)
        emb.set_image(url="attachment://leaves.jpg")
        emb.set_footer(text=FOOTER_TEXT)
        file = discord.File(os.path.join(BANNERS_DIR, "leaves.jpg"), filename="leaves.jpg")
        await ch.send(embed=emb, file=file)
    except Exception as e:
        print(f"Leave failed: {e}")

@bot.event
async def on_member_update(before, after):
    try:
        if before.premium_since is None and after.premium_since is not None:
            role = after.guild.get_role(BOOST_ROLE_ID)
            if role and role not in after.roles:
                try:
                    await after.add_roles(role, reason="Server boost — VIP")
                except Exception:
                    pass
            emb = discord.Embed(title=f"✦ Thank you for boosting! — {BRAND_NAME}", description=f"{after.mention} boosted the server and received 💎 **VIP**!", color=THEME_COLOR, timestamp=datetime.now(timezone.utc))
            emb.set_thumbnail(url=after.display_avatar.url)
            emb.set_footer(text=FOOTER_TEXT)
            ch = bot.get_channel(BOOST_CHANNEL_ID) or await bot.fetch_channel(BOOST_CHANNEL_ID)
            await ch.send(content=after.mention, embed=emb)
    except Exception as e:
        print(f"Boost error: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound, commands.MissingPermissions)):
        return
    if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument, commands.UserInputError)):
        await cmd_fail(ctx)

# ==================== COMMANDS ====================
@bot.command()
async def ping(ctx):
    emb = discord.Embed(title=f"✦ Pong — {BRAND_NAME}", description=f"Latency: **`{round(bot.latency*1000)}ms`**", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def help(ctx):
    emb = discord.Embed(
        title=f"✦ {BRAND_NAME} Help",
        description=(
            f"**Prefix:** `{PREFIX}`\n"
            "Higher perm can use lower perm commands.\n\n"
            "**Everyone**\n"
            "`+help` `+ping` `+userinfo` `+serverinfo` `+snipe`\n\n"
            "**Perm 1**\n"
            "`+warn` `+tempmute` `+unmute` `+mutelist` `+sanctions` `+perms`\n\n"
            "**Perm 2**\n"
            "`+del sanction`\n\n"
            "**Perm 3**\n"
            "`+clearwarns`\n\n"
            "**Perm 4**\n"
            "`+clear` `+lock` `+unlock` `+derank` `+addrole` `+delrole`\n\n"
            "**Perm 5**\n"
            "`+banlist` `+baninfo` `+blist` `+linkalt`\n\n"
            "**Perm 6**\n"
            "`+temprole` `+modstats` `+syncroles` `+create` `+changeperm`\n\n"
            "**Special Users only**\n"
            "`+ban` `+unban` `+kick` `+bl` `+unbl`\n\n"
            "**Tickets (staff)**\n"
            "`+claim` `+close` `+rename` `+add` `+remove` `+commands`"
        ),
        color=THEME_COLOR
    )
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command(name="antinuke")
async def antinuke_cmd(ctx, mode: str = None):
    """+antinuke [on|off|status] — toggle or view anti-nuke (Perm 6 / Special)."""
    global ANTI_NUKE_ENABLED
    if str(ctx.author.id) not in SPECIAL_USERS and not has_perm(ctx.author, 6):
        return await cmd_fail(ctx)
    if mode is None or mode.lower() in ("status", "info"):
        lines = [f"**Enabled:** `{ANTI_NUKE_ENABLED}`", f"**Window:** `{ANTI_NUKE_WINDOW}s`", "", "**Thresholds:**"]
        for k, v in ANTI_NUKE_THRESHOLDS.items():
            lines.append(f"• `{k}` → {v}")
        emb = discord.Embed(title=f"✦ Anti-Nuke — {BRAND_NAME}", description="\n".join(lines), color=THEME_COLOR)
        emb.set_footer(text=FOOTER_TEXT)
        return await ctx.send(embed=emb)
    m = mode.lower()
    if m in ("on", "enable", "true", "1"):
        ANTI_NUKE_ENABLED = True
        return await ctx.send(embed=discord.Embed(description="✅ Anti-nuke **enabled**.", color=THEME_COLOR))
    if m in ("off", "disable", "false", "0"):
        ANTI_NUKE_ENABLED = False
        return await ctx.send(embed=discord.Embed(description="⚠️ Anti-nuke **disabled**.", color=0xFFAA00))
    return await cmd_usage(ctx, "`+antinuke [on|off|status]`")

@bot.command()
async def perms(ctx):
    cache = resolve_role_ids(ctx.guild)
    emb = discord.Embed(title=f"✦ {BRAND_NAME} Permissions", color=THEME_COLOR)
    for level in sorted(ROLES.keys()):
        mentions = [ctx.guild.get_role(rid).mention for rid in cache.get(level, []) if ctx.guild.get_role(rid)]
        emb.add_field(name=f"▸ Perm {level}", value="\n".join(mentions) or "*None*", inline=False)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb, allowed_mentions=discord.AllowedMentions.none())

@bot.command()
async def snipe(ctx):
    data = snipe_data.get(str(ctx.channel.id))
    if not data:
        return await empty_result(ctx, "Nothing to snipe.")
    emb = discord.Embed(title=f"✦ Snipe — {BRAND_NAME}", description=censor_blacklisted(data.get("content") or ""), color=THEME_COLOR)
    emb.add_field(name="Author", value=data["author"], inline=True)
    emb.add_field(name="Deleted", value=data.get("time", "?"), inline=True)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command(aliases=["warns"])
async def sanctions(ctx, *, target: str = None):
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    elif ctx.message.reference:
        user = await get_target(ctx, None)
    elif target:
        user = await get_target(ctx, target)
    user = user or ctx.author
    uid = str(user.id)
    lst = sanctions_data.get(uid, [])
    if not lst:
        emb = discord.Embed(description="No sanctions received", color=THEME_COLOR)
        emb.set_author(name=str(user), icon_url=user.display_avatar.url)
        emb.set_footer(text=FOOTER_TEXT)
        return await ctx.send(embed=emb)
    ordered = _sort_sanctions_newest_first(lst)
    lines = [f"**{i}.** `{s.get('date','?')}`\n↳ {s.get('reason','No reason')}" for i, s in enumerate(ordered, 1)]
    emb = discord.Embed(title=f"✦ Sanctions — {BRAND_NAME}", description="\n\n".join(lines)[:4000], color=THEME_COLOR)
    emb.set_author(name=str(user), icon_url=user.display_avatar.url)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def warn(ctx, *, args=None):
    if not has_perm(ctx.author, get_cmd_perm("warn")):
        return await cmd_fail(ctx)
    user = None
    reason = "No reason provided"
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        if args:
            reason = args
            for m in ctx.message.mentions:
                reason = reason.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
            reason = reason.strip() or "No reason provided"
    elif ctx.message.reference:
        user = await get_target(ctx, None)
        if args:
            reason = args.strip() or "No reason provided"
    elif args:
        parts = args.split(None, 1)
        user = await get_target(ctx, parts[0])
        if user and len(parts) > 1:
            reason = parts[1]
    if not user:
        return await cmd_usage(ctx, "`+warn <@member> [reason]`")
    target_member = await get_member(ctx.guild, user)
    if target_member and not can_moderate(ctx.author, target_member):
        return await ctx.send("You can't warn someone with equal or higher rank.")
    add_sanction(user.id, reason, ctx.author.id)
    emb = discord.Embed(title=f"✦ Warn — {BRAND_NAME}", description=f"{user.mention} was warned\n**Reason:** {reason}", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def tempmute(ctx, *, args=None):
    if not has_perm(ctx.author, get_cmd_perm("tempmute")):
        return await cmd_fail(ctx)
    user = None
    rest = args or ""
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        for m in ctx.message.mentions:
            rest = rest.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
    elif ctx.message.reference:
        user = await get_target(ctx, None)
    tokens = rest.strip().split()
    if user is None and tokens and tokens[0].isdigit():
        user = await get_target(ctx, tokens[0])
        tokens = tokens[1:]
    duration = None
    reason = "No reason"
    for i, tok in enumerate(tokens):
        if parse_duration(tok):
            duration = tok
            reason = " ".join(tokens[i+1:]).strip() or "No reason"
            break
    if not user or not duration:
        return await cmd_usage(ctx, "`+tempmute <@member> <duration> [reason]`")
    delta = parse_duration(duration)
    member = await get_member(ctx.guild, user)
    if not member or not can_moderate(ctx.author, member):
        return await ctx.send("Cannot mute this user.")
    try:
        await member.timeout(datetime.now(timezone.utc) + delta, reason=reason)
        add_sanction(member.id, f"tempmute {duration} - {reason}", ctx.author.id)
        emb = discord.Embed(title=f"✦ Temp Mute — {BRAND_NAME}", description=f"{member.mention} muted for **{duration}**\n**Reason:** {reason}", color=THEME_COLOR)
        emb.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=emb)
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def unmute(ctx, *, target: str = None):
    if not has_perm(ctx.author, get_cmd_perm("unmute")):
        return await cmd_fail(ctx)
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    elif ctx.message.reference:
        user = await get_target(ctx, None)
    elif target:
        user = await get_target(ctx, target)
    if not user:
        return await cmd_usage(ctx, "`+unmute <@member>`")
    member = await get_member(ctx.guild, user)
    if not member:
        return await cmd_usage(ctx, "`+unmute <@member>`")
    try:
        await member.timeout(None, reason=f"Unmuted by {ctx.author}")
        emb = discord.Embed(title=f"✦ Unmute — {BRAND_NAME}", description=f"{member.mention} has been unmuted.", color=THEME_COLOR)
        emb.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=emb)
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def clear(ctx, *, args: str = None):
    """+clear [amount] [@member] — silent delete, no bot reply.
    Examples:
      +clear
      +clear 20
      +clear @user
      +clear 50 @user
    """
    if not has_perm(ctx.author, get_cmd_perm("clear")):
        return await cmd_fail(ctx)

    amount = 10
    target_user = None

    if ctx.message.mentions:
        target_user = ctx.message.mentions[0]

    if args:
        tokens = args.split()
        for tok in tokens:
            if tok.isdigit():
                amount = int(tok)
                break
        if target_user is None:
            for tok in tokens:
                if not tok.isdigit() and not tok.startswith("<@"):
                    target_user = await get_target(ctx, tok)
                    if target_user:
                        break
    # Reply-to also targets that user
    if target_user is None and ctx.message.reference:
        target_user = await get_target(ctx, None)

    if amount < 1 or amount > 100:
        try:
            await ctx.message.delete()
        except Exception:
            pass
        return

    clearing_channels.add(ctx.channel.id)
    try:
        # Delete the command message first
        try:
            await ctx.message.delete()
        except Exception:
            pass

        def check(m):
            if target_user:
                return m.author.id == target_user.id
            return True

        # Purge up to `amount` matching messages (command already deleted)
        await ctx.channel.purge(limit=amount, check=check)
        # No bot response — stays silent
    except Exception:
        pass
    finally:
        clearing_channels.discard(ctx.channel.id)


@bot.command()
async def lock(ctx):
    if not has_perm(ctx.author, get_cmd_perm("lock")):
        return await cmd_fail(ctx)
    try:
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(description=f"{ctx.channel.mention} locked.", color=THEME_COLOR))
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def unlock(ctx):
    if not has_perm(ctx.author, get_cmd_perm("unlock")):
        return await cmd_fail(ctx)
    try:
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(description=f"{ctx.channel.mention} unlocked.", color=THEME_COLOR))
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def addrole(ctx, *, args=None):
    """+addrole [user] <role>
    Examples:
      +addrole head of recruitment     (adds to yourself)
      +addrole @user Moderator
      +addrole Moderator
    """
    if not has_perm(ctx.author, get_cmd_perm("addrole")) and not has_role_manage_extra(ctx.author):
        return await cmd_fail(ctx)
    if not args:
        return await cmd_usage(ctx, "`+addrole [@member] <role>`")

    user = None
    role_name = None

    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        role_name = args
        for m in ctx.message.mentions:
            role_name = role_name.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
        role_name = role_name.strip()
    elif ctx.message.reference:
        user = await get_target(ctx, None)
        role_name = args.strip()
    else:
        # Try first token as user ID, otherwise whole string is role (self)
        parts = args.split(None, 1)
        if parts[0].isdigit() and len(parts[0]) >= 15 and ctx.guild.get_member(int(parts[0])):
            user = await get_target(ctx, parts[0])
            role_name = parts[1] if len(parts) > 1 else None
        else:
            user = ctx.author
            role_name = args.strip()

    if not user or not role_name:
        return await cmd_usage(ctx, "`+addrole [@member] <role>`")

    member = await get_member(ctx.guild, user)
    if not member:
        return await ctx.send("Could not find that member.")

    role = find_role(ctx.guild, role_name)
    if not role:
        return await ctx.send(f"Could not find a role matching **{role_name}**.")

    # Hierarchy checks
    if role >= ctx.author.top_role and str(ctx.author.id) not in SPECIAL_USERS:
        return await ctx.send("You can't assign a role equal or higher than your top role.")
    if role >= ctx.guild.me.top_role:
        return await ctx.send("My role must be above that role to assign it.")

    if role in member.roles:
        return await ctx.send(f"{member.mention} already has {role.mention}.")

    try:
        await member.add_roles(role, reason=f"addrole by {ctx.author}")
        await ctx.send(f"1 role was added to 1 member")
    except discord.Forbidden:
        await ctx.send("I don't have permission to add that role.")
    except Exception as e:
        await ctx.send(f"Failed: {e}")


@bot.command()
async def delrole(ctx, *, args=None):
    """+delrole [user] <role>
    Examples:
      +delrole head of recruitment
      +delrole @user Moderator
    """
    if not has_perm(ctx.author, get_cmd_perm("delrole")) and not has_role_manage_extra(ctx.author):
        return await cmd_fail(ctx)
    if not args:
        return await cmd_usage(ctx, "`+delrole [@member] <role>`")

    user = None
    role_name = None

    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        role_name = args
        for m in ctx.message.mentions:
            role_name = role_name.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
        role_name = role_name.strip()
    elif ctx.message.reference:
        user = await get_target(ctx, None)
        role_name = args.strip()
    else:
        parts = args.split(None, 1)
        if parts[0].isdigit() and len(parts[0]) >= 15 and ctx.guild.get_member(int(parts[0])):
            user = await get_target(ctx, parts[0])
            role_name = parts[1] if len(parts) > 1 else None
        else:
            user = ctx.author
            role_name = args.strip()

    if not user or not role_name:
        return await cmd_usage(ctx, "`+delrole [@member] <role>`")

    member = await get_member(ctx.guild, user)
    if not member:
        return await ctx.send("Could not find that member.")

    role = find_role(ctx.guild, role_name)
    if not role:
        return await ctx.send(f"Could not find a role matching **{role_name}**.")

    if role >= ctx.author.top_role and str(ctx.author.id) not in SPECIAL_USERS:
        return await ctx.send("You can't manage a role equal or higher than your top role.")
    if role >= ctx.guild.me.top_role:
        return await ctx.send("My role must be above that role to remove it.")

    if role not in member.roles:
        return await ctx.send(f"{member.mention} does not have {role.mention}.")

    try:
        await member.remove_roles(role, reason=f"delrole by {ctx.author}")
        await ctx.send("1 role was successfully removed from 1 member")
    except discord.Forbidden:
        await ctx.send("I don't have permission to remove that role.")
    except Exception as e:
        await ctx.send(f"Failed: {e}")


@bot.command()
async def derank(ctx, *, target: str = None):
    if not has_perm(ctx.author, get_cmd_perm("derank")):
        return await cmd_fail(ctx)
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    elif ctx.message.reference:
        user = await get_target(ctx, None)
    elif target:
        user = await get_target(ctx, target)
    if not user:
        return await cmd_usage(ctx, "`+derank <@member>`")
    member = await get_member(ctx.guild, user)
    if not member or not can_moderate(ctx.author, member):
        return await ctx.send("Cannot derank this user.")
    try:
        cache = resolve_role_ids(ctx.guild)
        staff_ids = set()
        for rids in cache.values():
            staff_ids.update(rids)
        roles = [r for r in member.roles if r.id in staff_ids and r != ctx.guild.default_role and not r.managed]
        if not roles:
            return await ctx.send("No staff roles to remove.")
        await member.remove_roles(*roles, reason=f"Derank by {ctx.author}")
        await ctx.send(f"{member.mention} was deranked successfully")
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def userinfo(ctx, *, target: str = None):
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    elif ctx.message.reference:
        user = await get_target(ctx, None)
    elif target:
        user = await get_target(ctx, target)
    user = user or ctx.author
    member = ctx.guild.get_member(user.id)
    emb = discord.Embed(title=f"✦ User Info — {BRAND_NAME}", color=THEME_COLOR)
    emb.set_author(name=str(user), icon_url=user.display_avatar.url)
    emb.set_thumbnail(url=user.display_avatar.url)
    emb.add_field(name="ID", value=f"`{user.id}`", inline=True)
    emb.add_field(name="Created", value=discord.utils.format_dt(user.created_at, "R"), inline=True)
    if member and member.joined_at:
        emb.add_field(name="Joined", value=discord.utils.format_dt(member.joined_at, "R"), inline=True)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def serverinfo(ctx):
    g = ctx.guild
    emb = discord.Embed(title=f"✦ {g.name}", description=f"**{BRAND_NAME}**", color=THEME_COLOR)
    if g.icon:
        emb.set_thumbnail(url=g.icon.url)
    emb.add_field(name="Members", value=f"`{g.member_count}`", inline=True)
    emb.add_field(name="Boosts", value=f"`{g.premium_subscription_count or 0}`", inline=True)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

# Special commands

@bot.command()
async def clearwarns(ctx, *, target: str = None):
    if not has_perm(ctx.author, get_cmd_perm("clearwarns")):
        return await cmd_fail(ctx)
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    elif ctx.message.reference:
        user = await get_target(ctx, None)
    elif target:
        user = await get_target(ctx, target)
    if not user:
        return await cmd_usage(ctx, "`+clearwarns <@member>`")
    target_member = await get_member(ctx.guild, user)
    if target_member and not can_moderate(ctx.author, target_member):
        return await ctx.send("You can't clear warns of someone with equal or higher rank.")
    uid = str(user.id)
    count = len(sanctions_data.get(uid, []))
    sanctions_data[uid] = []
    save_sanctions()
    emb = discord.Embed(title=f"✦ Clear Warns — {BRAND_NAME}", description=f"Cleared **{count}** sanction(s) from {user.mention}", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command(name="del")
async def del_sanction(ctx, action: str = None, *, rest: str = None):
    if action != "sanction":
        return
    if not has_perm(ctx.author, get_cmd_perm("del")):
        return await cmd_fail(ctx)
    user = None
    number = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    if rest:
        tokens = rest.split()
        for tok in tokens:
            if tok.isdigit() and user is None and len(tok) >= 15:
                user = await get_target(ctx, tok)
            elif tok.isdigit():
                number = tok
    if user is None and ctx.message.reference:
        user = await get_target(ctx, None)
    if not user or not number:
        return await cmd_usage(ctx, "`+del sanction <@member> <number>`")
    uid = str(user.id)
    lst = sanctions_data.get(uid, [])
    if not lst:
        return await cmd_fail(ctx)
    ordered = _sort_sanctions_newest_first(lst)
    num = int(number)
    if num < 1 or num > len(ordered):
        return await cmd_usage(ctx, "`+del sanction <@member> <number>`")
    deleted = ordered[num - 1]
    sanctions_data[uid] = [s for s in lst if s is not deleted]
    save_sanctions()
    emb = discord.Embed(title=f"✦ Del Sanction — {BRAND_NAME}", description=f"Deleted: **{deleted.get('date','?')}**: {deleted.get('reason','')}", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def mutelist(ctx):
    if not has_perm(ctx.author, get_cmd_perm("mutelist")):
        return await cmd_fail(ctx)
    muted = [m for m in ctx.guild.members if m.timed_out_until and m.timed_out_until > datetime.now(timezone.utc)]
    if not muted:
        return await empty_result(ctx, "No one is currently muted.")
    lines = [f"{m.mention} — until {discord.utils.format_dt(m.timed_out_until, 'R')}" for m in muted[:25]]
    emb = discord.Embed(title=f"✦ Mute List — {BRAND_NAME}", description="\n".join(lines), color=THEME_COLOR)
    emb.set_footer(text=f"{FOOTER_TEXT}  •  {len(muted)} muted")
    await ctx.send(embed=emb)

@bot.command()
async def banlist(ctx):
    if not has_perm(ctx.author, get_cmd_perm("banlist")):
        return await cmd_fail(ctx)
    try:
        bans = [entry async for entry in ctx.guild.bans(limit=50)]
    except Exception as e:
        return await ctx.send(f"Failed: {e}")
    if not bans:
        return await empty_result(ctx, "There are no banned users.")
    lines = []
    for entry in bans[:40]:
        reason = entry.reason or "No reason"
        if len(reason) > 60:
            reason = reason[:57] + "..."
        lines.append(f"**{entry.user}** (`{entry.user.id}`)\n↳ {reason}")
    emb = discord.Embed(title=f"✦ Ban List — {BRAND_NAME}", description="\n\n".join(lines), color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def baninfo(ctx, *, target: str = None):
    if not has_perm(ctx.author, get_cmd_perm("baninfo")):
        return await cmd_fail(ctx)
    user = None
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    elif target:
        user = await get_target(ctx, target)
    if not user:
        return await cmd_usage(ctx, "`+baninfo <@member|id>`")
    try:
        ban_entry = await ctx.guild.fetch_ban(user)
    except discord.NotFound:
        return await ctx.send(f"**{user}** is not banned.")
    except Exception as e:
        return await ctx.send(f"Failed: {e}")
    emb = discord.Embed(title=f"✦ Ban Info — {BRAND_NAME}", color=THEME_COLOR)
    emb.set_author(name=str(user), icon_url=user.display_avatar.url)
    emb.add_field(name="User", value=f"{user} (`{user.id}`)", inline=False)
    emb.add_field(name="Reason", value=ban_entry.reason or "No reason", inline=False)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def modstats(ctx):
    if not has_perm(ctx.author, get_cmd_perm("modstats")):
        return await cmd_fail(ctx)
    counts = {}
    for uid, entries in sanctions_data.items():
        for s in entries:
            mid = str(s.get("moderator", "0"))
            if mid and mid != "0":
                counts[mid] = counts.get(mid, 0) + 1
    if not counts:
        return await ctx.send("No moderation actions recorded yet.")
    sorted_mods = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:25]
    lines = [f"**{i}.** <@{mid}> — `{cnt}` actions" for i, (mid, cnt) in enumerate(sorted_mods, 1)]
    emb = discord.Embed(title=f"✦ Moderator Statistics — {BRAND_NAME}", description="\n".join(lines), color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def syncroles(ctx):
    if not has_perm(ctx.author, get_cmd_perm("syncroles")) and str(ctx.author.id) not in SPECIAL_USERS:
        return await cmd_fail(ctx)
    cache = resolve_role_ids(ctx.guild, force=True)
    lines = []
    for level in sorted(cache.keys()):
        roles = [ctx.guild.get_role(rid).mention for rid in cache[level] if ctx.guild.get_role(rid)]
        lines.append(f"**▸ Perm {level}:** {' '.join(roles) if roles else '*none*'}")
    emb = discord.Embed(title=f"✦ Roles Synced — {BRAND_NAME}", description="\n".join(lines) or "No roles matched.", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def temprole(ctx, *, args: str = None):
    if not has_perm(ctx.author, get_cmd_perm("temprole")):
        return await cmd_fail(ctx)
    if not args:
        return await cmd_usage(ctx, "`+temprole <@member> <duration> <role>` (e.g. 1h)")
    user = None
    rest = args
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        for m in ctx.message.mentions:
            rest = rest.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
    tokens = rest.strip().split()
    if user is None and tokens and tokens[0].isdigit() and len(tokens[0]) >= 15:
        user = await get_target(ctx, tokens[0])
        tokens = tokens[1:]
    duration = None
    duration_idx = None
    for i, tok in enumerate(tokens):
        if parse_duration(tok):
            duration = tok
            duration_idx = i
            break
    if duration is None or user is None:
        return await cmd_usage(ctx, "`+temprole <@member> <duration> <role>`")
    role_name = " ".join(tokens[:duration_idx] + tokens[duration_idx+1:]).strip()
    if not role_name:
        return await cmd_usage(ctx, "`+temprole <@member> <duration> <role>`")
    delta = parse_duration(duration)
    member = await get_member(ctx.guild, user)
    role = find_role(ctx.guild, role_name)
    if not member or not role or not delta:
        return await cmd_usage(ctx, "`+temprole <@member> <duration> <role>`")
    if role >= ctx.author.top_role and str(ctx.author.id) not in SPECIAL_USERS:
        return await cmd_fail(ctx)
    try:
        if role not in member.roles:
            await member.add_roles(role, reason=f"Temp role {duration} by {ctx.author}")
        ends_at = datetime.now(timezone.utc) + delta
        schedule_temprole(ctx.guild.id, member.id, role.id, ends_at)
        emb = discord.Embed(title=f"✦ Temp Role — {BRAND_NAME}", description=f"Gave **{role.name}** to {member.mention} for **{duration}**\nRemoves {discord.utils.format_dt(ends_at, 'R')}", color=THEME_COLOR)
        emb.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=emb)
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def create(ctx, emoji: str = None, *, name: str = None):
    if not has_perm(ctx.author, get_cmd_perm("create")):
        return await cmd_fail(ctx)
    if emoji and not name:
        name = emoji
        emoji = None
    if not name:
        return await cmd_usage(ctx, "`+create [emoji] <name>`")
    role_name = f"{emoji} {name}".strip() if emoji else name.strip()
    existing = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), ctx.guild.roles)
    if existing:
        return await ctx.send(f"A role named **{role_name}** already exists.")
    try:
        new_role = await ctx.guild.create_role(name=role_name, reason=f"Created by {ctx.author}")
        await ctx.send(f"Successfully created role **{new_role.name}**")
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def linkalt(ctx, *, args: str = None):
    if not has_perm(ctx.author, get_cmd_perm("linkalt")):
        return await cmd_fail(ctx)
    if not args:
        return await ctx.send("Usage: `+linkalt <main> <alt>`")
    main_user = alt_user = None
    mentions = list(ctx.message.mentions)
    if len(mentions) >= 2:
        main_user, alt_user = mentions[0], mentions[1]
    else:
        parts = args.split(None, 1)
        if len(parts) >= 2:
            main_user = await get_target(ctx, parts[0])
            alt_user = await get_target(ctx, parts[1])
    if not main_user or not alt_user or main_user.id == alt_user.id:
        return await cmd_fail(ctx)
    main_id, alt_id = str(main_user.id), str(alt_user.id)
    if alt_id not in blacklist:
        blacklist.append(alt_id)
        save_blacklist()
    if main_id not in linked_alts:
        linked_alts[main_id] = []
    if alt_id not in linked_alts[main_id]:
        linked_alts[main_id].append(alt_id)
        save_linked_alts()
    try:
        await ctx.guild.ban(alt_user, reason=f"Linked alt of {main_id}")
    except Exception:
        pass
    if main_id not in blacklist:
        blacklist.append(main_id)
        save_blacklist()
    emb = discord.Embed(title=f"✦ Link Alt — {BRAND_NAME}", description=f"Linked **{alt_user}** as alt of **{main_user}** and blacklisted.", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def changeperm(ctx, command: str = None, level: str = None):
    if not has_perm(ctx.author, get_cmd_perm("changeperm")):
        return await cmd_fail(ctx)
    if not command or level is None:
        return await ctx.send("Usage: `+changeperm <command> <level|none>`")
    cmd = command.lower().strip()
    if level.lower() in ("none", "off", "disable"):
        command_overrides[cmd] = "none"
        save_command_perms()
        return await ctx.send(f"Permission for `{cmd}` set to **none**.")
    try:
        lvl = int(level)
        if lvl < 0 or lvl > 6:
            return await ctx.send("Level must be 0-6 or `none`.")
    except ValueError:
        return await ctx.send("Level must be 0-6 or `none`.")
    command_overrides[cmd] = lvl
    save_command_perms()
    await ctx.send(f"Permission for `{cmd}` set to **Perm {lvl}**.")

@bot.command(name="commands")
async def commands_command(ctx):
    if not has_staff_permission(ctx.author):
        return await cmd_fail(ctx)
    emb = discord.Embed(title=f"✦ Ticket Commands — {BRAND_NAME}", color=THEME_COLOR)
    emb.add_field(name="Ticket tools", value="`+claim` `+close` `+rename <name>` `+add <user>` `+remove <user>`", inline=False)
    emb.add_field(name="Note", value="Panels auto-post on bot startup.", inline=False)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def ban(ctx, *, args=None):
    if str(ctx.author.id) not in BAN_COMMAND_USERS:
        return await cmd_fail(ctx)
    user = None
    reason = "No reason"
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        if args:
            reason = args
            for m in ctx.message.mentions:
                reason = reason.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
            reason = reason.strip() or "No reason"
    elif ctx.message.reference:
        user = await get_target(ctx, None)
        if args:
            reason = args.strip() or "No reason"
    elif args:
        parts = args.split(None, 1)
        user = await get_target(ctx, parts[0])
        if user and len(parts) > 1:
            reason = parts[1]
    if not user:
        return await cmd_usage(ctx, "`+ban <@member> [reason]`")
    try:
        await ctx.guild.ban(user, reason=reason)
    except Exception:
        pass
    emb = discord.Embed(title=f"✦ Ban — {BRAND_NAME}", description=f"{user.mention} banned.\n**Reason:** {reason}", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def unban(ctx, user_id=None):
    if str(ctx.author.id) not in BAN_COMMAND_USERS:
        return
    if not user_id:
        return await cmd_fail(ctx)
    uid = user_id.strip().replace("<@", "").replace("!", "").replace(">", "")
    if not uid.isdigit():
        return await cmd_fail(ctx)
    try:
        user = await bot.fetch_user(int(uid))
        await ctx.guild.unban(user)
        emb = discord.Embed(title=f"✦ Unban — {BRAND_NAME}", description=f"{user} unbanned.", color=THEME_COLOR)
        emb.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=emb)
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def kick(ctx, *, args=None):
    if str(ctx.author.id) not in KICK_COMMAND_USERS:
        return await cmd_fail(ctx)
    user = None
    reason = "No reason"
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        if args:
            reason = args
            for m in ctx.message.mentions:
                reason = reason.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
            reason = reason.strip() or "No reason"
    elif ctx.message.reference:
        user = await get_target(ctx, None)
        if args:
            reason = args.strip() or "No reason"
    elif args:
        parts = args.split(None, 1)
        user = await get_target(ctx, parts[0])
        if user and len(parts) > 1:
            reason = parts[1]
    if not user:
        return await cmd_usage(ctx, "`+kick <@member> [reason]`")
    member = await get_member(ctx.guild, user)
    if not member:
        return await cmd_fail(ctx)
    try:
        await member.kick(reason=reason)
        emb = discord.Embed(title=f"✦ Kick — {BRAND_NAME}", description=f"{user.mention} kicked.\n**Reason:** {reason}", color=THEME_COLOR)
        emb.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=emb)
    except Exception as e:
        await ctx.send(f"Failed: {e}")

@bot.command()
async def bl(ctx, *, args=None):
    if str(ctx.author.id) not in BL_COMMAND_USERS:
        return await cmd_fail(ctx)
    user = None
    reason = "No reason"
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
        if args:
            reason = args
            for m in ctx.message.mentions:
                reason = reason.replace(f"<@{m.id}>", "").replace(f"<@!{m.id}>", "")
            reason = reason.strip() or "No reason"
    elif ctx.message.reference:
        user = await get_target(ctx, None)
        if args:
            reason = args.strip() or "No reason"
    elif args:
        parts = args.split(None, 1)
        user = await get_target(ctx, parts[0])
        if user and len(parts) > 1:
            reason = parts[1]
    if not user:
        return await cmd_usage(ctx, "`+bl <@member> [reason]`")
    uid = str(user.id)
    if uid not in blacklist:
        blacklist.append(uid)
        save_blacklist()
    try:
        await ctx.guild.ban(user, reason=f"Blacklisted: {reason}")
    except Exception:
        pass
    emb = discord.Embed(title=f"✦ Blacklist — {BRAND_NAME}", description=f"{user.mention} banned and blacklisted.\nreason: {reason}", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def unbl(ctx, user_id=None):
    if str(ctx.author.id) not in BL_COMMAND_USERS:
        return
    if not user_id:
        return await cmd_fail(ctx)
    uid = user_id.strip().replace("<@", "").replace("!", "").replace(">", "")
    if not uid.isdigit():
        return await cmd_fail(ctx)
    if uid in blacklist:
        blacklist.remove(uid)
        save_blacklist()
    try:
        user = await bot.fetch_user(int(uid))
        await ctx.guild.unban(user)
    except Exception:
        pass
    emb = discord.Embed(title=f"✦ Unblacklist — {BRAND_NAME}", description=f"`{uid}` removed from blacklist and unbanned.", color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

@bot.command()
async def blist(ctx):
    if not has_perm(ctx.author, get_cmd_perm("blist")):
        return await cmd_fail(ctx)
    if not blacklist:
        return await empty_result(ctx, "No blacklisted users.")
    lines = []
    for uid in blacklist[:40]:
        try:
            user = await bot.fetch_user(int(uid))
            lines.append(f"**{user}** (`{uid}`)")
        except Exception:
            lines.append(f"Unknown (`{uid}`)")
    emb = discord.Embed(title=f"✦ Blacklist — {BRAND_NAME}", description="\n".join(lines), color=THEME_COLOR)
    emb.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=emb)

# Ticket commands
@bot.command(name="claim")
async def claim_command(ctx):
    if is_ticket_opener(ctx.channel, ctx.author) or not has_staff_permission(ctx.author):
        return await ctx.reply("❌ Cannot claim.", mention_author=False)
    if not ctx.channel.topic or not str(ctx.channel.topic).startswith("ticket-"):
        return await ctx.reply("❌ Ticket channels only.")
    try:
        async for msg in ctx.channel.history(limit=20):
            if msg.author.id == bot.user.id and msg.embeds:
                embed = msg.embeds[0]
                for field in embed.fields:
                    if field.name.lower() == "claimed by":
                        return await ctx.reply("❌ Already claimed.")
                embed.add_field(name="Claimed by", value=ctx.author.mention, inline=True)
                await msg.edit(embed=embed)
                await ctx.reply(f"✅ Claimed by {ctx.author.mention}")
                return
        await ctx.reply("❌ Could not find ticket message.")
    except Exception as e:
        await ctx.reply(f"❌ {e}")

@bot.command(name="close")
async def close_command(ctx):
    if not ctx.channel.topic or not str(ctx.channel.topic).startswith("ticket-"):
        return await ctx.reply("❌ Ticket channels only.")
    if not (is_ticket_opener(ctx.channel, ctx.author) or has_staff_permission(ctx.author)):
        return await ctx.reply("❌ No permission.", mention_author=False)
    await close_ticket(ctx.channel, ctx.author)

@bot.command(name="rename")
async def rename_command(ctx, *, new_name=None):
    if not has_staff_permission(ctx.author):
        return await ctx.reply("❌ No permission.", mention_author=False)
    if not ctx.channel.topic or not str(ctx.channel.topic).startswith("ticket-"):
        return await ctx.reply("❌ Ticket channels only.")
    if not new_name or len(new_name.strip()) < 2:
        return await ctx.reply("❌ Provide a name.")
    try:
        await ctx.channel.edit(name=new_name.lower().replace(" ", "-")[:100])
        await ctx.reply("✅ Renamed.")
    except Exception as e:
        await ctx.reply(f"❌ {e}")

@bot.command(name="add")
async def add_command(ctx, *, user_input=None):
    if not ctx.channel.topic or not str(ctx.channel.topic).startswith("ticket-"):
        return await ctx.reply("❌ Ticket channels only.")
    if not can_add_or_remove(ctx.author, ctx.channel):
        return await ctx.reply("❌ No permission.", mention_author=False)
    if not user_input:
        return await ctx.reply("❌ Provide a user.")
    target = await resolve_member(ctx, user_input)
    if not target:
        return await ctx.reply("❌ User not found.")
    try:
        await ctx.channel.set_permissions(target, view_channel=True, send_messages=True, attach_files=True, read_message_history=True)
        await ctx.reply(f"✅ Added {target.mention}")
    except Exception as e:
        await ctx.reply(f"❌ {e}")

@bot.command(name="remove")
async def remove_command(ctx, *, user_input=None):
    if not ctx.channel.topic or not str(ctx.channel.topic).startswith("ticket-"):
        return await ctx.reply("❌ Ticket channels only.")
    if not can_add_or_remove(ctx.author, ctx.channel):
        return await ctx.reply("❌ No permission.", mention_author=False)
    if not user_input:
        return await ctx.reply("❌ Provide a user.")
    target = await resolve_member(ctx, user_input)
    if not target:
        return await ctx.reply("❌ User not found.")
    if ctx.channel.topic.startswith("ticket-") and str(target.id) == ctx.channel.topic.replace("ticket-", ""):
        return await ctx.reply("❌ Cannot remove the ticket opener.")
    try:
        await ctx.channel.set_permissions(target, overwrite=None)
        await ctx.reply(f"✅ Removed {target.mention}")
    except Exception as e:
        await ctx.reply(f"❌ {e}")

# Keep-alive
class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"STEAL A BRAINROT Bot is online")
    def log_message(self, format, *args):
        return

def start_keep_alive():
    port = int(os.environ.get("PORT", 8080))
    try:
        server = HTTPServer(("0.0.0.0", port), _HealthHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"Keep-alive on port {port}")
    except Exception as e:
        print(f"Keep-alive failed: {e}")

if __name__ == "__main__":
    start_keep_alive()
    if not TOKEN:
        print("ERROR: Set DISCORD_BOT_TOKEN environment variable.")
    else:
        bot.run(TOKEN)

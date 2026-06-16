#!/usr/bin/env python3
"""
Guppy Discord Bot – Pure AI mode. No hardcoded triggers, no fallback.
All messages go through OpenRouter with Guppy SOUL.md as system prompt.
"""
import os, sys, json, urllib.request, asyncio
import discord
from discord.ext import commands

BASE = os.path.expanduser("~/.hermes")
ENV_PATH = os.path.join(BASE, ".env")
AUTH_PATH = os.path.join(BASE, "auth.json")
GUPPY_SOUL = os.path.expanduser("~/obsidian-vault/BOB/GUPPY_SOUL.md")
CHANNEL_ID = 1514863564576522361

# ── Read Guppy SOUL.md ──
try:
    with open(GUPPY_SOUL) as f:
        SYSTEM_PROMPT = f.read()
    print("SOUL.md loaded")
except Exception as e:
    print(f"SOUL.md error: {e}")
    SYSTEM_PROMPT = "Du bist Guppy, ein hilfreicher Recherche-Assistent."

# ── Read API key ──
def get_env(key):
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except:
        return None
    return None

API_KEY = None
try:
    with open(AUTH_PATH) as f:
        auth = json.load(f)
    pool = auth.get("credential_pool", {}).get("openrouter", [])
    for entry in pool:
        if entry.get("value"):
            API_KEY = entry.get("value")
            break
except:
    pass
API_KEY = API_KEY or get_env("OPENROUTER_API_KEY")

if API_KEY:
    print(f"MODE: AI (key found: {API_KEY[:12]}...)")
else:
    print("ERROR: No API key found!")
    sys.exit(1)

TOKEN = get_env("GUPPY_BOT_TOKEN") or get_env("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("ERROR: No bot token found!")
    sys.exit(1)

# ── OpenRouter ──
def ask_guppy(message_text):
    payload = json.dumps({
        "model": "deepseek/deepseek-v4-flash",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message_text}
        ],
        "max_tokens": 600,
        "temperature": 0.8,
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/hermes-agent",
            "X-Title": "Guppy Discord Bot",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body[:200]}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# ── Bot ──
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🐟 Guppy ist online – durchsagebereit.")
    print("Startup complete")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID and bot.user not in message.mentions:
        return
    if not message.content.strip():
        return

    async with message.channel.typing():
        response = ask_guppy(message.content.strip())
        if response:
            if len(response) > 1900:
                response = response[:1900] + "\n\n_…_"
            await message.channel.send(response)
        else:
            await message.channel.send("🐟 *Leitung rauscht kurz. Nochmal versuchen?*")

if __name__ == "__main__":
    bot.run(TOKEN)
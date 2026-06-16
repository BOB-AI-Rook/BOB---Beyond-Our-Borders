#!/usr/bin/env python3
"""
Template: Standalone Discord Bot with OpenRouter AI.
Kopieren, Token eintragen, SOUL.md-Pfad setzen, Channel-ID anpassen.
"""
import os, sys, json, urllib.request, urllib.parse, asyncio, html, re
import discord
from discord.ext import commands

# ── Paths ──
ENV_PATH = os.path.expanduser("~/.hermes/.env")
SOUL_PATH = os.path.expanduser("~/obsidian-vault/BOB/SOUL.md")  # ← ANPASSEN
CHANNEL_ID = 000000000000000000  # ← ANPASSEN (Discord Channel ID)

# ── Load personality ──
try:
    with open(SOUL_PATH) as f:
        PERSONA = f.read()
except:
    PERSONA = "Du bist ein hilfsbereiter Assistent."

SYSTEM_MSG = PERSONA + "\n\nAntworte auf Deutsch. Kurz und präzise."

# ── Read config ──
def get_env(key):
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except:
        return None

TOKEN = get_env("BOT_TOKEN")  # ← ANPASSEN: z.B. GUPPY_BOT_TOKEN
API_KEY = get_env("OPENROUTER_API_KEY")

if not TOKEN or not API_KEY:
    print("FEHLER: Token oder API-Key nicht in .env gefunden")
    sys.exit(1)

# ── OpenRouter AI ──
def ask_ai(query: str) -> str:
    payload = json.dumps({
        "model": "deepseek/deepseek-v4-flash",
        "messages": [
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": query}
        ],
        "max_tokens": 600,
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/hermes-agent",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"API-Fehler {e.code}"
    except Exception as e:
        return f"Fehler: {e}"

# ── Bot ──
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return
    if not message.content.strip():
        return

    async with message.channel.typing():
        response = ask_ai(message.content.strip())
        if response and len(response) > 1900:
            response = response[:1900] + "\n\n..."
        await message.channel.send(response)

if __name__ == "__main__":
    bot.run(TOKEN)

#!/usr/bin/env python3
"""Guppy Discord Bot – Pure OpenRouter AI. No hardcoded triggers."""
import os, sys, json, urllib.request, discord
from discord.ext import commands

BASE = os.path.expanduser("~/.hermes")
ENV_PATH = os.path.join(BASE, ".env")
GUPPY_SOUL = os.path.expanduser("~/obsidian-vault/BOB/GUPPY_SOUL.md")
CHANNEL_ID = 1514863564576522361

def get_env(key):
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith(key + "="):
                    raw = line.split("=", 1)[1].strip()
                    return raw.strip("'").strip('"')
    except:
        return None
    return None

TOKEN=get_en..._KEY = get_env("OPENROUTER_API_KEY")
if not TOKEN:
    print("GUPPY_BOT_TOKEN not found")
    sys.exit(1)
if not API_KEY:
    print("OPENROUTER_API_KEY not found")
    sys.exit(1)

with open(GUPPY_SOUL) as f:
    PERSONA = f.read().strip()
SYSTEM_MSG = PERSONA + "\n\nAntworte auf Deutsch. Maximal 2000 Zeichen."

def ask_ai(query):
    messages = [
        {"role": "system", "content": SYSTEM_MSG},
        {"role": "user", "content": query}
    ]
    payload = json.dumps({
        "model": "deepseek/deepseek-v4-flash",
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.7,
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/hermes-agent",
            "X-Title": "Guppy Discord Bot",
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Guppy bereit.")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.id != CHANNEL_ID: return
    content = message.content.strip()
    if not content: return
    if content.startswith("!"):
        await bot.process_commands(message)
        return
    async with message.channel.typing():
        response = ask_ai(content)
        if len(response) > 1900:
            response = response[:1900] + "\n..."
        await message.channel.send(response)

if __name__ == "__main__":
    bot.run(TOKEN)
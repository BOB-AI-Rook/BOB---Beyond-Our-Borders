# Export Package: Guppy Bot → Anderer Hermes Agent

Konkretes Beispiel aus der Praxis (Juni 2026). Der Guppy Discord Bot (reiner KI-Modus, OpenRouter) wurde als standalone Package exportiert.

## Betroffene Dateien

| Pfad auf Quellsystem | Wohin auf Zielsystem |
|-----------------------|---------------------|
| `~/.hermes/scripts/guppy-bot.py` | `~/.hermes/scripts/guppy-bot.py` |
| `~/obsidian-vault/BOB/GUPPY_SOUL.md` | `~/obsidian-vault/BOB/GUPPY_SOUL.md` (oder eigener Pfad) |
| `~/.hermes/.env` → `GUPPY_BOT_TOKEN=...` | `GUPPY_BOT_TOKEN=...` in `~/.hermes/.env` |
| `~/.hermes/.env` → `OPENROUTER_API_KEY=...` | `OPENROUTER_API_KEY=...` in `~/.hermes/.env` |

## Anpassungen auf Zielsystem

1. `CHANNEL_ID` im Script auf Ziel-Channel-ID ändern (Discord: Entwicklermodus → Rechtsklick Channel → ID kopieren)
2. Pfad zu `GUPPY_SOUL.md` im Script prüfen (`GUPPY_SOUL = os.path.expanduser(...)`)
3. Selbst wenn der Name des anderen Bots nicht "Guppy" ist: **Den `SYSTEM_PROMPT` im Script ändern** — das `GUPPY_SOUL.md` definiert die Persönlichkeit, nicht feste Trigger.

## Token-Quellen

Der Bot liest Tokens und API-Keys aus zwei Quellen:

```python
# Aus .env (primär)
API_KEY = get_env("OPENROUTER_API_KEY")

# Alternativ aus credential pool (auth.json)
with open(AUTH_PATH) as f:
    auth = json.load(f)
    pool = auth.get("credential_pool", {}).get("openrouter", [])
    for entry in pool:
        if entry.get("value"):
            API_KEY = entry["value"]
            break

# Bot-Token (aus .env)
TOKEN = get_env("GUPPY_BOT_TOKEN") or get_env("DISCORD_BOT_TOKEN")
```

Beide Methoden sind valide. `.env` ist einfacher, `auth.json` ist nötig wenn der OpenRouter-Key vom Hermes Gateway verwaltet wird.

## Bot ist standalone

Kein Hermes-Skill nötig. Keine Skill-Registrierung. Läuft als unabhängiger `discord.py`-Prozess.

## Vollständiges Export-Kommando

```bash
# Auf dem Quellsystem:
mkdir -p /tmp/guppy-export
cp ~/.hermes/scripts/guppy-bot.py /tmp/guppy-export/
cp ~/obsidian-vault/BOB/GUPPY_SOUL.md /tmp/guppy-export/
# README mit Setup-Anleitung dazu schreiben

# Auf Zielsystem übertragen:
scp /tmp/guppy-export/* user@zielsystem:~/

# Auf Zielsystem:
mkdir -p ~/.hermes/scripts ~/obsidian-vault/BOB
mv ~/guppy-bot.py ~/.hermes/scripts/
mv ~/GUPPY_SOUL.md ~/obsidian-vault/BOB/
echo 'GUPPY_BOT_TOKEN=*** >> ~/.hermes/.env
echo 'OPENROUTER_API_KEY=*** >> ~/.hermes/.env

# Starten:
PYTHONUNBUFFERED=1 /usr/local/lib/hermes-agent/venv/bin/python3 -u \
  ~/.hermes/scripts/guppy-bot.py &
```
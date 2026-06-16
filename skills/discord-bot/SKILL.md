---
name: discord-bot
description: "Deploy and manage standalone Discord bots from Hermes (token lifecycle, .env credentials, background process management, channel binding, SOUL.md personality, OpenRouter integration). Umbrella skill absorbing standalone-discord-bots, discord-bot-subagent, discord-subagent-bot, discord-bot-creation, and guppy-bot-setup."
platforms: [linux]
---

# Discord Bot Management

## ⚠️ Entry Point — IMMER DIESEN SKILL LADEN

Dies ist der **kanonische Skill** für ALLE standalone Discord Bots. Wenn der User "Guppy", "Bot", "Discord Bot", "standalone Bot", "eigenen Bot" oder ähnliches sagt → `skill_view(name="discord-bot")`.

**NICHT** die absorbierten alten Skills laden: `guppy-bot-setup`, `standalone-discord-bots`, `discord-bot-subagent`, `discord-subagent-bot`, `discord-bot-creation`. Diese existieren nicht mehr als separate Skills — sie wurden alle hier zusammengeführt. Ein Aufruf verursacht nur Frust (Fehlermeldung oder veralteter Stand).

Use when the user wants to create, deploy, or maintain an independent Discord bot that is NOT the main Hermes agent's Discord connection.

Typical triggers: "gib Guppy einen eigenen Bot", "kannst du einen Bot für Kanal X erstellen", "ich brauche einen separaten Discord Bot für Y".

## Bot-Setup (einmalig)

### 1. Discord Developer Portal

Der Benutzer muss auf https://discord.com/developers/applications:
- Eine **New Application** erstellen
- Unter **Bot** → **Add Bot**
- Token kopieren
- **Message Content Intent** aktivieren (für Bots die Nachrichten lesen)
- Unter **OAuth2 → URL Generator** → `bot` Scope + `Send Messages`/`Read Message History`/`View Channels` Permissions → Link generieren und Bot zum Server einladen

### 2. Token im Hermes .env speichern

```bash
# Token in ~/.hermes/.env eintragen
echo 'BOTNAME_BOT_TOKEN=MTUx...' >> ~/.hermes/.env
```

Wichtig: Der Token gehört NIE in die Chat-Historie oder in öffentliche Kanäle. Sobald er im Chat sichtbar war, muss er im Developer Portal **sofort regeneriert** werden.

### 3. Bot-Script schreiben

Das Script braucht:

| Komponente | Hinweis |
|---|---|
| Token aus `.env` lesen | Via `get_env("BOTNAME_BOT_TOKEN")` — gleiche Funktion wie im Sync-Script |
| `discord.Intents.default()` + `message_content = True` | Sonst sieht der Bot keine Nachrichten |
| `CHANNEL_ID` als Konstante | Aus der Discord-UI kopieren (Rechtsklick auf Channel → ID kopieren) |
| `on_ready()` Callback | Bestätigungsnachricht in den Ziel-Channel senden |
| `on_message()` Handler | Nur im Ziel-Channel oder bei Mention reagieren |

**Token-Verarbeitung korrekt:** Der Token ist ein String wie `MTUx...Pjc`. Beim Einlesen aus `.env` DARF er nicht gekürzt werden. `print()` oder `repr()` in Chat-nahen Ausgaben vermeiden. Token-Verifikation via `discord.py` (Gateway) ist strenger als via REST-Curl — ein Token der im REST-Curl funktioniert kann von `discord.py` noch als "Improper token" abgelehnt werden.

### 4. Bot als Hintergrundprozess starten

```bash
python3 /pfad/zu/bot.py
```

→ immer als `background=true` mit `notify_on_complete=true` starten.
→ `-u` (unbuffered) Flag ist nicht nötig — discord.py logged asynchron.

### 5. Prozess-Management

```bash
# Status prüfen
process(action="poll", session_id="...")

# Auf Ausgabe warten
process(action="wait", session_id="...", timeout=10)

# Log abrufen
process(action="log", session_id="...", limit=50)

# Beenden
process(action="kill", session_id="...")
```

## Guppy-Modus: Reine KI, keine hartcodierten Trigger

**User-Preference (kritisch):** Guppy soll NUR über OpenRouter/KI antworten. Keine Begrüßungs-Erkennung, kein "wer bist du"-Pattern, kein DuckDuckGo-Fallback, keine hartcodierten Antworten. Jede Nachricht geht direkt als `user`-Prompt an die KI.

```python
# Reiner KI-Modus – keine hartcodierten Trigger
@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.id != CHANNEL_ID: return
    content = message.content.strip()
    if not content: return

    async with message.channel.typing():
        response = ask_ai(content)
        await message.channel.send(response[:1900])
```

### OpenRouter API-Key aus .env (nicht auth.json)

Der OpenRouter-Key steht in `~/.hermes/.env` unter `OPENROUTER_API_KEY`. **Nicht aus `auth.json` lesen** — der Credential-Pool speichert dort nur die Konfiguration, nicht das Secret.

```python
def get_env(key):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip().strip("'").strip('"')

API_KEY=get_en...
if not API_KEY:
    print("OPENROUTER_API_KEY nicht gefunden!")
    sys.exit(1)
```

### Kein DuckDuckGo-Fallback

Frühere Versionen fielen auf DuckDuckGo zurück, wenn OpenRouter nicht antwortete. Der Benutzer lehnt diesen Ansatz ab. Bei API-Fehlern stattdessen eine kurze Fehlermeldung senden.

### SOUL.md als System-Prompt

```python
SOUL_PATH = os.path.expanduser("~/obsidian-vault/BOB/GUPPY_SOUL.md")
with open(SOUL_PATH) as f:
    PERSONA = f.read()
SYSTEM_MSG = PERSONA + "\nAntworte auf Deutsch, kurz und präzise."
```

## Bot-Definition (Guppy — reiner KI-Modus)

Das Guppy-Script liegt unter `~/.hermes/scripts/guppy-bot.py`.

**Kernlogik:**
- `on_message` fängt alle Nachrichten im Ziel-Channel (ausser Bot-Nachrichten)
- **Jede** Nachricht geht direkt als `user`-Prompt an OpenRouter/DeepSeek V4 Flash
- **Keine** hartcodierten Trigger (keine Begrüßungserkennung, kein "wer bist du"-Pattern, kein DuckDuckGo-Fallback)
- Antwort mit `async with message.channel.typing()` (zeigt "schreibt..."-Indikator)
- Antworten auf max 1900 Zeichen gekürzt (Discord-Limit)
- System-Prompt = Inhalt der `GUPPY_SOUL.md` aus dem Obsidian Vault
- `get_env("OPENROUTER_API_KEY")` für den API-Key (aus `.env`, nicht aus `auth.json`)
- Bei API-Fehlern: kurze Fehlermeldung, kein Fallback

## Merged Sibling Skills

The following standalone Discord bot skills have been absorbed into this umbrella skill. Each covers a variant approach to the same pattern. Their unique content is preserved below and in the support directories.

### standalone-discord-bots (autonomous-ai-agents)

Originally in English, covered the "pure AI" bot pattern with SOUL.md personality, credential pool approach (auth.json instead of .env), and a more generic template. Key additional content:

**Architecture diagram:**
```
┌─────────────────────┐     ┌──────────────────────────┐
│  Hermes Gateway      │     │  Standalone Bot           │
│  (primary Discord)   │     │  (secondary Discord)      │
│  Token: DISCORD_...  │     │  Token: eigener Bot-Token │
├─────────────────────┤     ├──────────────────────────┤
│  ~/.hermes/auth.json │◄────│  Liest OpenRouter-Key     │
│  (credential pool)   │     │  aus auth.json            │
│  OpenRouter Key      │     │                           │
└─────────────────────┘     │  Lädt SOUL.md als          │
                            │  System-Prompt             │
                            │                            │
                            │  Nutzt OpenRouter via       │
                            │  OpenAI-kompatible REST     │
                            └──────────────────────────┘
```

**Credential Pool reading (alternative to .env):**
```python
def get_openrouter_key():
    with open(os.path.expanduser("~/.hermes/auth.json")) as f:
        auth = json.load(f)
    pool = auth.get("credential_pool", {}).get("openrouter", [])
    for entry in pool:
        if entry.get("value"):
            return entry["value"]
    raise RuntimeError("Kein OpenRouter-Key")
```

This approach reads from auth.json instead of .env. Prefer the .env method (documented above) for simplicity, but auth.json is viable when the credential pool is maintained by the Hermes gateway.

### discord-bot-subagent (devops)

Framed the bot as a "Hermes sub-agent" — same OpenRouter pattern, same SOUL.md approach. Key unique content:

**System Prompt Construction pattern:**
```python
SYSTEM_MSG = f"""{SOUL_CONTENT}

Du bist mit dem Discord-Bot '<Name>' verbunden und antwortest auf Deutsch.
Du bekommst Nachrichten von Nutzern im Channel #<channel-name>.
Antworte freundlich, präzise und mit einer Prise Humor.
Halte Antworten kurz und informativ (max 3-4 Absätze).
"""
```

**AI Query with custom headers (OpenRouter):**
```python
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/hermes-agent",
        "X-Title": f"[NAME] Discord Bot",
    }
)
```

### discord-subagent-bot (discord/)

German-language variant with complete working bot template including:
- `commands.Bot` subclass (instead of bare `discord.Client`)
- Startup announcement (`channel.send("🐟 ... ist online.")`)
- Channel-only + @mention fallback
- Error message: "[NAME] *Leitung rauscht kurz. Nochmal versuchen?*"

The working script template from this skill is preserved at `templates/bot-template.py`.

### discord-bot-creation (dogfood/)

Concise German-language workflow summary. Unique content was the Vagrant/iCloud sync hint and the simplified 4-step structure. Already covered by the other absorbed skills.

### guppy-bot-setup (software-development/)

Guppy-specific German-language variant. Unique content:

**iCloud Sync (Vagrant/VM environments):**
```bash
cd /root && /usr/local/lib/hermes-agent/venv/bin/python3 ~/.hermes/scripts/sync-obsidian.py push
# For content changes: delete + re-upload is needed
```

## Export & Transfer (Bot auf anderen Hermes Agent kopieren)

Wenn der Bot auf einen anderen Hermes Agent übertragen werden soll, braucht es nur **3 Dateien**:

| Datei | Beschreibung |
|-------|-------------|
| `guppy-bot.py` | Bot-Script (standalone, kein Hermes-Skill nötig) |
| `GUPPY_SOUL.md` | Persönlichkeit / System-Prompt |
| `.env`-Einträge | `BOTNAME_BOT_TOKEN=***` + `OPENROUTER_API_KEY=***` |

**Anpassungen auf dem Zielsystem:**
- `CHANNEL_ID` im Script auf die Ziel-Channel-ID ändern
- Pfad zu `GUPPY_SOUL.md` im Script anpassen (falls anderswo abgelegt)
- Tokens in `~/.hermes/.env` setzen

**Wichtig:** Das Bot-Script ist **vollkommen standalone** — kein Hermes-Skill nötig, keine Skill-Registrierung. Es läuft als unabhängiger Python-Prozess via `discord.py`. Einfach `scp`/`rsync` der 3 Dateien + Startkommando und der Bot läuft.

**Start auf dem Zielsystem:**
```bash
PYTHONUNBUFFERED=1 /usr/local/lib/hermes-agent/venv/bin/python3 -u \
  ~/.hermes/scripts/guppy-bot.py &
```

Details und konkretes Beispiel aus der Praxis in `references/export-package.md`.

## Sicherheit

- **Token-Leak:** Wenn ein Token im Chat sichtbar war → sofort im Developer Portal regenerieren
- **Keine Ausgabe von Secrets:** `print()` im Bot-Script sollte keine Tokens enthalten
- **Channel-ID hartcodiert:** Der Bot reagiert NUR in seinem zugewiesenen Channel (oder bei Mention)

## ⚠️ Pitfalls

### ❌ Doppelantworten / Mehrfachantworten
**Ursache:** Es laufen mehrere Bot-Prozesse parallel. Jeder Prozess startet eine eigene discord.py-Gateway-Verbindung, und alle antworten auf die gleichen Nachrichten.

**Symptom:** Auf jede Nachricht kommen 2-3 identische oder leicht variierende Antworten.

**Lösung:** Vor Neustart immer alle Bot-Prozesse killen:
```bash
pkill -f "guppy-bot.py"
ps aux | grep guppy-bot | grep -v grep  # Sollte 0 anzeigen
# Dann starten
```

**Prävention:** Nie zwei `terminal(background=True)`-Aufrufe für denselben Bot in einer Session ausführen. Das `process`-System trackt laufende Instanzen, aber es können Prozesse aus vorherigen Sessions übrig sein, die ausserhalb der `process`-Liste laufen.

### ❌ Bot antwortet nicht
**Ursache 1:** Message Content Intent fehlt im Discord Developer Portal.
**Check:** Bot → Privileged Gateway Intents → **Message Content Intent** aktivieren.

**Ursache 2:** Channel-ID falsch.
**Check:** `CHANNEL_ID` im Script prüfen.

**Ursache 3:** Bot nicht auf dem Server.
**Check:** Bot muss via OAuth2-URL invited sein, nicht nur der Token erstellt.
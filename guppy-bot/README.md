# 🐟 Guppy Discord Bot – Export Package

Setup für einen weiteren Hermes Agent – **3 Dateien, 5 Minuten.**

## Mitgelieferte Dateien

| Datei | Zweck |
|-------|-------|
| `guppy-bot.py` | Bot-Script (standalone, kein Hermes-Skill nötig) |
| `GUPPY_SOUL.md` | Persönlichkeit / System-Prompt |
| `README.md` | Diese Anleitung |

## Setup auf dem Zielsystem

### 1. Discord Bot anlegen (einmalig)

- [Discord Developer Portal](https://discord.com/developers) → New Application → Bot
- Token kopieren
- **Privileged Gateway Intents** aktivieren: `Message Content Intent`
- Bot einladen: OAuth2 URL Generator → `bot` Scope → `Send Messages` + `Read Message History`

### 2. Dateien kopieren

```bash
# Auf dem Ziel-Hermes-System:
mkdir -p ~/.hermes/scripts
mkdir -p ~/obsidian-vault/BOB
```

`guppy-bot.py` → `~/.hermes/scripts/guppy-bot.py`
`GUPPY_SOUL.md` → `~/obsidian-vault/BOB/GUPPY_SOUL.md`

### 3. Tokens in `.env` setzen

```bash
echo 'GUPPY_BOT_TOKEN=<DISCORD_TOKEN>' >> ~/.hermes/.env
echo 'OPENROUTER_API_KEY=<API_KEY>' >> ~/.hermes/.env
```

Oder alternativ: `DISCORD_BOT_TOKEN` als Key-Name.

### 4. Channel-ID anpassen

In `guppy-bot.py` die Zeile:
```python
CHANNEL_ID = 1514863564576522361
```
auf die **Ziel-Channel-ID** ändern (Discord: Entwicklermodus → Rechtsklick Channel → ID kopieren)

### 5. Starten

```bash
PYTHONUNBUFFERED=1 /usr/local/lib/hermes-agent/venv/bin/python3 -u \
  ~/.hermes/scripts/guppy-bot.py &
```

### 6. Stoppen

```bash
pkill -f guppy-bot.py
```

## Wichtige Details

- **Reiner KI-Modus** – JEDE Nachricht geht an OpenRouter. Keine hardcodierten Commands.
- **Nur eine Instanz** – Nie zwei Bot-Prozesse gleichzeitig → Doppelantworten.
- **Python-Umgebung** – Nutzt Hermes-eigenes venv unter `/usr/local/lib/hermes-agent/venv/bin/python3`
- **OpenRouter-Modell** – `deepseek/deepseek-v4-flash` (in `guppy-bot.py` änderbar)

## Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| Bot antwortet nicht | `Message Content Intent` aktivieren (Discord Dev Portal) |
| Doppelantworten | `pkill -f guppy-bot.py` + frischer Start |
| OpenRouter offline | Bot zeigt "*Leitung rauscht kurz*" |
| Channel-ID falsch | Entwicklermodus in Discord → Rechtsklick auf Channel → ID kopieren |
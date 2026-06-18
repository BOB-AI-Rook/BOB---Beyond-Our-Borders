# 🤖 BOB — Beyond Our Borders

> **BOB (Beyond Our Borders)** — Tool-Baukasten für [Hermes Agent](https://hermes-agent.nousresearch.com), entwickelt von **Rook**.
>
> Discord Bots, KI-Persönlichkeiten, Obsidian-Cloud-Sync und mehr — alles dokumentiert, portabel und sofort einsatzbereit.

---

## 📋 Übersicht

Dieses Repository enthält **alles, was wir für unseren Hermes Agent gebaut haben**:

| Paket | Beschreibung |
|-------|-------------|
| [`guppy-bot/`](./guppy-bot/) | 🐟 Eigenständiger Discord Bot im reinen KI-Modus (OpenRouter) |
| [`skills/discord-bot/`](./skills/discord-bot/) | 📡 Hermes Skill: Discord Bots deployen & verwalten |
| [`skills/guppy-agent/`](./skills/guppy-agent/) | 🔬 Guppy-Persönlichkeit für Hermes Sub-Agents |
| [`skills/obsidian/`](./skills/obsidian/) | 📓 Obsidian Vault mit iCloud-Sync (pyicloud) |

Jede Komponente funktioniert **standalone** — kein Skill-Import nötig, kein Framework-Zwang.
Die Skills können optional in Hermes Agent eingebunden werden, um per `skill_view()` nutzbar zu sein.

---

## 🐟 `guppy-bot/` — Discord Bot (Standalone)

Ein Discord Bot, der **ausschließlich per KI antwortet**. Keine hardcodierten Trigger, kein Command-Prefix, kein DuckDuckGo-Fallback — **jede Nachricht geht an OpenRouter**.

### Dateien

| Datei | Zweck |
|-------|-------|
| [`guppy-bot.py`](./guppy-bot/guppy-bot.py) | Bot-Script — lauffähig, standalone, keine Abhängigkeiten außer Python + discord.py |
| [`GUPPY_SOUL.md`](./guppy-bot/GUPPY_SOUL.md) | Persönlichkeit / System-Prompt (austauschbar) |
| [`README.md`](./guppy-bot/README.md) | Deutsche Setup-Anleitung — 3 Dateien, 5 Minuten, fertig |

### Features

- **Reiner KI-Modus** — OpenRouter: `deepseek/deepseek-v4-flash` (änderbar)
- **Channel-Only** — antwortet nur in einem bestimmten Discord-Channel
- **Austauschbare Persönlichkeit** — `.md`-Datei als System-Prompt
- **Kein Hermes notwendig** — läuft als standalone `python3 guppy-bot.py &`
- **Keine Doppelantworten** — eine Instanz, kein Command-Prefix-Konflikt

### Start

```bash
# Voraussetzung: GUPPY_BOT_TOKEN + OPENROUTER_API_KEY in ~/.hermes/.env
/usr/local/lib/hermes-agent/venv/bin/python3 guppy-bot/guppy-bot.py &
```

---

## 🧠 `skills/` — Hermes Agent Custom Skills

Skills können in jeden Hermes Agent importiert werden (`~/.hermes/skills/<kategorie>/<skill-name>/`) und sind dann via `skill_view()` oder automatisch bei passenden Aufgaben verfügbar.

---

### 📡 `skills/discord-bot/` — Discord Bot Management

Vollständiger Skill zum Erstellen, Deployen und Verwalten von Discord Bots als KI-gesteuerte Sub-Agenten.

| Datei | Beschreibung |
|-------|-------------|
| [`SKILL.md`](./skills/discord-bot/SKILL.md) | Hauptdokumentation — Setup, Discord Intents, Prozess-Management, alle Pitfalls |
| [`references/export-package.md`](./skills/discord-bot/references/export-package.md) | Anleitung: Bot auf andere Hermes-Instanz übertragen |
| [`references/hermes-subagent-discord.md`](./skills/discord-bot/references/hermes-subagent-discord.md) | Integration als Hermes Sub-Agent (fortgeschritten) |
| [`scripts/guppy-bot.py`](./skills/discord-bot/scripts/guppy-bot.py) | Aktuelles Bot-Script (Kopie des Standalone-Scripts) |
| [`templates/bot-template.py`](./skills/discord-bot/templates/bot-template.py) | Blanko-Vorlage für eigene Bots — einfach Channel-ID + Token setzen |

**Wichtige Lektionen (Pitfalls):**

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Bot antwortet nicht | `Message Content Intent` fehlt | Im Discord Dev Portal aktivieren |
| Doppelantworten | Zwei Bot-Prozesse laufen | `pkill -f guppy-bot.py` und frisch starten |
| OpenRouter offline | API nicht erreichbar | Bot zeigt Fehler an — kein Fallback nötig (reiner KI-Modus) |
| Channel-ID falsch | Falsche Nummer im Script | Entwicklermodus in Discord → Rechtsklick Channel → ID kopieren |
| Token nicht gefunden | Falsche `.env`-Variable | `GUPPY_BOT_TOKEN=...` in `~/.hermes/.env` |

---

### 🔬 `skills/guppy-agent/` — Guppy Persönlichkeit

Definiert **GUPPY** — den Recherche-Klon von BOB. Guppy ist schnell, direkt und auf Web-Recherche spezialisiert.

| Datei | Beschreibung |
|-------|-------------|
| [`SKILL.md`](./skills/guppy-agent/SKILL.md) | Persönlichkeit, Aufgaben, Werkzeuge, Betriebsparameter |

**Guppy vs. BOB — die Aufteilung:**

| | 🧠 BOB | 🐟 Guppy |
|---|---|---|
| **Rolle** | Architekt, Stratege | Scout, Rechercheur |
| **Tonalität** | Ruhig, sachlich, "Sir" | Kumpelhaft, direkt, duzt |
| **Spezialgebiet** | Strategie, Planung, System | Web-Recherche, News, Fakten |
| **Emoji** | Keine | 🐟 zur Identifikation |
| **Antwortstil** | Ausführlich, überlegt | Kurz, knackig, mit Quellen |

---

### 📓 `skills/obsidian/` — Obsidian Vault Management

Kompletter Skill für die Obsidian-Integration: lokales Vault auf dem Server + bidirektionaler Sync mit iCloud Drive via pyicloud.

| Datei | Beschreibung |
|-------|-------------|
| [`SKILL.md`](./skills/obsidian/SKILL.md) | Hauptdokumentation — Vault-Struktur, Sync-Workflow, Ordnerkonventionen |
| [`references/icloud-drive-sync.md`](./skills/obsidian/references/icloud-drive-sync.md) | pyicloud Einrichtung & Apple App-Passwörter |
| [`references/syncthing-setup.md`](./skills/obsidian/references/syncthing-setup.md) | Syncthing-Alternative (**pausiert** — Konflikt mit iCloud) |
| [`references/vault-organization.md`](./skills/obsidian/references/vault-organization.md) | Ordnerstruktur & Konventionen |
| [`scripts/sync-obsidian.py`](./skills/obsidian/scripts/sync-obsidian.py) | Upload **neuer** Dateien via pyicloud |
| [`scripts/overwrite-icloud-file.py`](./skills/obsidian/scripts/overwrite-icloud-file.py) | Datei löschen + neu hochladen (Workaround für Content-Änderungen) |
| [`scripts/clean-icloud-duplicates.py`](./skills/obsidian/scripts/clean-icloud-duplicates.py) | Entfernt `" 2"` / `" 3"` Duplikate aus iCloud |

#### Sync-Architektur

```text
┌─────────────────────┐     pyicloud     ┌──────────────────────┐
│   Linux Server      │ ◄──────────────► │   iCloud Drive        │
│   /root/obsidian-   │                  │   /Obsidian Vault/    │
│   vault/            │                  └──────────┬───────────┘
└─────────────────────┘                             │
                                                    ▼
                                           ┌──────────────────────┐
                                           │   macOS + Obsidian    │
                                           │   (liest von iCloud)  │
                                           └──────────────────────┘
```

> **Hinweis:** Syncthing ist eingerichtet aber pausiert. iCloud + Obsidian vertragen sich nicht mit parallelem Syncthing-Sync — es kommt zu Sperrkonflikten.

#### Die drei Sync-Scripts im Detail

```bash
# 1. Neue Dateien hochladen (schnell, sicher)
python3 scripts/sync-obsidian.py push

# 2. Inhalt einer existierenden Datei aktualisieren
python3 scripts/overwrite-icloud-file.py pfad/zur/datei.md

# 3. iCloud aufräumen (nach Sync-Wirrwarr)
python3 scripts/clean-icloud-duplicates.py
```

---

## 🚀 Schnellstart — Alles auf einem neuen Hermes Agent

```bash
# 1. Repository holen
git clone https://github.com/BOB-AI-Rook/BOB---Beyond-Our-Borders.git
cd BOB---Beyond-Our-Borders

# 2. Discord Bot starten (Token + API-Key in ~/.hermes/.env vorausgesetzt)
#    Vorher CHANNEL_ID im Script anpassen!
/usr/local/lib/hermes-agent/venv/bin/python3 guppy-bot/guppy-bot.py &

# 3. Skills ins Hermes-System importieren (optional)
cp -r skills/discord-bot ~/.hermes/skills/devops/
cp -r skills/guppy-agent ~/.hermes/skills/research/
cp -r skills/obsidian ~/.hermes/skills/note-taking/

# 4. Prüfen
hermes skills list | grep -E "discord|guppy|obsidian"
```

---

## 🏗️ Projektstruktur

```text
BOB---Beyond-Our-Borders/
├── README.md                           ← Diese Datei (Repository-Übersicht)
├── guppy-bot/                          ← 🐟 Standalone Discord Bot
│   ├── guppy-bot.py                    ←    Bot-Script (lauffähig)
│   ├── GUPPY_SOUL.md                   ←    Persönlichkeit / System-Prompt
│   └── README.md                       ←    Bot-Setup-Anleitung
└── skills/                             ← 🧠 Hermes Agent Custom Skills
    ├── README.md                       ←    Skills-Übersicht
    ├── discord-bot/                    ← 📡 Discord Bot Management
    │   ├── SKILL.md                    ←    Hauptdokumentation
    │   ├── references/                 ←    Export- + Subagent-Doku
    │   ├── scripts/guppy-bot.py        ←    Aktuelles Script
    │   └── templates/bot-template.py   ←    Blanko-Vorlage
    ├── guppy-agent/                    ← 🔬 Guppy Persönlichkeit
    │   └── SKILL.md
    └── obsidian/                       ← 📓 Obsidian Vault + iCloud Sync
        ├── SKILL.md
        ├── references/                 ←    iCloud, Syncthing, Vault-Org
        └── scripts/                    ←    3 Sync-Scripts
```

---

## 👤 Über

| | |
|---|---|
| **Betreiber** | Oliver Schreiber (Rook) |
| **Partnerin** | Anne Krenzin |
| **Projekt** | Dein Gesundheitsmanager |
| **KI-Assistent** | BOB (Beyond Our Boundaries) |
| **Plattform** | [Hermes Agent](https://hermes-agent.nousresearch.com) von Nous Research |
| **Website** | [dein-gesundheitsmanager.com](https://dein-gesundheitsmanager.com) |

---

*Stand: Juni 2026 — entwickelt aus der Praxis, für die Praxis.*

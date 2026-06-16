# 🤖 BOB — Beyond Our Borders

> **BOB (Beyond Our Borders)** — KI-Assistent und Tool-Baukasten für **Hermes Agent**, entwickelt von **Rook** //

Dieses Repository enthält alle **Custom Skills, Bot-Scripts und Konfigurationen**, die für den Hermes Agent erstellt wurden — komplett dokumentiert, portabel und einsatzbereit für jedes Hermes-System.

---

## 📦 Inhalt

### 🐟 `guppy-bot/` — Discord Bot (Standalone)

Der **Guppy Discord Bot** — ein eigenständiger KI-Bot im reinen KI-Modus ohne hardcodierte Trigger. Jede Nachricht wird direkt an OpenRouter geschickt.

| Datei | Beschreibung |
|-------|-------------|
| [`guppy-bot.py`](./guppy-bot/guppy-bot.py) | Bot-Script — lauffähig, standalone, keine Skill-Registrierung nötig |
| [`GUPPY_SOUL.md`](./guppy-bot/GUPPY_SOUL.md) | Persönlichkeit/System-Prompt |
| [`README.md`](./guppy-bot/README.md) | Deutsche Setup-Anleitung (3 Dateien, 5 Minuten) |

**Features:**
- Reiner KI-Modus via OpenRouter — kein DuckDuckGo-Fallback, keine Trigger-Wörter
- Channel-Only: antwortet nur in einem bestimmten Discord-Channel
- Persönlichkeit aus `GUPPY_SOUL.md` (austauschbar)
- Start mit einem `&` — läuft unabhängig von Hermes

---

### 🧠 `skills/` — Hermes Agent Custom Skills

Skills, die über `hermes skills` in Hermes Agent geladen werden können. Enthalten vollständige Dokumentation, Scripts, Referenzen und Templates.

#### 📡 `skills/discord-bot/` — Discord Bot Management

Skill zum Erstellen, Deployen und Verwalten von Discord Bots als KI-gesteuerte Sub-Agenten.

| Datei | Beschreibung |
|-------|-------------|
| `SKILL.md` | Hauptdokumentation — Setup, Intents, Prozess-Management |
| `references/export-package.md` | Export-Anleitung für andere Hermes-Instanzen |
| `references/hermes-subagent-discord.md` | Integration als Hermes Sub-Agent |
| `scripts/guppy-bot.py` | Aktuelles Bot-Script (Kopie) |
| `templates/bot-template.py` | Blanko-Vorlage für eigene Bots |

**Key-Takeaways (Pitfalls):**
- `Message Content Intent` muss im Discord Dev Portal aktiviert sein
- Nie zwei Bot-Prozesse gleichzeitig → Doppelantworten
- Channel-ID im Script hardcodiert (kein Command-Handling nötig)
- OpenRouter-Key aus `.env`, nicht aus der auth.json

#### 🔬 `skills/guppy-agent/` — Guppy Persönlichkeit

Der Skill, der die Guppy-Persönlichkeit für Hermes Sub-Agents definiert.

| Datei | Beschreibung |
|-------|-------------|
| `SKILL.md` | Persönlichkeit, Aufgaben, Werkzeuge, Betriebsparameter |

**Guppy im Vergleich zu BOB:**
| | BOB | Guppy |
|---|---|---|
| Rolle | Architekt, Stratege | Scout, Rechercheur |
| Tonalität | Ruhig, sachlich, "Sir" | Kumpelhaft, direkt, duzt |
| Spezialgebiet | Strategie, Planung, System | Web-Recherche, News, Fakten |
| Emoji | Keine | 🐟 zur Identifikation |

#### 📓 `skills/obsidian/` — Obsidian Vault Management

Kompletter Skill für die Obsidian-Integration — lokal + iCloud-Sync via pyicloud.

| Datei | Beschreibung |
|-------|-------------|
| `SKILL.md` | Hauptdokumentation — Vault-Struktur, Sync-Workflow |
| `references/icloud-drive-sync.md` | pyicloud Einrichtung & App-Passwörter |
| `references/syncthing-setup.md` | Syncthing-Alternative (pausiert) |
| `references/vault-organization.md` | Ordnerstruktur & Konventionen |
| `scripts/sync-obsidian.py` | Upload neuer Dateien via pyicloud |
| `scripts/overwrite-icloud-file.py` | Datei löschen + neu hochladen (Workaround für Content-Änderungen) |
| `scripts/clean-icloud-duplicates.py` | Entfernt `" 2"`/`" 3"` Duplikate aus iCloud |

**Sync-Architektur:**
```
┌─────────────────┐     pyicloud     ┌──────────────────┐
│  Linux Server   │ ◄──────────────► │  iCloud Drive     │
│  /root/obsidian-│                  │  /Obsidian Vault/ │
│  vault/         │                  └────────┬─────────┘
└─────────────────┘                           │
                                              ▼
                                     ┌──────────────────┐
                                     │  macOS + Obsidian  │
                                     │  (liest von iCloud)│
                                     └──────────────────┘
```

*Hinweis: Syncthing ist eingerichtet aber pausiert — iCloud + Obsidian vertragen sich nicht mit parallelem Syncthing-Sync.*

---

## 🚀 Schnellstart — Bot auf neuem Hermes Agent

```bash
# 1. Repository klonen
git clone https://github.com/BOB-AI-Rook/BOB---Beyond-Our-Borders.git
cd BOB---Beyond-Our-Borders

# 2. Guppy Bot starten (nach Token-Setup in ~/.hermes/.env)
/usr/local/lib/hermes-agent/venv/bin/python3 guppy-bot/guppy-bot.py &

# 3. Skill importieren
cp -r skills/discord-bot ~/.hermes/skills/devops/
cp -r skills/obsidian ~/.hermes/skills/note-taking/
```

---

## 🧩 Skills ins Hermes-System einbinden

Skills werden nach `~/.hermes/skills/<kategorie>/<skill-name>/SKILL.md` kopiert. Hermes erkennt sie automatisch beim nächsten Start.

```bash
# Nach dem Kopieren prüfen
hermes skills list
```

---

## 🏗️ Projektstruktur

```
BOB---Beyond-Our-Borders/
├── README.md                       ← Diese Datei
├── guppy-bot/                      ← Standalone Discord Bot
│   ├── guppy-bot.py                ← Bot-Script
│   ├── GUPPY_SOUL.md               ← Persönlichkeit
│   └── README.md                   ← Bot-Anleitung
└── skills/                         ← Hermes Agent Skills
    ├── README.md                   ← Skills-Übersicht
    ├── discord-bot/                ← Discord Bot Management Skill
    │   ├── SKILL.md
    │   ├── references/
    │   ├── scripts/
    │   └── templates/
    ├── guppy-agent/                ← Guppy Persönlichkeit
    │   └── SKILL.md
    └── obsidian/                   ← Obsidian Vault Sync
        ├── SKILL.md
        ├── references/
        └── scripts/
```

---

## 👤 Über

**Betreiber:** Rook // BOB
**KI-Assistent:** BOB (Beyond Our Borders)
**Plattform:** [Hermes Agent](https://hermes-agent.nousresearch.com) von Nous Research  
**Website:** [[[BOB - Beyond Our Borders](https://beyondourborders.cloud/)]

---

*Letzte Aktualisierung: Juni 2026*

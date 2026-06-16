# Discord Bot als Hermes Sub-Agent Bridge

## Aktueller Stand (14. Juni 2026) – Direkter KI-Call statt Hermes-Subprozess

**Implementiert:** Der Guppy-Bot ruft **nicht** `hermes chat -q` auf, sondern sendet Nachrichten direkt an die OpenRouter-API (`deepseek/deepseek-v4-flash`) via `urllib.request`. Die Antwort wird roh an Discord zurückgegeben — keine Tools, keine Skills, kein Session-Overhead.

**Vorteile des direkten KI-Calls:**
- Latenz ~1–3s (statt 5–15s für Hermes-Session)
- Kein Subprozess-Management
- Einfacheres Script, weniger Fehlerquellen

**Nachteile:**
- Kein Toolzugriff (Websuche, Dateizugriff)
- Kein Skill-System
- Kein persistenter Dialog (jeder Call ist standalone)

**Fazit:** Der direkte OpenRouter-Call ist der richtige Ansatz für einen reinen Chat-Bot mit Persönlichkeit. Ein Hermes-Subprozess wäre notwendig, wenn der Bot Tools braucht (Recherche, Dateien lesen, Berechnungen).

Einen Discord-Bot nicht als statischen DuckDuckGo-Scraper betreiben, sondern als **Echtzeit-Bridge** zu einem Hermes Sub-Agenten. Der Bot leitet Nachrichten an einen dedizierten Hermes-Agenten weiter (eigener Profile, eigene Skills, eigene Persönlichkeit) und gibt die Antwort zurück — nahezu in Echtzeit, mit vollem Hermes-Toolset.

## Architektur (Design)

```
Discord User ──> Nachricht ──> Guppy Bot (Python, discord.py)
                                    │
                               [hermes chat -q "Frage" --skills guppy-skills]
                                    │
                               Hermes Agent Session
                               (eigener Profile mit Guppy-Persona)
                                    │
                               Antwort mit Synthese, Quellen, Analyse
                                    │
Guppy Bot ──> Antwort ──> Discord User
```

## Ansätze (nach Priorität)

### Ansatz A: `hermes chat -q` (Quick-Win)

Der Bot ruft `hermes chat --query "Frage" --skills guppy -t web,terminal,file` als Subprozess auf.

**Vorteile:** Einfach, sofort nutzbar, kein zusätzlicher Service nötig.
**Nachteile:** Jede Anfrage startet einen neuen Session-Container (~5–15s Latenz).
**Token/Setup:** Kein zusätzlicher Token — der Bot nutzt die Hermes-Installation des Hosts.

```python
import subprocess, json

def hermes_ask(question: str) -> str:
    result = subprocess.run(
        ["hermes", "chat", "--query", question,
         "--skills", "guppy",
         "-t", "web,terminal,file",
         "--json"],
        capture_output=True, text=True, timeout=120
    )
    return json.loads(result.stdout).get("response", result.stdout)
```

### Ansatz B: Hermes MCP Server (zukünftig)

Hermes kann als MCP-Server laufen. Der Bot verbindet sich als MCP-Client und hat eine persistente Session. Anfragen werden über MCP-Tools geroutet.

**Vorteile:** Persistente Session, niedrigere Latenz.
**Nachteile:** Erfordert `hermes mcp setup`, noch nicht im Standard-Deployment.

### Ansatz C: Hermes WebUI API (experimentell)

Die Hermes WebUI hat einen internen Chat-Endpunkt. Der Bot sendet Nachrichten per HTTP.

**Vorteile:** Kein Subprozess, HTTP-basiert.
**Nachteile:** WebUI muss laufen, API ist intern (keine stabile REST-API nach aussen).

## Skills für den Sub-Agenten

Jeder Discord-Bot bekommt einen eigenen Satz Skills:

```
# Beispiel: guppy-skill
name: guppy
description: "Guppy — der forschende Klon von BOB"
toolsets: [web, terminal, file]
```

## Bot-spezifische Einschränkungen

- **Discord-Output-Limit:** 2000 Zeichen pro Nachricht. Antworten kürzen oder splitten.
- **Latenz:** Discord erwartet Antwort innerhalb von 15 Min (mit `typing()`-Indikator). Hermes-Sessions sind meist in 5–15s fertig.
- **Kein persistenter Dialog:** Jede `hermes chat -q` startet eine frische Session. Für Kontext müsste die Historie als Teil der Query mitgeschickt werden.
---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. To persist the path across sessions, write it to `.env`:
```bash
echo "OBSIDIAN_VAULT_PATH=/root/obsidian-vault" >> ~/.hermes/.env
```  
If it is unset, use `~/Documents/Obsidian Vault`.

**Important:** This env var must be resolved before calling file tools — do not pass `$OBSIDIAN_VAULT_PATH` to `read_file`/`write_file`/`patch`/`search_files`. Resolve it first (e.g. via terminal) and pass the concrete absolute path.

**Mac iCloud Vault path** (when the vault lives in iCloud Drive):
```
/Users/<username>/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault
```
This path is only accessible from macOS — on Linux, use Syncthing or pyicloud to sync it.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

### Cross-Linking nach Batch-Erstellung

Wenn mehrere zusammenhängende Dokumente im selben Ordner erstellt oder aktualisiert werden (z.B. eine neue Wissensdomäne wie `DGM/`), müssen sie **nachträglich** untereinander verknüpft werden. Obsidians Graph View zeigt sonst isolierte Knoten.

**Workflow:**
1. Alle Dateien im Zielordner anlegen oder aktualisieren
2. In **jeder** Datei einen `## Verknüpfte Dokumente` Abschnitt am Ende anfügen
3. Die Links sollten bidirektional sein: Wenn Datei A auf B verlinkt, sollte B auch auf A verlinken
4. Pro Datei nur die thematisch relevanten Querverweise, nicht alle anderen blindlings

**Schreibkonvention:**
```markdown
## Verknüpfte Dokumente

- [[Dateiname-ohne-Endung]] – Kurzbeschreibung des Bezugs
- [[Andere-Datei]] – Warum diese relevant ist
```

Am Ende `patch`-Befehle für alle Dateien ausführen, nicht einzeln hintereinander weg — die paralysierbare Workflow-Struktur senkt die Turn-Zahl.

## Vault-Organisation für Firmen-/Projektwissen

Bei neuen Firmen/Kunden/Projekten einen strukturierten Ordner mit Wikilinks anlegen. Siehe `references/vault-organization.md` für das Schema mit 7 Dokumenttypen und vollvernetztem Obsidian-Graph.

**Wichtig:** Nach dem Anlegen neuer Dateien direkt `[[Wikilinks]]` am Ende jeder Datei setzen – sonst zeigt der Obsidian Graph View isolierte Knoten.

## iCloud Drive Sync

If the vault lives in iCloud Drive and the agent runs on Linux (no native iCloud client), use `pyicloud` for filesystem access. See `references/icloud-drive-sync.md` for the full workflow: authentication, 2FA handling, recursive download/upload, known pitfalls, and API quirks.

**Sync-Script (im Skill enthalten):** `scripts/sync-obsidian.py` liegt im Skill-Verzeichnis und wird nach erfolgreicher Einrichtung auch nach `~/.hermes/scripts/` kopiert. Es liest `ICLOUD_APPLE_ID` und `ICLOUD_APP_PASSWORD` aus `~/.hermes/.env` und unterstützt vier Modi:

```bash
python3 ~/.hermes/scripts/sync-obsidian.py pull    # Download von iCloud
python3 ~/.hermes/scripts/sync-obsidian.py push    # Upload neuer Dateien (sicher — kein Duplikat-Risiko)
python3 ~/.hermes/scripts/sync-obsidian.py sync    # Bidirektional (pull + push)
python3 ~/.hermes/scripts/sync-obsidian.py status  # Status anzeigen
```

**⚠️ Stale-Copy-Pitfall:** Die Kopie in `~/.hermes/scripts/` kann hinter der Skill-Version zurückbleiben, wenn dieses Skill per `skill_manage(action='patch')` aktualisiert wurde. Vor dem ersten Sync-Aufruf **immer prüfen**, ob die beiden Versionen identisch sind: `diff ~/.hermes/skills/note-taking/obsidian/scripts/sync-obsidian.py ~/.hermes/scripts/sync-obsidian.py`. Bei Abweichungen die Skill-Version kopieren: `cp ~/.hermes/skills/note-taking/obsidian/scripts/sync-obsidian.py ~/.hermes/scripts/sync-obsidian.py`. Ein veraltetes Script ohne `mkdir()`-Unterstützung bricht beim Anlegen neuer Unterordner in iCloud ab.

**🛡️ Duplikat-freier Upload:** `push`-Modus lädt **nur Dateien hoch, die noch nicht in iCloud existieren** (Differenzbildung: `local_files - cloud_files`). Das ist die sichere Wahl, wenn der Benutzer ausdrücklich keine Duplikate wünscht. `sync` (pull + push) ist sicher für bidirektionalen Abgleich, `pull` überschreibt lokal ohne Warnung.

**⚠️ Content-Change Blindheit:** `push` vergleicht **nur Dateinamen**, nicht Dateiinhalte. Wenn eine lokale Datei bearbeitet wurde deren Name aber bereits in iCloud existiert, wird sie NICHT hochgeladen. Das Script sagt dann `"Keine neuen lokalen Dateien zum Hochladen"` obwohl sich der Inhalt geändert hat. Workaround: Die Datei aus iCloud löschen und neu pushen. Dafür gibt es das Hilfsskript `scripts/overwrite-icloud-file.py`:

```bash
python3 ~/.hermes/scripts/overwrite-icloud-file.py BOB/BOB_SOUL.md
# oder rekursiv für eine Dateiliste
```

**🧹 Duplikat-Bereinigung:** Wenn Sync-Versuche mit einer alten Script-Version (ohne `mkdir`) oder wiederholte Uploads Duplikate erzeugt haben (erkennbar an Dateinamen wie `"name 2.md"`, `"name 3.md"`), das Skript `scripts/clean-icloud-duplicates.py` verwenden:

```bash
python3 ~/.hermes/scripts/clean-icloud-duplicates.py dry-run   # Nur anzeigen, nicht löschen
python3 ~/.hermes/scripts/clean-icloud-duplicates.py run       # Löschen durchführen
```

**Initialer Einrichtungs-Workflow:**
1. Credentials in `.env` eintragen (`ICLOUD_APPLE_ID` + `ICLOUD_APP_PASSWORD`)
2. `pip install pyicloud` (ins Hermes-Venv)
3. Erstmaligen Sync starten → 2FA-Code vom trusted device eingeben
4. Script danach ohne 2FA wiederverwendbar (Session-Cookie wird persistiert)

**Wichtige Pitfalls (pyicloud):**
- `folder.dir()` gibt eine Liste von **Strings** zurück (Item-Namen), **keine Dictionaries**
- Datei-Inhalt: `resp = sub.open()` → `resp.content` (NICHT `.read()` – Response-Object!)
- Upload: `folder.upload(file_object)` – erwartet ein geöffnetes File-Objekt mit `.name`-Attribut, nicht `bytes`
- Ordner-Prüfung: `try: sub.dir()` schlägt fehl bei Dateien → except-Zweig = Datei
- Ordner anlegen: `folder.mkdir(name)` erzeugt Unterordner in iCloud
- **Content-Änderungen erkennen:** Der Sync-Script-`push`-Modus vergleicht Dateigrößen, nicht nur Dateinamen. Lokal geänderte Dateien mit gleichem Namen werden erkannt und neu hochgeladen. Vor Upload wird die alte Cloud-Datei gelöscht (pyicloud erlaubt kein direktes Überschreiben).

**Wichtig:** pyicloud funktioniert nicht bei Apple-Accounts mit Advanced Data Protection via App-spezifischem Passwort (Fehler -20101, SRP-Handshake schlägt fehl). **Workaround:** normales Apple-ID-Passwort + 2FA verwenden – der OAuth2-Flow umgeht SRP. Session-Cookie wird in `~/.pyicloud/session` für Folgesitzungen gecacht.

**Shell-Escaping von Passwörtern:** Passwörter mit `#` werden in Shell-Befehlen als Kommentar interpretiert. `.env`-Einträge per Python schreiben, nicht per `echo`/heredoc.

## Syncthing Sync (Alternative zu pyicloud)

Wenn pyicloud dauerhaft nicht funktioniert oder ein Echtzeit-Sync gewünscht ist, Syncthing verwenden. Siehe `references/syncthing-setup.md` für die vollständige Einrichtung: Installation, REST-API-Konfiguration, Gerätekopplung und geteilte Ordner.

**Syncthing** ist zuverlässiger als pyicloud (bidirektionaler Echtzeit-Sync, funktioniert mit allen Apple-Sicherheitsstufen). pyicloud mit Main-Password+2FA-Workaround ist eine gute Alternative wenn Syncthing zu aufwändig ist.

**Wichtiger Pitfall:** Syncthing NICHT direkt in einen iCloud-Drive-Ordner syncen lassen — iCloud und Syncthing konkurrieren um Dateiänderungen. Stattdessen in einen lokalen Ordner syncen und diesen in Obsidian öffnen. Details in `references/syncthing-setup.md` §Wichtige Pitfalls.

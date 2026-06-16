# iCloud Drive Sync für Obsidian Vault (via pyicloud)

Nutzt die Python-Bibliothek `pyicloud`, um auf iCloud Drive zuzugreifen und einen Obsidian-Vault auf einem Linux-System zu synchronisieren.

## Voraussetzungen

- Apple-ID mit aktiviertem iCloud Drive
- App-spezifisches Passwort (empfohlen) oder Hauptpasswort
- pyicloud installiert: `pip install pyicloud`

## App-spezifisches Passwort erstellen

1. https://appleid.apple.com/account/manage
2. "App-spezifische Passwörter" → "Passwort generieren"
3. Namen z. B. "Hermes Bob" vergeben
4. Generiertes Passwort notieren (Format: `xxxx-xxxx-xxxx-xxxx`)

## Authentifizierung

```python
from pyicloud import PyiCloudService

api = PyiCloudService('apple-id@email.com', 'app-spezifisches-passwort')

# 2FA-Code abfragen (falls nötig)
if api.requires_2fa:
    code = input('2FA-Code: ')
    result = api.validate_2fa_code(code)
    print(f'2FA valid: {result}')
```

## iCloud Drive Dateien auflisten

```python
# Root von iCloud Drive
drive = api.drive

# Dateien/Ordner im Root auflisten (dir() gibt Strings zurück)
for name in drive.dir():
    print(name)

# In einen Ordner navigieren und rekursiv erkunden
def explore(cloud_folder, path="", depth=0):
    indent = "  " * depth
    for name in cloud_folder.dir():
        print(f"{indent}{name}")
        try:
            sub = cloud_folder[name]
            # Prüfen ob Ordner (dir() schlägt fehl bei Dateien)
            try:
                sub.dir()
                explore(sub, f"{path}/{name}", depth + 1)
            except:
                pass  # Ist eine Datei
        except:
            pass

# Vault-Pfad finden — oft nicht direkt "Obsidian Vault"
# Mögliche Pfade: drive['Obsidian Vault'], drive['Obsidian']['BOB-VAULT']
explore(drive['Obsidian'])
```

## Vault-Dateien herunterladen

```python
import os

def download_folder(cloud_folder, local_path):
    """Rekursiv einen iCloud-Ordner in ein lokales Verzeichnis herunterladen.
    
    Hinweis: dir() gibt *Strings* zurück (Item-Namen), keine Dicts.
    Zugriff auf Unterordner/Dateien erfolgt via cloud_folder[name].
    """
    os.makedirs(local_path, exist_ok=True)
    for name in cloud_folder.dir():
        item_path = os.path.join(local_path, name)
        try:
            sub = cloud_folder[name]
            # Prüfen ob Ordner (hat dir())
            try:
                sub.dir()
                download_folder(sub, item_path)
            except:
                # Ist eine Datei
                resp = sub.open()
                content = resp.content  # Response.content, NICHT .read()!
                with open(item_path, 'wb') as f:
                    f.write(content)
                print(f"  Downloaded: {item_path} ({len(content)} Bytes)")
        except Exception as e:
            print(f"  Fehler bei {name}: {e}")

# Vault-Pfad kann tiefer liegen (z.B. 'Obsidian/BOB-VAULT')
vault = api.drive['Obsidian']['BOB-VAULT']
download_folder(vault, '/pfad/zum/lokalen/vault')
```

## Dateien hochladen (in iCloud Drive)

```python
def upload_file(local_path, cloud_folder, cloud_name=None):
    """Lokale Datei in iCloud-Ordner hochladen.
    
    Wichtig: upload() erwartet ein geöffnetes File-Objekt (mit .name-Attribut),
    NICHT die Datei als Bytes. cloud_folder.upload(data, name) führt zu:
    TypeError: DriveNode.upload() takes 2 positional arguments but 3 were given
    """
    name = cloud_name or os.path.basename(local_path)
    with open(local_path, 'rb') as f:
        cloud_folder.upload(f)
    print(f"  Uploaded: {name}")
```

### Unterordner erstellen vor Upload

```python
# Ordner-Struktur in iCloud aufbauen
rel_parts = rel_path.split(os.sep)
cloud_folder = vault_folder
for part in rel_parts[:-1]:
    try:
        cloud_folder = cloud_folder[part]  # existiert?
    except:
        cloud_folder.mkdir(part)           # neu anlegen
        cloud_folder = cloud_folder[part]

# Datei hochladen
with open(local_file, 'rb') as f:
    cloud_folder.upload(f)
```

## Sync-Workflow (bidirektional)

1. **Pull**: Kompletten Vault aus iCloud Drive herunterladen
2. **Arbeiten**: Notizen lokal lesen/schreiben/erstellen
3. **Push**: Geänderte/neue Dateien zurück in iCloud Drive hochladen

## Sync-Script (wiederverwendbar)

Das fertige Script liegt im Skill-Verzeichnis und in `~/.hermes/scripts/sync-obsidian.py`.

Es liest Credentials aus der `.env` und unterstützt vier Modi:

```bash
# Nur Download von iCloud
python3 ~/.hermes/scripts/sync-obsidian.py pull

# Nur Upload lokaler Änderungen (fehlende Dateien)
python3 ~/.hermes/scripts/sync-obsidian.py push

# Bidirektional: Pull dann Push
python3 ~/.hermes/scripts/sync-obsidian.py sync

# Status anzeigen
python3 ~/.hermes/scripts/sync-obsidian.py status
```

### `.env`-Variablen

```bash
ICLOUD_APPLE_ID=ihre@apple-id.com
ICLOUD_APP_PASSWORD=ihr-passwort-oder-app-spezifisch
```

> **Achtung bei Passwörtern mit `#`**: Shell-Befehle (echo/heredoc) schneiden
> alles ab `#` als Kommentar ab. `.env`-Einträge immer via Python schreiben:
> ```python
> with open('/root/.hermes/.env', 'a') as f:
>     f.write('ICLOUD_APP_PASSWORD=mein...\n')
> ```

## Bekannte Probleme

- **Push erkennt keine Inhaltsänderungen** — der `push`-Modus vergleicht nur Dateinamen (`local_files - cloud_files`). Wenn eine Datei lokal bearbeitet wurde aber bereits unter demselben Namen in iCloud existiert, wird sie **nicht** neu hochgeladen. Zum Aktualisieren muss die Datei zuerst auf iCloud gelöscht, dann neu hochgeladen werden:

  ```python
  cloud_file = cloud_folder['datei.md']
  cloud_file.delete()               # Alte Version löschen
  with open('lokale/datei.md', 'rb') as f:
      cloud_folder.upload(f)        # Neue Version hochladen
  ```

  **Workaround für Sync-Script:** Ein `--force`-Flag oder Content-Hash-Prüfung (z. B. SHA256) wäre nötig, um echten bidirektionalen Sync zu unterstützen. Aktuell ist `push` ein reiner **Erst-Upload** für neue Dateien.

- **pyicloud ist reverse-engineered** — Apple kann die API jederzeit ändern, dann bricht der Zugriff
- **2FA-Sitzung** — nach erfolgreicher 2FA wird ein Sitzungs-Cookie gespeichert, der für einige Zeit gültig bleibt
- **Kein Echtzeit-Sync** — pyicloud ist kein Daemon, sondern wird pro Aufruf ausgeführt
- **Große Dateien** — pyicloud hat Timeout-Probleme bei Dateien > 50 MB
- **Sonderzeichen** — Dateinamen mit Umlauten oder Sonderzeichen können Probleme machen
- **SRP-Authentifizierung fehlgeschlagen** — Fehler `-20101` / `Invalid email/password combination` trotz korrektem App-spezifischem Passwort. Tritt bei Accounts mit Advanced Data Protection oder neueren Apple-Sicherheitsstufen auf. pyiclouds SRP-Handshake wird von Apple abgewiesen.
  - **Workaround (funktioniert oft):** Statt des App-spezifischen Passworts das **normale Apple-ID-Passwort** verwenden. Der Login gelingt dann mit 2FA (Code auf trusted device). Der 2FA-Cookie wird in `~/.pyicloud/session` gespeichert und erlaubt Folgesitzungen ohne erneute 2FA für einige Zeit.
  - Falls auch das nicht funktioniert: zu Syncthing oder Git-Sync wechseln.
- **Shell-Escaping von Passwörtern** — Passwörter mit `#`, `$`, `!` oder anderen Shell-Sonderzeichen werden in `echo`/heredoc-Befehlen abgeschnitten. `.env`-Einträge immer via Python schreiben, nicht via Shell:
  ```python
  # Richtig: Python schreibt den Wert sicher
  with open('/root/.hermes/.env', 'a') as f:
      f.write('ICLOUD_APP_PASSWORD=mein...\n')
  ```
- **Hermes Secret Redaction** — Hermes redigiert API-Keys und Token in der Terminal-Ausgabe. Das kann den Anschein erwecken, ein Passwort sei falsch gespeichert, obwohl es korrekt ist. Zum Prüfen: `python3 -c "print(open('/root/.hermes/.env').read())"` oder das Sync-Script direkt ausführen.
- **Duplikate durch mehrfachen Push** — Wenn das Script mehrfach läuft und der erste Lauf vorzeitig abbricht (z. B. wegen fehlender Ordner-Erstellung), kann es zu Duplikaten mit Suffix ` 2.ext` / ` 3.ext` kommen. Diese lassen sich wie folgt bereinigen:
  ```python
  for name in cloud_folder.dir():
      if ' 2.' in name or ' 3.' in name:
          cloud_folder[name].delete()
  ```

## Alternative: Git-Sync (empfohlen)

Falls der Obsidian-Vault bereits per Git-Plugin synchronisiert wird, ist das Klonen des Git-Repos deutlich zuverlässiger als pyicloud:

```bash
git clone https://github.com/benutzer/obsidian-vault.git /pfad/zum/vault
```
# Syncthing für Obsidian Vault Sync

Syncthing ist eine Open-Source Peer-to-Peer-Synchronisationslösung. Ideal, wenn der Obsidian-Vault auf einem Mac liegt, der Agent aber auf einem Linux-Server läuft — und iCloud/pyicloud nicht funktioniert.

## Vorteile gegenüber pyicloud

- **Keine Apple-Abhängigkeit** — funktioniert auch mit Advanced Data Protection
- **Echtzeit-Sync** — Syncthing läuft als Daemon und syncet kontinuierlich
- **Bidirektional** — Änderungen auf beiden Seiten werden zusammengeführt
- **Keine Cloud** — direkte Peer-to-Peer-Verbindung (oder Relay-Fallback)

## Installation (Linux-Server)

```bash
# Via apt
apt-get install -y syncthing

# Oder via Download (neuere Version)
# https://syncthing.net/downloads/
```

## Einrichtung

### 1. Syncthing starten

Auf einem Headless-Server (kein Browser verfügbar) gibt es zwei Wege:

**Variante A: systemd-Service (dauerhaft, empfohlen)**

```bash
systemctl enable syncthing@root
systemctl start syncthing@root
# Der systemd-service startet automatisch ohne Browser-Fenster.
```

**Variante B: Background-Prozess (für temporäre Sessions)**

```bash
terminal(background=true, command="syncthing --no-browser --home=/root/.config/syncthing")
```

Nach dem Start mit `background=true` die REST-API für die Konfiguration nutzen (siehe unten). Der Prozess läuft im Hintergrund, solange die Session aktiv ist.

**Wichtig:** `--no-browser` verhindert, dass Syncthing versucht, die Web-UI im Browser zu öffnen — auf einem Server ohne GUI würde das sonst fehlschlagen.

### 2. Device-ID ermitteln

```bash
syncthing --device-id --home=/root/.config/syncthing
```

### 3. Remote-Gerät via REST-API hinzufügen

API-Key aus der config.xml holen:

```bash
grep -oP 'apikey="\K[^"]+' /root/.config/syncthing/config.xml
```

Gerät hinzufügen:

```bash
curl -s -X POST -H "X-API-Key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "deviceID": "<REMOTE_DEVICE_ID>",
    "name": "<NAME>",
    "addresses": ["dynamic"],
    "compression": "metadata",
    "introducer": false,
    "autoAcceptFolders": false,
    "paused": false
  }' http://127.0.0.1:8384/rest/config/devices
```

### 4. Geteilten Ordner anlegen

```bash
mkdir -p /pfad/zum/vault

curl -s -X PUT -H "X-API-Key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "obsidian-vault",
    "label": "Obsidian Vault",
    "path": "/pfad/zum/vault",
    "type": "sendreceive",
    "devices": [
      {"deviceID": "<EIGENE_DEVICE_ID>", "introducedBy": "", "encryptionPassword": ""},
      {"deviceID": "<REMOTE_DEVICE_ID>", "introducedBy": "", "encryptionPassword": ""}
    ],
    "rescanIntervalS": 60,
    "fsWatcherEnabled": true,
    "ignorePerms": false,
    "autoNormalize": true
  }' http://127.0.0.1:8384/rest/config/folders/obsidian-vault
```

### 5. Config neu laden / Syncthing neustarten

```bash
curl -s -X POST -H "X-API-Key: <API_KEY>" \
  http://127.0.0.1:8384/rest/system/restart
```

### 6. Status prüfen

```bash
# Verbundene Geräte und Ordner anzeigen
curl -s -X GET -H "X-API-Key: <API_KEY>" \
  http://127.0.0.1:8384/rest/system/connections | python3 -m json.tool

# Systemstatus
curl -s -X GET -H "X-API-Key: <API_KEY>" \
  http://127.0.0.1:8384/rest/system/status | python3 -m json.tool

# Per-Ordner Sync-Status (zeigt ob alle Dateien synchronisiert sind)
curl -s -X GET -H "X-API-Key: <API_KEY>" \
  "http://127.0.0.1:8384/rest/db/status?folder=obsidian-vault" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'State: {d[\"state\"]}')
print(f'Files: {d[\"globalFiles\"]} global, {d[\"localFiles\"]} local')
print(f'In Sync: {d[\"inSyncFiles\"]}')
print(f'Need: {d[\"needFiles\"]} files ({d[\"needBytes\"]/1024:.0f}KB)')
print(f'Errors: {d[\"errors\"]}')
"
# Wenn needFiles=0 und inSyncFiles=globalFiles, ist alles synchron.
```

## Auf dem Mac (Client-Seite)

1. **Syncthing installieren** → https://syncthing.net/downloads/ (macOS-Version)
2. **Starten** → Web-UI öffnet sich im Browser bei `http://127.0.0.1:8384`
3. **Remote-Device hinzufügen:**
   - "Add Remote Device"
   - Device-ID des Linux-Servers eingeben
   - Name vergeben
4. **Obsidian-Vault-Ordner teilen:**
   - "Add Folder"
   - Pfad zum lokalen Obsidian-Vault (z. B. in iCloud Drive)
   - Mit dem Linux-Server-Gerät teilen
   - Folder ID: `obsidian-vault` (muss mit der ID auf dem Server übereinstimmen)

## Nach dem Sync

Sobald die Verbindung steht, wird der Vault automatisch synchronisiert. Der Agent kann dann mit dem Obsidian-Skill ganz normal auf die Dateien zugreifen:

```bash
ls /pfad/zum/vault/*.md
```

## Wichtige Pitfalls

### Syncthing + iCloud Drive = Konflikte

Syncthing sollte **NICHT** direkt in einen iCloud-Drive-Ordner syncen. iCloud und Syncthing konkurrieren dann um Dateiänderungen, was zu Sync-Konflikten, doppelten Dateien und Inkonsistenzen führt.

**Richtiges Vorgehen:**
1. Syncthing auf dem Mac in einen **lokalen Ordner ausserhalb von iCloud** syncen lassen (z. B. `~/Obsidian Vault (Sync)`)
2. In Obsidian diesen **lokalen Ordner als Vault öffnen** (nicht den iCloud-Ordner)
3. Wer den iCloud-Vault behalten will, kopiert Notizen manuell oder nutzt Git-Sync

**Alternative:** Nur einseitig syncen — der Agent schreibt in den lokalen Ordner auf dem Server, der Benutzer arbeitet weiter im iCloud-Vault und kopiert bei Bedarf Notizen manuell rüber.

## Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| Geräte finden sich nicht | Beide Seiten müssen die Device-ID des jeweils anderen kennen. Prüfen mit `curl .../rest/system/connections` |
| Keine Verbindung bei getrennten Netzwerken | Syncthing nutzt globale Discovery-Server und Relay-Fallback. Port 22000/TCP und 21027/UDP müssen nicht manuell geöffnet werden |
| Ordner wird nicht synchronisiert | Prüfen ob die Folder-ID auf beiden Seiten identisch ist |
| Konflikte | Syncthing erzeugt `filename.sync-conflict-<DATUM>-<DEVICEID>.md` bei gleichzeitigen Änderungen |
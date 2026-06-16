#!/usr/bin/env python3
"""Sync Obsidian Vault from/to iCloud Drive via pyicloud.

Usage:
  sync-obsidian.py pull      # Download from iCloud (default)
  sync-obsidian.py push      # Upload local changes to iCloud
  sync-obsidian.py sync      # Pull then push (bidirectional)
  sync-obsidian.py status    # Show sync status

Credentials werden aus ~/.hermes/.env gelesen:
  ICLOUD_APPLE_ID      [required] Apple-ID (E-Mail)
  ICLOUD_APP_PASSWORD  [required] App-spezifisches Passwort oder Hauptpasswort

2FA: Falls nötig, fordert das Script den 6-stelligen Code interaktiv an.
      Sitzung wird von pyicloud gecached (~/.pyicloud/), solange das Cookie lebt.
"""

import os
import sys
from pyicloud import PyiCloudService

ICLOUD_PATH = ["Obsidian", "BOB-VAULT"]
LOCAL_PATH = os.path.expanduser("~/obsidian-vault")
ENV_PATH = os.path.expanduser("~/.hermes/.env")


def get_env(key):
    """Lese einen Wert aus der .env Datei."""
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


def connect():
    apple_id = get_env("ICLOUD_APPLE_ID")
    password = get_env("ICLOUD_APP_PASSWORD")
    if not apple_id or not password:
        print("❌ Keine iCloud-Zugangsdaten in ~/.hermes/.env gefunden!")
        print("   Bitte setzen Sir:")
        print("   ICLOUD_APPLE_ID=ihre@email.com")
        print("   ICLOUD_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx")
        return None
    print("🔄 Verbinde mit iCloud...")
    api = PyiCloudService(apple_id, password)
    if api.requires_2fa:
        print("⚠️  2FA-Code erforderlich!")
        print("   Bitte prüfen Sir Ihr iPhone/Mac auf einen 6-stelligen Code.")
        code = input("   2FA-Code: ").strip()
        if not api.validate_2fa_code(code):
            print("❌ 2FA fehlgeschlagen!")
            return None
        print("✅ 2FA bestätigt")
    return api


def get_vault(api):
    drive = api.drive
    folder = drive
    for part in ICLOUD_PATH:
        folder = folder[part]
    return folder


def pull(api):
    """Download complete vault from iCloud."""
    folder = get_vault(api)
    total_files = 0
    total_bytes = 0

    def download(cloud_folder, local_path):
        nonlocal total_files, total_bytes
        os.makedirs(local_path, exist_ok=True)
        for name in cloud_folder.dir():
            item_path = os.path.join(local_path, name)
            try:
                sub = cloud_folder[name]
                try:
                    sub.dir()  # Ist Ordner?
                    download(sub, item_path)
                except:
                    resp = sub.open()
                    content = resp.content  # Response.content, nicht .read()!
                    with open(item_path, "wb") as f:
                        f.write(content)
                    total_files += 1
                    total_bytes += len(content)
                    print(f"  📥 {name} ({(len(content)/1024):.1f} KB)")
            except Exception as e:
                print(f"  ❌ {name}: {e}")

    print(f"\n📥 Pull: Downloade Vault von iCloud nach {LOCAL_PATH}...\n")
    download(folder, LOCAL_PATH)
    print(f"\n✅ Pull abgeschlossen: {total_files} Dateien ({total_bytes/1024:.1f} KB)")


def push(api):
    """Upload local files to iCloud, including content changes."""
    folder = get_vault(api)

    def list_cloud(cloud_folder, prefix=""):
        existing = {}  # path -> size
        for name in cloud_folder.dir():
            path = os.path.join(prefix, name) if prefix else name
            try:
                sub = cloud_folder[name]
                try:
                    sub.dir()
                    existing.update(list_cloud(sub, path))
                except:
                    # Get file size from cloud if available
                    try:
                        size = sub.size or 0
                    except:
                        size = 0
                    existing[path] = size
            except:
                pass
        return existing

    print("\n☁️  Scanne iCloud-Bestand...")
    cloud_files = list_cloud(folder)
    print(f"   {len(cloud_files)} Dateien in iCloud gefunden")

    # Scan local with sizes
    local_files = {}
    def scan_local(local_path, prefix=""):
        if not os.path.isdir(local_path):
            return
        for name in os.listdir(local_path):
            if name.startswith("."):
                continue
            rel = os.path.join(prefix, name) if prefix else name
            full = os.path.join(local_path, name)
            if os.path.isdir(full):
                scan_local(full, rel)
            else:
                local_files[rel] = os.path.getsize(full)
    scan_local(LOCAL_PATH)
    print(f"   {len(local_files)} Dateien lokal gefunden")

    # New files (don't exist in cloud)
    new_files = set(local_files.keys()) - set(cloud_files.keys())

    # Changed files (same name, different size)
    changed_files = set()
    for path, local_size in local_files.items():
        if path in cloud_files and cloud_files[path] != local_size:
            changed_files.add(path)

    to_upload = new_files | changed_files
    if not to_upload:
        print("✅ Keine Änderungen – lokaler Stand identisch mit iCloud")
        return

    print(f"\n📤 Push: {len(to_upload)} Dateien ({len(new_files)} neue, {len(changed_files)} geänderte)...\n")
    for rel_path in sorted(to_upload):
        local_file = os.path.join(LOCAL_PATH, rel_path)
        try:
            parts = rel_path.split(os.sep)
            cloud_folder = folder
            for part in parts[:-1]:
                try:
                    cloud_folder = cloud_folder[part]
                except:
                    cloud_folder.mkdir(part)
                    cloud_folder = cloud_folder[part]

            # Delete existing file first (required for pyicloud overwrite)
            try:
                existing = cloud_folder[parts[-1]]
                existing.delete()
            except:
                pass

            with open(local_file, "rb") as f:
                cloud_folder.upload(f)
            size_kb = os.path.getsize(local_file) / 1024
            tag = "🔄" if rel_path in changed_files else "📤"
            print(f"  {tag} {rel_path} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"  ❌ {rel_path}: {e}")

    print(f"\n✅ Push abgeschlossen: {len(to_upload)} Dateien ({len(new_files)} neue, {len(changed_files)} geänderte)")


def sync(api):
    """Pull then push = bidirektional."""
    pull(api)
    push(api)
    print("\n✨ Bidirektionaler Sync komplett")


def status(api):
    items = get_vault(api).dir()
    print(f"\n📊 Vault-Status:")
    print(f"   Ordner in iCloud: {len(items)}")
    print(f"   Lokaler Pfad: {LOCAL_PATH}")
    print(f"   Sync-Script: {__file__}")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "pull"
    api = connect()
    if not api:
        sys.exit(1)
    if action == "pull":
        pull(api)
    elif action == "push":
        push(api)
    elif action == "sync":
        sync(api)
    elif action == "status":
        status(api)
    else:
        print(f"❌ Unbekannter Befehl: {action}")
        print("   Verfügbar: pull, push, sync, status")
        sys.exit(1)
    sys.exit(0)

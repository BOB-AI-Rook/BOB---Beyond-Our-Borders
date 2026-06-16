#!/usr/bin/env python3
"""Remove duplicate iCloud files created by stale sync scripts.

iCloud-Vault syncs mit einer alten Script-Version (vor der mkdir()-Unterstützung)
oder wiederholte manuelle Uploads erzeugen manchmal Duplikate mit Namenssuffixen
wie " 2", " 3" etc. (z.B. "BOB_SOUL 2.md", "app 3.json").

Dieses Script findet alle Dateien mit " 2." oder " 3." im Namen unter dem
iCloud-Vault-Pfad und löscht sie.

Verwendung:
  python3 clean-icloud-duplicates.py dry-run   # Nur anzeigen, nicht löschen
  python3 clean-icloud-duplicates.py run       # Löschen durchführen

Credentials werden aus ~/.hermes/.env gelesen:
  ICLOUD_APPLE_ID      [required] Apple-ID (E-Mail)
  ICLOUD_APP_PASSWORD  [required] App-spezifisches Passwort oder Hauptpasswort
"""
import os
import sys

sys.path.insert(0, os.path.expanduser('/usr/local/lib/hermes-agent/venv/lib/python3.11/site-packages'))
from pyicloud import PyiCloudService

ICLOUD_PATH = ["Obsidian", "BOB-VAULT"]
ENV_PATH = os.path.expanduser("~/.hermes/.env")


def get_env(key):
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
        print("   Bitte setzen Sie:")
        print("   ICLOUD_APPLE_ID=ihre@email.com")
        print("   ICLOUD_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx")
        return None
    print("🔄 Verbinde mit iCloud...")
    api = PyiCloudService(apple_id, password)
    if api.requires_2fa:
        print("⚠️  2FA-Code erforderlich! Prüfen Sie Ihr trusted device.")
        code = input("   2FA-Code: ").strip()
        if not api.validate_2fa_code(code):
            print("❌ 2FA fehlgeschlagen!")
            return None
        print("✅ 2FA bestätigt")
    return api


def find_dupes(cloud_folder, prefix=""):
    """Find all files matching 'name 2.ext' or 'name 3.ext' pattern."""
    dupes = []
    for name in cloud_folder.dir():
        rel = os.path.join(prefix, name) if prefix else name
        try:
            sub = cloud_folder[name]
            try:
                sub.dir()  # folder
                dupes.extend(find_dupes(sub, rel))
            except AttributeError:
                pass
            except Exception:
                if " 2." in name or " 3." in name:
                    dupes.append((rel, sub))
        except Exception:
            pass
    return dupes


def main():
    dry_run = len(sys.argv) < 2 or sys.argv[1] != "run"
    label = "🔍 Dry-Run" if dry_run else "🗑️  Löschmodus"
    print(f"\n{label}: Durchsuche iCloud-Vault nach Duplikaten...\n")

    api = connect()
    if not api:
        sys.exit(1)

    drive = api.drive
    folder = drive
    for part in ICLOUD_PATH:
        folder = folder[part]

    dupes = find_dupes(folder)

    if not dupes:
        print("✅ Keine Duplikate gefunden.")
        return

    for rel, _ in sorted(dupes, key=lambda x: x[0]):
        action = "  (trocken)" if dry_run else ""
        print(f"  🗑️  {rel}{action}")

    print(f"\n{'🔍 ' + str(len(dupes)) + ' Duplikate gefunden (dry-run — nichts gelöscht).' if dry_run else
           '🗑️  ' + str(len(dupes)) + ' Duplikate werden gelöscht...'}")

    if dry_run:
        print("\n💡 Zum Löschen ausführen:")
        print(f"   python3 {sys.argv[0]} run")
        return

    for rel, sub in sorted(dupes, key=lambda x: x[0]):
        try:
            sub.delete()
            print(f"  ✅ {rel} — gelöscht")
        except Exception as e:
            print(f"  ❌ {rel} — Fehler: {e}")

    print(f"\n✅ {len(dupes)} Duplikate gelöscht")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Overwrite an existing file on iCloud with the local version.

Usage:
  overwrite-icloud-file.py <relative_path> [relative_path2 ...]

Example:
  overwrite-icloud-file.py BOB/BOB_SOUL.md
  overwrite-icloud-file.py DGM/Firmenprofil.md DGM/Anne-Krenzin.md

What it does:
  1. Deletes the file on iCloud (including its parent-folder lookup)
  2. Re-uploads the local version

Prerequisite:
  ICLOUD_APPLE_ID and ICLOUD_APP_PASSWORD set in ~/.hermes/.env
"""
import os
import sys
sys.path.insert(0, '/usr/local/lib/hermes-agent/venv/lib/python3.11/site-packages')
from pyicloud import PyiCloudService

ICLOUD_PATH = ["Obsidian", "BOB-VAULT"]
LOCAL_ROOT = os.path.expanduser("~/obsidian-vault")
ENV_PATH = os.path.expanduser("~/.hermes/.env")


def get_env(key):
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f'{key}='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


def navigate(folder, parts):
    """Drill into a folder path. Returns the leaf parent folder and the leaf name."""
    for part in parts[:-1]:
        try:
            folder = folder[part]
        except KeyError:
            folder.mkdir(part)
            folder = folder[part]
    return folder, parts[-1]


def main():
    if len(sys.argv) < 2:
        print("Usage: overwrite-icloud-file.py <relative_path> [...]")
        sys.exit(1)

    apple_id = get_env('ICLOUD_APPLE_ID')
    password = get_env('ICLOUD_APP_PASSWORD')
    if not apple_id or not password:
        print("❌ Keine iCloud-Zugangsdaten in ~/.hermes/.env gefunden!")
        sys.exit(1)

    api = PyiCloudService(apple_id, password)
    drive = api.drive
    folder = drive
    for part in ICLOUD_PATH:
        folder = folder[part]

    for rel_path in sys.argv[1:]:
        parts = rel_path.replace('\\', '/').split('/')
        local_file = os.path.join(LOCAL_ROOT, rel_path)

        if not os.path.isfile(local_file):
            print(f"⚠️  Lokale Datei nicht gefunden: {local_file}")
            continue

        parent, leaf_name = navigate(folder, parts)
        size = os.path.getsize(local_file)

        # Delete old if exists
        try:
            old = parent[leaf_name]
            old.delete()
            print(f"🗑️  {rel_path} (alte Version gelöscht)")
        except KeyError:
            print(f"ℹ️  {rel_path} existiert noch nicht auf iCloud")

        # Upload new
        with open(local_file, 'rb') as f:
            parent.upload(f)
        print(f"📤 {rel_path} hochgeladen ({size/1024:.1f} KB)")

    print("✅ Fertig")


if __name__ == '__main__':
    main()

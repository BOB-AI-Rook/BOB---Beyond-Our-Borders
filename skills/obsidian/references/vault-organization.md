# Vault-Organisation für Firmen-/Projektwissen

## Strukturmuster

Bei neuen Firmen/Kunden/Projekten einen eigenen Ordner im Vault anlegen:

```
/<PROJEKT-KÜRZEL>/
  Firmenprofil.md         # Stammdaten, Partner, Tech-Stack
  <Person>-Profil.md      # Schlüsselpersonen (Inhaber, Gründer)
  Produkte-Dienstleistungen.md  # Angebotsübersicht
  Website-Struktur.md     # Seiteninventar, Technik, SEO-Notizen
  Soziale-Medien.md       # Plattform-Präsenz
  Projekt-<Name>-Notizen.md  # Laufende Projekte (Redesign, Launch)
  Infografik-<Jahr>.md    # Grafische Zusammenfassungen (optional)
```

## Wikilinks (Obsidian Graph View)

Jedes Dokument im Ordner bekommt am Ende einen `## Verknüpfte Dokumente`-Block mit `[[Wikilinks]]` zu allen anderen relevanten Dateien im selben Ordner.

**Beispiel:**
```markdown
---

## Verknüpfte Dokumente

- [[Firmenprofil]] – Unternehmensdaten
- [[Anne-Krenzin]] – Inhaberin & Vita
- [[Produkte-Dienstleistungen]] – Angebote im Überblick
- [[Digitales-Lehrbuch]] – Purple Companion
- [[Website-Struktur]] – Seiteninventar & Technik
- [[Soziale-Medien]] – Plattform-Präsenz
```

**Regeln:**
- Jede Datei verlinkt auf alle anderen im selben Ordner (vollständiger Graph)
- Wikilinks nutzen den Dateinamen ohne `.md`-Extension
- Nach dem Link kommt ein Gedankenstrich `–` mit Kurzbeschreibung
- Der Block steht am Ende der Datei, nach `---` getrennt

## Kategorien von Dokumenten

| Typ | Beschreibung | Enthält |
|-----|-------------|---------|
| **Firmenprofil** | Stammdaten | Adresse, USt-ID, Rechtsform, Partner, Tech-Stack, Werte |
| **Personen-Profil** | Schlüsselpersonen | Vita, Ausbildung, Referenzen, Arbeitsweise |
| **Produkte** | Angebotsübersicht | Alle Produkte/Dienstleistungen mit Kurzbeschreibung |
| **Website-Struktur** | Webanalyse | Seiteninventar, Tech-Stack, Blog-Index, Social-Media-Links |
| **Soziale-Medien** | Plattformen | Handles, Plattform-Typen, verbundene Profile |
| **Projekt-Notizen** | Laufende Projekte | Erste Analyse, Todo-Liste, Entscheidungen |
| **Infografik** | Visuelle Zusammenfassung | Beschreibung der erstellten Grafik, Design-Notizen |
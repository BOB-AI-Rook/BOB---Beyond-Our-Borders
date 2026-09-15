# website/

Zwei Dinge, eine gemeinsame Asset-Quelle:

```
website/
├── assets/          # Design System — von beiden genutzt, eine Quelle der Wahrheit
│   ├── tokens.css   # Design Tokens
│   ├── bob.css      # Komponentenbibliothek
│   ├── favicon.svg
│   ├── fonts/       # selbstgehostete Webfonts
│   ├── icons/       # sprite.svg (25 Icons) + Ornamente
│   └── img/         # Bildwelt (WebP)
├── style-guide/     # Der Style Guide — dokumentiert das System
└── v2/              # Die neue Website — nutzt das System
```

**Die alte Website wird nicht angefasst.** Ihr Quellcode liegt nicht in diesem Repo —
`v2/` ist eine eigenständige neue Fassung, die parallel zur laufenden Seite existiert.
Nichts hier überschreibt oder deployt etwas automatisch.

## Ansehen

```bash
cd website && python3 -m http.server 8080
```

- Neue Website → <http://localhost:8080/v2/>
- Style Guide → <http://localhost:8080/style-guide/>

Immer über einen Server öffnen, nicht über `file://` — sonst blockiert CORS die
Schriften und das externe Icon-Sprite.

## Was `v2/` enthält

Eine vollständige Einzelseite mit dem kompletten Inhalt der aktuellen Seite,
wörtlich übernommen und in das Retro-Futurism-System übersetzt:

| Abschnitt | Inhalt |
|---|---|
| Hero | „Agentic AI that gets things done." + Freisteller auf Kreis, Trust-Leiste |
| About | HERMES-Panel in Olive, 3 Fakten, gerahmtes Bild |
| Features | Die vier Capabilities als Karten (01–04) |
| System | Architektur-Panel in Ink: 4 Komponenten mit Kennzahlen + Ausführungsschleife |
| Work | HERMES Core als breite Kachel + 4 Modul-Kacheln |
| Proven | Drei Produktionskennzahlen + Vertrauens-Chips |
| Contact | CTA-Panel in Rust mit E-Mail und Social |
| Footer | Vier Spalten, Ink |

Dazu: funktionierende Mobile-Navigation, Cookie-Hinweis mit `localStorage`,
Skip-Link, Favicon, Open-Graph-Metadaten.

## Deployment

`v2/` ist statisches HTML ohne Build-Schritt. Es braucht `../assets/`, also muss
`website/` als Ganzes ausgeliefert werden — dann liegt die neue Fassung unter `/v2/`
und lässt sich neben der alten Seite testen. Soll sie später die Wurzel werden,
`v2/index.html` nach oben ziehen und die Asset-Pfade von `../assets/` auf `assets/`
ändern.

## Inhalt ändern

Alles Visuelle kommt aus `assets/tokens.css` und `assets/bob.css` — in `v2/index.html`
steht nur Inhalt und Seitenlayout. Farben, Radien oder Typo ändert man in den Tokens,
nicht in der Seite. Die Regeln dazu stehen im [Style Guide](./style-guide/).

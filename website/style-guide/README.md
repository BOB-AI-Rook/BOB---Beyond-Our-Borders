# BOB Design System — Retro-Futurism v1.0

Style Guide für den Relaunch von **[beyondourborders.cloud](https://beyondourborders.cloud/)**.

Der Guide ist selbst in seinem eigenen Design gebaut — er ist kein Screenshot-PDF,
sondern lauffähiger Code. Was im Guide zu sehen ist, ist genau das, was die Website ausliefert.

```
website/
├── assets/                 # gemeinsam genutzt von Style Guide und Website
│   ├── tokens.css          # Design Tokens — einzige Quelle der Wahrheit
│   ├── bob.css             # Komponentenbibliothek — produktionsreif
│   ├── favicon.svg
│   ├── fonts/              # Selbstgehostete Webfonts + fonts.css
│   ├── icons/
│   │   ├── sprite.svg      # 25 Icons als SVG-Sprite
│   │   ├── spark.svg       # Ornament: Funke
│   │   ├── orbit-ring.svg  # Ornament: Orbit
│   │   └── wireframe-terrain.svg
│   └── img/                # 11 Motive, WebP, alle aus einem Prompt
├── style-guide/index.html  # Der Style Guide (dieses Dokument)
└── v2/index.html           # Die neue Website
```

## Ansehen

```bash
cd website && python3 -m http.server 8080
# Style Guide → http://localhost:8080/style-guide/
# Website    → http://localhost:8080/v2/
```

Über `file://` fehlen wegen CORS die Schriften und das Icon-Sprite — immer über einen Server öffnen.

## In die Website einbinden

```html
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/tokens.css">
<link rel="stylesheet" href="/assets/bob.css">
```

Icons per Sprite:

```html
<svg><use href="/assets/icons/sprite.svg#i-orchestration"/></svg>
```

`<body class="bob-grain">` setzen — das Korn-Overlay gehört zum System und ist nicht optional.

## Die kurzen Regeln

| | |
|---|---|
| **Farbe** | 60 % Creme · 25 % Ink · 10 % Olive · 5 % Rust. Kein `#FFF`, kein `#000`. |
| **Akzent auf Dunkel** | Nie `--bob-rust`, immer `--bob-rust-soft`. `bob.css` erzwingt das über `.on-dark`. |
| **Display** | Anton, immer Versalien, 2–4 Zeilen, **genau eine** Zeile in Rust. |
| **Schriftrollen** | Anton = Headline · Space Grotesk = Fließtext · Space Mono = Label · Parisienne = Signatur (max. 1×/Seite). |
| **Buttons** | Enden immer in einem Kreis-Dot mit Icon. Ein Primary pro Bildschirm. |
| **Form** | Pill (999px) für Interaktives, 22px Karte, 32px Panel. |
| **Ornamente** | Max. 3 pro Bildschirmhöhe, immer `pointer-events:none`. |
| **Verboten** | Verläufe, Glow, Neon, Glasmorphismus, fremde Icon-Sets. |

Vollständige Begründung und Kontrastwerte: Abschnitte 02, 03 und 09 im Guide.

## Assets erweitern

**Bilder** — ausschließlich über den dokumentierten Prompt erzeugen, nur `[MOTIV]` tauschen.
So bleibt die Bildfamilie geschlossen (Abschnitt 06 im Guide).

**Icons** — im 24×24-Raster, Strichstärke 1.75, runde Enden, nur Kreise/Bögen/45°-Diagonalen.
Als neues `<symbol id="i-…">` in `sprite.svg` ergänzen.

## Technisches

- **Schriften selbstgehostet** — keine Requests an Google Fonts. Für eine deutsche
  Seite ist das Hotlinking von Google Fonts ein DSGVO-Risiko; die Dateien liegen
  unter `assets/fonts/` (latin + latin-ext, ~220 KB).
- **Kontrast** — alle dokumentierten Kombinationen erfüllen mindestens WCAG AA.
- **Motion** — respektiert `prefers-reduced-motion`; der Rundstempel hält dann an.
- **Responsive** — geprüft bei 390 / 768 / 1280 / 1600 px, kein horizontaler Überlauf.
- **Bilder** — WebP, zusammen ~1,4 MB.

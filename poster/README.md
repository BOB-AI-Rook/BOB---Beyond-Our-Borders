# BOB Poster — "A Chatbot, An Agent, Or Both?"

Nachbau des RISEKLIX-Posterlayouts mit den Inhalten von
[beyondourborders.cloud](https://beyondourborders.cloud/).
Design (Raster, Farben, Typo-System, Bildaufbau) bleibt unverändert —
nur die Texte sind auf BOB / HERMES umgestellt.

| Datei | Zweck |
|---|---|
| `bob-poster.html` | Fertiges, self-contained Poster (1024 × 1536, Fonts eingebettet) |
| `bob-poster.png`  | Export in 2× (2048 × 3072) |
| `poster.body.html` | Markup (Formen, Silhouetten, Text) |
| `poster.style.css` | Layout, Typografie, Textur |
| `fonts.css` | Anton / Archivo / Source Serif 4 als Base64-woff2 |
| `build.py` | Baut `bob-poster.html` aus Body + Style + Fonts |
| `shot.js` | Rendert das PNG (Playwright + Chromium) |

## Build

```bash
python3 poster/build.py      # HTML neu zusammenbauen
node poster/shot.js          # PNG rendern
```

## Textzuordnung (Original → BOB)

| Original | BOB |
|---|---|
| DATA SHOWS POTENTIAL. / PEOPLE MAKE IT REAL. | ANSWERS SHOW POTENTIAL. / EXECUTION MAKES IT REAL. |
| AI VISIBILITY, STRATEGY, … | MULTI-AGENT, ORCHESTRATION, AUTOMATION, KNOWLEDGE, INTEGRATIONS |
| TOOLS — TRACK/ANALYZE/… | CHATBOT — ASK/ANSWER/SUGGEST/EXPLAIN/REPEAT |
| AGENCY — RESEARCH/CREATE/… | HERMES — UNDERSTAND/ROUTE/EXECUTE/DELIVER/DONE |
| A DASHBOARD, AN AGENCY, OR BOTH? | A CHATBOT, AN AGENT, OR BOTH? |
| Choose the missing capability… | Choose the system that finishes the work, not the one with the best answer. |
| RISEKLIX | BOB — Beyond Our Borders, built on the HERMES agent system |

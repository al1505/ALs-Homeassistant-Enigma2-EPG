# HA Project Conventions v1.0 — Home-Assistant-Hausstil

> Last updated: 2026-06-03
> Status: **Geseedet aus der kanonischen HA-Baseline** (`H:\ALs-CustomDev\04-design\ha-project-conventions.md`)
>
> **Projekttyp:** HA **Custom Integration** (Python, `custom_components/als_enigma2_epg`) — kein Lovelace-Card. Die Card-spezifischen Abschnitte (§1 Custom Properties, §2 Card-Font, §5.1, §7 Card-Container, §8) gelten sinngemäß für die Card-Konsumenten dieser Integration (z.B. die Harmony Companion Card). **Für dieses Repo maßgeblich:** §3 Logo/Icons (Brand-PNGs), §4 Icons (`icons.json`/MDI), §5.2 Config-Flow, §6 Voice & Tone (inkl. `strings.json`), §9 HACS/Release.

> **Governance (CustomDev):** Das ist KEINE Markenpalette. HA-Projekte erben das
> **Theme des Nutzers** über CSS-Variablen. Jede Card/Integration sieht so aus, wie
> der Nutzer sein HA eingestellt hat (Light/Dark, eigenes Theme). Es gibt deshalb
> **keine festen Hex-Farben**, keinen eigenen Font, kein eigenes Logo. Dieses Dokument
> ist die Single Source of Truth für den HA-Hausstil und wird in jedes HA-Projekt nach
> `docs/brand-guidelines.md` geseedet.
>
> **Abgrenzung:** `04-design/bhb-brand-guidelines.md` ist die Kundenmarke BHB und gilt
> NUR für BHB-Projekte — niemals für HA-Projekte. Die globale **MDI-only**-Regel
> (siehe §4) gilt projektübergreifend, also auch hier.
>
> **Tiefere Mandate:** Die technischen Pflicht-Patterns leben kanonisch in
> `D:\ALs\Codex\HA-ARCHITECTURE.md` (das Was/Warum), `HA-COOKBOOK.md` (Rezepte) und
> `HA-RETROSPECTIVE.md` (Lessons Learned). Dieses Dokument ist der Design-/Konventions-Auszug.

## Quick Reference

| Element | Value |
|---------|-------|
| Farben | **HA-Theme-Variablen** (`var(--primary-color)` …) — KEINE festen Hex |
| Typografie | HA-Default (geerbt, kein eigener Font-Load) |
| Icons | Material Design Icons (`mdi:*` / `<ha-icon>`) — ausschließlich |
| Light/Dark | folgt automatisch dem HA-Theme (nicht selbst umschalten) |
| Kapselung (Card) | Shadow DOM Pflicht (`attachShadow({ mode: 'open' })`) — für konsumierende Cards |
| Setup (diese Integration) | **Config-Flow** (`config_flow: true`) + OptionsFlow — kein YAML-only |
| Datenholer | EIN `DataUpdateCoordinator`, alle Entities lesen daraus |
| Voice | Professionell, klar, sachlich (DE) |

---

## 1. Color Palette — = HA-Theme-Variablen

> **KEINE eigene Palette. KEINE festen Hex-Werte.** Eine HA-Card/Integration erbt das
> Theme des Nutzers. Wer feste Farben hardcodet, bricht Light/Dark und fremde Themes.
> Verbindlich aus `HA-ARCHITECTURE.md` §4.2: *„Keine festen Farbwerte. Immer HA-Variablen
> verwenden (z. B. `var(--primary-text-color)`)."*

### Kern-Theme-Variablen (immer diese nutzen)

| Variable | Verwendung |
|----------|------------|
| `var(--primary-color)` | Akzent, aktive Zustände, CTAs, Links |
| `var(--accent-color)` | Sekundärer Akzent / Highlights |
| `var(--card-background-color)` | Card-Fläche / Hintergrund |
| `var(--primary-background-color)` | Seiten-/Panel-Hintergrund |
| `var(--secondary-background-color)` | abgesetzte Flächen, Sub-Bereiche |
| `var(--primary-text-color)` | Überschriften, Fließtext |
| `var(--secondary-text-color)` | Captions, gedämpfter Text, Labels |
| `var(--disabled-text-color)` | deaktivierte Elemente, Platzhalter |
| `var(--divider-color)` | Trennlinien, Rahmen, Borders |
| `var(--state-icon-active-color)` | aktives Icon (z.B. eingeschaltet) |
| `var(--state-icon-color)` | Standard-Icon-Farbe |

### Semantic / State (HA-eigene Variablen)

| State | Variable |
|-------|----------|
| Erfolg / Ein | `var(--success-color)` (Fallback `var(--state-active-color)`) |
| Warnung | `var(--warning-color)` |
| Fehler / Aus | `var(--error-color)` |
| Info | `var(--info-color)` |

### Card-lokale Custom Properties (nur wenn nötig)

Wenn eine Card **nutzer-konfigurierbare** Akzentfarben anbietet (z.B. Energiefluss-Farben,
Hub-Identity-Farben), wird ein **eigener CSS-Custom-Property mit Theme-Fallback** definiert —
niemals ein nackter Hex-Literal im Style:

```css
/* gut: konfigurierbar, fällt auf Theme zurück */
color: var(--w-heute, var(--primary-color));
background: var(--remote-bg, var(--card-background-color));
```

```css
/* verboten: feste Markenfarbe, ignoriert Nutzer-Theme */
color: #1B4F82;
```

> Quelle ist der Nutzer (Editor-Eingabe) → in `--custom-prop` schreiben → mit
> Theme-Variable als Fallback rendern.

---

## 2. Typography — HA-Default

> **Kein eigener Web-Font, kein `@font-face`, kein Google-Fonts-Load.** Die Card erbt
> die Schrift des HA-Frontends (HA nutzt seinen eigenen Sans-Stack). Das hält Cards
> schnell, offline-/intranet-tauglich und konsistent mit dem restlichen Dashboard.

### Regeln

- Font-Family **nicht** setzen — erben lassen (`font-family: inherit;` falls nötig).
- Größen relativ/in `px` an HA angelehnt; keine extremen Abweichungen vom HA-Look.
- Für Zahlen in KPIs/Tabellen: `font-feature-settings: 'tnum';` (tabellarische Ziffern).
- Per-Element-Schriftgröße/-art **nur**, wenn die Card es dem Nutzer als Konfig anbietet
  (siehe Harmony-Card Text-Element-Editor) — dann über Konfig, nicht hardcodiert.

```css
/* Default in der Card */
:host { font-family: inherit; color: var(--primary-text-color); }
```

---

## 3. Logo Usage

> HA-Projekte führen **kein eigenes Marken-Logo** in der UI. Identität kommt vom
> HA-Theme des Nutzers.

**Integrationen** (HACS Brand-Store) brauchen lediglich technische Icons:

| Datei | Größe | Zweck |
|-------|-------|-------|
| `custom_components/<domain>/icon.png` | 256×256 | HA-Integrationsseite |
| `custom_components/<domain>/icon@2x.png` | 512×512 | Retina |
| `custom_components/<domain>/brand/icon.png` | 256×256 | HACS-Brand-Store |
| `custom_components/<domain>/brand/icon@2x.png` | 512×512 | HACS-Brand-Store |

Don'ts: keine fremden Marken-Assets, kein Logo-Overlay in der Card, echtes PNG (kein
umbenanntes JPEG — sonst wird das Icon nicht angezeigt, siehe Cookbook §6.3).

---

## 4. Icons — MDI / ha-icon (ausschließlich)

> **VERBINDLICH — globale CustomDev-Regel, überstimmt jeden Engine-Default.**

- **Set: ausschließlich Material Design Icons** (`mdi:*`).
- **In Cards (JS/Lovelace):** `<ha-icon icon="mdi:NAME"></ha-icon>` oder Konfig-Wert `mdi:NAME`.
- **In Integrations:** `icons.json` mappt Entities auf MDI:
  ```json
  { "entity": { "sensor": { "epg": { "default": "mdi:television-play" } } }, "services": {} }
  ```
  Minimum-Inhalt wenn keine Entity-Icons: `{}` bzw. `{ "services": {} }`.
- **Keine** Emojis als UI-Icons. **Keine** anderen Icon-Sets (kein Lucide/Heroicons/Font Awesome).
- Icon-Farbe per `currentColor` bzw. Theme-Variable (`var(--state-icon-active-color)`), nicht fest.

> Hinweis: Emojis in README/Doku (Feature-Listen) sind erlaubt — diese Regel betrifft
> **UI-Icons** in Card und Integration.

---

## 5. Setup / Config-Flow

> Wie wird das Projekt eingerichtet? Cards über den Lovelace-Editor, Integrationen über
> den HA Config-Flow. Patterns kanonisch in `HA-COOKBOOK.md` §4–§5.

### 5.1 Custom Card (JavaScript)

- **Shadow DOM Pflicht:** `this.attachShadow({ mode: 'open' });` (CSS-Isolation, kein Bleeding).
- **Editor statt YAML:** `static getConfigElement()` + `static getStubConfig()` implementieren →
  vollständige Konfiguration im UI, kein YAML-Zwang.
- **Registrierung:** `customElements.define("<name>", Klasse)` + `window.customCards.push({ type, name, description })`.
- **YAML-Typ:** `type: custom:<name>` (== String aus `customElements.define`).
- **Silent-Return** am Anfang jeder Render-Funktion: `if (!this._hass) return;` (kein Crash beim HA-Boot).
- **Service-Calls** immer absichern: `hass.callService(...).catch(()=>{})`.
- **XSS:** jede Nutzer-String-Ausgabe durch eine `esc()`-Funktion (HTML-Injection verhindern).
- **Dateiname kleingeschrieben** (`ha-energiebilanz-card.js`) — HAOS/Linux ist case-sensitiv.
- **Editor-DOM:** Card im Shadow-DOM, **Editor** ggf. im Light-DOM (HA-Selektoren greifen dort).

### 5.2 Custom Integration (Python)

- **`config_flow: true`** im `manifest.json` — Einrichtung über UI, kein YAML-only.
- **`ConfigFlow` + `OptionsFlow`:** Ersteinrichtung + nachträgliches Ändern (`async_get_options_flow`).
- **`strings.json`:** alle Fehlerkeys des Config-Flow (`cannot_connect`, `invalid_auth`, `timeout`, …) + Feld-Labels.
- **`DataUpdateCoordinator`:** EIN zentraler Datenholer, alle Entities lesen daraus (kein Abruf pro Entity).
- **`CoordinatorEntity`** als Basis aller Entities; `_attr_has_entity_name = True`.
- **`async_config_entry_first_refresh()`** im Setup (sonst `unavailable` nach Neustart).
- **`_device_info()`** zentral, alle Entities gruppieren sich zu EINEM Device.
- **Lange Werte** (URLs/Beschreibungen >255 Zeichen): State = `"(See Details)"`, voller Wert in `extra_state_attributes`.
- **`manifest.json`-Pflichtfelder:** `domain`, `name`, `version`, `codeowners`, `config_flow`, `iot_class`, `documentation`, `issue_tracker`, `requirements`, `dependencies`.

### 5.3 Versionskompatibilität

- `hacs.json`/`manifest.json`: HA-Mindestversion **`2024.1.0`** (projektübergreifend einheitlich).

---

## 6. Voice & Tone

> Gilt für README, UI-Texte, Config-Flow-Strings, Fehlermeldungen, CHANGELOG.

| Trait | We Are | We Are Not |
|-------|--------|------------|
| Professionell | sachkundig | steif, floskelhaft |
| Klar | direkt, knapp | vage, wortreich |
| Sachlich | belegt, präzise | werblich, übertrieben |
| Vertrauenswürdig | verlässlich | großspurig |

### Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Dokumentation | klar, anleitend | „Datei nach `/config/www/community/<name>/` kopieren." |
| Config-Flow-Fehler | ruhig, lösungsorientiert | „Verbindung fehlgeschlagen — IP-Adresse und Port prüfen." |
| Erfolg | knapp, bestätigend | „Gespeichert." |

### Prohibited Terms (Anti-AI-Slop, DE + EN)

| Avoid | Reason |
|-------|--------|
| revolutionär / bahnbrechend | überzogene Behauptung |
| nahtlos / seamless | Floskel |
| Synergie / synergy | Corporate-Jargon |
| leveragen | „nutzen" verwenden |
| ganzheitlich | inhaltsleer |
| Best-in-Class / erstklassig | vage Behauptung |
| in der heutigen schnelllebigen Welt | Füll-Phrase |

---

## 7. Design Components

> Komponenten erben Farbe/Form aus dem HA-Theme. Die folgenden Tokens nutzen Theme-Variablen,
> keine festen Werte.

### Card-Container

- HA rendert Cards in `<ha-card>` — dessen Radius/Shadow/Background kommen vom Theme.
- Eigene Container: `background: var(--card-background-color)`, `color: var(--primary-text-color)`.

### Buttons / interaktive Elemente

| Element | Background | Text/Icon |
|---------|------------|-----------|
| Primär / aktiv | `var(--primary-color)` | `var(--text-primary-color)` |
| Standard | `var(--secondary-background-color)` | `var(--primary-text-color)` |
| Deaktiviert | — | `var(--disabled-text-color)` |
| Fehler/destruktiv | — | `var(--error-color)` |

### Border / Divider

- Rahmen & Trennlinien: `1px solid var(--divider-color)`.
- Eckradius an HA angelehnt (HA-Default ~12px Cards); nicht mit fremden Marken-Radien überschreiben.

### Z-Index (aus `HA-ARCHITECTURE.md` §4.2)

| Layer | Bereich |
|-------|---------|
| Hintergrund | 0–10 |
| Klick-Zonen | 20–30 |
| Steuerung/Overlay | 50+ |

### Motion

- Dezente Transitions; keine grellen Effekte. Beispiel: `transition: all 150ms ease;`

---

## 8. Mobile-First UX

- **Touch:** Wischgesten via `touchstart/touchend`; `touch-action: pan-y` (vertikales Scrollen nicht blockieren).
- **Bottom-Sheet** statt Hover-Tooltip auf Smartphones (Finger verdeckt sonst den Inhalt).
- **0-Pixel-Dilemma:** dynamische Balken bei 0% mit unsichtbarer 100%-Höhe-Klickzone überlagern.
- **SVG-Touch:** Koordinaten mathematisch skalieren (`Internal_Width / Element_Width`).

---

## 9. HACS / Release

> Sichtbarkeit + Updates laufen über GitHub-Releases. Patterns kanonisch in `HA-COOKBOOK.md` §2–§3.

### Pflicht pro HA-Repo

- `hacs.json`:
  - Card: `{ "name": "...", "render_readme": true, "filename": "<card>.js" }`
  - Integration: `{ "name": "...", "render_readme": true, "homeassistant": "2024.1.0" }`
- `.github/workflows/validate.yaml` (`hacs/action@main`, `category: plugin` bzw. `integration`).
- Integration zusätzlich: `.github/workflows/hassfest.yaml` (`home-assistant/actions/hassfest@master`).
- **README mit HACS-Badge** (`my.home-assistant.io/redirect/hacs_repository/?...`) — `repository` = GitHub-Repo-Name.
- **PayPal-Badge** Pflicht (`https://paypal.me/al1505`).

### Release-Workflow (verbindlich)

1. Version bumpen (Card: im JS-Header; Integration: **zusätzlich** in `manifest.json` — sonst erkennt HACS kein Update).
2. `git add <dateien>` — **niemals** `-A`.
3. Commit + Push.
4. `git tag vX.Y.Z && git push origin vX.Y.Z`.
5. **`gh release create vX.Y.Z`** — Pflicht. HACS erkennt neue Versionen NUR über getaggte Releases, nicht über Commits.

### Konventionen

- Repo-Name mit Großbuchstaben (`ALs-Homeassistant-...`) — HACS-kompatibel.
- Semantic Versioning (`vMAJOR.MINOR.PATCH`).
- Entwicklung auf Feature-Branch, nicht direkt auf `master`.
- Plugin-Pfad in HA: `/config/www/community/<plugin-name>/`.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-03 | Aus kanonischer HA-Baseline geseedet und für die **Enigma2 Custom Integration** adaptiert (Integration-Framing im Kopf + Quick Reference; Card-Abschnitte gelten sinngemäß für Konsumenten-Cards). Theme-Variablen statt Palette; MDI-only; Config-Flow; HACS/Release. |

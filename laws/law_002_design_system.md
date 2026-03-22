# Dark Hangar: The EN-OS Design Specification
**Status:** Canonical / Binding (`law_002`)

This document is the absolute authoritative source of truth for the Mechanical / Dark Hangar user interface aesthetic. All Autonomous Agents generating UI (via Stroke, Astro, or React) MUST adhere to these exact design tokens.

## 1. Topography & Structure
- **Border Radius:** `0px` universally. No rounded corners. The interface must feel brutally functional, like military hardware.
- **Borders:** `1px solid rgba(255, 255, 255, 0.1)`. Panels and containers must be starkly delineated.
- **Backgrounds:** 
  - Base App: `#000000` (True Black)
  - Surface elements (Headers, Terminals): `#0A0A0A` to `#111111`.
  - Glassmorphism is FORBIDDEN.

## 2. Typography
- **Primary Typeface:** `JetBrains Mono`. All numerical displays, logs, status indicators, and headers must use monospace to reinforce the CLI-first ethos.
- **Weights:** Variable (300 for normal text, 700 for data readouts).
- **Line Height:** Dense. Information density over white space.

## 3. The Threat Interface Palette
We do not use generic "red, yellow, green". We use high-visibility neon accent lighting on deep black backgrounds.
- **CRITICAL (Primary Action / Error):** `Neon Amber` / `Safety Orange` (#FF6600)
- **STABLE (Success / Online):** `Matrix Green` (#00FF00)
- **ANALYSIS (Info / Selected):** `Cyan` / `Electric Blue` (#00FFFF)
- **TEXT (Base):** Pale Ash `#E0E0E0`

## 4. Interaction Physics
- **Hover States:** Immediate hard borders or un-muting of text color. No slow, bouncy CSS transitions.
- **Selection:** Solid filled boxes for selected states, hollow 1px borders for unselected.
- **Cursor:** Rely on the global environment context (e.g., crosshairs for specific data point selection, text-cursors for logs).

## 5. Constraint Cage Enforcement
If you are generating a React or Astro component:
1. You MUST NOT use TailwindCSS unless explicitly directed. Use raw CSS or standard inline styling if required by the target project.
2. You MUST NOT inject arbitrary gradients, rounded cards, or soft drop-shadows.
3. Your component MUST look completely native if dropped randomly inside a 1990s hacker terminal.

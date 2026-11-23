# Copen Haus – guest guide

Static site (no build step). Open `index.html` in a browser to preview.

## Pages
| URL | Page |
|---|---|
| `/` (`index.html`) | Guest guidebook (the main page guests get): house manual, trash & rules, getting here, food, pick-up & tours, apps & emergency, Wi-Fi QR and host contacts. Opens in `?lang=` if present; otherwise the language last picked with 한/ENG on that phone; otherwise Korean if the phone's language is Korean, English for everything else. |
| `/brochure/` (`brochure/index.html`) | Short arrival guide in the same design as the guidebook: check-in & check-out, getting here, the 7 house rules, host contacts and emergency numbers. No links to the guidebook. Meant as quick info for guests before check-in. Picks its language the same way as the guidebook (shared 한/ENG memory). Not linked from the guidebook. |

The 한/ENG button on either page updates `?lang=` in the address, so a shared link or a reload keeps the language.

Appliance guides can be linked directly: `#heating`, `#washer`, `#dryer`, `#microwave`, `#induction`, `#tv`.

## First-time guest features
- "처음 오셨다면 이 순서로" steps under the hero: door, Wi-Fi, heating, trash & rules, and the check-out checklist.
- "지금 필동은" card: Seoul time plus what matters right now (quiet hours, trash days, check-out/check-in, Monday/Sunday closures).
- Appliance grid at the top of the house manual; app download buttons open the App Store on iPhone and Google Play on Android.
- KakaoTalk/LINE in-app browsers get an "Open in browser" button.

## Files
| File | Used for |
|---|---|
| `index.html` | Guidebook page (all CSS/JS inline) |
| `brochure/index.html` | Arrival brochure page (all CSS/JS inline) |
| `img/` | Guidebook diagrams and building photos (from the printed 1F guidebook) |
| `hero.jpg` | Hero photo |
| `qr.png` | Wi-Fi QR code (guidebook) |
| `og.jpg` | Link preview image (KakaoTalk, LINE, etc.) |
| `favicon.png`, `apple-touch-icon.png` | Browser tab / home-screen icons |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |

## Publish on GitHub Pages
1. Upload all files to the repository root.
2. Settings → Pages → Source: *Deploy from a branch* → Branch `main` / `(root)` → Save.
3. Link previews use `https://ywy9102-bot.github.io/CopenHaus/og.jpg` (set in the `og:image` line of both pages).

## Before sharing publicly
The page contains the host's phone number, Wi-Fi password and the house address.
Both pages have `<meta name="robots" content="noindex,nofollow,noarchive">` so search engines skip them,
but anyone with the link can read them. Remove that meta tag if you want the pages to be searchable.

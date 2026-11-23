# Copen Haus – guest guide

Static site (no build step). Open `index.html` in a browser to preview.

## Pages
| URL | Page |
|---|---|
| `/` (`index.html`) | Guest guidebook (the main page guests get): house manual, trash & rules, getting here, food, pick-up & tours, apps & emergency, Wi-Fi QR and host contacts. Korean, English and Japanese (`?lang=ko|en|ja`). Opens in `?lang=` if present; otherwise the language last picked with the language button on that phone; otherwise the phone's language (Korean → Korean, Japanese → Japanese, everything else → English). |
| `/brochure/` (`brochure/index.html`) | Short arrival guide in the same design as the guidebook: check-in & check-out, getting here, the 7 house rules, host contacts and emergency numbers. No links to the guidebook. Meant as quick info for guests before check-in. Picks its language the same way as the guidebook (shared 한/ENG memory). Not linked from the guidebook. |

The 한/ENG button on either page updates `?lang=` in the address, so a shared link or a reload keeps the language.
The guidebook's language button (globe icon, top right and in the sticky menu bar) opens a list: 한국어 / English / 日本語. The brochure is still Korean/English only; it ignores `ja` and falls back to the phone's language.

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
| `img/` | Guidebook diagrams and building photos (from the printed 1F guidebook); `img/en/` and `img/ja/` hold the same diagrams relettered in English and Japanese |
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

## Adding a language (e.g. Chinese)
The guidebook is built so a new language is mostly translation work. For Simplified (`zh-hans`) and Traditional (`zh-hant`) Chinese:
1. `index.html` head script: add the code to `CH_LANGS` (the phone-language detection already maps `zh-CN/zh-SG/zh-Hans` → `zh-hans` and `zh-TW/zh-HK/zh-MO/zh-Hant` → `zh-hant`), and add its Google Fonts family to `CH_FONT` (Noto Sans SC / Noto Sans TC).
2. CSS: add `html:not([data-lang=zh-hans]) .zh-hans` to the hide rule, plus a font/line-break block like the `html[lang=ja]` one.
3. Text: next to every `class="ja"` element add a `class="zh-hans"` one; next to every `data-label-ja` / `data-toast-ja` / `data-alt-ja` add `data-label-zh-hans` etc. Anything missing falls back to English.
4. Script: add a row to the `LANG` table (tab title, "switched" message, screen-reader text), and the `zh-hans` strings in the "지금 필동" card, copy-failed and in-app messages.
5. Language list (`#langmenu`) and the language button labels: one more row / span each.
Diagrams (`img/en/`) are reused for every non-Korean language unless you add `data-src-zh-hans`.

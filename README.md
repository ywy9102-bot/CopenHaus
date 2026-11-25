# Copen Haus – guest guide

Static site (no build step). Open `index.html` in a browser to preview.

## Pages
| URL | Page |
|---|---|
| `/` (`index.html`) | Guest guidebook (the main page guests get): house manual, trash & rules, getting here, food, pick-up & tours, apps & emergency, Wi-Fi QR and host contacts. Korean, English, Japanese, Simplified Chinese and Traditional Chinese (`?lang=ko|en|ja|zh-CN|zh-TW`). Opens in `?lang=` if present; otherwise the language last picked with the language button on that phone; otherwise the phone's language (Korean → Korean, Japanese → Japanese, zh-CN/zh-SG/zh-Hans → Simplified, zh-TW/zh-HK/zh-MO/zh-Hant → Traditional, everything else → English). |
| `/brochure/` (`brochure/index.html`) | Short arrival guide in the same design as the guidebook: check-in & check-out (incl. 220V / plug type and supplies to bring), getting here, the 7 house rules, host contacts and emergency numbers. No links to the guidebook. Meant as quick info for guests before check-in. Korean, English, Japanese, Simplified and Traditional Chinese, with the same language button, `?lang=` codes, phone-language detection and remembered choice as the guidebook (the choice is shared between the two pages). Japanese/Chinese text reuses the guidebook's reviewed translations, and the walking map uses the same per-language images. Not linked from the guidebook. |

The language button on either page updates `?lang=` in the address, so a shared link or a reload keeps the language.
The guidebook's language button (globe icon, top right and in the sticky menu bar) opens a list: 한국어 / English / 日本語 / 简体中文 / 繁體中文. Simplified Chinese uses mainland wording, Traditional Chinese uses Taiwan wording. `?lang=zh-hans` / `zh-hant` / `zh-HK` also work; the address always shows `zh-CN` or `zh-TW`.

Appliance guides can be linked directly: `#heating`, `#washer`, `#dryer`, `#microwave`, `#induction`, `#tv`, `#power` (220V / plug type), `#amenities` (what’s in the house), `#trouble` (if something’s not working). Safety info (fire extinguisher, breaker, first aid) is under emergency numbers at `#safety`.

## First-time guest features
- "처음 오셨다면 이 순서로" steps under the hero: door, Wi-Fi, heating, trash & rules, and the check-out checklist.
- "지금 필동은" card: Seoul time plus what matters right now (quiet hours, trash days, check-out/check-in, Monday/Sunday closures).
- Appliance grid at the top of the house manual; app download buttons open the App Store on iPhone and Google Play on Android.
- KakaoTalk/LINE in-app browsers get an "Open in browser" button.

## Floor picker (GF · 1F · 2F · 3F)
Wi-Fi and the washer/dryer differ by unit. The welcome card asks "몇 층에 묵으세요?" once; the Wi-Fi card and the washer/dryer cards have the same GF·1F·2F·3F buttons, and all of them stay in sync. The pick is remembered on that phone (`ch-floor`) and can be changed anytime. `?floor=gf|1|2|3` opens the page on that floor (handy for per-unit links). Old `?floor=b1` links and a saved `b1` pick are read as GF.
- Before a floor is picked, floor-specific info is hidden: no Wi-Fi password or QR, and the laundry cards ask the guest to pick a floor.
- Markup: anything with `data-fl` shows only for the listed floors (`0` = not picked yet, e.g. `data-fl="gf 2 3"`). `<span data-floor-name>` is filled with the floor name in the current language.
- Wi-Fi (password `Copen_0077` on every floor; the copy button copies only the password): GF `Copen_Beige` (`qr-gf.png`), 1F `Copen_Green` (`qr.png`), 2F `Copen_Blue` (`qr-2f.png`), 3F `Copen_Pink` (`qr-3f.png`).
- Washer/dryer: only 1F (Samsung) has a guide. GF, 2F and 3F show "guide coming soon" + contact the host. To add a floor's guide, copy the `data-fl="1"` block next to it, set its `data-fl`, and drop that floor from the `data-fl="gf 2 3"` placeholder.

## Files
| File | Used for |
|---|---|
| `index.html` | Guidebook page (all CSS/JS inline) |
| `brochure/index.html` | Arrival brochure page (all CSS/JS inline) |
| `img/` | Guidebook diagrams and building photos (from the printed 1F guidebook); `img/en/`, `img/ja/`, `img/zh-hans/` and `img/zh-hant/` hold the same diagrams relettered in English, Japanese, Simplified and Traditional Chinese |
| `hero.jpg` | Hero photo |
| `qr.png`, `qr-gf.png`, `qr-2f.png`, `qr-3f.png` | Wi-Fi QR codes per floor (1F, GF, 2F, 3F) |
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

## Adding a language
The guidebook is built so a new language is mostly translation work (Chinese was added this way, as `zh-hans` / `zh-hant`):
1. `index.html` head script: add the code to `CH_LANGS` and its Google Fonts family to `CH_FONT`.
2. CSS: add `html:not([data-lang=xx]) .xx` to the hide rule, plus a font/line-break block like the `html[lang=ja]` / `html[lang|=zh]` ones.
3. Text: next to every `class="ja"` element add a `class="xx"` one; next to every `data-label-ja` / `data-toast-ja` / `data-alt-ja` add `data-label-xx` etc. Anything missing falls back to English.
4. Script: add a row to the `LANG` table (tab title, "switched" message, screen-reader text), and the strings in the "지금 필동" card, copy-failed and in-app messages.
5. Language list (`#langmenu`) and the language button labels: one more row / span each.

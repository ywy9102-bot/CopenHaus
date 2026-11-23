# Copen Haus – guest guide

Static one-page site (no build step). Open `index.html` in a browser to preview.

## Files
| File | Used for |
|---|---|
| `index.html` | The page (all CSS/JS inline) |
| `hero.jpg` | Hero photo |
| `qr.png` | Wi-Fi QR code |
| `og.jpg` | Link preview image (KakaoTalk, LINE, etc.) |
| `favicon.png`, `apple-touch-icon.png` | Browser tab / home-screen icons |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |

## Publish on GitHub Pages
1. Upload all files to the repository root.
2. Settings → Pages → Source: *Deploy from a branch* → Branch `main` / `(root)` → Save.
3. Replace `YOUR-USERNAME` and `YOUR-REPO` in the `og:image` line of `index.html`
   (for a `username.github.io` repository the URL is `https://username.github.io/og.jpg`).

## Before sharing publicly
The page contains the host's phone number, Wi-Fi password and the house address.
`index.html` has `<meta name="robots" content="noindex,nofollow,noarchive">` so search engines skip it,
but anyone with the link can read it. Remove that meta tag if you want the page to be searchable.

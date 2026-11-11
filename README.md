# Gmail Cleaner — PWA

An installable phone app that lists your Gmail **Trash** and **Spam** and deletes them **permanently**: per email, by selection, or "Empty now".
It runs entirely in the browser and talks only to Google, so there's no server and your PC can stay off. English / العربية toggle included.

No terminal needed. Setup takes about 15 minutes, all in a web browser.

---

## 1. Put the app online (GitHub Pages, free)

1. Sign in at **github.com**, then **New repository** → name it `gmail-cleaner` → **Public** → Create.
2. On the repo page click **uploading an existing file**, then select **all the files** in this folder (there are no subfolders) → **Commit changes**.
3. Go to **Settings → Pages**. Under *Build and deployment* choose **Deploy from a branch**, then **main** / **/(root)** → Save.
4. After about 1 minute your app is live at:
   `https://YOUR-GITHUB-USERNAME.github.io/gmail-cleaner/`

> The Client ID isn't a secret, so a public repo is fine. There are no passwords or tokens in these files.

## 2. Create a Google sign-in for it (Google Cloud Console)

You can reuse the Google Cloud project your Flask cleaner already uses.

1. Open **console.cloud.google.com** and pick the project.
2. **APIs & Services → Library → Gmail API → Enable** (skip this if it's already enabled).
3. **Google Auth Platform** (formerly *OAuth consent screen*):
   - **Audience:** External, *Testing*. Under **Test users** add your own Gmail address.
   - **Data access → Add or remove scopes:** add `https://mail.google.com/`. Permanent delete needs this full-access scope.
4. **Clients → Create client → Web application**
   - **Authorized JavaScript origins → Add URI:** `https://YOUR-GITHUB-USERNAME.github.io`
     (origin only: no `/gmail-cleaner/` path and no trailing slash)
   - Leave *Authorized redirect URIs* empty → **Create**.
5. Copy the **Client ID** (ends in `.apps.googleusercontent.com`).

> Your Flask app uses a *Desktop* client. This one must be a separate **Web application** client.

## 3. Open it on your phone

1. Open your GitHub Pages URL in **Chrome** (Android) or **Safari** (iPhone).
2. Paste the Client ID → **Save**. It's stored on that device only. You can also put it in `config.js` before uploading, which skips this step on every device.
3. Tap **Sign in with Google**. You'll see *"Google hasn't verified this app"*. That's expected because it's your own app in Testing mode, so tap **Continue** and allow access.

## 4. Install it

- **Android (Chrome):** tap the **Install** button in the app header, or ⋮ menu → **Install app / Add to Home screen**.
- **iPhone (Safari):** Share button → **Add to Home Screen**.

---

## Good to know

- **Sign-in lasts 1 hour.** A browser-only app gets 1-hour Google access tokens with no refresh, which is Google's rule. When it expires the app says so and one tap signs you back in.
- **Deletes are permanent.** Every delete asks for confirmation first. "Empty now" deletes in batches of 500 and shows progress.
- **Offline:** the app opens without a connection but can't load or delete mail until you're back online.
- **Your hourly auto-empty on the PC is unaffected.** This is a separate client in the same Google project.
- **Updating the app:** edit the files in GitHub, then bump `VERSION` in `sw.js` (e.g. `gc-v2`) so phones pick up the change.
- **iPhone note:** if sign-in ever misbehaves inside the installed home-screen app, open the same URL in Safari and sign in there.

## Files

| File | Purpose |
|---|---|
| `index.html` | App layout |
| `app.css` | Styling (dark, mobile-first, RTL-aware) |
| `app.js` | Gmail API calls, sign-in, UI logic, EN/AR text |
| `config.js` | Optional: hard-code your Client ID |
| `sw.js` | Service worker (offline app shell) |
| `manifest.webmanifest`, `*.png` | Install metadata and icons |

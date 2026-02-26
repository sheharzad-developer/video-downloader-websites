# Deploy to Vercel — Step by Step

Follow these steps to put your Video Downloader project on Vercel. You’ll need a **GitHub account** and a **Vercel account** (both free).

---

## Part 1: Put your code on GitHub

### Step 1: Install Git (if you don’t have it)

- **Mac:** Open Terminal and run: `git --version`. If it’s not installed, install Xcode Command Line Tools: `xcode-select --install`.
- **Windows:** Download and install [Git for Windows](https://git-scm.com/download/win).
- **Linux:** e.g. `sudo apt install git` (Ubuntu/Debian).

### Step 2: Create a new repository on GitHub

1. Go to [github.com](https://github.com) and sign in.
2. Click the **+** (top right) → **New repository**.
3. **Repository name:** e.g. `video-downloader-websites`.
4. Choose **Public**.
5. **Do not** check “Add a README” (you already have code).
6. Click **Create repository**.

### Step 3: Initialize Git in your project and push

The project has a **.gitignore** so `venv/`, `db.sqlite3`, and other local files are not pushed to GitHub.

Open Terminal (or Command Prompt / PowerShell) and go to your project folder:

```bash
cd "/Volumes/Samsung External SSD 1/Project/Video-Downloader-Websites"
```

Run these commands one by one (replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repo name, e.g. `myuser` and `video-downloader-websites`):

```bash
# 1. Initialize Git (only if this folder is not already a Git repo)
git init

# 2. Add all project files (except what’s in .gitignore)
git add .

# 3. First commit
git commit -m "Initial commit: video downloader project for Vercel"

# 4. Rename branch to main (if needed)
git branch -M main

# 5. Add GitHub as remote (use the URL from your new repo)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 6. Push to GitHub
git push -u origin main
```

If Git asks for credentials, use your GitHub username and a **Personal Access Token** (not your password). Create one at: GitHub → Settings → Developer settings → Personal access tokens.

---

## Part 2: Deploy on Vercel

### Step 4: Sign up / log in to Vercel

1. Go to [vercel.com](https://vercel.com).
2. Click **Sign Up** or **Log In**.
3. Choose **Continue with GitHub** so Vercel can read your repos.

### Step 5: Import your project

1. On the Vercel dashboard, click **Add New…** → **Project**.
2. You’ll see a list of your GitHub repositories. Find **video-downloader-websites** (or whatever you named it).
3. Click **Import** next to that repo.

### Step 6: Configure the project (important)

On the “Configure Project” screen, set these:

| Setting | Value |
|--------|--------|
| **Framework Preset** | Other (or leave as detected) |
| **Root Directory** | Leave **empty** (use repo root) |
| **Build Command** | `python manage.py export_vercel_pages` |
| **Output Directory** | `public` |
| **Install Command** | Leave **empty** (the project’s `vercel.json` uses `uv pip install -r requirements.txt` to avoid “externally-managed-environment” errors). If you had set a custom install command before, clear it. |

Do **not** change the **Root Directory** unless your project lives in a subfolder of the repo.

Then click **Deploy**.

### Step 7: Wait for the first build

- Vercel will install dependencies and run the build command.
- The first deploy can take 1–2 minutes.
- If the build fails, go to **Step 9** (troubleshooting).

### Step 8: Open your site

When the build finishes:

1. Click **Visit** (or the link Vercel shows).
2. Your site will be at a URL like: `https://video-downloader-websites-xxxx.vercel.app`.

Try:

- **Home / All-in-One:** `https://your-project.vercel.app/`
- **TikTok:** `https://your-project.vercel.app/tiktok`
- **Facebook:** `https://your-project.vercel.app/facebook`
- **Instagram:** `https://your-project.vercel.app/instagram`
- **YouTube:** `https://your-project.vercel.app/youtube`
- **YouTube to MP3:** `https://your-project.vercel.app/youtube-mp3`

Paste a video URL and click **Download** to test the API.

---

## Part 3: Optional — Environment variables and custom domain

### Step 9: Add environment variables (optional)

If you use your **own Cobalt API** (not the default public one):

1. In Vercel, open your project.
2. Go to **Settings** → **Environment Variables**.
3. **Key:** `COBALT_API_URL`
4. **Value:** your Cobalt API base URL (e.g. `https://your-cobalt.example.com`)
5. Choose **Production** (and optionally Preview/Development).
6. Click **Save**.
7. Trigger a new deploy: **Deployments** → **⋯** on the latest → **Redeploy**.

### Step 10: Use a custom domain (optional)

1. In the project, go to **Settings** → **Domains**.
2. Enter your domain (e.g. `download.example.com`).
3. Follow Vercel’s instructions to add the DNS records they show (at your domain registrar or DNS provider).
4. After DNS propagates, Vercel will issue SSL and your site will be available on that domain.

---

## Troubleshooting

### Build fails with “externally-managed-environment” or “pip install” error

Vercel’s build image uses Python managed by **uv**. The project’s `vercel.json` sets:

```json
"installCommand": "uv pip install -r requirements.txt"
```

Make sure this is in your repo and that you **did not** override the Install Command in the Vercel dashboard with `pip install -r requirements.txt`. If you did, clear the Install Command so `vercel.json` is used.

### Build fails with “python: command not found”

- Vercel uses **Python 3** by default. Your `vercel.json` and `requirements.txt` are already correct.
- If it still fails, in **Project Settings** → **General** → **Node.js Version** leave as default; the build uses the **Build Command** (Python), not Node.

### Build fails on “python manage.py export_vercel_pages”

- Make sure **Build Command** is exactly: `python manage.py export_vercel_pages`
- If your repo doesn’t have a `public/` folder yet, the build creates it. Ensure `config`, `downloader`, `api`, and `manage.py` are in the repo root.

### “404” on /tiktok or /api/download

- **Pages:** The project uses **rewrites** in `vercel.json` so `/tiktok` serves `tiktok.html`. Don’t remove `vercel.json`.
- **API:** The serverless function is at `api/download.py`. It must be in the repo and deployed; then `/api/download` works.

### Download works locally but not on Vercel

- Check **Vercel** → **Functions** → **api/download** for errors.
- On the **Hobby** plan, functions have a **10 second** timeout; long Cobalt requests may fail. **Pro** allows 60 seconds (set in `vercel.json`).

---

## Quick reference: commands you ran

```bash
cd "/Volumes/Samsung External SSD 1/Project/Video-Downloader-Websites"
git init
git add .
git commit -m "Initial commit: video downloader project for Vercel"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Then: **Vercel** → **Add New** → **Project** → **Import** repo → set **Build Command** and **Output Directory** → **Deploy**.

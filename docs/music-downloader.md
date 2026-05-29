# Music Downloader

A self-hosted web app to download music from Spotify albums, playlists, or tracks. No Spotify API key needed — it uses Spotify's public embed page for metadata and yt-dlp for the actual audio.

## How it works

1. You paste a Spotify URL into the web UI
2. The app fetches the track list from Spotify's **public embed page** (no API key or login needed)
3. For each track, it searches YouTube and downloads the best match via yt-dlp
4. ID3 tags (title, artist, album, track number) are written from Spotify metadata using mutagen
5. Files are saved as `MUSIC_DIR/{artist}/{album}/{title}.mp3`

> **Why not spotdl?** spotdl relies on YouTube Music and Spotify's official API — both aggressively rate-limit residential IPs. This approach uses only public Spotify embed pages and regular YouTube search, which is far more reliable.

---

## Install

> These commands assume you have already cloned the HomeCore repo and are inside the `HomeCore` folder (see [initial-setup](initial-setup.md)).

```bash
# Copy the app files to the server location
sudo cp music-downloader/main.py /opt/downloader/
sudo cp music-downloader/index.html /opt/downloader/

# Install Python dependencies
sudo pip3 install fastapi uvicorn requests mutagen

# yt-dlp is already installed from initial-setup — verify:
yt-dlp --version
```

---

## Configure the music directory

Open the config at the top of `main.py`:

```bash
sudo nano /opt/downloader/main.py
```

Find this line near the top and change it if your music folder is in a different location:

```python
MUSIC_DIR = "/music"
```

If you followed the [initial-setup guide](initial-setup.md), `/music` is already a symlink to `/mnt/hd/music` — no change needed.

Save: `Ctrl+O → Enter → Ctrl+X`

---

## Run as a system service

```bash
# Copy the service file
sudo cp music-downloader/downloader.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable --now downloader

# Check it started correctly
sudo systemctl status downloader
# Should show: active (running)
```

Opens at `http://YOUR_SERVER_IP:8888`.

> **Note:** The service runs as `root` for simplicity. In a production environment you'd create a dedicated user. For a home server this is acceptable.

---

## Usage

1. Open `http://YOUR_SERVER_IP:8888` in any browser
2. Paste a Spotify URL (album, playlist, or single track)
3. A preview of the track list appears — click **Download all** to confirm
4. Each track downloads one by one with a live progress log

You can also paste a YouTube URL directly to download a single video as MP3.

### What if a track fails?

If a track fails (usually because yt-dlp matched the wrong YouTube video), the error card shows two options:
- **Search YouTube** — searches automatically and shows 3 suggestions to pick from
- **Open YouTube** — opens YouTube in a new tab so you can find the right video and paste the URL manually

---

## Verify it's working

Open `http://YOUR_SERVER_IP:8888`. You should see the Music Downloader UI with an input field. Paste any Spotify album URL and you should see the track list appear within a few seconds.

---

## Pair with Navidrome

Once music is downloaded to `/music`, set up [Navidrome](navidrome.md) to stream it to any Subsonic-compatible client (Symfonium, DSub, etc.) — your own personal Spotify.

---

## Next step

→ [Set up Navidrome](navidrome.md)

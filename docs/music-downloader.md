# Music Downloader

A self-hosted web app to download music from Spotify albums, playlists, or tracks. No Spotify API key needed — it uses Spotify's public embed page for metadata and yt-dlp for the actual audio.

## How it works

1. You paste a Spotify URL into the web UI
2. The app fetches the track list from Spotify's public embed page (no API key or login needed)
3. For each track, it searches YouTube and downloads the best match via yt-dlp
4. ID3 tags (title, artist, album, track number) are written from Spotify metadata using mutagen
5. Files are saved as `{MUSIC_DIR}/{artist}/{album}/{title}.mp3`

> **Why not spotdl?** spotdl relies on YouTube Music and Spotify's official API — both aggressively rate-limit residential IPs. This approach uses only public Spotify embed pages and regular YouTube search, which is far more reliable.

---

## Install

```bash
# Create the app directory
sudo mkdir -p /opt/downloader

# Copy the app files
sudo cp music-downloader/main.py /opt/downloader/
sudo cp music-downloader/index.html /opt/downloader/

# Install Python dependencies
sudo pip3 install fastapi uvicorn requests mutagen

# Make sure yt-dlp and ffmpeg are installed (from initial-setup)
yt-dlp --version
ffmpeg -version
```

### Set your music directory

Open `/opt/downloader/main.py` and change this line near the top if needed:

```python
MUSIC_DIR = "/music"
```

Make sure `/music` points to your actual music folder (it should be a symlink to `/mnt/hd/music` if you followed the [initial setup guide](initial-setup.md)).

---

## Run as a system service

```bash
# Copy the service file
sudo cp music-downloader/downloader.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable --now downloader

# Check it's running
sudo systemctl status downloader
```

Opens at `http://YOUR_SERVER_IP:8888`.

---

## Usage

1. Open `http://YOUR_SERVER_IP:8888` in any browser
2. Paste a Spotify URL (album, playlist, or single track)
3. A preview of the track list appears — confirm and click **Download all**
4. Each track downloads one by one. Errors are shown with a manual retry option

You can also paste a YouTube URL to download a single video as MP3.

### What if a track fails?

If a track fails to download (usually because the YouTube search found the wrong video), you have two options directly in the UI:
- **Search YouTube** — searches and shows 3 suggestions to pick from
- **Open YouTube** — opens YouTube search in a new tab so you can find the right video and paste the URL

---

## Pair with Navidrome

Once music is in `/music`, set up [Navidrome](navidrome.md) to stream it to any Subsonic client (Symfonium, DSub, etc.) — basically your own Spotify.

---

## Next step

→ [Set up Navidrome](navidrome.md)

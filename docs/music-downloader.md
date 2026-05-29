# Music Downloader

A self-hosted web app to download music from Spotify albums/playlists using Spotify's embed page for metadata and yt-dlp for the actual audio. No Spotify API key needed.

## How it works

1. You paste a Spotify album/playlist/track URL
2. The app scrapes the track list from Spotify's public embed page (no API key needed)
3. For each track, it searches YouTube and downloads the best match via yt-dlp
4. ID3 tags (title, artist, album, track number) are written from Spotify metadata using mutagen
5. Files are saved as `{artist}/{album}/{title}.mp3`

> **Why not spotdl?** spotdl relies on YouTube Music and Spotify's API — both of which rate-limit heavily on residential IPs. This approach scrapes the public embed page and uses regular YouTube search, which is much more reliable.

## Install

```bash
# Copy files to server
sudo mkdir -p /opt/downloader
sudo cp music-downloader/main.py /opt/downloader/
sudo cp music-downloader/index.html /opt/downloader/

# Install Python dependencies
sudo pip3 install fastapi uvicorn requests mutagen yt-dlp

# Install the systemd service
sudo cp music-downloader/downloader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now downloader
```

## Usage

Open `http://YOUR_SERVER_IP:8888` in your browser.

- Paste a Spotify album, playlist, or track URL → preview the track list → click **Download all**
- Paste a YouTube URL → downloads directly
- If a track fails, you can search YouTube manually or paste a custom link

## Music directory

By default, music is saved to `/music`. Change the `MUSIC_DIR` constant in `main.py` to match your setup.

## Pair with Navidrome

[Navidrome](navidrome.md) can serve your music library as a Subsonic-compatible API, letting you stream from any Subsonic client (Symfonium, DSub, etc.).

## Requirements

- Python 3.8+
- `yt-dlp` in PATH
- `ffmpeg` for audio conversion: `sudo apt install ffmpeg`

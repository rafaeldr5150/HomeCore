# Radarr, Sonarr & Bazarr

Radarr manages movies, Sonarr manages TV series. You tell them what you want; they find it, download it, rename it, and put it in the right folder. Bazarr then finds subtitles for everything automatically.

## How the automation works

```
You add "Inception" to Radarr
        │
        ▼
Radarr searches Prowlarr's indexers
        │
        ▼
Radarr finds a torrent and sends it to qBittorrent
        │
        ▼
qBittorrent downloads to /downloads/
        │
        ▼
Radarr detects the download is complete
        │
        ▼
Radarr renames and moves:
/downloads/... → /movies/Inception (2010)/Inception (2010).mkv
        │
        ▼
Jellyfin sees the new file and adds it to your library
        │
        ▼
Bazarr finds and downloads a subtitle for it
```

**You only need to do step 1. Everything else is automatic.**

---

## Install Radarr

```bash
curl -o /tmp/install_radarr.sh \
  https://raw.githubusercontent.com/Radarr/Radarr/develop/distribution/debian/install.sh
sudo bash /tmp/install_radarr.sh
sudo systemctl enable --now radarr
```

Opens at `http://YOUR_SERVER_IP:7878`.

> If the script URL doesn't work, check the [official Radarr install guide](https://wiki.servarr.com/radarr/installation/linux).

## Install Sonarr

```bash
curl -o /tmp/install_sonarr.sh \
  https://raw.githubusercontent.com/Sonarr/Sonarr/develop/distribution/debian/install.sh
sudo bash /tmp/install_sonarr.sh
sudo systemctl enable --now sonarr
```

Opens at `http://YOUR_SERVER_IP:8989`.

> If the script URL doesn't work, check the [official Sonarr install guide](https://wiki.servarr.com/sonarr/installation/linux).

## Install Bazarr

```bash
# Install dependencies
sudo apt install -y python3-dev python3-pip python3-libxml2 python3-lxml libxml2-dev libxslt1-dev

# Download and extract
sudo mkdir -p /opt/bazarr
cd /opt/bazarr
sudo wget https://github.com/morpheus65535/bazarr/releases/latest/download/bazarr.zip
sudo unzip bazarr.zip -d .

# Install Python requirements
sudo pip3 install -r requirements.txt

# Create the systemd service
sudo tee /etc/systemd/system/bazarr.service << EOF
[Unit]
Description=Bazarr
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/bazarr/bazarr.py
WorkingDirectory=/opt/bazarr
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now bazarr
```

Opens at `http://YOUR_SERVER_IP:6767`.

---

## Configure Radarr

### 1. Set the root folder
**Settings → Media Management → Root Folders → Add Root Folder** → type `/movies` → **OK**

### 2. Add qBittorrent as download client
**Settings → Download Clients → Add (`+`) → qBittorrent**
- Host: `127.0.0.1`
- Port: `8080`
- Username: `admin`
- Password: the password you set in qBittorrent
- Category: `radarr`
- Click **Test** → green checkmark → **Save**

### 3. Indexers come from Prowlarr
No manual setup needed — once you connect Prowlarr to Radarr (see [Prowlarr guide](prowlarr.md)), indexers sync automatically.

### 4. Add your first movie
**Movies → Add New Movie** → search for any movie → click it → select a quality profile → **Add Movie**

Radarr will immediately start searching. Check **Activity → Queue** to see it downloading.

---

## Configure Sonarr

Same steps as Radarr:

1. **Settings → Media Management → Root Folders** → `/tv`
2. **Settings → Download Clients** → add qBittorrent with category `tv-sonarr`
3. **Series → Add New Series** → search and add

---

## Configure Bazarr

### 1. Connect to Sonarr
**Settings → Sonarr → Enable → Host:** `127.0.0.1` **Port:** `8989`
**API Key:** copy from Sonarr → **Settings → General → API Key**
Click **Test** then **Save**

### 2. Connect to Radarr
Same process: **Settings → Radarr**, port `7878`, Radarr's API key.

### 3. Add subtitle providers
**Settings → Providers → Add Provider**

Free providers that work well:
- **OpenSubtitles.com** — requires a free account at opensubtitles.com
- **Subscene** — no account needed
- **Supersubtitles** — no account needed

### 4. Set languages
**Settings → Languages → Add Profile** → add your preferred language(s) → apply to Movies and Series in their respective Bazarr settings pages.

### 5. Search for missing subtitles on existing library
**Bazarr → Movies → Select All → Search** (repeat in the Series tab)

---

## Quality profiles

Radarr and Sonarr have "quality profiles" that define what resolution/format you accept. The default **HD-1080p** profile downloads 1080p when available and falls back to 720p — a good starting point for most people.

---

## Verify everything is working

1. Open Radarr at `http://YOUR_SERVER_IP:7878`
2. Add a movie to your watchlist
3. Go to **Activity → Queue** — you should see it appear and start downloading within a few minutes
4. Once downloaded, check `/movies/` — the file should be there, renamed and organized
5. Open Jellyfin — the movie should appear in your library automatically

---

## Next step

→ [Set up Music Downloader](music-downloader.md)

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
Radarr renames and moves file to /movies/Inception (2010)/Inception (2010).mkv
        │
        ▼
Jellyfin sees the new file and adds it to your library
        │
        ▼
Bazarr finds and downloads a subtitle for it
```

**You only need to do step 1.**

---

## Install Radarr

```bash
curl -o /tmp/install_radarr.sh \
  https://raw.githubusercontent.com/Radarr/Radarr/develop/distribution/debian/install.sh
sudo bash /tmp/install_radarr.sh
sudo systemctl enable --now radarr
```

Opens at `http://YOUR_SERVER_IP:7878`.

## Install Sonarr

```bash
curl -o /tmp/install_sonarr.sh \
  https://raw.githubusercontent.com/Sonarr/Sonarr/develop/distribution/debian/install.sh
sudo bash /tmp/install_sonarr.sh
sudo systemctl enable --now sonarr
```

Opens at `http://YOUR_SERVER_IP:8989`.

## Install Bazarr

```bash
sudo apt install -y python3-pip
sudo pip3 install bazarr
# Or follow the official guide: https://wiki.servarr.com/bazarr/installation/linux
sudo systemctl enable --now bazarr
```

Opens at `http://YOUR_SERVER_IP:6767`.

---

## Configure Radarr

### 1. Set the root folder
**Settings → Media Management → Root Folders → Add Root Folder** → `/movies`

### 2. Add qBittorrent as download client
**Settings → Download Clients → Add → qBittorrent**
- Host: `127.0.0.1`
- Port: `8080`
- Username: `admin`
- Password: your qBittorrent password
- Category: `radarr`
- Click **Test** (should show a green checkmark) then **Save**

### 3. Indexers come from Prowlarr
No manual setup needed — once you connect Prowlarr to Radarr (see [Prowlarr guide](prowlarr.md)), the indexers sync automatically.

### 4. Add your first movie
**Movies → Add New Movie** → search for any movie → select quality profile → **Add Movie**

Radarr will immediately start searching for it. Check **Activity → Queue** to see progress.

---

## Configure Sonarr

Same steps as Radarr:

1. **Settings → Media Management → Root Folders** → `/tv`
2. **Settings → Download Clients** → add qBittorrent with category `tv-sonarr`
3. **Series → Add New Series** → search and add

---

## Configure Bazarr

### 1. Connect to Sonarr
**Settings → Sonarr**
- Enable: yes
- Host: `127.0.0.1`, Port: `8989`
- API Key: find it in Sonarr at **Settings → General → API Key**
- Click **Test** then **Save**

### 2. Connect to Radarr
**Settings → Radarr**
- Host: `127.0.0.1`, Port: `7878`
- API Key: find it in Radarr at **Settings → General → API Key**

### 3. Add subtitle providers
**Settings → Providers → Add Provider**

Free providers that work well:
- **OpenSubtitles.com** (requires free account at opensubtitles.com)
- **Subscene** (no account needed)
- **Supersubtitles**

### 4. Set languages
**Settings → Languages → Add Profile** → add your preferred language(s) (e.g. English, Portuguese)

Apply the language profile to both Movies and Series in Bazarr settings.

### 5. Search for missing subtitles
After setup, trigger a search for everything already in your library:
**Bazarr → Movies → Select All → Search** (repeat for Series)

---

## Quality profiles

Both Radarr and Sonarr have "quality profiles" that define what resolution/format you prefer. The default **HD-1080p** profile is a good starting point — it downloads 1080p when available and falls back to 720p.

---

## Next step

→ [Set up Music Downloader](music-downloader.md)

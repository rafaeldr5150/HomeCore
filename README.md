# HomeCore

A complete, battle-tested guide to building a fully self-hosted multimedia hub. Replace Google Photos, Spotify, and streaming services with your own infrastructure — all running on a single machine, accessible from anywhere.

This guide was built and tested on a **2012 Mac Mini** (Intel Core i5, 16GB RAM, 4.6TB external HDD) running Ubuntu 22.04. If it works on that, it works on anything.

---

## What you get

| Service | What it does | Replaces |
|---|---|---|
| **Jellyfin** | Stream movies & TV to any device | Netflix / Plex |
| **Nextcloud** | Personal cloud, file sync, photo backup | Google Drive / Google Photos |
| **Radarr** | Automatically finds and downloads movies | — |
| **Sonarr** | Automatically finds and downloads TV series | — |
| **Prowlarr** | Manages torrent indexers for Radarr & Sonarr | — |
| **Bazarr** | Downloads subtitles for everything automatically | — |
| **qBittorrent** | Torrent client with web UI | — |
| **Music Downloader** | Download albums/playlists from Spotify via YouTube | Spotify / spotdl |
| **Navidrome** | Stream your music library from any device | Spotify |
| **ES-DE + RetroArch** | Retro gaming frontend with scraped box art | — |

---

## How it all fits together

HomeCore is not just a list of apps — each piece has a role and they work together as a system:

```
                        ┌──────────────────────────────────────────────────┐
                        │                  HOME SERVER                     │
                        │                                                  │
  Phone / Laptop ───────┤  [Tailscale VPN]  ◄── remote access             │
  (anywhere)            │                                                  │
                        │  ┌─────────── MEDIA AUTOMATION ─────────────┐   │
  TV / Fire Stick ──────┤  │  Prowlarr (indexers)                     │   │
  (local network)       │  │      │                                   │   │
                        │  │      ├──► Radarr ──► qBittorrent         │   │
                        │  │      └──► Sonarr ──► qBittorrent         │   │
                        │  │                │                         │   │
                        │  │                ▼                         │   │
                        │  │          /downloads/                     │   │
                        │  │                │                         │   │
                        │  │    Radarr/Sonarr imports & renames       │   │
                        │  │                │                         │   │
                        │  │         ┌──────┴──────┐                  │   │
                        │  │         ▼             ▼                  │   │
                        │  │      /movies/        /tv/                │   │
                        │  │         │             │                  │   │
                        │  │         └──── Jellyfin ◄── Bazarr        │   │
                        │  └──────────────────────────────────────────┘   │
                        │                                                  │
                        │  ┌─────────── MUSIC ──────────────────────┐     │
                        │  │  Spotify URL ──► Music Downloader       │     │
                        │  │                      │                  │     │
                        │  │                   /music/               │     │
                        │  │                      │                  │     │
                        │  │                  Navidrome              │     │
                        │  └────────────────────────────────────────┘     │
                        │                                                  │
                        │  ┌─────────── CLOUD ──────────────────────┐     │
                        │  │  Phone auto-upload ──► Nextcloud        │     │
                        │  │  (replaces Google Photos/Drive)         │     │
                        │  └────────────────────────────────────────┘     │
                        └──────────────────────────────────────────────────┘
```

**The typical flow for a movie:**
1. You add a movie to your Radarr watchlist
2. Radarr searches Prowlarr's indexers and finds a torrent
3. Radarr sends it to qBittorrent to download into `/downloads/`
4. When finished, Radarr imports it into `/movies/` with the correct name
5. Jellyfin picks it up automatically and shows it in your library
6. Bazarr finds and downloads a subtitle for it

**You only do step 1. Everything else is automatic.**

---

## Architecture

```
External HDD (/mnt/hd)    ~4TB+
├── movies/               ← Radarr-managed movie library
├── tv/                   ← Sonarr-managed TV library
├── music/                ← Music Downloader output, read by Navidrome
└── nextcloud/
    ├── html/             ← Nextcloud app files
    ├── data/             ← User files (photos, documents, etc.)
    └── db/               ← MariaDB database

Root disk (/)             ~60GB needed
├── /downloads/           ← Temporary torrent downloads
├── /opt/downloader/      ← Music Downloader app
└── services running as systemd units or Docker containers
```

---

## Hardware requirements

| Component | Minimum | Recommended |
|---|---|---|
| CPU | Dual-core, 2GHz | Quad-core, 3GHz+ |
| RAM | 4 GB | 8–16 GB |
| OS Disk | 30 GB SSD | 120 GB SSD |
| Media Disk | 1 TB HDD | 4 TB+ HDD |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

> **No GPU needed.** Jellyfin can use Intel Quick Sync (integrated graphics) for hardware transcoding. A dedicated GPU is never required.

---

## Prerequisites

Before starting, you should be comfortable with:
- Opening a terminal and typing commands
- Connecting to a server via SSH (`ssh user@ip`)
- Editing a text file with `nano` (basic navigation: write, save with `Ctrl+O`, exit with `Ctrl+X`)

You do **not** need to know Linux deeply. Every command is written out in full in the guides.

---

## Getting started

### 1. Install Ubuntu 22.04 on your server

Download [Ubuntu 22.04 LTS Server](https://ubuntu.com/download/server). During installation:
- Create a user (e.g. `myuser`)
- Enable **OpenSSH server** when prompted

### 2. Follow the setup guides in order

| Step | Guide |
|---|---|
| 1 | [Initial Setup](docs/initial-setup.md) — SSH, HDD mount, Docker, firewall |
| 2 | [Nextcloud](docs/nextcloud.md) — personal cloud |
| 3 | [Jellyfin](docs/jellyfin.md) — media server |
| 4 | [qBittorrent](docs/qbittorrent.md) — torrent client |
| 5 | [Prowlarr](docs/prowlarr.md) — indexer manager |
| 6 | [Radarr + Sonarr + Bazarr](docs/radarr-sonarr-bazarr.md) — media automation |
| 7 | [Music Downloader](docs/music-downloader.md) — download music from Spotify |
| 8 | [Navidrome](docs/navidrome.md) — stream your music |
| 9 | [ES-DE + Emulators](docs/es-de.md) — retro gaming |
| 10 | [Tailscale](docs/tailscale.md) — remote access from anywhere |

---

## Music Downloader

One of the most useful tools in this stack. Paste a Spotify album, playlist, or track URL and it:

1. Scrapes the track list from Spotify's **public embed page** — no API key, no rate limits
2. Searches YouTube for each track via **yt-dlp**
3. Downloads and converts to MP3
4. Writes correct **ID3 tags** (title, artist, album, track number) from Spotify metadata

> **Why not spotdl?** spotdl relies on YouTube Music and Spotify's API, both of which aggressively rate-limit residential IPs. This approach uses only public endpoints and regular YouTube search — much more reliable.

---

## Tested systems (ES-DE / RetroArch)

| System | Core | Status |
|---|---|---|
| NES | nestopia | ✅ |
| SNES | snes9x | ✅ |
| Game Boy / GBC | gambatte | ✅ |
| Game Boy Advance | mGBA | ✅ |
| Mega Drive | Genesis Plus GX | ✅ |
| Master System | Genesis Plus GX | ✅ |
| Nintendo 64 | mupen64plus | ✅ (symlink fix required, see [ES-DE guide](docs/es-de.md)) |
| PlayStation | Beetle PSX | ✅ |
| Dreamcast | Flycast | ✅ |
| Arcade / MAME | MAME | ✅ |
| Neo Geo | FinalBurn Neo | ✅ |

---

## Common issues & fixes

### Nextcloud "Trusted domain" error
When accessing via Tailscale IP on a non-standard port, include the port in trusted domains:
```bash
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 3 --value='YOUR_IP:8084'
```

### Nextcloud containers using wrong disk after reboot
Docker may bind to empty directories if containers start before the HDD is mounted. Fix:
```bash
cd /opt/nextcloud && docker compose down && docker compose up -d
docker exec nextcloud-nextcloud-1 php occ files:scan admin
```

### Nextcloud brute-force lockout
```bash
docker exec nextcloud-db-1 mysql -u nextcloud -pYOUR_DB_PASSWORD nextcloud \
  -e 'DELETE FROM oc_bruteforce_attempts;'
```

### qBittorrent "downloads in root folder" warning
Set qBittorrent's default save path to `/downloads`, not `/movies`. See [qBittorrent guide](docs/qbittorrent.md).

### N64 not launching in ES-DE
One-line fix in [ES-DE guide](docs/es-de.md).

---

## Contributing

Pull requests welcome. If you set this up and hit a problem not covered here, open an issue or submit a fix.

---

## License

MIT

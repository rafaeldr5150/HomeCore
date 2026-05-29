# Home Server Guide

A complete, battle-tested guide to building a fully self-hosted home server. Replace Google Photos, Spotify, and streaming services with your own infrastructure running on a single machine — old or new hardware works fine.

This guide was built and tested on a **2012 Mac Mini** (Intel Core i5, 16GB RAM, 4.6TB external HDD) running Ubuntu 22.04. If it works on that, it works on anything.

---

## What you get

| Service | What it does | Replaces |
|---|---|---|
| **Jellyfin** | Stream movies & TV to any device | Netflix / Plex |
| **Nextcloud** | Personal cloud, file sync, photo backup | Google Drive / Google Photos |
| **Radarr** | Automatically finds and downloads movies | — |
| **Sonarr** | Automatically finds and downloads TV series | — |
| **Bazarr** | Downloads subtitles for everything automatically | — |
| **Prowlarr** | Manages torrent/usenet indexers for Radarr & Sonarr | — |
| **qBittorrent** | Torrent client with web UI | — |
| **Music Downloader** | Download albums/playlists from Spotify via YouTube | Spotify / spotdl |
| **Navidrome** | Stream your music library from any device | Spotify |
| **ES-DE + RetroArch** | Retro gaming frontend with scraped box art | — |

---

## Architecture

```
                        ┌─────────────────────────────────────────────┐
                        │              HOME SERVER                     │
                        │                                              │
  Phone / Laptop ───────┤  [Tailscale VPN]                            │
  (anywhere)            │       │                                      │
                        │       ▼                                      │
  TV / Fire Stick ──────┤  Jellyfin :8096    Nextcloud :8084          │
  (local network)       │  Radarr   :7878    Navidrome :4533          │
                        │  Sonarr   :8989    Music DL  :8888          │
                        │  Bazarr   :6767    ES-DE                    │
                        │  qBit     :8080    Prowlarr  :9696          │
                        │                                              │
                        │  ┌──────────────────────────────────────┐   │
                        │  │  External HDD (/mnt/hd)   ~4TB       │   │
                        │  │  ├── movies/                         │   │
                        │  │  ├── tv/                             │   │
                        │  │  ├── music/                          │   │
                        │  │  └── nextcloud/ (data + DB)          │   │
                        │  └──────────────────────────────────────┘   │
                        └─────────────────────────────────────────────┘
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

> **No GPU needed.** Jellyfin can use Intel Quick Sync (integrated graphics) for hardware transcoding. A dedicated GPU is optional and not required.

---

## Getting started

### 1. Prerequisites

- A machine running **Ubuntu 22.04 LTS** with SSH access
- An external HDD (or large internal drive) for media storage
- A [Tailscale](https://tailscale.com) account (free) for remote access

### 2. Clone this repo on your server

```bash
git clone https://github.com/YOUR_USERNAME/home-server-guide
cd home-server-guide
```

### 3. Follow the setup guides in order

1. [Initial Setup](docs/initial-setup.md) — mount the HDD, install dependencies
2. [Nextcloud](docs/nextcloud.md) — personal cloud via Docker
3. [Jellyfin](docs/jellyfin.md) — media server
4. [qBittorrent](docs/qbittorrent.md) — torrent client
5. [Radarr + Sonarr + Bazarr](docs/radarr-sonarr-bazarr.md) — automated media management
6. [Music Downloader](docs/music-downloader.md) — download music from Spotify
7. [Navidrome](docs/navidrome.md) — stream your music library
8. [ES-DE + Emulators](docs/es-de.md) — retro gaming
9. [Tailscale](docs/tailscale.md) — remote access from anywhere

---

## Music Downloader

One of the most useful tools in this stack. Paste a Spotify album, playlist, or track URL and it:

1. Scrapes the track list from Spotify's **public embed page** — no API key, no rate limits
2. Searches YouTube for each track via **yt-dlp**
3. Downloads and converts to MP3
4. Writes correct **ID3 tags** (title, artist, album, track number) from Spotify metadata

> **Why not spotdl?** spotdl relies on YouTube Music and Spotify's API, both of which aggressively rate-limit residential IPs. This approach uses only public endpoints and regular YouTube search — much more reliable in practice.

The web UI looks like this:

```
┌─────────────────────────────────────────┐
│  Music Downloader                       │
│  ─────────────────────────────────────  │
│  [ https://open.spotify.com/album/... ] │
│  [ Download ]                           │
│                                         │
│  ♫ 11 tracks found                      │
│  ─────────────────────────────────────  │
│  Artist — Track 1                       │
│  Artist — Track 2                       │
│  ...                                    │
│  [ Download all ]                       │
└─────────────────────────────────────────┘
```

See the full setup guide: [docs/music-downloader.md](docs/music-downloader.md)

---

## Remote access

All services are accessible remotely via **Tailscale** — a zero-config VPN that works through NAT without port forwarding. Install it on your server and phone, and your home server's local IPs become reachable from anywhere.

See [docs/tailscale.md](docs/tailscale.md).

---

## Tested systems (ES-DE / RetroArch)

| System | Core | Status |
|---|---|---|
| NES | nestopia | ✅ Works |
| SNES | snes9x | ✅ Works |
| Game Boy / GBC | gambatte | ✅ Works |
| Game Boy Advance | mGBA | ✅ Works |
| Mega Drive | Genesis Plus GX | ✅ Works |
| Master System | Genesis Plus GX | ✅ Works |
| Nintendo 64 | mupen64plus | ✅ Works (see note) |
| PlayStation | Beetle PSX | ✅ Works |
| Dreamcast | Flycast | ✅ Works |
| Arcade / MAME | MAME | ✅ Works |
| Neo Geo | FinalBurn Neo | ✅ Works |

> **N64 note**: Ubuntu ships `mupen64plus_libretro.so` but ES-DE looks for `mupen64plus_next_libretro.so`. A one-line symlink fix is in [docs/es-de.md](docs/es-de.md).

---

## Common issues & fixes

### Nextcloud "Trusted domain" error
When accessing via Tailscale IP on a non-standard port, you must include the port in the trusted domains config:
```bash
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 3 --value='YOUR_IP:8084'
```

### Nextcloud containers using wrong disk after reboot
Docker may bind to empty directories if containers start before the external HDD is mounted. Always ensure the HDD is mounted, then restart the containers:
```bash
cd /opt/nextcloud && docker compose down && docker compose up -d
```

### qBittorrent "downloads in root folder" warning
Radarr/Sonarr warn if qBittorrent downloads directly to the media root folder. Set qBittorrent's default save path to `/downloads` instead. See [docs/qbittorrent.md](docs/qbittorrent.md).

### N64 not launching in ES-DE
See the symlink fix in [docs/es-de.md](docs/es-de.md).

---

## Contributing

Pull requests welcome. If you set this up and hit a problem not covered here, open an issue or submit a fix.

---

## License

MIT

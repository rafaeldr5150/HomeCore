# Radarr, Sonarr & Bazarr

Radarr manages movies, Sonarr manages TV series. Both monitor RSS feeds, search for releases, and send downloads to qBittorrent automatically. Bazarr downloads subtitles for everything.

## Install

All three install the same way. Example for Radarr:

```bash
# Install via the official script
curl -o /tmp/install_radarr.sh https://raw.githubusercontent.com/Radarr/Radarr/develop/distribution/debian/install.sh
sudo bash /tmp/install_radarr.sh
```

For Sonarr and Bazarr, follow the official docs:
- [Sonarr install](https://wiki.servarr.com/sonarr/installation/linux)
- [Bazarr install](https://wiki.servarr.com/bazarr/installation/linux)

## Radarr configuration

1. Open `http://YOUR_SERVER_IP:7878`
2. **Settings → Media Management**: set root folder to `/movies`
3. **Settings → Download Clients**: add qBittorrent
   - Host: `127.0.0.1`, Port: `8080`
   - Category: `radarr`
4. **Settings → Indexers**: add via Prowlarr sync

## Sonarr configuration

1. Open `http://YOUR_SERVER_IP:8989`
2. **Settings → Media Management**: set root folder to `/tv`
3. **Settings → Download Clients**: add qBittorrent
   - Host: `127.0.0.1`, Port: `8080`
   - Category: `tv-sonarr`

## Bazarr configuration

1. Open `http://YOUR_SERVER_IP:6767`
2. **Settings → Sonarr**: connect to Sonarr with its API key
3. **Settings → Radarr**: connect to Radarr with its API key
4. **Settings → Providers**: add subtitle providers (OpenSubtitles, Subscene, etc.)
5. **Settings → Languages**: set your preferred languages

### Force subtitle search for all episodes

```bash
# Via Bazarr API — search missing subtitles for all series
curl -X POST "http://localhost:6767/api/episodes/wanted/search/all" \
  -H "X-API-KEY: YOUR_BAZARR_API_KEY"
```

## qBittorrent download path

qBittorrent should **not** download directly to `/movies` or `/tv` (Radarr/Sonarr root folders). Use `/downloads` instead:

```bash
# Set default save path in qBittorrent settings
# Settings → Downloads → Default Save Path: /downloads
```

This avoids the "downloads in root folder" warning and lets Radarr/Sonarr properly import and rename files.

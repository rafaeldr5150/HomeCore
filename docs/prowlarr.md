# Prowlarr

Prowlarr is the indexer manager — it connects to torrent sites and feeds search results to Radarr and Sonarr automatically. Without it, Radarr and Sonarr can't find anything to download.

Think of it as the search engine that sits between your media managers and the torrent sites:

```
Prowlarr (indexers) ──► Radarr ──► qBittorrent ──► /movies
                    └──► Sonarr ──► qBittorrent ──► /tv
```

## Install

```bash
curl -o /tmp/install_prowlarr.sh \
  https://raw.githubusercontent.com/Prowlarr/Prowlarr/develop/distribution/debian/install.sh
sudo bash /tmp/install_prowlarr.sh
sudo systemctl enable --now prowlarr
```

Opens at `http://YOUR_SERVER_IP:9696`.

> If the script URL above doesn't work, check the [official Prowlarr install guide](https://wiki.servarr.com/prowlarr/installation/linux) for the latest instructions.

---

## Add indexers (torrent sites)

Indexers are the torrent sites Prowlarr will search. The more you add, the better your chances of finding what you want.

1. Go to **Indexers → Add Indexer** (the `+` button)
2. Search for a site by name
3. Click it, fill in any credentials if required, click **Test** then **Save**

**Free public indexers to start with** (no account needed):
- **1337x** — good for movies and TV
- **YTS** — high-quality movie torrents, small file sizes
- **EZTV** — TV series

**For better results:** create free accounts on semi-private trackers like TorrentGalaxy or TorrentLeech. They have more content and faster speeds.

---

## Connect to Radarr and Sonarr

After adding indexers, sync them to Radarr and Sonarr:

1. Go to **Settings → Apps → Add** (`+`)
2. Select **Radarr**:
   - Prowlarr Server: `http://localhost:9696`
   - Radarr Server: `http://localhost:7878`
   - API Key: copy from Radarr → **Settings → General → API Key**
   - Click **Test** → should show a green checkmark → **Save**
3. Repeat for **Sonarr** (same steps, port `8989`)

Prowlarr will now automatically push all your indexers into Radarr and Sonarr — no need to add them manually in each app.

---

## Verify it's working

Open Radarr → **Settings → Indexers**. You should see the indexers you added in Prowlarr listed there automatically.

---

## Next step

→ [Set up Radarr, Sonarr & Bazarr](radarr-sonarr-bazarr.md)

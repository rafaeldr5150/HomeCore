# Prowlarr

Prowlarr is the "indexer manager" — it connects to torrent sites and feeds search results to Radarr and Sonarr automatically. Without it, Radarr and Sonarr can't find anything to download.

Think of it as the search engine that sits between your media managers and the torrent sites.

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

---

## Add indexers (torrent sites)

Indexers are the torrent sites Prowlarr will search. The more you add, the better your chances of finding what you want.

1. Go to **Indexers → Add Indexer** (the `+` button)
2. Search for the sites you want to use
3. Click the indexer name, fill in any required credentials, click **Test** then **Save**

> **Recommended free public indexers to start with:** 1337x, RARBG mirror, YTS (movies), EZTV (TV). These require no account.
>
> For better results, create free accounts on private or semi-private trackers like TorrentGalaxy or TorrentLeech.

---

## Connect to Radarr and Sonarr

This step makes Prowlarr automatically sync its indexers to Radarr and Sonarr.

1. Go to **Settings → Apps**
2. Click `+` to add an application
3. Select **Radarr**:
   - Prowlarr Server: `http://localhost:9696`
   - Radarr Server: `http://localhost:7878`
   - API Key: paste Radarr's API key (find it in Radarr → Settings → General)
   - Click **Test** then **Save**
4. Repeat for **Sonarr** (port `8989`)

After saving, Prowlarr will automatically push all your indexers into Radarr and Sonarr. You don't need to add them manually in each app.

---

## Verify it's working

In Radarr, go to **Settings → Indexers** — you should see the indexers from Prowlarr listed there automatically.

---

## Next step

→ [Set up Radarr, Sonarr & Bazarr](radarr-sonarr-bazarr.md)

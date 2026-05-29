# Remote Access with Tailscale

Tailscale creates a private VPN between your devices, letting you access your home server from anywhere — no port forwarding or dynamic DNS needed.

## Install on the server

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Follow the link it prints to authenticate with your Tailscale account.

## Get your server's Tailscale IP

```bash
tailscale ip -4
# Example output: 100.x.x.x
```

## Install on your phone/laptop

Download the Tailscale app and sign in with the same account. Your server will appear in the device list.

## Access your services remotely

Once connected, use the Tailscale IP instead of your local IP:

| Service | URL |
|---|---|
| Jellyfin | `http://100.x.x.x:8096` |
| Nextcloud | `http://100.x.x.x:8084` |
| Radarr | `http://100.x.x.x:7878` |
| Sonarr | `http://100.x.x.x:8989` |
| Prowlarr | `http://100.x.x.x:9696` |
| Bazarr | `http://100.x.x.x:6767` |
| qBittorrent | `http://100.x.x.x:8080` |
| Music Downloader | `http://100.x.x.x:8888` |
| Navidrome | `http://100.x.x.x:4533` |

## Nextcloud trusted domains

Nextcloud requires trusted domains to be configured. Include both the port number:

```bash
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 2 \
  --value='100.x.x.x'
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 3 \
  --value='100.x.x.x:8084'
```

> Including the domain **with** the port is required when using a non-standard port.

---

## Setup complete

Your HomeCore is fully operational. From anywhere in the world, with Tailscale active on your phone or laptop, you have:

- **Jellyfin** — stream your movies and TV shows
- **Nextcloud** — your private Google Drive and Google Photos
- **Radarr + Sonarr** — automated media downloads
- **Navidrome** — stream your music library to any Subsonic app
- **Music Downloader** — download from Spotify links directly to the server
- **ES-DE** — retro gaming frontend with scraped artwork

Everything runs on your own hardware, under your control, with no subscriptions.

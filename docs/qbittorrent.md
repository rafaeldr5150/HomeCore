# qBittorrent

Torrent client used by Radarr and Sonarr to download media. Accessed via a web UI.

## Install

```bash
sudo apt install -y qbittorrent-nox

# Create a systemd service so it starts automatically on boot
sudo tee /etc/systemd/system/qbittorrent.service << EOF
[Unit]
Description=qBittorrent
After=network.target

[Service]
ExecStart=/usr/bin/qbittorrent-nox --webui-port=8080
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now qbittorrent
```

Opens at `http://YOUR_SERVER_IP:8080`.

---

## First login

Open the web UI and you'll be prompted to set a password. Recent versions of qBittorrent no longer have a default password — you must create one on the first visit.

- **Username:** `admin`
- **Password:** set on first login (choose something and remember it — Radarr and Sonarr will need it)

---

## Set the download path

qBittorrent must download to `/downloads/`, **not** directly to `/movies` or `/tv`. Downloading to the media root folder causes a warning in Radarr/Sonarr and breaks the import workflow.

1. Open **Tools → Options → Downloads**
2. Set **Default Save Path** to `/downloads`
3. Click **Save**

---

## Set per-category paths

Radarr and Sonarr use categories to identify their downloads. Set the save path for each:

1. Open **View → Categories** (left sidebar)
2. Right-click **radarr** → **Edit** → set Save Path to `/downloads` → **OK**
3. Right-click **tv-sonarr** → **Edit** → set Save Path to `/downloads` → **OK**

> These categories are created automatically when you add qBittorrent as a download client in Radarr and Sonarr.

---

## Verify it's working

Open the web UI at `http://YOUR_SERVER_IP:8080` and log in. If you see the main interface with the sidebar, qBittorrent is running correctly.

---

## Next step

→ [Set up Prowlarr](prowlarr.md)

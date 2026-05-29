# qBittorrent

Torrent client used by Radarr and Sonarr to download media.

## Install

```bash
sudo apt install -y qbittorrent-nox

# Create a systemd service
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

Opens at `http://YOUR_SERVER_IP:8080`. Default credentials: `admin` / `adminadmin`.

## Important: set the download path

qBittorrent must **not** download directly to `/movies` or `/tv`. Set the default path to `/downloads`:

- Web UI → **Tools → Options → Downloads → Default Save Path**: `/downloads`

Then set per-category paths:

- Web UI → **View → Categories** → right-click `radarr` → Edit → Save path: `/downloads`
- Same for `tv-sonarr`

This lets Radarr/Sonarr import and move files properly after download.

## Configure categories

Radarr uses category `radarr`, Sonarr uses `tv-sonarr`. These are created automatically when you add qBittorrent as a download client in Radarr/Sonarr.

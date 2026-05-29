# Navidrome

Navidrome is a self-hosted music streaming server compatible with all Subsonic clients (Symfonium, DSub, Ultrasonic, etc.). Think of it as your personal Spotify.

## Install

```bash
# Download latest release
NAVIDROME_VERSION=$(curl -s https://api.github.com/repos/navidrome/navidrome/releases/latest | grep tag_name | cut -d'"' -f4)
wget "https://github.com/navidrome/navidrome/releases/download/${NAVIDROME_VERSION}/navidrome_${NAVIDROME_VERSION#v}_linux_amd64.tar.gz" -O /tmp/navidrome.tar.gz

sudo mkdir -p /opt/navidrome /var/lib/navidrome
sudo tar -xf /tmp/navidrome.tar.gz -C /opt/navidrome navidrome
sudo chmod +x /opt/navidrome/navidrome
```

## Configure

Create `/etc/navidrome/navidrome.toml`:

```toml
MusicFolder = "/music"
DataFolder   = "/var/lib/navidrome"
Port         = 4533
LogLevel     = "info"
```

## Run as a service

```bash
sudo tee /etc/systemd/system/navidrome.service << EOF
[Unit]
Description=Navidrome Music Server
After=network.target

[Service]
ExecStart=/opt/navidrome/navidrome --configfile /etc/navidrome/navidrome.toml
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now navidrome
```

Opens at `http://YOUR_SERVER_IP:4533`.

## Mobile clients

- **Symfonium** (Android) — best UI, supports offline sync
- **DSub** (Android) — free and feature-rich
- **Substreamer** (iOS)

Connect using Subsonic protocol: server URL, username, and password.

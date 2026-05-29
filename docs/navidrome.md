# Navidrome

Navidrome is a self-hosted music streaming server compatible with all Subsonic clients (Symfonium, DSub, Ultrasonic, etc.). Once set up, you can stream your entire music library from your phone — your own personal Spotify.

## Install

```bash
# Download the latest release
NAVIDROME_VERSION=$(curl -s https://api.github.com/repos/navidrome/navidrome/releases/latest \
  | grep '"tag_name"' | cut -d'"' -f4 | sed 's/v//')

wget "https://github.com/navidrome/navidrome/releases/download/v${NAVIDROME_VERSION}/navidrome_${NAVIDROME_VERSION}_linux_amd64.tar.gz" \
  -O /tmp/navidrome.tar.gz

# If the version detection above fails, check the latest release manually at:
# https://github.com/navidrome/navidrome/releases
# and replace ${NAVIDROME_VERSION} with the version number (e.g. 0.53.3)

sudo mkdir -p /opt/navidrome /var/lib/navidrome
sudo tar -xf /tmp/navidrome.tar.gz -C /opt/navidrome navidrome
sudo chmod +x /opt/navidrome/navidrome
```

---

## Configure

```bash
sudo mkdir -p /etc/navidrome

sudo tee /etc/navidrome/navidrome.toml << EOF
MusicFolder = "/music"
DataFolder   = "/var/lib/navidrome"
Port         = 4533
LogLevel     = "info"
EOF
```

---

## Run as a system service

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

On first open, you'll be prompted to create an admin account. Do that, then Navidrome will scan your `/music` folder.

---

## Mobile clients

Connect any of these apps using the **Subsonic** protocol:

| App | Platform | Notes |
|---|---|---|
| **Symfonium** | Android | Best UI, supports offline sync |
| **DSub** | Android | Free and feature-rich |
| **Substreamer** | iOS | Clean UI |
| **Amperfy** | iOS | Open source |

**Connection settings** (same for all apps):
- Server URL: `http://YOUR_SERVER_IP:4533`
- Username / Password: the admin account you created

---

## Verify it's working

Open `http://YOUR_SERVER_IP:4533`. After logging in, your albums should appear in the library. If the library is empty, click **Rescan** in the admin panel and wait a moment.

---

## Next step

→ [Set up ES-DE + Emulators](es-de.md)

# Jellyfin

Open-source media server — stream movies, TV shows, and music to any device.

## Install

```bash
curl -fsSL https://repo.jellyfin.org/install-debuntu.sh | sudo bash
sudo systemctl enable --now jellyfin
```

Opens at `http://YOUR_SERVER_IP:8096`.

## Initial setup

1. Create an admin account
2. Add libraries:
   - **Movies** → `/movies`
   - **TV Shows** → `/tv`
   - **Music** → `/music`
3. Let the library scan complete

## Hardware transcoding (optional)

If your server has Intel integrated graphics, enable Quick Sync for transcoding:

```bash
# Check if Intel GPU is available
ls /dev/dri/

# Add jellyfin user to render group
sudo usermod -aG render jellyfin
sudo systemctl restart jellyfin
```

Then in Jellyfin: **Dashboard → Playback → Transcoding** → enable Intel QuickSync.

## Access from outside your network

Use [Tailscale](tailscale.md) for secure remote access without port forwarding.

## Fire TV / Android TV

Install the **Jellyfin** app from the Amazon App Store or Google Play. Works great even on older Fire Sticks for direct-play content (no transcoding needed).

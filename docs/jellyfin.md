# Jellyfin

Open-source media server — stream movies, TV shows, and music to any device on your network (or remotely via Tailscale).

## Install

```bash
curl -fsSL https://repo.jellyfin.org/install-debuntu.sh | sudo bash
sudo systemctl enable --now jellyfin
```

Opens at `http://YOUR_SERVER_IP:8096`.

---

## Initial setup (web wizard)

Open the URL above in your browser. You'll see a setup wizard:

1. **Select language** → choose yours
2. **Create admin account** → pick a username and password
3. **Add media libraries** → this is the important part (see below)
4. **Skip** the remaining optional steps

### Adding libraries

Click **Add Media Library** for each of the following:

| Content Type | Display Name | Folder |
|---|---|---|
| Movies | Movies | `/movies` |
| Shows | TV Shows | `/tv` |
| Music | Music | `/music` |

For each library:
1. Select the content type from the dropdown
2. Give it a name
3. Click the `+` next to **Folders** and type the path
4. Leave all other settings as default
5. Click **OK**

After finishing the wizard, Jellyfin will scan all three folders. This may take a few minutes depending on how many files you have.

---

## Hardware transcoding (optional)

If your server has Intel integrated graphics, you can enable hardware-accelerated transcoding. This reduces CPU usage when streaming to devices that can't play the original file format.

```bash
# Check if Intel GPU device exists
ls /dev/dri/

# Add jellyfin to the render group
sudo usermod -aG render jellyfin
sudo systemctl restart jellyfin
```

Then in Jellyfin:
**Dashboard → Playback → Transcoding → Hardware acceleration** → select **Intel QuickSync**

---

## Access on TV / Fire Stick

Install the **Jellyfin** app:
- **Fire TV**: search "Jellyfin" in the Amazon App Store
- **Android TV**: search in Google Play
- **Apple TV**: search in App Store

When prompted for server address, enter `http://YOUR_SERVER_LOCAL_IP:8096`.

> For access from outside your home network, use [Tailscale](tailscale.md) and enter your Tailscale IP instead.

---

## Access on phone / browser

Open `http://YOUR_SERVER_IP:8096` in any browser. Jellyfin has a full web player — no app needed.

---

## Keeping the library up to date

Jellyfin automatically scans for new files periodically. You can also trigger a manual scan:
**Dashboard → Libraries → (your library) → Scan All Libraries**

After Radarr or Sonarr downloads something, it usually appears in Jellyfin within a few minutes automatically.

---

## Next step

→ [Set up qBittorrent](qbittorrent.md)

# Initial Setup

This guide prepares your Ubuntu server from scratch. Follow these steps before setting up any individual service.

## Prerequisites

- A machine with **Ubuntu 22.04 LTS** installed (desktop or server edition)
- Basic comfort with a terminal (typing commands and pressing Enter)
- An external HDD or large partition for media storage

> **New to Linux?** You only need to know how to: open a terminal, type commands, and use a text editor (`nano`). Every command you need is written out in full below.

---

## 1. Access your server via SSH

SSH lets you control the server remotely from your laptop or desktop — no monitor needed on the server.

**On the server**, find its local IP:
```bash
ip a | grep "inet " | grep -v 127
# Look for something like: inet 192.168.1.100
```

**On your laptop** (Windows/Mac/Linux):
```bash
ssh your_username@192.168.1.100
# Type your password when prompted
```

> On Windows, open **PowerShell** or **Command Prompt** and run the `ssh` command above.

---

## 2. Update the system

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 3. Mount your external HDD

```bash
# List all drives and find yours (look for the large one, e.g. /dev/sdb)
lsblk

# Create the mount point
sudo mkdir -p /mnt/hd

# Get your drive's UUID (replace sdb1 with your partition)
sudo blkid /dev/sdb1
# Output example: UUID="a1b2c3d4-..." TYPE="ext4"

# Add to /etc/fstab so it mounts automatically on every boot
echo 'UUID=YOUR_UUID_HERE /mnt/hd ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Mount it now without rebooting
sudo mount -a

# Verify it's mounted
df -h /mnt/hd
```

> The `nofail` option is important — it prevents the server from failing to boot if the drive is disconnected.

---

## 4. Create the folder structure

```bash
sudo mkdir -p /mnt/hd/{movies,tv,music}
sudo mkdir -p /mnt/hd/nextcloud/{html,data,db}
sudo mkdir -p /downloads
sudo mkdir -p /opt/downloader

# Create symlinks so services can use short paths
sudo ln -s /mnt/hd/movies /movies
sudo ln -s /mnt/hd/tv /tv
sudo ln -s /mnt/hd/music /music
```

---

## 5. Install Docker

Docker runs Nextcloud (and optionally other services) in isolated containers.

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Allow your user to run Docker without sudo
sudo usermod -aG docker $USER

# Apply group change (or log out and back in)
newgrp docker

# Verify
docker --version
```

---

## 6. Configure the firewall (UFW)

UFW blocks unwanted connections while allowing your services to be reached on the local network.

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (IMPORTANT — do this first or you'll lock yourself out)
sudo ufw allow ssh

# Allow each service port
sudo ufw allow 8096   # Jellyfin
sudo ufw allow 8084   # Nextcloud
sudo ufw allow 7878   # Radarr
sudo ufw allow 8989   # Sonarr
sudo ufw allow 6767   # Bazarr
sudo ufw allow 9696   # Prowlarr
sudo ufw allow 8080   # qBittorrent
sudo ufw allow 8888   # Music Downloader
sudo ufw allow 4533   # Navidrome

# Check status
sudo ufw status
```

---

## 7. Install dependencies

```bash
# Python and pip
sudo apt install -y python3-pip ffmpeg

# yt-dlp (used by Music Downloader)
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
  -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# RetroArch + libretro cores (for ES-DE gaming)
sudo apt install -y retroarch \
  libretro-nestopia libretro-snes9x libretro-gambatte \
  libretro-mgba libretro-genesis-plus-gx libretro-mupen64plus \
  libretro-mame

# Fix N64 core name (ES-DE looks for a different filename)
sudo ln -s /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_libretro.so \
           /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_next_libretro.so
```

---

## 8. Verify everything

```bash
# HDD mounted
df -h /mnt/hd

# Docker running
docker ps

# Firewall active
sudo ufw status

# yt-dlp installed
yt-dlp --version
```

If all four commands return output without errors, you're ready to set up the individual services.

---

## Next step

→ [Set up Nextcloud](nextcloud.md)

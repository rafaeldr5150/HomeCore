# Initial Setup

This guide prepares your Ubuntu server from scratch. Follow these steps before setting up any individual service.

## Prerequisites

- A machine with **Ubuntu 22.04 LTS** installed ([official install guide](https://ubuntu.com/tutorials/install-ubuntu-server))
- Basic comfort with a terminal (typing commands and pressing Enter)
- An external HDD or large partition for media storage

> **New to Linux?** You only need to know how to: open a terminal, type commands, and use the `nano` text editor. Every command you need is written out in full below.

---

## 1. Access your server via SSH

SSH lets you control the server remotely from your laptop — no monitor needed on the server.

**On the server**, find its local IP:
```bash
ip a | grep "inet " | grep -v 127
# Look for something like: inet 192.168.1.100
```

**On your laptop** (Windows PowerShell, Mac/Linux Terminal):
```bash
ssh your_username@192.168.1.100
# Type your password when prompted
```

---

## 2. Update the system

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 3. Prepare your external HDD

### If the drive is brand new (needs formatting)

```bash
# List all drives — identify yours by size (e.g. /dev/sdb)
lsblk

# Create a partition (interactive — press n, p, 1, Enter, Enter, w)
sudo fdisk /dev/sdb

# Format as ext4
sudo mkfs.ext4 /dev/sdb1
```

### Mount the drive

```bash
# Create the mount point
sudo mkdir -p /mnt/hd

# Get the UUID of your partition
sudo blkid /dev/sdb1
# Example output: UUID="a1b2c3d4-1234-..." TYPE="ext4"

# Add to /etc/fstab so it mounts automatically on every boot
# Replace YOUR_UUID with the value from blkid
echo 'UUID=YOUR_UUID /mnt/hd ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Mount now without rebooting
sudo mount -a

# Verify it worked
df -h /mnt/hd
# Should show your drive's size
```

> The `nofail` option prevents the server from failing to boot if the drive is unplugged.

---

## 4. Create the folder structure

```bash
# Media folders on the external HDD
sudo mkdir -p /mnt/hd/{movies,tv,music}
sudo mkdir -p /mnt/hd/nextcloud/{html,data,db}

# Temporary download folder on the root disk
sudo mkdir -p /downloads

# Music downloader app folder
sudo mkdir -p /opt/downloader

# Symlinks so services can use short paths like /movies instead of /mnt/hd/movies
sudo ln -s /mnt/hd/movies /movies
sudo ln -s /mnt/hd/tv /tv
sudo ln -s /mnt/hd/music /music
```

---

## 5. Install Docker

Docker runs Nextcloud in an isolated container.

```bash
curl -fsSL https://get.docker.com | sh

# Allow your user to run Docker without sudo
sudo usermod -aG docker $USER

# Apply the group change without logging out
newgrp docker

# Verify
docker --version
```

---

## 6. Configure the firewall

UFW blocks unwanted traffic while keeping your services accessible on the local network.

```bash
# Enable the firewall
sudo ufw enable

# IMPORTANT: allow SSH first or you'll lose remote access
sudo ufw allow ssh

# Allow each service
sudo ufw allow 8096   # Jellyfin
sudo ufw allow 8084   # Nextcloud
sudo ufw allow 7878   # Radarr
sudo ufw allow 8989   # Sonarr
sudo ufw allow 6767   # Bazarr
sudo ufw allow 9696   # Prowlarr
sudo ufw allow 8080   # qBittorrent
sudo ufw allow 8888   # Music Downloader
sudo ufw allow 4533   # Navidrome

# Verify
sudo ufw status
```

---

## 7. Install dependencies

```bash
# Python, pip, and ffmpeg (required for audio conversion)
sudo apt install -y python3-pip ffmpeg

# yt-dlp — the tool used by Music Downloader to download audio from YouTube
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
  -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# RetroArch and libretro cores for ES-DE gaming
sudo apt install -y retroarch \
  libretro-nestopia \
  libretro-snes9x \
  libretro-gambatte \
  libretro-mgba \
  libretro-genesis-plus-gx \
  libretro-mupen64plus \
  libretro-mame

# Fix: ES-DE expects mupen64plus_next but Ubuntu ships mupen64plus
sudo ln -s /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_libretro.so \
           /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_next_libretro.so
```

---

## 8. Clone the HomeCore repo

The repo contains config files and the Music Downloader app you'll need later.

```bash
sudo apt install -y git
git clone https://github.com/rafaeldr5150/HomeCore
cd HomeCore
```

Keep this terminal open in the `HomeCore` folder for the next steps.

---

## Verify everything is ready

```bash
df -h /mnt/hd          # HDD mounted
docker --version        # Docker installed
sudo ufw status         # Firewall active
yt-dlp --version        # yt-dlp installed
ls /movies /tv /music   # Symlinks exist
```

All five should return output without errors. If any fail, re-check the relevant step above.

---

## Next step

→ [Set up Nextcloud](nextcloud.md)

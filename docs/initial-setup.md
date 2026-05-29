# Initial Setup

## 1. Install Ubuntu 22.04

Download [Ubuntu 22.04 LTS](https://ubuntu.com/download/server) and install it. During setup:
- Create a user (e.g., `youruser`)
- Enable OpenSSH server

## 2. Mount your external HDD

```bash
# Find your drive
lsblk

# Create mount point
sudo mkdir -p /mnt/hd

# Get the UUID of your drive
sudo blkid /dev/sdb1

# Add to /etc/fstab for auto-mount on boot
echo "UUID=YOUR_DRIVE_UUID /mnt/hd ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab

sudo mount -a
```

> **Important**: The `nofail` option prevents boot failure if the drive is disconnected.

## 3. Create the folder structure

```bash
sudo mkdir -p /mnt/hd/{movies,tv,music,nextcloud/{html,data,db}}
sudo mkdir -p /downloads
```

## 4. Install dependencies

```bash
sudo apt update && sudo apt upgrade -y

# Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# RetroArch cores (for ES-DE)
sudo apt install -y retroarch libretro-nestopia libretro-snes9x \
  libretro-gambatte libretro-mgba libretro-genesis-plus-gx \
  libretro-mupen64plus libretro-mame

# Python tools
sudo apt install -y python3-pip

# yt-dlp (music downloader)
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

## 5. Fix N64 core name for ES-DE

ES-DE expects `mupen64plus_next_libretro.so` but Ubuntu ships `mupen64plus_libretro.so`:

```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_libretro.so \
           /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_next_libretro.so
```

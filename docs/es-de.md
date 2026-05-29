# ES-DE + Emulators

ES-DE is a polished frontend for retro gaming that auto-scrapes box art and metadata from ScreenScraper.

## Install ES-DE

```bash
# Visit https://es-de.org/#downloads in a browser, right-click the Linux x86_64 AppImage
# and copy the download link. Then on your server:
wget "PASTE_DOWNLOAD_URL_HERE" -O ES-DE_x64.AppImage

sudo mv ES-DE_x64.AppImage /opt/ES-DE.AppImage
sudo chmod +x /opt/ES-DE.AppImage
```

## Install RetroArch cores

```bash
sudo apt install -y \
  libretro-nestopia \        # NES
  libretro-snes9x \          # SNES
  libretro-gambatte \        # Game Boy / Game Boy Color
  libretro-mgba \            # Game Boy Advance
  libretro-genesis-plus-gx \ # Mega Drive / Master System
  libretro-mupen64plus \     # Nintendo 64
  libretro-mame \            # Arcade (MAME)
  libretro-flycast            # Dreamcast
```

## Fix N64 core name

ES-DE looks for `mupen64plus_next_libretro.so` but Ubuntu only ships `mupen64plus_libretro.so`:

```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_libretro.so \
           /usr/lib/x86_64-linux-gnu/libretro/mupen64plus_next_libretro.so
```

## ROMs folder structure

ES-DE expects ROMs organized by system:

```
~/ROMs/
├── nes/
├── snes/
├── n64/
├── gba/
├── gbc/
├── gb/
├── megadrive/
├── mastersystem/
├── psx/
├── dreamcast/
├── arcade/
└── neogeo/
```

## Scrape media with Skyscraper

[Skyscraper](https://github.com/muldjord/skyscraper) downloads box art, screenshots, and metadata from ScreenScraper:

```bash
# Install
sudo curl -L https://raw.githubusercontent.com/muldjord/skyscraper/master/update_skyscraper.sh | bash

# Scrape a system (requires ScreenScraper account)
Skyscraper -p nes -s screenscraper --user YOUR_USER --password YOUR_PASS

# Generate game list after scraping
Skyscraper -p nes
```

> ScreenScraper has daily rate limits. Scrape a few systems per day or get a supporter account for higher limits.

---

## Next step

→ [Set up remote access with Tailscale](tailscale.md)

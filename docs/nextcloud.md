# Nextcloud

Self-hosted Google Drive/Photos replacement.

## Deploy with Docker Compose

```bash
cd nextcloud/
# Edit docker-compose.yml and replace all YOUR_* placeholders with real passwords
docker compose up -d
```

See [`nextcloud/docker-compose.yml`](../nextcloud/docker-compose.yml).

> **Important**: Make sure your external HDD is mounted **before** starting the containers for the first time. If the containers start before the HDD is mounted, Docker will bind to empty directories on the root filesystem and your data will end up in the wrong place.

## Add trusted domains

After the container starts, add your server's IP and Tailscale IP as trusted domains:

```bash
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 1 --value='YOUR_LOCAL_IP'
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 2 --value='YOUR_TAILSCALE_IP'
# If accessing on a non-standard port, include the port:
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 3 --value='YOUR_TAILSCALE_IP:8084'
```

## Rescan files after copying data directly to the server

If you copy files directly to `/mnt/hd/nextcloud/data/admin/files/` (e.g., a Google Photos export), run:

```bash
docker exec nextcloud-nextcloud-1 php occ files:scan admin
```

## Clear brute-force lockout

If the mobile app gets locked out after too many failed login attempts:

```bash
docker exec nextcloud-db-1 mysql -u nextcloud -pYOUR_DB_PASSWORD nextcloud \
  -e 'DELETE FROM oc_bruteforce_attempts;'
```

## Fix stuck file locks (upload errors)

```bash
# Remove stale lock file locks
docker exec nextcloud-db-1 mysql -u nextcloud -pYOUR_DB_PASSWORD nextcloud \
  -e 'DELETE FROM oc_file_locks WHERE 1;'

# Rescan
docker exec nextcloud-nextcloud-1 php occ files:scan admin
```

## Mobile app setup

1. Install **Nextcloud** from your app store
2. Server address: `http://YOUR_TAILSCALE_IP:8084` (requires Tailscale active on phone)
3. Enable **Auto Upload** in Settings to replace Google Photos backup

# Nextcloud

Self-hosted replacement for Google Drive and Google Photos. Sync files, auto-backup phone photos, and access everything from anywhere via Tailscale.

## Deploy with Docker Compose

> **Important:** Make sure your external HDD is mounted at `/mnt/hd` **before** starting the containers. If the containers start before the HDD is mounted, Docker will create the data files on the root disk instead. If this happens, see the fix at the bottom of this page.

```bash
# From inside the HomeCore folder you cloned in initial-setup
cd nextcloud

# Edit the compose file and replace the placeholder passwords
nano docker-compose.yml
# Replace: YOUR_DB_ROOT_PASSWORD, YOUR_DB_PASSWORD, YOUR_ADMIN_PASSWORD
# Save: Ctrl+O → Enter → Ctrl+X

# Start the containers
docker compose up -d

# Check they're running
docker ps
# You should see nextcloud-nextcloud-1 and nextcloud-db-1
```

Nextcloud will be available at `http://YOUR_SERVER_IP:8084`.
The first startup takes about 30–60 seconds.

---

## Add trusted domains

Nextcloud only responds to requests from addresses it recognizes. Add your server's IP and Tailscale IP:

```bash
# Local network IP
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 1 \
  --value='YOUR_LOCAL_IP'

# Tailscale IP (without port)
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 2 \
  --value='YOUR_TAILSCALE_IP'

# Tailscale IP with port (required when using a non-standard port like 8084)
docker exec nextcloud-nextcloud-1 php occ config:system:set trusted_domains 3 \
  --value='YOUR_TAILSCALE_IP:8084'
```

> To find your Tailscale IP, see the [Tailscale guide](tailscale.md).

---

## Rescan files after copying data directly to the server

If you copy files directly into `/mnt/hd/nextcloud/data/admin/files/` (e.g. importing a Google Photos export), Nextcloud won't show them until you trigger a rescan:

```bash
docker exec nextcloud-nextcloud-1 php occ files:scan admin
```

---

## Fix: brute-force lockout

If the mobile app gets blocked after too many failed login attempts:

```bash
docker exec nextcloud-db-1 mysql -u nextcloud -pYOUR_DB_PASSWORD nextcloud \
  -e 'DELETE FROM oc_bruteforce_attempts;'
```

---

## Fix: stuck uploads ("error uploading" message)

If uploads keep failing with an error, there may be stale lock records in the database:

```bash
# Remove stale locks
docker exec nextcloud-db-1 mysql -u nextcloud -pYOUR_DB_PASSWORD nextcloud \
  -e 'DELETE FROM oc_file_locks WHERE 1;'

# Rescan to rebuild the file index
docker exec nextcloud-nextcloud-1 php occ files:scan admin
```

---

## Fix: containers using wrong disk after reboot

If after a reboot your files disappear, the containers started before the HDD was mounted. Fix:

```bash
# Make sure the HDD is mounted first
df -h /mnt/hd   # Should show your drive

# Restart the containers so they bind to the correct paths
cd /opt/nextcloud   # or wherever your docker-compose.yml is
docker compose down && docker compose up -d

# Rescan after restart
docker exec nextcloud-nextcloud-1 php occ files:scan admin
```

To prevent this permanently, ensure the HDD is in `/etc/fstab` with `nofail` (covered in [initial-setup](initial-setup.md)).

---

## Mobile app setup

1. Install **Nextcloud** from your phone's app store
2. Server address: `http://YOUR_TAILSCALE_IP:8084` (requires Tailscale active on the phone)
3. Login with the `admin` account and the password you set in `docker-compose.yml`
4. Enable **Auto Upload** in Settings to automatically back up photos and videos

---

## Verify it's working

Open `http://YOUR_SERVER_IP:8084` in a browser. You should see the Nextcloud login page. Log in with `admin` and your password.

---

## Next step

→ [Set up Jellyfin](jellyfin.md)

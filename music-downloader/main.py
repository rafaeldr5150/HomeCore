from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import subprocess
import threading
import uuid
import re
import json as json_module
import requests as http_requests

app = FastAPI()
jobs = {}

EMBED_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Directory where music is stored — adjust to your setup
MUSIC_DIR = "/music"


def get_spotify_tracks_from_embed(url):
    """Fetches track list from Spotify embed page (no API key required)."""
    m = re.search(r"spotify\.com(?:/intl-[a-z-]+)?/([^/?]+)/([a-zA-Z0-9]+)", url)
    if not m:
        return None, "Invalid Spotify URL"

    type_ = m.group(1)
    id_ = m.group(2)

    if type_ not in ("album", "playlist", "track"):
        return None, f"Type '{type_}' not supported"

    embed_url = f"https://open.spotify.com/embed/{type_}/{id_}"
    try:
        r = http_requests.get(embed_url, headers=EMBED_HEADERS, timeout=15)
        if r.status_code != 200:
            return None, f"Embed returned {r.status_code}"

        nd = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.DOTALL)
        if not nd:
            return None, "Could not extract data from Spotify"

        data = json_module.loads(nd.group(1))
        entity = data["props"]["pageProps"]["state"]["data"]["entity"]

        tracks = []
        if type_ == "track":
            tracks.append({
                "title": entity["title"],
                "artist": entity.get("subtitle", "Unknown"),
                "album": entity.get("title", "Unknown Album"),
            })
        else:
            album_name = entity.get("name") or entity.get("title", "Unknown Album")
            for i, t in enumerate(entity.get("trackList", []), 1):
                tracks.append({
                    "title": t["title"],
                    "artist": t.get("subtitle", entity.get("subtitle", "Unknown")),
                    "album": album_name,
                    "track_number": i,
                })

        return tracks, None
    except Exception as e:
        return None, str(e)


def parse_line(line):
    if "Downloaded" in line or "Saved" in line:
        return {"type": "success", "text": line}
    elif "Skipping" in line:
        return {"type": "skip", "text": line}
    elif "Error" in line or "error" in line:
        return {"type": "error", "text": line}
    return {"type": "info", "text": line}


def safe_path(s):
    return re.sub(r'[<>:"/\\|?*\n\r]', "_", s).strip()


def run_download(job_id, url):
    jobs[job_id]["status"] = "running"
    try:
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--embed-thumbnail",
               "--add-metadata", "-o", f"{MUSIC_DIR}/%(artist)s/%(title)s.%(ext)s", url]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            parsed = parse_line(line)
            jobs[job_id]["lines"].append(parsed)
            if len(jobs[job_id]["lines"]) > 200:
                jobs[job_id]["lines"] = jobs[job_id]["lines"][-200:]
            if parsed["type"] == "success":
                jobs[job_id]["success"].append(parsed["text"])
            if parsed["type"] == "error":
                url_match = re.search(r'AudioProviderError.*?- (https?://\S+)', line)
                if url_match:
                    jobs[job_id]["errors"].append({
                        "line": line, "youtube_url": url_match.group(1),
                        "spotify_url": None, "pending": False
                    })
        process.wait()
        jobs[job_id]["status"] = "done"
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["lines"].append({"type": "error", "text": str(e)})


def run_download_tracks(job_id, tracks):
    jobs[job_id]["status"] = "running"
    for track in tracks:
        artist = track.get("artist", "Unknown Artist")
        title = track.get("title", "Unknown Title")
        album = track.get("album", "Unknown Album")
        query = f"{artist} - {title}"
        jobs[job_id]["lines"].append({"type": "info", "text": f"Downloading: {query}"})

        output = f"{MUSIC_DIR}/{safe_path(artist)}/{safe_path(album)}/{safe_path(title)}.%(ext)s"
        cmd = ["yt-dlp", f"ytsearch1:{query}", "-x", "--audio-format", "mp3",
               "--embed-thumbnail", "--add-metadata", "-o", output, "--no-playlist"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            mp3_path = f"{MUSIC_DIR}/{safe_path(artist)}/{safe_path(album)}/{safe_path(title)}.mp3"
            try:
                from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TRCK, ID3NoHeaderError
                try:
                    tags = ID3(mp3_path)
                except ID3NoHeaderError:
                    tags = ID3()
                track_num = str(track.get("track_number", ""))
                tags['TIT2'] = TIT2(encoding=3, text=title)
                tags['TPE1'] = TPE1(encoding=3, text=artist)
                tags['TALB'] = TALB(encoding=3, text=album)
                tags['TPE2'] = TPE2(encoding=3, text=artist)
                if track_num:
                    tags['TRCK'] = TRCK(encoding=3, text=track_num)
                tags.save(mp3_path)
            except Exception as e:
                jobs[job_id]["lines"].append({"type": "info", "text": f"Tags: {e}"})
            jobs[job_id]["lines"].append({"type": "success", "text": f"Downloaded: {query}"})
            jobs[job_id]["success"].append(f"Downloaded: {query}")
        else:
            err = (result.stderr or result.stdout or "unknown error").strip().split("\n")[-1]
            jobs[job_id]["lines"].append({"type": "error", "text": f"Error: {query} — {err}"})
            jobs[job_id]["errors"].append({
                "line": f"Failed to download: {title}", "youtube_url": None,
                "spotify_url": None, "pending": False, "name": query
            })

    jobs[job_id]["status"] = "done"


def search_youtube(query, limit=3):
    try:
        result = subprocess.run(
            ["yt-dlp", f"ytsearch{limit}:{query}", "--get-title", "--get-url", "--get-duration", "--no-playlist"],
            capture_output=True, text=True, timeout=30
        )
        lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
        results = []
        i = 0
        while i + 2 < len(lines):
            results.append({"title": lines[i], "url": lines[i + 1], "duration": lines[i + 2]})
            i += 3
        return results
    except Exception:
        return []


HTML = open("/opt/downloader/index.html").read()


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


@app.get("/manifest.json")
def manifest():
    return {"name": "Music Downloader", "short_name": "MusicDL", "start_url": "/",
            "display": "standalone", "background_color": "#121212", "theme_color": "#1DB954",
            "icons": [{"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml"}]}


@app.get("/icon.svg")
def icon():
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" rx="40" fill="#121212"/><circle cx="96" cy="96" r="65" fill="none" stroke="#1DB954" stroke-width="8"/><circle cx="96" cy="96" r="10" fill="#1DB954"/></svg>'
    return Response(content=svg, media_type="image/svg+xml")


@app.post("/spotify-tracks")
def spotify_tracks(data: dict):
    url = data.get("url", "")
    tracks, error = get_spotify_tracks_from_embed(url)
    if error:
        return {"error": error}
    return {"tracks": tracks}


@app.post("/download")
def download(data: dict):
    url = data.get("url", "")
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "pending", "lines": [], "errors": [], "success": [], "last_spotify_url": None}
    t = threading.Thread(target=run_download, args=(job_id, url))
    t.daemon = True
    t.start()
    return {"job_id": job_id}


@app.post("/download-tracks")
def download_tracks(data: dict):
    tracks = data.get("tracks", [])
    if not tracks:
        return {"error": "No tracks received"}
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "pending", "lines": [], "errors": [], "success": [], "last_spotify_url": None}
    t = threading.Thread(target=run_download_tracks, args=(job_id, tracks))
    t.daemon = True
    t.start()
    return {"job_id": job_id}


@app.get("/status/{job_id}")
def status(job_id: str):
    return jobs.get(job_id, {"status": "error", "lines": [], "errors": [], "success": []})


@app.post("/search")
def search(data: dict):
    query = data.get("query", "")
    limit = data.get("limit", 3)
    results = search_youtube(query, limit)
    return {"results": results}

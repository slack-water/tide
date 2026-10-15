#!/usr/bin/env python3
"""download free-licensed portrait thumbnails from wikipedia/commons.

only images wikipedia marks as free (pilicense=free) are used. writes
images/<node id>.jpg and images/credits.json (file page, artist, license).
re-run safely; existing images are skipped. delete one to refetch it.
"""
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
IMG = HERE / "images"
API = "https://en.wikipedia.org/w/api.php"
UA = {"User-Agent": "tide-ytt/0.1 (personal study project)"}

# graph node id -> english wikipedia article title
TITLES = {
    "F001": "Lahiri Mahasaya", "F002": "Swami Vivekananda", "F003": "Sri Aurobindo",
    "F004": "Swami Sri Yukteswar Giri", "F005": "Paramahansa Yogananda",
    "F006": "Swami Kuvalayananda", "F007": "Shri Yogendra", "F008": "Sivananda Saraswati",
    "F009": "Tirumalai Krishnamacharya", "F010": "K. Pattabhi Jois", "F011": "B. K. S. Iyengar",
    "F012": "Indra Devi", "F013": "T. K. V. Desikachar", "F014": "Swami Vishnudevananda",
    "F015": "Satchidananda Saraswati", "F016": "Satyananda Saraswati", "F017": "Swami Rama",
    "F018": "Maharishi Mahesh Yogi", "F019": "Yogi Bhajan", "F020": "Bishnu Charan Ghosh",
    "F021": "Bikram Choudhury", "F022": "Muktananda", "F023": "Swami Kripalvananda",
    "F024": "Amrit Desai", "F025": "Richard Hittleman", "F026": "Sharon Gannon",
    "F027": "John Friend (yoga teacher)", "F028": "Beryl Bender Birch", "F029": "Baron Baptiste",
    "F030": "Ana Forrest", "F031": "Paul Grilley", "F032": "Paulie Zink",
    "F033": "Mark Singleton (scholar)", "F034": "Elizabeth De Michelis", "F035": "Joseph Alter",
    "F036": "James Mallinson (author)", "F037": "Georg Feuerstein",
    "X_Mahavatar_Babaji": "Mahavatar Babaji", "X_Ramakrishna_Paramahamsa": "Ramakrishna",
    "X_Paramahamsa_Madhavdasji": "Paramahamsa Madhavdasji",
    "X_Swami_Brahmananda_Saraswati": "Brahmananda Saraswati", "X_Bhagawan_Nityananda": "Bhagawan Nityananda",
}

# commons files picked by hand where the article's lead image isn't free.
# checked by eye: search hits can be a different person with the same name.
FILES = {
    "F016": "Swami Satyananda Saraswati.jpg",
    "F020": "Bishnu Charan Ghosh, atop motorcycle, 1919.jpg",
    "F022": "Muktananda-00-D.jpg",
    "F027": "JohnFriendCopenhagen2010.jpg",
    "F029": "Baron Baptiste by Gage Skidmore.jpg",
}


def fetch(url):
    """GET with backoff — wikimedia rate-limits bursts with 429."""
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(5 * 2 ** attempt)
    raise RuntimeError(f"still rate-limited: {url}")


def get(params):
    return json.loads(fetch(API + "?" + urllib.parse.urlencode({"format": "json", **params})))


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def main():
    IMG.mkdir(exist_ok=True)
    credits_path = IMG / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}
    for nid, title in TITLES.items():
        if (IMG / f"{nid}.jpg").exists():
            continue
        fname = FILES.get(nid)
        if not fname:
            q = get({"action": "query", "redirects": 1, "prop": "pageimages", "piprop": "name",
                     "pilicense": "free", "titles": title})
            fname = next(iter(q["query"]["pages"].values())).get("pageimage")
        if not fname:
            print(f"{nid}: no free image ({title})")
            continue
        meta = get({"action": "query", "prop": "imageinfo", "iiprop": "extmetadata|url",
                    "iiurlwidth": 200, "titles": "File:" + fname})
        info = next(iter(meta["query"]["pages"].values()))["imageinfo"][0]
        ext = info["extmetadata"]
        (IMG / f"{nid}.jpg").write_bytes(fetch(info["thumburl"]))
        credits[nid] = {
            "article": title, "file": fname,
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(fname),
            "artist": strip_tags(ext.get("Artist", {}).get("value")),
            "license": strip_tags(ext.get("LicenseShortName", {}).get("value")),
        }
        credits_path.write_text(json.dumps(credits, ensure_ascii=False, indent=1))
        print(f"{nid}: {fname} [{credits[nid]['license']}]", flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()

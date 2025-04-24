import json
from pathlib import Path

DATA_FILE = Path("posts.json")

def load_posts():
    if DATA_FILE.exists():
        with open(DATA_FILE,"r") as f:
            return json.load(f)
        return[]

def save_posts(posts):
    with open(DATA_FILE,"w") as f:
        json.dump(posts, f, indent=2)
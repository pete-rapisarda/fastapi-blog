import json
from pathlib import Path
from models import Post

DATA_FILE = Path("posts.json")
DELETED_FILE = Path("deleted_posts.json")

def load_posts() -> list[Post]:
    if DATA_FILE.exists():
        with open(DATA_FILE,"r") as f:
            post_data = json.load(f)
            posts = []
            for data in post_data:
                posts.append(Post(**data))
        return posts

def save_posts(posts:list[Post]) -> None:
    with open(DATA_FILE,"w") as f:
        json.dump(posts, f, indent=2)

def load_deleted_posts() -> list[Post]:
    if DELETED_FILE.exists():
        with open(DELETED_FILE,"r") as f:
            deleted_post_data = json.load(f)
            deleted_posts = []
            for data in deleted_post_data:
                deleted_posts.append(Post(**data))
        return deleted_posts

def save_deleted_posts(posts:list[Post]) -> None:
    with open(DELETED_FILE, "w") as f:
        json.dump(posts, f, indent=2)
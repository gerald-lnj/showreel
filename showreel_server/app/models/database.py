"""
Had issues getting mongod to run on my local machine. Will use a json file instead.
"""
from functools import lru_cache
import json
import os
from typing import Dict, List

from app.models.schemas import Reel, Clip

CLIPS_JSON_FILEPATH = os.path.join(os.getcwd(), "app", "models", "clips.json")
REELS_JSON_FILEPATH = os.path.join(os.getcwd(), "app", "models", "reels.json")


@lru_cache(maxsize=None)
def load_clips_from_json() -> Dict[str, Clip]:
    """
    Load all clips from JSON file, cache the response to avoid repeated R/W
    """
    clips = {}
    with open(CLIPS_JSON_FILEPATH) as json_file:
        raw_clips = json.load(json_file)
        for raw_clip in raw_clips:
            clip = Clip.from_dict(**raw_clip)
            clips[clip.id] = clip
    return clips


@lru_cache
def get_clip(_id: str) -> Clip:
    return load_clips_from_json()[_id]


@lru_cache(maxsize=None)
def load_reels_from_json() -> List[Reel]:
    """
    Load all Reels from JSON file, cache the response to avoid repeated R/W
    """
    reels = []
    with open(REELS_JSON_FILEPATH) as json_file:
        raw_reels = json.load(json_file)
        for raw_reel in raw_reels:
            reels.append(Reel.from_dict(**raw_reel))
    return reels


@lru_cache
def get_reel(index: int) -> Reel:
    return load_reels_from_json()[index]


def save_reel(reel: Reel):
    """
    Save Reel to JSON and invalidate cache.
    """
    with open(REELS_JSON_FILEPATH, "r+") as json_file:
        raw_reels: List[Dict] = json.load(json_file)
        raw_reels.append(reel.dict())
        json_file.seek(0)
        json.dump(raw_reels, json_file)
    load_reels_from_json.cache_clear()
    get_reel.cache_clear()

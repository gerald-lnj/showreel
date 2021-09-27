"""
Endpoints definition and routing
"""

import logging

from flask import Blueprint, jsonify

from app.models.database import get_clip, load_clips_from_json

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

clip_bp = Blueprint("clip", __name__, url_prefix="/clip")


@clip_bp.route("/", methods=["GET"])
def get_clips():
    return jsonify([clip.dict() for clip in load_clips_from_json()])


@clip_bp.route("/<clip_id>", methods=["GET"])
def get_clip_id(clip_id: str):
    try:
        clip_id = int(clip_id)
    except (ValueError, KeyError):
        return "path argument clip_id must be an integer.", 400
    try:
        return get_clip(clip_id).dict()
    except IndexError:
        return f"Clip with index {clip_id} not found.", 404

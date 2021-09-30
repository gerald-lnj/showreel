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
    return jsonify([clip.dict() for clip in load_clips_from_json().values()])


@clip_bp.route("/<clip_id>", methods=["GET"])
def get_clip_id(clip_id: str):
    try:
        return get_clip(clip_id).dict()
    except IndexError:
        return f"Clip with ID {clip_id} not found.", 404

"""
Endpoints definition and routing
"""

import logging
from typing import List

from flask import Blueprint, request

from app.models.database import get_reel, save_reel
from app.models.database import get_clip
from app.models.schemas import Definition, Standard, Reel

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

reel_bp = Blueprint("reel", __name__, url_prefix="/reel")


@reel_bp.route("/", methods=["POST"])
def create_reel():
    if request.method == "POST":
        try:
            name: str = request.json["name"]
            standard: str = request.json["standard"]
            definition: str = request.json["definition"]
            clip_indexes: List[int] = request.json["clips"]
            save: bool = bool(request.json["save"])
        except (KeyError, TypeError) as e:
            return str(e), 400

    standard = getattr(Standard, standard)
    definition = Definition(definition)
    clips = [get_clip(index) for index in clip_indexes]

    reel = Reel(name=name, standard=standard, definition=definition, clips=clips)

    if save:
        save_reel(reel)
        return reel.dict(), 201

    else:
        return reel.dict()


@reel_bp.route("/<reel_id>", methods=["GET"])
def get_reel_id(reel_id: str):
    try:
        reel_id = int(reel_id)
    except (ValueError, KeyError):
        return "path argument reel_id must be an integer.", 400
    try:
        return get_reel(reel_id).dict()
    except IndexError:
        return f"Reel with index {reel_id} not found.", 404

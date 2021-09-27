import logging

from app.models.schemas import Reel, Clip, Timecode, Standard, Definition
from app.models.database import load_clips_from_json
from pydantic.error_wrappers import ValidationError

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.WARNING)

pal_hd_clip = Clip(
    name="pal_hd_clip",
    description="PAL HD Clip",
    standard=Standard.PAL,
    definition=Definition.HD,
    start_timecode=Timecode(Standard.PAL),
    end_timecode=Timecode.from_frames(25, Standard.PAL),
)

pal_sd_clip = Clip(
    name="pal_sd_clip",
    description="PAL SD Clip",
    standard=Standard.PAL,
    definition=Definition.SD,
    start_timecode=Timecode(Standard.PAL),
    end_timecode=Timecode.from_frames(50, Standard.PAL),
)

ntsc_hd_clip = Clip(
    name="ntsc_hd_clip",
    description="NTSD HD Clip",
    standard=Standard.NTSC,
    definition=Definition.HD,
    start_timecode=Timecode(Standard.NTSC),
    end_timecode=Timecode.from_frames(25, Standard.NTSC),
)

ntsc_sd_clip = Clip(
    name="ntsc_sd_clip",
    description="NTSD SD Clip",
    standard=Standard.NTSC,
    definition=Definition.SD,
    start_timecode=Timecode(Standard.NTSC),
    end_timecode=Timecode.from_frames(50, Standard.NTSC),
)


def test_reels_wrong_definition():
    try:
        Reel(
            name="Reel",
            standard=Standard.PAL,
            definition=Definition.HD,
            clips=[pal_hd_clip, pal_sd_clip],
        )
    except ValidationError:
        return True
    else:
        raise Exception("Reel creation should fail")


def test_reels_wrong_standard():
    try:
        Reel(
            name="Reel",
            standard=Standard.PAL,
            definition=Definition.HD,
            clips=[pal_hd_clip, ntsc_hd_clip],
        )
    except ValidationError:
        return True
    else:
        raise Exception("Reel creation should fail")


def test_normal_reel_creation():
    reel = Reel(
        name="Reel",
        standard=Standard.PAL,
        definition=Definition.HD,
        clips=[pal_hd_clip, pal_hd_clip],
    )

    assert reel.get_duration() == Timecode.from_frames(50, Standard.PAL)


def test_total_pal_sd_duration():
    clips = [
        clip
        for clip in load_clips_from_json()
        if clip.standard == Standard.PAL and clip.definition == Definition.SD
    ]
    reel = Reel(
        name="Reel", standard=Standard.PAL, definition=Definition.SD, clips=clips,
    )
    # assert str(reel.get_duration()) == "00:02:10:01"
    assert str(reel.get_duration()) == "00:02:11:01"


def test_total_ntsc_sd_duration():
    clips = [
        clip
        for clip in load_clips_from_json()
        if clip.standard == Standard.NTSC and clip.definition == Definition.SD
    ]
    reel = Reel(
        name="Reel", standard=Standard.NTSC, definition=Definition.SD, clips=clips,
    )
    assert str(reel.get_duration()) == "00:00:54:08"
